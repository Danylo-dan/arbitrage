import ccxt
import time
import requests
import numpy as np
import exchanges_networks
import random
import datetime
from datetime import datetime
import pytz
from datetime import datetime

# Київська часова зона
kiev_timezone = pytz.timezone('Europe/Kiev')

# Поточний час у Київському часовому поясі
kiev_time = datetime.now(kiev_timezone)

# Форматування часу у вигляді рядка
formatted_time = kiev_time.strftime('%Y-%m-%d %H:%M:%S')

print("Поточний час у Київському часі:", formatted_time)

# Функція для виконання вашого оновлення
def update_cache_and_blacklist():
    print("Оновлення кешу і чорного списку...")
    exchanges_networks.pair_good_exchanges = {}

# Telegram API настройки
telegram_token = '6666410951:AAHYL6NJmNDy98SBkPlLBzcJLuKvRfchMZ8'
CHANNEL_ID = '-1001966751554'

#Рахунок сигналів
n = 0

#Завантаження ринків для кожної біржі
for exchange in exchanges_networks.exchanges.values():
    exchange.load_markets()

# Змінні для відслідковування останніх бірж для купівлі та продажу
last_sell_exchange = None
balance = 350  # Початковий баланс

# Функція для перевірки наявності пари на біржі
def check_pair_on_exchange(exchange, pair):
    try:
        markets = exchange.load_markets()  # Завантажуємо ринки для біржі
        if pair in markets:
            return True
    except Exception as e:
        print(f"Помилка при перевірці пари {pair}: {e}")
    return False

# Функція для отримання ціни валютної пари на біржі
def get_price(exchange, symbol):
    try:
        ticker = exchange.fetch_ticker(symbol)
        return ticker['last']  # Остання ціна
    except Exception as e:
        return None

