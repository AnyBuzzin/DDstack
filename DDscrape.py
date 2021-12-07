from bs4 import BeautifulSoup
import requests
import sqlite3
from datetime import datetime, timedelta
from rich.progress import track
import concurrent.futures



### BS4 url request and card identifier and link###
def url_genorator() -> list:
    ### This function is far from optimal but it preforms it's function ###
    ### Needs optimizations ### 
	### Any Vehicle Added Here Needs to be Manually Encoded ### 
	extensions = {'/Volkswagen':['/Golf/','/Polo/','/Passat/'],
	'/Toyota':['/Corolla/','/Yaris/'],
	'/Audi':['/A4/','/A3/'],
	'/BMW':['/1-Series/','/3-Series/']}
	carlist = []
	carlist1 = []
	Page = '?start='
	URLS = []
	DD = 'https://www.donedeal.ie/cars'
	for x, value in extensions.items():
		for i in value:
			car = (x+i)
			carlist.append(car)
	Year = 2007
	for i in carlist:
	    for s in range(Year,2015):
	        carlist1.append(i + str(s))
	for y in carlist1:
	    j = 0
	    for _ in range(12):
	        URLS.append(DD + y + Page + str(j))
	        j += 14
	return URLS
def request_url(URL: str) -> str:
	###Sends a GET request to specified URL Using Requests libary###
	###Then Uses BeautifulSoup to Parse the raw html to lxml###
	try:
		html_text = requests.get(URL).text
		return (BeautifulSoup(html_text, "lxml" ))
	except:
		print("No Such URL")
		return None
def ident_cards(URL: str) -> str:
	###Takes lxml as input and returns all card items found in the lxml###
	links = []
	try:
		cards = request_url(URL).find_all("li", class_ = "card-item")
	except:
		print("No List items at this Url")
	for i in cards:
		links.append(i.find("a").get("href"))
	return links
def sterling_to_euro():
	html_text = requests.get('https://www.xe.com/currencyconverter/convert/?Amount=1&From=GBP&To=EUR').text
	html_format = (BeautifulSoup(html_text, 'lxml' ))
	exchangerate = html_format.find('p', class_='result__BigRate-sc-1bsijpp-1 iGrAod').text
	exchangerate = float(exchangerate[0:5])
	return exchangerate


### SQL Functions to check if a Car already exists in the DB ###
### SQL DB creation and table creation ###
def create_connection(db_path) -> sqlite3:
		conn = None
		try:
			conn = sqlite3.connect(db_path)
		except:
			print("Connot connect to this DataBase")
		return conn
def create_cursor(conn) -> sqlite3:
		c = None
		try:
			c = conn.cursor()
		except:
			print("Cannot connect to this DataBase")
		return c
def duplicate_check(rawlist,conn,c) -> sqlite3:
	clear =  []
	with conn:
		for i in rawlist:
			c.execute("SELECT * FROM RawCars WHERE URL=:URL",{'URL' : i})
			if len(c.fetchall()) > 0:
				rawlist.remove(i)
			elif i not in clear:
				clear.append(i)
	return clear
def create_table(c) -> sqlite3:
	c.execute("""CREATE TABLE IF NOT EXISTS RawCars(
					URL text,
					SellerName text,
					SellerType text,
					SellerVerification text,
					SellerAvgResponseRate text,
					SellerDonedealingSince text,
					SellerActiveAds text,
					SellerLifeTimeAds text,
					CarLocation text,
					CarMake text,
					CarModel text,
					CarYear text,
					CarBodyType text,
					CarSeats text,
					CarFuelType text,
					CarTransmission text,
					CarMillage text,
					CarEngineSize text,
					CarNCTExpiry text,
					CarTax text,
					CarColour text,
					AdViews text,
					CarPrice text,
					UploadDate datetime,
					TSU text)
					""")
	c.execute("""CREATE TABLE IF NOT EXISTS EncodedCars(
					URL text,
					SellerName text,
					SellerType int,
					SellerVerification int,
					SellerAvgResponseRate int,
					SellerDonedealingSince int,
					SellerActiveAds int,
					SellerLifeTimeAds int,
					CarLocation text,
					CarMake text,
					CarModel int,
					CarYear int,
					CarBodyType int,
					CarSeats int,
					CarFuelType int,
					CarTransmission int,
					CarMillage int,
					CarEngineSize int,
					CarNCTExpiry text,
					CarTax int,
					CarColour int,
					AdViews int,
					CarPrice int,
					UploadDate datetime,
					TSU int)
					""")
