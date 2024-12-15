import ccxt

# Список валютних пар для порівняння
currency_pairs = [
    'AVAX/USDT', 'GRT/USDT', 'PEPE/USDT', 'EIGEN/USDT', 'TIA/USDT', 'UNI/USDT', 'TERRA/USDT',
    'ALGO/USDT', 'TON/USDT', 'CRV/USDT', 'MKR/USDT', 'SAND/USDT', 'BCH/USDT', 'SUSHI/USDT', 'SHIB/USDT', 'AAVE/USDT',
    'ADA/USDT', 'ARB/USDT', 'ICP/USDT', '1INCH/USDT', 'BTC/USDT', 'SOL/USDT','FORTH/USDT',
    'BLUR/USDT', 'FLOKI/USDT', 'CHZ/USDT', 'XLM/USDT', 'INJ/USDT', 'XRP/USDT', 'YFI/USDT', 'WOOT/USDT', 'DOT/USDT',
    'WIF/USDT', 'ETH/USDT', 'LTC/USDT', 'EGLD/USDT', 'TRX/USDT', 'USDC/USDT', 'FTM/USDT', 'SNX/USDT', 'MANA/USDT',
    'EUR/USDT', 'DOGE/USDT', 'LINK/USDT', 'MEW/USDT', 'STRK/USDT', 'SUI/USDT', 'AXS/USDT', 'USDT/USDT', 'DAI/USDT',
    'BONK/USDT', 'FIL/USDT', 'APT/USDT', 'ATOM/USDT', 'XTZ/USDT', 'APE/USDT', 'FET/USDT', 'COTI/USDT', 'LDO/USDT',
    'MATIC/USDT', 'BTC-T/USDT', 'GLMR/USDT', 'BMEX/USDT',  'WLD/USDT', 'AXS-S/USDT', 'DOGE/USDT',
    'MTR/USDT', 'QTUM/USDT', 'SC/USDT', 'ANKR/USDT', 'API3/USDT', 'THOR/USDT', 'JOE/USDT', 'REV/USDT',
    'SP500/USDT', 'BAK/USDT', 'PUMAX/USDT', 'DOE/USDT', 'GURU/USDT', 'NEMS/USDT', 'GPU/USDT', 'GIGA/USDT', 'DARA/USDT',
    'MOLI/USDT', 'CA/USDT', 'TBULL/USDT', 'AKI/USDT', 'AIC/USDT', 'KRU/USDT', 'EWT/USDT', 'TAMA/USDT', 'MARIA/USDT',
    'SNEK/USDT', 'SIX/USDT', 'EGO/USDT', 'ELA/USDT', 'RAKE/USDT', 'KATA/USDT', 'AGT/USDT', 'KLAUS/USDT', 
    'WPAY/USDT', 'SIXT/USDT', 'METO/USDT', 'DEOD/USDT', 'SOLAMA/USDT', 'BST/USDT', 'GROK/USDT', 'GUMMY/USDT',
    'DOME/USDT', 'IMGNAI/USDT', 'MARSH/USDT', 'GARI/USDT', 'WORK/USDT', 'ALI/USDT', 'MAGNET/USDT', 'GOAT/USDT',
    'PBUX/USDT', 'PNK/USDT', 'ESE/USDT', 'KARRAT/USDT', 'STBU/USDT', 'STARK/USDT', 'PEANUT/USDT', 'SANTOS/USDT', 'ACT1/USDT'
    #  'ZERO/USDT','COME/USDT','SYN/USDT', 'WX/USDT', 'JUP/USDT', 'ETC/USDT','BTT/USDT','POLS/USDT', 'SCRT/USDT',
]
# Використовуємо множину, щоб позбутись дублікатів
unique_currency_pairs = list(set(currency_pairs))

# Ініціалізація об'єктів для бірж
binance = ccxt.binance()
ascendex = ccxt.ascendex()
bingx = ccxt.bingx()
bitget = ccxt.bitget()
bitmart = ccxt.bitmart()
bitrue = ccxt.bitrue()
bybit = ccxt.bybit()
coinbase = ccxt.coinbase()
cryptocom = ccxt.cryptocom()
exmo = ccxt.exmo()
gateio = ccxt.gateio()
hitbtc = ccxt.hitbtc()
htx = ccxt.htx()
kraken = ccxt.kraken()
kucoin = ccxt.kucoin()
mexc = ccxt.mexc()
okx = ccxt.okx()
poloniex = ccxt.poloniex()
whitebit = ccxt.whitebit()
xt = ccxt.xt()

#Завантаження ринків для кожної біржі
exchanges = {
    'binance': binance,
    'ascendex': ascendex,
    'bingx': bingx,
    'bitget': bitget,
    'bitmart': bitmart,
    'bitrue': bitrue,
    'bybit': bybit,
    'coinbase': coinbase,
    'cryptocom': cryptocom,
    'exmo': exmo,
    'gateio': gateio,
    'hitbtc': hitbtc,
    'htx': htx,
    'kraken': kraken,
    'kucoin': kucoin,
    'mexc': mexc,
    'okx': okx,
    'poloniex': poloniex,
    'whitebit': whitebit,
    'xt': xt
}

pair_good_exchanges = {}