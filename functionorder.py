
import DDscrape
import Encoding
import time


db =  "C:\Windows\System32\lillymay/Carmex.sqlite3"
while True:
    start = time.perf_counter()
    Encoding.main(db,DDscrape.main(db))
    finish = time.perf_counter()
    print("Duration" + str(start-finish))


