import time, requests, math, threading, pyautogui, datetime, csv
import hashlib, base64, hmac, json
from urllib.parse import urljoin, urlencode
from pyautogui import Point
from pairs import TRIANGLES
from decimal import Decimal as D

SECRET_KEY = ''
KEY = ''
BASE_URL = 'https://api.binance.com'
headers = {
    'X-MBX-APIKEY': KEY
}
FEE = 0.001
input = 50

def convert(pair):
    #Used to find the exchange rate between two currencies
    return float(requests.get("https://api.binance.com/api/v3/ticker/price?symbol=%s" % pair.upper()).json()['price'])

def convert_invert(pair):
    #Used to find the inverted exchange rate between two currencies
    return 1/float(requests.get("https://api.binance.com/api/v3/ticker/price?symbol=%s" % pair.upper()).json()['price'])

class triangle():
    #Class triangle is the triangle of pairs and their conversions
    def __init__(self, pairs):
        self.pair1 = pairs[0]
        self.pair2 = pairs[1]
        self.pair3 = pairs[2]

        #Each of the below parameters states whether the pair's exchange rate needs to be inverted
        self.pair1_invert = True
        self.pair2_invert = (self.pair1[:-4] != self.pair2[:len(self.pair1[:-4])])
        self.pair3_invert = False
    
    def get_conversions(self):
        #Retrives the exchange rates in a triangle and the final price
        c1 = convert_invert(self.pair1)
        c2 = convert_invert(self.pair2) if self.pair2_invert else convert(self.pair2)
        c3 = convert(self.pair3)
        return round(input*c1*c2*c3, 6)

def enact(pairs):
    #Initiates instance of triangle
    triangleObj = triangle(pairs)
    transac = str(pairs[0]) + " -> " + str(pairs[1]) + " -> " + str(pairs[2])
    global input
    #Infinite loop (stopped by moving mouse to top-left of screen) that gets the price change,
    #determines if it's profitable, and if so, records it in a csv file
    while True:
        f = triangleObj.get_conversions()
        if f > input:
            print("%s %30s %10s" % (datetime.datetime.now(), transac, round(f-input, 6)))
            with open('trading.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow([datetime.datetime.now(), transac, round(f-input, 6)])
            file.close()
            input += round(f-input, 6)
        time.sleep(0.5)
        if pyautogui.position() == Point(x=0, y=0):
            print("Final Balance: %s" % input)
            break

def main():
    print("%15s %33s %20s" % ("Time", "Transaction", "Profit (USDT)"))
    print("-------------------------------------------------------------------------")
    for item in TRIANGLES:
        #Creates a thread for each triangle and initates the trading
        threadobj = threading.Thread(target=enact, args=[item])
        threadobj.start()

main()