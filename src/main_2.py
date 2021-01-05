import time, requests, math, threading, pyautogui, datetime, csv
import hashlib, base64, hmac, json
from urllib.parse import urljoin, urlencode
from pyautogui import Point
from pairs import TRIANGLES
from decimal import Decimal as D

SECRET_KEY = 'Rr68d5pQTHaSRiOTd0MOks97MMNxjqYRvcKkHdNOshCYZeNXxN4ytoQaBDFnSjli'
KEY = 'U9K9ViEqcFcLvCviDLLAIE7OMue47DZeg7z2O5XV5Ep5jfv9Qq8TnbaxZjVStPJm'
BASE_URL = 'https://api.binance.com'
headers = {
    'X-MBX-APIKEY': KEY
}
FEE = 0.001

def convert(pair):
    return float(requests.get("https://api.binance.com/api/v3/ticker/price?symbol=%s" % pair.upper()).json()['price'])

def convert_invert(pair):
    return 1/float(requests.get("https://api.binance.com/api/v3/ticker/price?symbol=%s" % pair.upper()).json()['price'])

class triangle():
    def __init__(self, pairs):
        self.pair1 = pairs[0]
        self.pair2 = pairs[1]
        self.pair3 = pairs[2]

        #Whether the conversion needs to be inverted
        self.pair1_invert = True
        self.pair2_invert = (self.pair1[:-4] != self.pair2[:len(self.pair1[:-4])])
        self.pair3_invert = False

        self.input = 50
    
    def get_conversions(self):
        c1 = convert_invert(self.pair1)
        c2 = convert_invert(self.pair2) if self.pair2_invert else convert(self.pair2)
        c3 = convert(self.pair3)
        return round(self.input*c1*c2*c3, 6)

def enact(pairs):
    triangleObj = triangle(pairs)
    input = triangleObj.input
    transac = str(pairs[0]) + " -> " + str(pairs[1]) + " -> " + str(pairs[2])
    while True:
        f = triangleObj.get_conversions()
        if f > input:
            print("%s %30s %10s" % (datetime.datetime.now(), transac, round(f-input, 6)))
            with open('trading.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow([datetime.datetime.now(), transac, round(f-input, 6)])
            file.close()
        time.sleep(0.5)
        if pyautogui.position() == Point(x=0, y=0):
            break

def main():
    print("%15s %33s %20s" % ("Time", "Transaction", "Profit (USDT)"))
    print("-------------------------------------------------------------------------")
    for item in TRIANGLES:
        threadobj = threading.Thread(target=enact, args=[item])
        threadobj.start()

main()