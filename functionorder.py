
import DDscrape
import Encoding
import time


db = input("Enter the Exact file path to The DataBase  ")
db  = "C:\Windows\System32\lillymay/Carmex.sqlite3"
while True:
    start = time.perf_counter()
    DDscrape.main(db)
    Encoding.main(db)
    finish = time.perf_counter()
    print("Duration" + str(start-finish))


