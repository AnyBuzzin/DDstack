
import DDscrape
import Encoding
import time

new_list = ['https://www.donedeal.ie/cars-for-sale/volkswagen-passat-passat-1-6tdi-120bhp-trendline/27496233?campaign=10',
 'https://www.donedeal.ie/cars-for-sale/volkswagen-golf-gt-1-4tsi-120bhp/29802631',
  'https://www.donedeal.ie/cars-for-sale/2010-volkswagen-golf-gti-tsi-mk6/29801987',
   'https://www.donedeal.ie/cars-for-sale/mk6-golf/29798551'
   , 'https://www.donedeal.ie/cars-for-sale/volkswagen-golf-1-4-5-dr-7-speed-dsg-automatic/29563827', 'https://www.donedeal.ie/cars-for-sale/2012-volkswagen-golf-edition-r-1-6-tdi-105bhp-5dr/29798592', 'https://www.donedeal.ie/cars-for-sale/volkswagen-golf-1-4-tsi-7-speed-dsg-automatic-/29724471', 'https://www.donedeal.ie/cars-for-sale/volkswagen-golf-1-4-7-speed-dsg-automatic-/29672311', 'https://www.donedeal.ie/cars-for-sale/volkswagen-golf-estate-1-4-7-speed-dsg-automatic/29450773', 'https://www.donedeal.ie/cars-for-sale/volkswagen-golf-1-2-5dr-7-speed-dsg-automatic/29563828', 'https://www.donedeal.ie/cars-for-sale/12-vw-golf-tdi-rline-/29638749?campaign=3', 'https://www.donedeal.ie/cars-for-sale/volkswagen-golf-1-4-7-speed-dsg-automatic-/29672311?campaign=3', 'https://www.donedeal.ie/cars-for-sale/volkswagen-golf-estate-1-2-5dr-automatic-nationwi/29563848', 'https://www.donedeal.ie/cars-for-sale/volkswagen-golf-1-2-5dr-7-speed-dsg-automatic/29784183', 'https://www.donedeal.ie/cars-for-sale/volkswagen-golf-1-2-5d-r-7-speed-dsg-automatic/29784182', 'https://www.donedeal.ie/cars-for-sale/volkswagen-golf-1-4-tsi-7-speed-dsg-automatic-/29724471?campaign=3', 'https://www.donedeal.ie/cars-for-sale/golf-mk7-fresh-nct/29633508', 'https://www.donedeal.ie/cars-for-sale/volkswagen-polo-1-2-trendline-2010/29802934', 'https://www.donedeal.ie/cars-for-sale/volkswagen-polo-1-2-tdi-diesel/29436755?campaign=3', 'https://www.donedeal.ie/cars-for-sale/volkswagen-polo-1-2-5d-r-7-speed-dsg-automatic/29579690?campaign=3', 'https://www.donedeal.ie/cars-for-sale/volkswagen-polo-1-2-tsi-7-speed-dsg-automatic/29563844', 'https://www.donedeal.ie/cars-for-sale/volkswagen-polo-1-2-tsi-5-dr-7-speed-dsg-automatic/29563845', 
'https://www.donedeal.ie/cars-for-sale/volkswagen-polo-1-2-5d-r-7-speed-dsg-automatic/29579690', 'https://www.donedeal.ie/cars-for-sale/volkswagen-polo-1-2-5d-r-7-speed-dsg-automatic/29672310', 'https://www.donedeal.ie/cars-for-sale/volkswagen-polo-1-2-5d-r-7-speed-dsg-automatic/29672310?campaign=3', 'https://www.donedeal.ie/cars-for-sale/volkswagen-polo-1-2-tsi-5dr-7-speed-dsg-automatic/29560936', 'https://www.donedeal.ie/cars-for-sale/volkswagen-passat-highline-1-9tdi-sold-sold-sold/29742834', 'https://www.donedeal.ie/cars-for-sale/volkswagen-passat/29801760', 'https://www.donedeal.ie/cars-for-sale/08-volkswagen-passat-for-sale/29802563', 'https://www.donedeal.ie/cars-for-sale/volkswagen-passat-2008/29802499', 'https://www.donedeal.ie/cars-for-sale/2011-vw-passat-cc-2-0tdi/29799806?campaign=3', 'https://www.donedeal.ie/cars-for-sale/vw-passat-1-6tdi-comfortline-low-milage-nct2023/29164505', 'https://www.donedeal.ie/cars-for-sale/vw-passat-1-6tdi-comfortline-low-milage-nct2023/29164505?campaign=3', 'https://www.donedeal.ie/cars-for-sale/mercedes-e220-cdi-diesel-automatic-coupe/29450194?campaign=10', 'https://www.donedeal.ie/cars-for-sale/hyundai-sonata-auto-low-kilometres/29802735?campaign=10', 'https://www.donedeal.ie/cars-for-sale/hyundai-i40-diesel-saloon-ivory-leather/29802686?campaign=10', 'https://www.donedeal.ie/cars-for-sale/renault-zoe-iconic-r110-z-e-50-my19-r/29400169?campaign=10', 'https://www.donedeal.ie/cars-for-sale/renault-grand-scenic-scenic-3-bose-1-5/29671743?campaign=10', 'https://www.donedeal.ie/cars-for-sale/renault-zoe-play-r110-z-e-50-my19-ful/29226642?campaign=10', 'https://www.donedeal.ie/cars-for-sale/toyota-corolla/29800418', 'https://www.donedeal.ie/cars-for-sale/audi-a1-a1-sport-tdi-105bhp/29336006?campaign=10', 'https://www.donedeal.ie/cars-for-sale/audi-a4-a4-2-0tdi-150bhp-s-line-automatic/29274424?campaign=10', 'https://www.donedeal.ie/cars-for-sale/audi-a3-saloon-1-0tfsi-110-s-line-with-black-styl/26910380?campaign=10', 'https://www.donedeal.ie/cars-for-sale/jaguar-i-pace-all-electric-400ps-se-automatic/27700915?campaign=10', 'https://www.donedeal.ie/motorbikes-for-sale/honda-crf-africa-twin-super-adventure/29713382?campaign=10', 'https://www.donedeal.ie/cars-for-sale/toyota-yaris-luna-1-0-petrol/29800650', 'https://www.donedeal.ie/cars-for-sale/toyota-yaris-2008/29799852', 'https://www.donedeal.ie/motorbikes-for-sale/bmw-r1250-gs-adventure-rallye-te/29690683?campaign=10', 'https://www.donedeal.ie/cars-for-sale/toyota-yaris-1-0-low-miles-finance-available-/29800022', 'https://www.donedeal.ie/cars-for-sale/2012-toyota-yaris-1-0-petrol-5dr-nct-10-2023/29798212', 'https://www.donedeal.ie/cars-for-sale/toyota-yaris-toyota-yaris-automatic-5-dr-immacul/29800911', 'https://www.donedeal.ie/cars-for-sale/2008-audi-a4-auto/29800499', 'https://www.donedeal.ie/cars-for-sale/audi-a4-2009/29797727', 'https://www.donedeal.ie/cars-for-sale/audi-a4-2-0-tdi-technik-136ps-4dr/29802984', 'https://www.donedeal.ie/cars-for-sale/audi-a3-1-6-hatchback-low-km/29802648?campaign=3', 'https://www.donedeal.ie/cars-for-sale/2008-audi-a3-1-6-sportback/29801498?campaign=3', 'https://www.donedeal.ie/cars-for-sale/08-audi-a3-1-9tdi-nct-8-22/29802689', 'https://www.donedeal.ie/cars-for-sale/audi-a3-2008/29801899', 'https://www.donedeal.ie/cars-for-sale/2011-audi-a3-2-0-tdi-1-0wner-from-new/29802399', 'https://www.donedeal.ie/cars-for-sale/audi-a3-sportback-1-2-tfsi/29263254?campaign=3', 'https://www.donedeal.ie/cars-for-sale/audi-a3-2-0-tdi-nctd-12-23/29801885?campaign=3', 'https://www.donedeal.ie/cars-for-sale/audi-a3-s-line/29209057?campaign=3', 'https://www.donedeal.ie/cars-for-sale/audi-a3-sportback/29388939?campaign=3', 'https://www.donedeal.ie/cars-for-sale/audi-a3-1-6-tdi-s-line/29792207', 'https://www.donedeal.ie/cars-for-sale/bmw-1-6-mint-condition/29802306?campaign=3', 'https://www.donedeal.ie/cars-for-sale/bmw-1-6-mint-condition/29802306', 'https://www.donedeal.ie/cars-for-sale/bmw-1-series-d-sport-5dr-new-nct-200-road-tax/29802978', 'https://www.donedeal.ie/cars-for-sale/2013-bmw-1-series-2-0-diesel-nct-5-23/29802197',
 'https://www.donedeal.ie/cars-for-sale/bmw-320d-e92-only-169-000-km/29796642', 'https://www.donedeal.ie/cars-for-sale/bmw-320d-may-swap/28902506']

#input("Enter the Exact file path to The DataBase  ")
db = "C:\Windows\System32\lillymay/Carmex.sqlite3"
duration_list = []
while True:
    start = time.perf_counter()
    Encoding.main(db,DDscrape.main(db))
    finish = time.perf_counter()
    print("Duration" + str(start-finish))