def insert_car(car,conn,c) -> sqlite3:
		with conn:
			c.execute("""INSERT INTO RawCars VALUES (
					:URL,
					:SellerName,
					:SellerType,
					:SellerVerification,
					:SellerAvgResponseRate,
					:SellerDonedealingSince,
					:SellerActiveAds,
					:SellerLifeTimeAds,
					:CarLocation,
					:CarMake,
					:CarModel,
					:CarYear,
					:CarBodyType,
					:CarSeats,
					:CarFuelType,
					:CarTransmission,
					:CarMillage,
					:CarEngineSize,
					:CarNCTExpiry,
					:CarTax,
					:CarColour,
					:AdViews,
					:CarPrice,
					:UploadDate,
					:TSU)""",
			{'URL':car.link, 'SellerType':car.SellerType,
		'SellerName':car.SellerName,
		'SellerVerification':car.SellerVerification, 'SellerAvgResponseRate':car.SellerAvgResponseRate,
		'SellerDonedealingSince':car.SellerDonedealingSince, 'SellerActiveAds':car.SellerActiveAds,
		'SellerLifeTimeAds':car.SellerLifeTimeAds,
		'CarLocation':car.location, 'CarMake':car.Make,
		'CarModel':car.Model, 'CarYear':car.Year,
		'CarBodyType':car.BodyType, 'CarSeats':car.Seats, 'CarFuelType':car.FuelType,
		'CarTransmission':car.Transmission,'CarMillage':car.Millage,
		'CarEngineSize':car.EngineSize,'CarNCTExpiry':car.NCTExpiry,
		'CarTax':car.Tax, 'CarColour':car.Colour,
		'AdViews':car.AdViews, 'CarPrice':car.Price, 'UploadDate':car.UploadDate,
		'TSU':car.TSU})

			c.execute("""INSERT INTO EncodedCars VALUES (
					:URL,
					:SellerName,
					:SellerType,
					:SellerVerification,
					:SellerAvgResponseRate,
					:SellerDonedealingSince,
					:SellerActiveAds,
					:SellerLifeTimeAds,
					:CarLocation,
					:CarMake,
					:CarModel,
					:CarYear,
					:CarBodyType,
					:CarSeats,
					:CarFuelType,
					:CarTransmission,
					:CarMillage,
					:CarEngineSize,
					:CarNCTExpiry,
					:CarTax,
					:CarColour,
					:AdViews,
					:CarPrice,
					:UploadDate,
					:TSU)""",
		{'URL':car.link, 'SellerType':car.SellerType,
		'SellerName':car.SellerName,
		'SellerVerification':car.SellerVerification, 'SellerAvgResponseRate':car.SellerAvgResponseRate,
		'SellerDonedealingSince':car.SellerDonedealingSince, 'SellerActiveAds':car.SellerActiveAds,
		'SellerLifeTimeAds':car.SellerLifeTimeAds,
		'CarLocation':car.location, 'CarMake':car.Make,
		'CarModel':car.Model, 'CarYear':car.Year,
		'CarBodyType':car.BodyType, 'CarSeats':car.Seats, 'CarFuelType':car.FuelType,
		'CarTransmission':car.Transmission,'CarMillage':car.Millage,
		'CarEngineSize':car.EngineSize,'CarNCTExpiry':car.NCTExpiry,
		'CarTax':car.Tax, 'CarColour':car.Colour,
		'AdViews':car.AdViews, 'CarPrice':car.Price, 'UploadDate':car.UploadDate,
		'TSU':car.TSU})