# Функція для відправки повідомлення в Telegram канал з повідомленням про волатильність
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    params = {
        'chat_id': CHANNEL_ID,
        'text': message,
        'parse_mode': 'Markdown'  # Використовуємо Markdown для форматування посилань
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(f"Повідомлення на Telegram канал відправлено: {message}")
    else:
        print(f"Помилка при відправці повідомлення: {response.status_code}")

# Формуємо URL для біржі
def generate_exchange_url(exchange_name, pair):
    pair_for_url = pair.replace('/', '_')  # Заміна / на _ для URL
    if exchange_name == 'binance':
        return f"https://www.binance.com/en/trade/{pair_for_url}"
    elif exchange_name == 'ascendex':
        return f"https://ascendex.com/trade/{pair_for_url}"
    elif exchange_name == 'bingx':
        return f"https://bingx.com/en-us/trade/{pair_for_url}"
    elif exchange_name == 'bitget':
        return f"https://www.bitget.com/en/trade/{pair_for_url}"
    elif exchange_name == 'bitmart':
        return f"https://www.bitmart.com/trade/{pair_for_url}"
    elif exchange_name == 'bitrue':
        return f"https://www.bitrue.com/trade/{pair_for_url}"
    elif exchange_name == 'bybit':
        return f"https://www.bybit.com/en-US/trade/{pair_for_url}"
    elif exchange_name == 'coinbase':
        return f"https://www.coinbase.com/trade/{pair_for_url}"
    elif exchange_name == 'cryptocom':
        return f"https://crypto.com/exchange/{pair_for_url}"
    elif exchange_name == 'exmo':
        return f"https://exmo.com/en/trade/{pair_for_url}"
    elif exchange_name == 'gateio':
        return f"https://www.gate.io/en/trade/{pair_for_url}"
    elif exchange_name == 'hitbtc':
        return f"https://hitbtc.com/{pair_for_url}"
    elif exchange_name == 'htx':
        return f"https://www.htx.com/trade/{pair_for_url}"
    elif exchange_name == 'kraken':
        return f"https://www.kraken.com/en-us/trade/{pair_for_url}"
    elif exchange_name == 'kucoin':
        return f"https://www.kucoin.com/trade/{pair_for_url}"
    elif exchange_name == 'mexc':
        return f"https://www.mexc.com/trade/{pair_for_url}"
    elif exchange_name == 'okx':
        return f"https://www.okx.com/trade/{pair_for_url}"
    elif exchange_name == 'poloniex':
        return f"https://poloniex.com/exchange/{pair_for_url}"
    elif exchange_name == 'whitebit':
        return f"https://www.whitebit.com/trade/{pair_for_url}"
    elif exchange_name == 'xt':
        return f"https://www.xt.com/trade/{pair_for_url}"
    else:
        return "Exchange not found."

# Функція для отримання історичних цін на валютну пару
def get_historical_prices(exchange, symbol, timeframe='5m', limit=72):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        return [x[4] for x in ohlcv]  # Остання ціна закриття (close)
    except Exception as e:
        print(f"Помилка при отриманні історичних даних: {e}")
        return []

# Функція для обчислення волатильності
def calculate_volatility(prices):
    return np.std(prices)  # Стандартне відхилення

# Порогові значення волатильності для торгівлі
LOW_VOLATILITY_THRESHOLD = 0.01  # Допустима волатильність
HIGH_VOLATILITY_THRESHOLD = 0.05  # Небезпечна волатильність

# Основна функція для порівняння валютних пар
def compare_currency_pairs(currency_pairs):
    global last_sell_exchange, balance
    best_pair = None
    best_profit_in_usdt = 0  # Максимальний прибуток в USDT

    # Крок 1: Пошук валютної пари для купівлі
    for i, pair in enumerate(currency_pairs):
        print(f"Перевірка валютної пари {pair} ({i+1}/{len(currency_pairs)})")
        
        # Створимо словник для зберігання цін
        valid_prices = {}
        # Список цін для обчислення волатильності
        prices = []

        #___Біржі___
        #Список бірж, що підходять
        exchanges_for_trade = {}    

        # Перевіряємо ціни на валютну пару на різних біржах і виділяємо біржі для депозиту і виводу

        if pair not in exchanges_networks.pair_good_exchanges:
            for exchange_name, exchange in exchanges_networks.exchanges.items():
                try:
                    #___Фільтрація_бірж_____________________________________________________
                    currencies = exchange.fetch_currencies()   #взяття даних про валюти на біржі
                    base = ''    #базова валюта
                except:
                    print(f'Не вдалось отримати доступ до валют біржі {exchange_name}')
                    continue

                #Якщо дані про валюти None, то біржа пропускається
                if currencies == None:
                    continue

                for x in exchange.fetch_markets():    #знаходження базової валюти 
                      if x['symbol'] == pair:
                          base = x['base']
                if not base:  #відкидання бірж, де немає пари, яка проходить перевірку
                    continue

                    #відкидання бірж, де немає розділу про мережі або розділ про мережі пустий
                if bool('networks' in currencies[base]) == False or currencies[base]['networks'] == {}:
                   continue

                base_networks = currencies[base]['networks']

                #Взяття даних про можливість депозиту через мережу
                for x in base_networks:
                    network = base_networks[x]
                    if network['deposit'] == True or network['withdraw'] == True:
                        exchanges_for_trade.update({exchange_name:exchange})
            exchanges_networks.pair_good_exchanges.update({pair:exchanges_for_trade})
        #________________________________________________________________________
        
        #Визначення ціни серед перевірених бірж
        for exchange_name, exchange in exchanges_networks.pair_good_exchanges[pair].items():
            #___Визначення спреду на кожній біржі і фільтрація___
            orders = exchange.fetch_order_book(pair)
            bid = orders['bids'][0][0] if len(orders['bids']) > 0 else None
            ask = orders['asks'][0][0] if len(orders['asks']) > 0 else None
            spread = (ask - bid) if (bid and ask) else None
            if spread == None or spread >= 1:
                continue

            #___Визначення об'єму на кожній біржі і фільтрація___
            quote_volume = exchange.fetch_ticker(pair)['quoteVolume']
            if quote_volume == None or quote_volume < 1000000:
                continue

            price = get_price(exchange, pair)
            if price is not None:  # Перевірка на наявність ціни
                valid_prices[exchange_name] = price
                prices.append(price)  # Додаємо ціну для волатильності

        # Якщо ціни доступні хоча б на двох біржах, продовжуємо
        if len(valid_prices) >= 2:
            volatility = calculate_volatility(prices)

            # Перевірка волатильності
            if volatility > HIGH_VOLATILITY_THRESHOLD:
                volatility_message = "Висока волатильність — торгівля небезпечна!"
            elif volatility > LOW_VOLATILITY_THRESHOLD:
                volatility_message = "Волатильність допустима для торгівлі."
            else:
                volatility_message = "Низька волатильність — торгівля можлива."

            # Шукаємо біржу для купівлі
            if last_sell_exchange:  # Якщо вже був продаж, шукаємо валютну пару для купівлі на біржі продажу
                buy_exchange = last_sell_exchange
            else:
                # Якщо немає попереднього продажу, обираємо будь-яку біржу для купівлі
                buy_exchange = min(valid_prices, key=valid_prices.get)

            # Шукаємо найбільш вигідну біржу для продажу і перевіряємо на сумісність по мережам
            buy_object = eval(f'ccxt.{buy_exchange}()')

            #__________________________
            #___Копіюємо список з цінами без біржі купівлі і шукаємо підходящу по мережам біржу для продажу___

            #знаходження базової валюти
            for x in buy_object.fetch_markets():     
                  if x['symbol'] == pair:
                      base = x['base']

            vp_copy = valid_prices.copy()
            if buy_exchange in vp_copy:
                vp_copy.pop(buy_exchange)
            for y in list(vp_copy):
                n = 0
                sell_exchange = max(vp_copy, key=vp_copy.get)
                sell_object = eval(f'ccxt.{sell_exchange}()')
                for z in buy_object.fetch_currencies()[base]['networks']:
                    if z in sell_object.fetch_currencies()[base]['networks']:
                        n += 1
                        break
                if not n:
                    vp_copy.pop(sell_exchange)
                    continue
            if not vp_copy:
                sell_exchange = None
            #___________________________________________________________________________________________________

            # Перевірка, чи існують ці біржі в valid_prices
            if buy_exchange in valid_prices and sell_exchange in valid_prices:
                buy_price = valid_prices[buy_exchange]
                sell_price = valid_prices[sell_exchange]
                
                # Визначаємо кількість монет для купівлі
                amount_to_buy = balance / buy_price
                
                # Розрахунок потенційного прибутку в USDT
                profit_in_usdt = (sell_price - buy_price) * amount_to_buy

                # Якщо знайдений більший прибуток, оновлюємо найкращу пару
                if profit_in_usdt > best_profit_in_usdt:
                    best_profit_in_usdt = profit_in_usdt
                    best_pair = pair
                    best_buy_exchange = buy_exchange
                    best_sell_exchange = sell_exchange
                    best_buy_price = buy_price
                    best_sell_price = sell_price
                    best_volatility = volatility
                    best_volatility_message = volatility_message  # Повідомлення для волатильності

    # Якщо знайшли вигідну пару, виконуємо операцію
    if best_pair:
        buy_ex = eval(f'ccxt.{best_buy_exchange}()')
        sell_ex = eval(f'ccxt.{best_sell_exchange}()')

        for x in buy_ex.fetch_markets():    #знаходження базової валюти 
            if x['symbol'] == best_pair:
                base = x['base']

        for x in buy_ex.fetch_markets():    #знаходження валюти квоти 
            if x['symbol'] == best_pair:
                quote = x['quote']
        
        #__Повідомлення про мережі______________________________________________

        #__Мережі__
        withdraw_nets = []
        deposit_nets = []

        buy_networks = buy_ex.fetch_currencies()[base]['networks']
        sell_networks = sell_ex.fetch_currencies()[base]['networks']

        def withdrawal_networks(curr_networks):
            for y in curr_networks:
                if curr_networks[y]['withdraw'] == True:
                    if curr_networks[y]['fee'] == None:
                        fee = 'Немає інформації'
                        withdraw_nets.append(f'{y} --- Комісія за вивід: {fee}')
                    else:
                        fee = format(curr_networks[y]['fee'], '.8f') 
                        withdraw_nets.append(f'{y} --- Комісія за вивід: {fee}')

        def deposit_networks(curr_networks):
            for y in curr_networks:
                if curr_networks[y]['deposit'] == True:
                    if curr_networks[y]['fee'] == None:
                        fee = 'Немає інформації'
                        deposit_nets.append(f'{y} --- Комісія за депозит: {fee}')
                    else:
                        fee = format(curr_networks[y]['fee'], '.8f')
                        deposit_nets.append(f'{y} --- Комісія за депозит: {fee}')

        #________________________________________________________________________
        
        #Знаходження середньої комісії для виводу і депозиту з усіх мереж
        #__Список_з_комісіями__ 
        withdraw_fees = []
        deposit_fees = []

        #Цикли для заповнення списків з комісіями 
        for y in buy_networks:
                if buy_networks[y]['withdraw'] == True:
                    if buy_networks[y]['fee'] == None:
                        withdraw_fees.append(0)
                    else:
                        withdraw_fees.append(float(format(buy_networks[y]['fee'], '.8f')))
        
        for y in sell_networks:
                if sell_networks[y]['deposit'] == True:
                    if sell_networks[y]['fee'] == None:
                        deposit_fees.append(0)
                    else:
                        deposit_fees.append(float(format(sell_networks[y]['fee'], '.8f')))
        print(withdraw_fees)
        print(deposit_fees)

        #Знаходження середнього значення всіх комісій
        average_withdraw_fee = sum(withdraw_fees) / len(withdraw_fees)
        average_deposit_fee = sum(deposit_fees) / len(deposit_fees)

        #________________________________________________________________________
        
        #__Об'єми__
        base_buy_volume = buy_ex.fetch_ticker(best_pair)['baseVolume']#Об'єм базової валюти для біржі купівлі
        quote_buy_volume = buy_ex.fetch_ticker(best_pair)['quoteVolume']#Об'єм квоти для біржі купівлі

        base_sell_volume = sell_ex.fetch_ticker(best_pair)['baseVolume']#Об'єм базової валюти для біржі продажу
        quote_sell_volume = sell_ex.fetch_ticker(best_pair)['quoteVolume']#Об'єм квоти для біржі продажу

        #__Зміни за 24 години__
        buy_percentage = buy_ex.fetch_ticker(best_pair)['percentage'] #Зміна за 24 години на біржі купівлі
        sell_percentage = sell_ex.fetch_ticker(best_pair)['percentage'] #Зміна за 24 години на біржі продажу

        #__Спред__
        order_book_buy = buy_ex.fetch_order_book(best_pair) #Ордербук біржі КУПІВЛІ
        order_book_sell = sell_ex.fetch_order_book(best_pair) #Ордербук біржі ПРОДАЖУ

        bid_buy = order_book_buy['bids'][0][0] if len (order_book_buy['bids']) > 0 else None #Найкраща пропозиція купівлі біржі КУПІВЛІ
        ask_buy = order_book_buy['asks'][0][0] if len (order_book_buy['asks']) > 0 else None #Найкраща пропозиція продажу біржі КУПІВЛІ

        bid_sell = order_book_sell['bids'][0][0] if len (order_book_sell['bids']) > 0 else None #Найкраща пропозиція купівлі біржі ПРОДАЖУ
        ask_sell = order_book_sell['asks'][0][0] if len (order_book_sell['asks']) > 0 else None #Найкраща пропозиція продажу біржі ПРОДАЖУ

        spread_buy = (ask_buy - bid_buy) if (bid_buy and ask_buy) else None #Розрахунок спреду для біржі КУПІВЛІ
        spread_sell = (ask_sell - bid_sell) if (bid_sell and ask_sell) else None #Розрахунок спреду для біржі ПРОДАЖУ

        #__Повідомлення__

        #__Перехоплення якщо None в об'ємах і процентах__
        base_vol1 = f"Не знайдено даних за об'єм {base}" if base_buy_volume == None else f"об'єм {base} за 24 години: {base_buy_volume}"
        quote_vol1 = f"Не знайдено даних за об'єм {quote}" if quote_buy_volume == None else f"об'єм {quote} за 24 години: {quote_buy_volume}"

        base_vol2 = f"Не знайдено даних за об'єм {base}" if base_sell_volume == None else f"об'єм {base} за 24 години: {base_sell_volume}"
        quote_vol2 = f"Не знайдено даних за об'єм {quote}" if quote_sell_volume == None else f"об'єм {quote} за 24 години: {quote_sell_volume}"

        buy_perc = f"Не знайдено даних за зміну {base} протягом 24 годин" if buy_percentage == None else f"зміна {base} за 24 години:{buy_percentage}%"
        sell_perc = f"Не знайдено даних за зміну {base} протягом 24 годин" if sell_percentage == None else f"зміна {base} за 24 години:{sell_percentage}%"

        #__Перехоплення якщо None в ордербуках__
        buy_spread_message = f"Не знайдено даних за ордери на {best_pair}" if spread_buy == None else f"Спред для {best_pair}: {spread_buy: .10f}"
        sell_spread_message = f"Не знайдено даних за ордери на {best_pair}" if spread_sell == None else f"Спред для {best_pair}: {spread_sell: .10f}"

        #_____________________________________________________________________________________________

        #Формування списків з мережами 
        withdrawal_networks(buy_networks)
        deposit_networks(sell_networks)

        # Оновлення балансу після операції
        best_profit_in_usdt -= average_withdraw_fee*best_buy_price + average_deposit_fee*best_sell_price
        balance += best_profit_in_usdt   # Баланс після купівлі і продажу

        #__Формуємо повідомлення для Telegram__
        message = (f"🪙 Монета:🪙 \n"
                f"💎**{best_pair}**💎\n"
                f"{'━' * 24}\n"        
                f"📈 Купити на **[{best_buy_exchange}]({generate_exchange_url(best_buy_exchange, best_pair)})** за {best_buy_price: .7f} USDT\n"
                f"{'━' * 24}\n"        
                f"   Доступні мережі для виводу --- {withdraw_nets}\n"
                f"{'━' * 24}\n"        
                f"📉 Продати на **[{best_sell_exchange}]({generate_exchange_url(best_sell_exchange, best_pair)})** за {best_sell_price: .7f} USDT\n"
                f"   Доступні мережі для депозиту --- {deposit_nets}\n"
                f"{'━' * 24}\n"        
                f"📊 Волатильність на біржі {best_buy_exchange}: {best_volatility:.5f}\n"
                f"📊 Волатильність на біржі {best_sell_exchange}: {best_volatility:.5f}\n"
                f"📊 {best_volatility_message}\n"
                f"{'━' * 24}\n"        
                f"📊 Спред на біржі {best_buy_exchange}: {buy_spread_message}%\n"
                f"{'━' * 24}\n"        
                f"📊 Спред на біржі {best_sell_exchange}: {sell_spread_message}%\n"
                f"{'━' * 24}\n"        
                f"📊 Обсяг {best_buy_exchange}: {base_vol1}, {buy_perc}\n"
                f"{buy_perc}\n"
                f"{quote_vol1}\n"
                f"{'━' * 24}\n"        
                f"📊 Обсяг  {best_sell_exchange}: {base_vol2}, {sell_perc}\n"
                f"{sell_perc}\n"
                f"{quote_vol2}\n"
                f"{'━' * 24}\n"        
                f"💰 Розрахунковий баланс: **{balance:.2f} USDT**\n"
                f"{'━' * 24}\n"        
                f"💵 Розрахунковий прибуток на момент сигналу: **{best_profit_in_usdt:.2f} USDT**\n"
                f"{'━' * 24}\n"        
                f"📌 Оновлено: {formatted_time}\n")
        # Відправляємо повідомлення в Telegram
        print(message)
        #send_telegram_message(message)
                # Генерація випадкової затримки від 6 до 9 хвилин
        random_delay = random.randint(360,540)
        print(f"Час до наступного оновлення: {random_delay} секунд")
        time.sleep(random_delay)        
        message = (f"💎 продано : {best_pair} 💎\n\n"
                f"{'━' * 24}\n"        
                   f"💰 Оновлений баланс: {balance:.2f} USDT\n"
                f"{'━' * 24}\n"        
                   f"📈 Поточна ціна продажу: {best_sell_price:.5f} {best_pair.split('/')[1]}\n"
                f"{'━' * 24}\n"        
                   f"💵 Поточний прибуток: {best_profit_in_usdt:.2f} USDT")
        #send_telegram_message(message)

        last_sell_exchange = best_sell_exchange  # Оновлюємо останню біржу для продажу
    else:
        print("Не знайдено вигідних пар для торгівлі.")

# Викликаємо основну функцію
while True:
    start_time = time.time()  # Заміри часу початку
    compare_currency_pairs(exchanges_networks.unique_currency_pairs)
    end_time = time.time()  # Заміри часу закінчення
    elapsed_time = end_time - start_time  # Час, що пройшов
    
    print(f"\nПоточний баланс: {balance:.2f} USDT")
    print(f"Оновлення тривало {elapsed_time:.2f} секунд.")
    message = (f"Не знайдено вигідних пар для торгівлі.")
    message =(f"Оновлення тривало {elapsed_time:.2f} секунд.")
    print("\nОновлення завершено. Чекаємо 5 хвилин перед наступним оновленням...")

    n += 1

    random_delay_end = random.randint(60,240)
    time.sleep(random_delay_end)        
    # Поточний час у Київському часовому поясі
    kiev_time = datetime.now(kiev_timezone)

    # Форматування часу у вигляді рядка
    formatted_time = kiev_time.strftime('%Y-%m-%d %H:%M:%S')
    print("Поточний час у Київському часі:", formatted_time)

    # Якщо зараз 01:00, виконуємо оновлення
    if kiev_time.hour == 1 and kiev_time.minute in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        update_cache_and_blacklist()

    # Затримка на одну хвилину, щоб перевіряти кожну хвилину
    time.sleep(60)

