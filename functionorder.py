
import DDscrape
import Encoding
import time


db = input("Enter the Exact file path to The DataBase  ")
while True:
    start = time.perf_counter()
    Encoding.main(db,DDscrape.main(db))
    finish = time.perf_counter()
    print("Duration" + str(start-finish))