### All functions for extracing specific data about each Seller ###
### All functions return STRING values if the data is found. ###
### If the data is not Found the functions will retun a BOOL value of NONE ###
### All Functions Take LXML STRINGS as inputs ###
### Data is extracted directly from Advert Specific URL ###
def data_extraction(URL) -> object:  # sourcery no-metrics
	print(URL)
	lxml = request_url(URL)
	exchangerate = sterling_to_euro()

	try:
		conn = sqlite3.connect("C:\Windows\System32\lillymay/Carmex.sqlite3")
	except:
		print("Connot connect to this DataBase")
	try:
		c = conn.cursor()
	except:
		print("Cannot connect to this DataBase")


	
	### All functions for extracing specific data about each car ###
	### All functions return STRING values if the data is found. ###
	### If the data is not Found the functions will retun a BOOL value of NONE ###
	### All Functions Take LXML STRINGS as inputs ###
	### Data is extracted directly from Advert Specific URL ###
	
	def Car_creation() -> object:  # sourcery no-metrics
		
		class Car:

			def __init__(self, link, SellerType, SellerName, SellerVerification, SellerAvgResponseRate, SellerDonedealingSince, SellerActiveAds, SellerLifeTimeAds, location, Make, Model, Year, BodyType, Seats, FuelType, Transmission, Millage, EngineSize, NCTExpiry, Tax, Colour, AdViews, Price, UploadDate, TSU):
				self.link = link
				self.SellerType = SellerType
				self.SellerName = SellerName
				self.SellerVerification = SellerVerification
				self.SellerAvgResponseRate = SellerAvgResponseRate
				self.SellerDonedealingSince = SellerDonedealingSince
				self.SellerActiveAds = SellerActiveAds
				self.SellerLifeTimeAds = SellerLifeTimeAds
				self.location = location
				self.Make = Make
				self.Model = Model
				self.Year = Year
				self.BodyType = BodyType
				self.Seats = Seats
				self.FuelType = FuelType
				self.Transmission = Transmission
				self.Millage = Millage
				self.EngineSize = EngineSize
				self.NCTExpiry = NCTExpiry
				self.Tax = Tax
				self.Colour = Colour
				self.AdViews = AdViews
				self.Price = Price
				self.UploadDate = UploadDate
				self.TSU = TSU

			def __str__(self):
				return str(self.__class__) + ": " + str(self.__dict__)


		def CarData() -> list:
			try:
				return str(lxml.find("div", "KeyInfoList__Grid-sc-sxpiwc-0 gThfCS")).replace('<div class="KeyInfoList__Text-sc-sxpiwc-2 dGjCWx">', '').replace('<div class="KeyInfoList__KeyInfoListItem-sc-sxpiwc-1 cgHAZD">', ' ').replace('<div class="KeyInfoList__Text-sc-sxpiwc-2 dQdfES">', ',').replace("</div>", '').replace('<div class="KeyInfoList__Grid-sc-sxpiwc-0 gThfCS">', '').replace('<div class="Tooltip__Container-sc-1bir2sn-8 dpLbMZ"><div class="Tooltip__CTAContainer-sc-1bir2sn-9 jdZosK"><svg class="KeyInfoList__SIoInformationCircleOutline-sc-sxpiwc-3 bIKcNQ" data-testid="info-icon" fill="none" height="18" viewbox="0 0 24 24" width="18"><path d="M12 2C6.478 2 2 6.478 2 12s4.478 10 10 10 10-4.478 10-10S17.522 2 12 2z" stroke="currentColor" stroke-miterlimit="10" stroke-width="1.6"></path><path d="M10.479 10.48h1.74v6.304" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.6"></path><path d="M9.827 17.002h4.782" stroke="currentColor" stroke-linecap="round" stroke-miterlimit="10" stroke-width="1.6"></path><path d="M12 5.588a1.413 1.413 0 100 2.826 1.413 1.413 0 000-2.826z" fill="currentColor"></path></svg>', '').replace(' ', ',').split(",")
			except:
				print("Car Data Error")
				return None
		def SellerType() -> str:
			try:
				data = lxml.find("ul", "InfoTitle__SubtitleList-sc-qp6c10-3 jmKENu").text
				if "Private Seller" in data:
					return "Private Seller"
				else:
					return data
			except AttributeError:
				return None
		def SellerName() -> str:
			try:
				return lxml.find("p","InfoTitle__Title-sc-qp6c10-2 hyLdjl").text
			except AttributeError:
				return None
		def SellerVerification() -> str:
			try:
				return lxml.find("div", "VerifiedList__VerifiedContainer-sc-sahzdv-1 gmmHkd SellerInfoPanel__SVerifiedList-sc-1vsx0ry-11 hyuRLv").find('div',"VerifiedList__P-sc-sahzdv-0 frAZPz").text
			except AttributeError:
				return None
		def SellerResponseRate() -> str:
			try:
				return str(lxml.find("div", "SellerInfoPanel__AdCountStats-sc-1vsx0ry-4 kflWjg").find("p", "SellerInfoPanel__StatsValue-sc-1vsx0ry-6 fWBapn").text).replace('%','').replace('<50','50').replace('-','0').replace('< 50','50')
			except AttributeError:
				return None
		def SellerDDSince() -> str:
			try:
				return lxml.find("div", "SellerInfoPanel__AdCountStats-sc-1vsx0ry-4 kflWjg").find_next("p", "SellerInfoPanel__StatsValue-sc-1vsx0ry-6 fWBapn").find_next("p", "SellerInfoPanel__StatsValue-sc-1vsx0ry-6 fWBapn").find_next("p", "SellerInfoPanel__StatsValue-sc-1vsx0ry-6 fWBapn").text
			except AttributeError:
				return None
		def SellerActiveADS() -> str:
			try:
				return lxml.find("div", "SellerInfoPanel__AdCountStats-sc-1vsx0ry-4 kflWjg").find_next("p", "SellerInfoPanel__StatsValue-sc-1vsx0ry-6 fWBapn").find_next("p", "SellerInfoPanel__StatsValue-sc-1vsx0ry-6 fWBapn").find_next("p", "SellerInfoPanel__StatsValue-sc-1vsx0ry-6 fWBapn").find_next("p", "SellerInfoPanel__StatsValue-sc-1vsx0ry-6 fWBapn").text
			except  AttributeError:
				return None
		def SellerLifeTimeADS() -> str:
			try:
				return str(lxml.find("div", "SellerInfoPanel__AdCountStats-sc-1vsx0ry-4 kflWjg").find_next("p", "SellerInfoPanel__StatsValue-sc-1vsx0ry-6 fWBapn").find_next("p", "SellerInfoPanel__StatsValue-sc-1vsx0ry-6 fWBapn").find_next("p", "SellerInfoPanel__StatsValue-sc-1vsx0ry-6 fWBapn").find_next("p", "SellerInfoPanel__StatsValue-sc-1vsx0ry-6 fWBapn").find_next("p", "SellerInfoPanel__StatsValue-sc-1vsx0ry-6 fWBapn").text).replace("+",'')
			except  AttributeError:
				return None
		def CarLocation() -> str:
			try:
				return lxml.find("div", "InfoTitle__InfoTitleContainer-sc-qp6c10-0 iPMvez AdTitleBox__SInfoTitle-sc-1p2v1sf-0 bWrJlh").find("li", "InfoTitle__SubtitleItem-sc-qp6c10-4 MWEbJ").find_next("li", "InfoTitle__SubtitleItem-sc-qp6c10-4 MWEbJ").find_next("li", "InfoTitle__SubtitleItem-sc-qp6c10-4 MWEbJ").text
			except AttributeError:
				return None
		def CarMake(csv) -> str:
			try: 
				for i in range(len(csv)):
					if csv[i] == "Make/Model" and csv[i+1] != "/":
						return csv[i+1]
					else:
						return csv[i+4]
			except:
				print("No make found for this Car")
				return None
		def CarModel(csv) -> str:
			try: 
				for i in range(len(csv)):
					if csv[i-1] == "/":
						return csv[i+3]
			except:
				print("No make found for this Car")
				return None
		def CarYear(csv) -> str:
			try: 
				for i in range(len(csv)):
					if csv[i] == "Year":
						return csv[i+1]
			except:
				print("No make found for this Car")
				return None
		def CarBodyType(csv) -> str:
			try:
				for i in range(len(csv)):
					if csv[i] == "Body" and csv[i+1] == "Type":
						return str(csv[i+2]).replace('null', '0')
			except:
				print("No fuel Type found")
				return None
		def CarSeats(csv) -> str:
			try:
				for i in range(len(csv)):
					if csv[i] == "Seats":
						return csv[i+1]
			except:
				print("No fuel Type found")
				return None
		def CarFuelType(csv) -> str:
			try:
				for i in range(len(csv)):
					if csv[i] == "Fuel" and csv[i+1] == "Type":
						return csv[i+2]
			except:
				print("No fuel Type found")
				return None
		def CarTransmission(csv) -> str:
			try: 
				for i in range(len(csv)):
					if csv[i] == "Transmission":
						return str(csv[i+1]).replace('null', '0')
			except:
				print("No Transmission found for this Car")
				return None
		def CarMillage(csv) -> str:
			try: 
				for i in range(len(csv)):
					if csv[i] == "Mileage":
						return str(csv[i+1]+csv[i+2]+csv[i+3]).replace("Fuel","").replace("Type","").replace("---","")
			except:
				print("No Millage found for this Car")
				return None
		def CarEngineSize(csv) -> str:
			try:
				for i in range(len(csv)):
					if csv[i] == "(Litres)":
						return (float(csv[i+1])*1000)
			except:
				print("No Engine Size found")
				return None
		def CarNCTExpiry(csv) -> str:
			try: 
				for i in range(len(csv)):
					if csv[i] == "Expiry":
						return csv[i+1]+csv[i+2]
			except:
				return None
		def CarTax(csv) -> str:
			try: 
				for i in range(len(csv)):
					if csv[i] == "Tax":
						return csv[i+1]
			except:
				print("No TAX for this Car")
				return None
		def CarColour(csv) -> str:
			try:
				for i in range(len(csv)):
					if csv[i] == "Colour":
						return csv[i+1]
			except:
				print("No fuel Type found")
				return None
		def AdViews() -> str:
			try:
				return str(lxml.find("div", "InfoTitle__InfoTitleContainer-sc-qp6c10-0 iPMvez AdTitleBox__SInfoTitle-sc-1p2v1sf-0 bWrJlh").find("li", "InfoTitle__SubtitleItem-sc-qp6c10-4 MWEbJ").find_next("li", "InfoTitle__SubtitleItem-sc-qp6c10-4 MWEbJ").text).replace("views",'').replace(",",'')
			except:
				print("No AD Views Found")
				return None
		def CarPrice() -> str:
			try:
				price =  str(lxml.find("p", "Price__CurrentPrice-sc-e0e8wj-0 locENk").text).replace("€","").replace(",","")
				if "£" in price:
					sterling = price.replace("£","")
					return round(int(sterling)*exchangerate)
				else:
					return price
			except:
				print("No Listed Price Here")
				return None
		def UploadDate() -> sqlite3:

			t1 = datetime(year = datetime.now().year,
						month = datetime.now().month,
						day = datetime.now().day,
						minute = datetime.now().minute,
						second = datetime.now().second)
			try:
				TSU = lxml.find("div", "InfoTitle__InfoTitleContainer-sc-qp6c10-0 iPMvez AdTitleBox__SInfoTitle-sc-1p2v1sf-0 bWrJlh").find("li", "InfoTitle__SubtitleItem-sc-qp6c10-4 MWEbJ").text	
				
				if 'min' in TSU or 'mins' in TSU:
					minutessince = str(TSU).replace(' mins', '').replace(' min', '')
					return t1 - timedelta(minutes = int(minutessince))
				
				elif 'hours' in TSU or 'hour' in TSU:
					hourssince = str(TSU).replace(' hours', '').replace(' hour', '')
					return t1 - timedelta(hours = int(hourssince))

				elif 'days' in TSU or 'day' in TSU:
					daysince = str(TSU).replace(' days', '').replace(' day', '')
					return t1 - timedelta(days = int(daysince))
			except:
				print("No UploadDate found Here")
			return None	
		
		def Car_Object(csv) -> object:
			try:
				return Car(str(URL),
						SellerType(),
						SellerName(),
						SellerVerification(),
						SellerResponseRate(),
						SellerDDSince(),
						SellerActiveADS(),
						SellerLifeTimeADS(),
						CarLocation(),
						CarMake(csv),
						CarModel(csv),
						CarYear(csv),
						CarBodyType(csv),
						CarSeats(csv),
						CarFuelType(csv),
						CarTransmission(csv),
						CarMillage(csv),
						CarEngineSize(csv),
						CarNCTExpiry(csv),
						CarTax(csv),
						CarColour(csv),
						AdViews(),
						CarPrice(),
						UploadDate(),
						0)
			except:
				print("Cannot Construct Car Object From This DATA")
				return None
		csv = CarData()
		return Car_Object(csv)

	insert_car(Car_creation(),conn,c)


### TO DO def SellerPhoneNumber():### ### TO DO needs Clicking function to reveal number ###
### TO DO add date/time value compared to the TSU ###  


def main(db_path):
	conn = create_connection(db_path)
	c = create_cursor(conn)
	create_table(c)
	links = []
	clear = []
	testlist = ["https://www.donedeal.ie/cars"]
	with concurrent.futures.ThreadPoolExecutor() as executor:
		results = [executor.submit(ident_cards, x) for x in url_genorator()]
		for f in concurrent.futures.as_completed(results):	
			links += f.result()
		clear = duplicate_check(links,conn,c)
		cars = [executor.submit(data_extraction, x)for x in clear]
		for f in concurrent.futures.as_completed(cars):
			f.result()
	print("New Cars Scraped = ", len(clear))
	return clear

if __name__ == "__main__":
	main()


