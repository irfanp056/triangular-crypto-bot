#Related functions that might be useful (in no particular order)

#Information about user's account (balances, persmissions, etc.)
def snapshot():
    PATH = '/api/v3/account'
    timestamp = int((time.time() *1000))
    params = {
        'timestamp': timestamp
    }
    query_string = urlencode(params)
    params['signature'] = hmac.new(SECRET_KEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BASE_URL, PATH)
    r = requests.get(url, headers=headers, params=params)
    return r.json()

#Getting the server time - useful to stay synced
def get_server_time():
    PATH =  '/api/v1/time'
    params = None
    timestamp = int(time.time() * 1000)
    url = urljoin(BASE_URL, PATH)
    r = requests.get(url, params=params)
    print(url)
    print(r.json())

#Order a pair
def order(pair, side, quantity):
    PATH = '/api/v3/order'
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': pair,
        'side': side,
        'type': 'MARKET',
        'quantity': quantity,
        'recvWindow': 60000,
        'timestamp': timestamp
    }
    query_string = urlencode(params)
    params['signature'] = hmac.new(SECRET_KEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BASE_URL, PATH)
    r = requests.post(url, headers=headers, params=params)
    print(r.json())

#See all available orders on the exchange
def open_orders():
    PATH = '/api/v3/openOrders'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp
    }
    query_string = urlencode(params)
    params['signature'] = hmac.new(SECRET_KEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BASE_URL, PATH)
    r = requests.get(url, headers=headers, params=params)
    print(r.json())

#View exchange order book
def order_book():
    PATH = '/api/v3/ticker/bookTicker'
    url = urljoin(BASE_URL, PATH)
    r = requests.get(url)
    print(r.json())

#Custom rounding down function
def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

#Lists all pairs on Binance
def get_pairs():
    PATH = '/api/v3/exchangeInfo'
    url = urljoin(BASE_URL, PATH)
    r = requests.get(url, headers=headers)
    return r.json()

#Strip specific letters (e.g "USDT") from a string
def stripf(word, term):
    return word.replace(term, "")

#Returns whether each pair in a triangleneeds to be bought or sold in triangular arbitrage transaction
def sides(pairs):
    strip = lambda x: x.replace("USDT", "")
    if pairs[0][-4:] == 'USDT':
        first = "BUY"
    else:
        first = False
    if strip(pairs[0]) == pairs[1][:-len(strip(pairs[0]))]:
        second = "SELL"
    else:
        second = "BUY"
    if "USDT" == pairs[2][-4:]:
        third = "SELL"
    else:
        third = "BUY"
    return first, second, third

#The number of decimals a pair allows for its price when making an order
def get_precision(pairs):
    precisions = []
    info = requests.get("https://www.binance.com/api/v1/exchangeInfo").json()
    for pair in pairs:
        i = PAIRS.index(pair)
        ticksize = info["symbols"][i]["filters"][0]['tickSize']
        precision = abs(round(math.log(float(ticksize), 10)))
        precisions.append(precision)
    print("precisions: %s" % precisions)
    return precisions

#List allpairs on the exchange
def print_all_pairs():
    r = requests.get("https://api.binance.com/api/v3/ticker/price")
    print(r.json())

#Find price of specific pair
def price(pair):
    r = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={pair}")
    return r.json()

#Find the continuous price change of one pair
def price_change(pair):
    p = price(pair)
    print(p)
    while True:
        num = price(pair)
        if num != p:
            r = num-p
            change = f"{r:.9f}"
            t = time.time()
            print(f"Price: {num} | Change: {change} | Time (s): {t}")
            p = num
    return ""