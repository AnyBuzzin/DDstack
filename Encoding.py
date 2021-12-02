from math import sqrt
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd 
from datetime import datetime, timedelta
import numpy as np
from statistics import mode,mean,pstdev
from bs4 import BeautifulSoup
import requests
from rich.progress import track
from sklearn import linear_model, preprocessing
import concurrent.futures


### SQL Connection,crsor, and instertion  functions
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
def creat_tables(c,conn) -> sqlite3:
	with conn:
		c.execute("""CREATE TABLE IF NOT EXISTS PrivateSellersEncoded(
							URL text,
							SellerName text,
							SellerType int,
							Sellerlocation text,
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
							CarEngineSize float(53),
							CarNCTExpiry text,
							CarTax int,
							CarColour int,
							AdViews int,
							CarPrice int,
							UploadDate datetime,
							TSU int)
							""")
		c.execute("""CREATE TABLE IF NOT EXISTS DealershipsEncoded(
						URL text,
						SellerName text,
						SellerType int,
						Sellerlocation text,
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
						CarEngineSize float(53),
						CarNCTExpiry text,
						CarTax int,
						CarColour int,
						AdViews int,
						CarPrice int,
						UploadDate datetime,
						TSU int)
						""")
def insert_into_tables(c,conn) -> sqlite3:
	with conn:
		c.execute(""" SELECT * FROM EncodedCars WHERE SellerType = 3;""")
		privateseller = c.fetchall()
		for _ in privateseller:
			c.execute("""INSERT INTO PrivateSellersEncoded VALUES (
						:URL,
						:SellerName,
						:SellerType,
						:Sellerlocation,
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
				{'URL':_[0], 'SellerType':_[2],
			'SellerName':_[1], 'Sellerlocation':_[3],
			'SellerVerification':_[4], 'SellerAvgResponseRate':_[5],
			'SellerDonedealingSince':_[6], 'SellerActiveAds':_[7],
			'SellerLifeTimeAds':_[8],
			'CarLocation':_[9], 'CarMake':_[10],
			'CarModel':_[11], 'CarYear':_[12],
			'CarBodyType':_[13], 'CarSeats':_[14], 'CarFuelType':_[15],
			'CarTransmission':_[16],'CarMillage':_[17],
			'CarEngineSize':_[18],'CarNCTExpiry':_[19],
			'CarTax':_[20], 'CarColour':_[21],
			'AdViews':_[22], 'CarPrice':_[23],'UploadDate':_[24],
			'TSU':_[25]})

		c.execute(""" SELECT * FROM EncodedCars WHERE SellerType = 1 OR SellerType = 2;""")
		dealership  = c.fetchall()
		for _ in dealership:
			c.execute("""INSERT INTO DealershipsEncoded VALUES (
						:URL,
						:SellerName,
						:SellerType,
						:Sellerlocation,
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
				{'URL':_[0], 'SellerType':_[2],
			'SellerName':_[1], 'Sellerlocation':_[3],
			'SellerVerification':_[4], 'SellerAvgResponseRate':_[5],
			'SellerDonedealingSince':_[6], 'SellerActiveAds':_[7],
			'SellerLifeTimeAds':_[8],
			'CarLocation':_[9], 'CarMake':_[10],
			'CarModel':_[11], 'CarYear':_[12],
			'CarBodyType':_[13], 'CarSeats':_[14], 'CarFuelType':_[15],
			'CarTransmission':_[16],'CarMillage':_[17],
			'CarEngineSize':_[18],'CarNCTExpiry':_[19],
			'CarTax':_[20], 'CarColour':_[21],
			'AdViews':_[22], 'CarPrice':_[23],'UploadDate':_[24],
			'TSU':_[25]})
def request_url(URL: str) -> str:
	###Sends a GET request to specified URL Using Requests libary###
	###Then Uses BeautifulSoup to Parse the raw html to lxml###
        try:
            html_text = requests.get(URL).text
            return (BeautifulSoup(html_text, "lxml" ))
        except:
            print("No Such URL")
            return None

### All following function manipulate the EncodedCars Table
### Every function Encodes a colunm in a specific way
### Each Function has a LEGEND to describe the label Encoding and any other encoding methods
#  
def seller_type_encoder(c,conn) -> sqlite3:
	### LEGEND ###
	# 1 = independent dealer
	# 2 = franchise dealer
	# 3 = private seller
	
	def independent_dealer(c,conn) -> sqlite3:
		with conn:
			c.execute("""UPDATE EncodedCars SET SellerType = 1 WHERE SellerType = :independentDealer;"""
			,{'independentDealer': "Independent Dealer"})
	
	def franchise_dealer(c,conn) -> sqlite3:
		with conn:
			c.execute("""UPDATE EncodedCars SET SellerType = 2 WHERE SellerType = :FranchiseDealer;"""
			,{'FranchiseDealer': "Franchise Dealer"})

	def private_seller(c,conn) -> sqlite3:
		
		with conn:
			c.execute("""UPDATE EncodedCars SET SellerType = 3 WHERE SellerType = :PrivateSeller;"""
			,{'PrivateSeller': "Private Seller"})
	
	def non_numerical_drop(c,conn):
		with conn:
			c.execute("""DELETE FROM EncodedCars WHERE SellerType > 3 OR SellerType IS NULL;""")
			conn.commit
			return c.fetchall

	independent_dealer(c,conn)
	franchise_dealer(c,conn)
	private_seller(c,conn)
	non_numerical_drop(c,conn)

def car_fuel_encoder(c,conn) -> sqlite3:
	### LEGEND ###
	# 1 = Petrol
	# 2 = Diesel
	# 3 = Hybrid
	# 4 = Eletric
	def petrol(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarFuelType = 1 WHERE CarFuelType = :Petrol;""",
			{'Petrol': 'Petrol' })
	
	def diesel(c,conn) -> sqlite3:
		with conn:
				c.execute(""" UPDATE EncodedCars SET CarFuelType = 2 WHERE CarFuelType = :Diesel;""",
				{'Diesel': 'Diesel' })

	def hybrid(c,conn) -> sqlite3:
		with conn:
				c.execute(""" UPDATE EncodedCars SET CarFuelType = 3 WHERE CarFuelType = :Hybrid;""",
				{'Hybrid': 'Hybrid' })

	def electric(c,conn) -> sqlite3:
		with conn:
				c.execute(""" UPDATE EncodedCars SET CarFuelType = 4 WHERE CarFuelType = :Electric;""",
				{'Electric': 'Electric' })

	def non_numerical_drop(c,conn):
		with conn:
			c.execute("""DELETE FROM EncodedCars WHERE CarFuelType = '---' OR CarFuelType IS NULL OR CarFuelType = 'Other';""")
			conn.commit


	def na_drop(c,conn) -> sqlite3:
		with conn:
			c.execute("""DELETE FROM EncodedCars WHERE CarFuelType = 'n/a';""")
			conn.commit

			


	petrol(c,conn)
	diesel(c,conn)
	hybrid(c,conn)
	electric(c,conn)
	non_numerical_drop(c,conn)
	na_drop(c,conn)

def car_transmission_encoder(c,conn) -> sqlite3:
	### LEGEND ### 
	# 0 = No Date
	# 1 = Manual
	# 2 = Automatic

	def no_data(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarTransmission = 0 WHERE CarTransmission = '---' OR CarTransmission > 2;""")

	def manual(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarTransmission = 1 WHERE CarTransmission = :Manual;""",
			{'Manual':'Manual'})

	def automatic(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarTransmission = 2 WHERE CarTransmission = :Automatic;""",
			{'Automatic':'Automatic'})

	manual(c,conn)
	automatic(c,conn)
	no_data(c,conn)

def seller_response_rate_encoder(c,conn) -> sqlite3:
	with conn:
		c.execute(""" UPDATE EncodedCars SET SellerAvgResponseRate = 0 WHERE SellerAvgResponseRate IS NULL;""")

def seller_verification_encoder(c,conn) -> sqlite3:
	### LEGNED ###
	# 0 = no data
	# 1 = email
	# 2 = phone
	# 3 = identity
	
	def email(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET SellerVerification = 1 Where SellerVerification = 'email Verified';""")
	
	def phone(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET SellerVerification = 2 Where SellerVerification = 'phone Verified';""")
	
	def identity(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET SellerVerification = 3 Where SellerVerification = 'identity Verified';""")

	def no_data(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET SellerVerification = 0 Where SellerVerification IS NULL;""")
		
	email(c,conn)
	phone(c,conn)
	identity(c,conn)
	no_data(c,conn)

def seller_activeads_encoder(c,conn) -> sqlite3:
	with conn:
		c.execute(""" UPDATE EncodedCars SET SellerActiveAds = 1 WHERE SellerActiveAds IS NULL;""")

def seller_lifetimeads_encoder(c,conn) -> sqlite3:
	with conn:
		c.execute(""" UPDATE EncodedCars SET SellerLifeTimeAds = 1 WHERE SellerLifeTimeAds IS NULL;""")

def car_bodytype_encoder(c,conn) -> sqlite3:

	### LEGEND ###
	# 0 = no data
	# 1 = cabriolet or convertiable
	# 2 = coupe
	# 3 = estate or estate/jeep
	# 4 = Hatchback
	# 5 = MPV/SUV
	# 6 = saloon
	# 7 = van

	def cabriolet(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarBodyType = 1 WHERE CarBodyType = 'Cabriolet' OR CarBodyType = 'Convertible';""")

	def coupe(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarBodyType = 2 WHERE CarBodyType = 'Coupe';""")

	def estate(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarBodyType = 3 WHERE CarBodyType = 'Estate' OR CarBodyType = 'Estate/Jeep';""")

	def hatchback(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarBodyType = 4 WHERE CarBodyType = 'Hatchback';""")

	def MPV_SUV(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarBodyType = 5 WHERE CarBodyType = 'MPV' OR CarBodyType = 'SUV' OR CarBodyType = 'Crossover';""")

	def saloon(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarBodyType = 6 WHERE CarBodyType = 'Saloon';""")
	
	def van(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarBodyType = 7 WHERE CarBodyType = 'van' OR CarBodyType = 'Van';""")

	def no_data(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarBodyType = 0 WHERE CarBodyType IS '---';""")

	def no_data_1(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarBodyType = 0 WHERE CarBodyType > 7 ;""")

	cabriolet(c,conn)
	coupe(c,conn)
	estate(c,conn)
	hatchback(c,conn)
	MPV_SUV(c,conn)
	saloon(c,conn)
	van(c,conn)
	no_data(c,conn)
	no_data_1(c,conn)

def delete_new_cars(c,conn) -> sqlite3:
	with conn:
		c.execute(""" DELETE FROM EncodedCars WHERE CarYear > 2015 OR CarYear < 2004 ;""")
		conn.commit

def car_colour_encoder(c,conn) -> sqlite3:
	### LEGEND ###
	# 1 = Beige
	# 2 = Black
	# 3 = Blue
	# 4 = Brown
	# 5 = Green
	# 6 = Grey
	# 7 = Gold
	# 8 = Orange
	# 9 = Red
	# 10 = Silver
	# 11 = White
	# 12 = Yellow
	# 13 = Purple
	# 14 = Bronze
	# 15 = Burgundy
	# 0 = no data/other

	def Beige(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarColour = 1 WHERE CarColour = 'Beige';""")

	def Black(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarColour = 2 WHERE CarColour = 'Black';""")
	
	def Blue(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarColour = 3 WHERE CarColour = 'Blue';""")

	def Brown(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarColour = 4 WHERE CarColour = 'Brown';""")

	def Green(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarColour = 5 WHERE CarColour = 'Green';""")

	def Grey(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarColour = 6 WHERE CarColour = 'Grey';""")

	def Gold(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarColour = 7 WHERE CarColour = 'Gold';""")

	def Orange(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarColour = 8 WHERE CarColour = 'Orange';""")

	def Red(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarColour = 9 WHERE CarColour = 'Red';""")

	def Silver(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarColour = 10 WHERE CarColour = 'Silver';""")

	def White(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarColour = 11 WHERE CarColour = 'White';""")

	def Yellow(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarColour = 12 WHERE CarColour = 'Yellow';""")

	def Purple(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarColour = 13 WHERE CarColour = 'Purple';""")

	def Bronze(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarColour = 14 WHERE CarColour = 'Bronze';""")

	def Burgundy(c,conn) -> sqlite3:
			with conn:
				c.execute(""" UPDATE EncodedCars SET CarColour = 15 WHERE CarColour = 'Burgundy';""")

	def no_data_other(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarColour = 0 WHERE CarColour = '---' OR CarColour = 'Other';""")
			c.execute(""" UPDATE EncodedCars SET CarColour = 0 WHERE CarColour = 'null';""")
	
	Beige(c,conn)
	Black(c,conn)
	Blue(c,conn)
	Brown(c,conn)
	Green(c,conn)
	Grey(c,conn)
	Gold(c,conn)
	Orange(c,conn)
	Red(c,conn)
	Silver(c,conn)
	White(c,conn)
	Yellow(c,conn)
	Purple(c,conn)
	Bronze(c,conn)
	Burgundy(c,conn)
	no_data_other(c,conn)

def CarSeats(c,conn) -> sqlite3:

	def null(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarSeats = 0 WHERE CarSeats = '---';""")

	def over_7(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarSeats = 0 WHERE CarSeats > 7;""")

	null(c,conn)
	over_7(c,conn)

def car_model_encoder(c,conn) -> sqlite3:
	### LEGEND ###
	# 0 = no data
	# 1 = Golf
	# 2 = Polo
	# 3 = Passat
	# 4 = Corolla
	# 5 = Yaris
	# 6 = A4
	# 7 = A3
	# 8 = 1-Series
	# 9 = 3-Series


	def model_is_null(c,conn) -> sqlite3:
		with conn:
			c.execute(""" SELECT URL,CarMake FROM EncodedCars WHERE CarModel IS NULL;""")
			url_list = c.fetchall()
			for i in url_list:
				c.execute(""" UPDATE EncodedCars SET CarModel = :model WHERE URL = :URL""",
				{'model':i[1],'URL':i[0]})

	def unwanted_model(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars Set CarModel = 0 WHERE CarModel > 9;""")

	def golf(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarModel = 1 WHERE CarModel = 'Golf';""")
	
	def polo(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarModel = 2 WHERE CarModel = 'Polo';""")

	def passat(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarModel = 3 WHERE CarModel = 'Passat';""")

	def corolla(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarModel = 4 WHERE CarModel = 'Corolla';""")

	def yaris(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarModel = 5 WHERE CarModel = 'Yaris';""")

	def a4(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarModel = 6 WHERE CarModel = 'A4';""")

	def a3(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarModel = 7 WHERE CarModel = 'A3';""")

	def series_1(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarModel = 8 WHERE CarModel = '1-Series';""")

	def series_3(c,conn) -> sqlite3:
		with conn:
			c.execute(""" UPDATE EncodedCars SET CarModel = 9 WHERE CarModel = '3-Series';""")

	def no_data(c,conn) -> sqlite3:
		with conn:
			c.execute(""" DELETE FROM EncodedCars WHERE CarModel = 0;""")
			conn.commit

	model_is_null(c,conn)
	golf(c,conn)
	polo(c,conn)
	passat(c,conn)
	corolla(c,conn)
	yaris(c,conn)
	a4(c,conn)
	a3(c,conn)
	series_1(c,conn)
	series_3(c,conn)
	unwanted_model(c,conn)
	no_data(c,conn)

def engine_size_encoder(c,conn) -> sqlite3:
	### LEGEND ###
	# 0 = no data

	with conn:
		c.execute(""" UPDATE EncodedCars SET CarEngineSize = 0 WHERE CarEngineSize ='---' OR CarEngineSize IS NULL;""")

def seller_DD_since_encoder(c,conn) -> sqlite3:
	### LEGEND ### 
	# 0 = no data
	with conn:
		c.execute(""" UPDATE EncodedCars SET SellerDonedealingSince = 0 WHERE SellerDonedealingSince IS NULL ;""")

def car_millage_encoder(c,conn) -> sqlite3:
	with conn:
		c.execute(""" SELECT CarMillage, URL FROM EncodedCars;""")
		data = c.fetchall()
		for _ , x in data:
			url = str(x).replace("(","").replace("')","")

			c.execute(""" UPDATE EncodedCars SET CarMillage = 0 WHERE CarMillage = "";""")

			if "km" in str(_):
				km = str(_).replace("km","")
				if int(km)< 1000:
					km = str(km)+"00"
				c.execute(""" UPDATE EncodedCars SET CarMillage = :millage WHERE URL = :url;""",
				{"millage":km, "url":url})
			
			if "mi" in str(_):
				mi = str(_).replace("mi","")
				if int(mi) < 1000:
					mi = str(mi)+"00"
				mi = round(int(mi)*1.60934)
				c.execute(""" UPDATE EncodedCars SET CarMillage = :millage WHERE URL = :url;""",
				{"millage":mi, "url":url})

def car_NCT_encoder(c,conn) -> sqlite3:
	t1 = datetime(year = datetime.now().year,
							month = datetime.now().month,
							day = datetime.now().day,
							hour = datetime.now().hour,
							minute = datetime.now().minute)
	
	def is_null():
			c.execute(""" UPDATE EncodedCars SET CarNCTExpiry = 0 WHERE CarNCTExpiry is NULL;""")
	
	with conn:
		c.execute(""" SELECT CarNCTExpiry, URL FROM EncodedCars;""")
		data = c.fetchall()
		for _ , x in data:
			url = str(x).replace("('","'").replace("')","',")
			if "Jan" in str(_):
				year = str(_).replace("Jan","")
				t2 = datetime(int(year), 1, 1) 
				Expiry = t2-t1
				c.execute(""" UPDATE EncodedCars SET CarNCTExpiry = :Expiry WHERE URL =:url;""",
				{"Expiry":str(Expiry), "url":url})
			
			if "Feb" in str(_):
				year = str(_).replace("Feb","")
				t2 = datetime(int(year), 2, 1)
				Expiry = t2-t1
				c.execute(""" UPDATE EncodedCars SET CarNCTExpiry = :Expiry WHERE URL =:url;""",
				{"Expiry":str(Expiry), "url":url})
			
			if "Mar" in str(_):
				year = str(_).replace("Mar","")
				t2 = datetime(int(year), 3, 1)
				Expiry = t2-t1
				c.execute(""" UPDATE EncodedCars SET CarNCTExpiry = :Expiry WHERE URL =:url;""",
				{"Expiry":str(Expiry), "url":url})
			
			if "Apr" in str(_):
				year = str(_).replace("Apr","")
				t2 = datetime(int(year), 4, 1)
				Expiry = t2-t1
				c.execute(""" UPDATE EncodedCars SET CarNCTExpiry = :Expiry WHERE URL =:url;""",
				{"Expiry":str(Expiry), "url":url})
			
			if "May" in str(_):
				year = str(_).replace("May","")
				t2 = datetime(int(year), 5, 1)
				Expiry = t2-t1
				c.execute(""" UPDATE EncodedCars SET CarNCTExpiry = :Expiry WHERE URL =:url;""",
				{"Expiry":str(Expiry), "url":url})
			
			if "Jun" in str(_):
				year = str(_).replace("Jun","")
				t2 = datetime(int(year), 6, 1)
				Expiry = t2-t1
				c.execute(""" UPDATE EncodedCars SET CarNCTExpiry = :Expiry WHERE URL =:url;""",
				{"Expiry":str(Expiry), "url":url})
			
			if "Jul" in str(_):
				year = str(_).replace("Jul","")
				t2 = datetime(int(year), 7, 1)
				Expiry = t2-t1
				c.execute(""" UPDATE EncodedCars SET CarNCTExpiry = :Expiry WHERE URL =:url;""",
				{"Expiry":str(Expiry), "url":url})
			
			if "Aug" in str(_):
				year = str(_).replace("Aug","")
				t2 = datetime(int(year), 8, 1)
				Expiry = t2-t1
				c.execute(""" UPDATE EncodedCars SET CarNCTExpiry = :Expiry WHERE URL =:url;""",
				{"Expiry":str(Expiry), "url":url})
			
			if "Sep" in str(_):
				year = str(_).replace("Sep","")
				t2 = datetime(int(year), 9, 1)
				Expiry = t2-t1
				c.execute(""" UPDATE EncodedCars SET CarNCTExpiry = :Expiry WHERE URL =:url;""",
				{"Expiry":str(Expiry), "url":url})
			
			if "Oct" in str(_):
				year = str(_).replace("Oct","")
				t2 = datetime(int(year), 10, 1)
				Expiry = t2-t1
				c.execute(""" UPDATE EncodedCars SET CarNCTExpiry = :Expiry WHERE URL =:url;""",
				{"Expiry":str(Expiry), "url":url})
			
			if "Nov" in str(_):
				year = str(_).replace("Nov","")
				t2 = datetime(int(year), 11, 1)
				Expiry = t2-t1
				c.execute(""" UPDATE EncodedCars SET CarNCTExpiry = :Expiry WHERE URL =:url;""",
				{"Expiry":str(Expiry), "url":url})
			
			if "Dec" in str(_):
				year = str(_).replace("Dec","")
				t2 = datetime(int(year), 12, 1)
				Expiry = t2-t1
				c.execute(""" UPDATE EncodedCars SET CarNCTExpiry = :Expiry WHERE URL =:url;""",
				{"Expiry":str(Expiry), "url":url})

			if "EURO"in str(_):
				c.execute(""" UPDATE EncodedCars SET CarNCTExpiry = 0 WHERE URL =:url;""",
				{"url":url})
			
			if "Warranty" in str(_):
				c.execute(""" UPDATE EncodedCars SET CarNCTExpiry = 0 WHERE URL =:url;""",
				{"url":url})

		
		is_null()

def car_price_encoder(c,conn) -> sqlite3:
	with conn:
		c.execute(""" DELETE FROM EncodedCars WHERE CarPrice = 0 ;""")
		c.execute(""" DELETE FROM EncodedCars WHERE CarPrice = 1 ;""")
		c.execute(""" DELETE FROM EncodedCars WHERE CarPrice < 124 ;""")
		c.execute(""" DELETE FROM EncodedCars WHERE CarPrice = 12345 ;""")
		c.execute(""" DELETE FROM EncodedCars WHERE CarPrice = 123456 ;""")
		c.execute(""" DELETE FROM EncodedCars WHERE CarPrice = 1234567 ;""")
		c.execute(""" DELETE FROM EncodedCars WHERE CarPrice = 12345678 ;""")
		c.execute(""" DELETE FROM EncodedCars WHERE CarPrice = 'No Price' ;""")
		
		conn.commit

def wanted_scrap_breaking(c,conn) -> sqlite3:
	with conn:
		c.execute(""" DELETE FROM EncodedCars WHERE URL LIKE '%breaking%';""")
		c.execute(""" DELETE FROM EncodedCars WHERE URL LIKE '%alloys%';""")
		c.execute(""" DELETE FROM EncodedCars WHERE URL LIKE '%airbag%';""")
		c.execute(""" DELETE FROM EncodedCars WHERE URL LIKE '%injectors%';""")
		c.execute(""" DELETE FROM EncodedCars WHERE URL LIKE '%wanted%';""")
		c.execute(""" DELETE FROM EncodedCars WHERE URL LIKE '%remapping%';""")
		c.execute(""" DELETE FROM EncodedCars WHERE URL LIKE '%recovery%';""")
		c.execute(""" DELETE FROM EncodedCars WHERE URL LIKE '%trailer%';""")
		c.execute(""" DELETE FROM EncodedCars WHERE URL LIKE '%for-parts%';""")
		c.execute(""" DELETE FROM EncodedCars WHERE URL LIKE '%bought-for-cash%';""")
		c.execute(""" DELETE FROM EncodedCars WHERE URL LIKE '%cash-for-cars%';""")
		c.execute(""" DELETE FROM EncodedCars WHERE URL LIKE '%any-vehicle%';""")
		c.execute(""" DELETE FROM EncodedCars WHERE URL LIKE '%wheel-stick%';""")
		c.execute(""" DELETE FROM EncodedCars WHERE URL LIKE '%reversing-camera%';""")
		c.execute(""" DELETE FROM EncodedCars WHERE URL LIKE '%brett-car-sales%';""")


### Imputations ###
def car_body_type_imputer(c,conn) -> sqlite3:
    modedict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
    with conn:
        c.execute(""" SELECT CarModel, CarBodyType FROM EncodedCars;""")
        data =  c.fetchall()
        for cm, cbt in data:
            if cm != 0:
                modedict[cm].append(cbt)
        for i in modedict.keys():
            modedict[i] = mode(modedict[i])
        for x in modedict:
            y = modedict[x]
            c.execute(""" UPDATE EncodedCars SET CarBodyType = :y WHERE CarBodyType = 0 AND CarModel = :x;""",
                {'y': y, 'x': x})
            conn.commit

def car_seats_imputer(c,conn) -> sqlite3:
    modedict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
    with conn:
        c.execute(""" SELECT CarBodyType, CarSeats FROM EncodedCars; """)
        data = c.fetchall()
        for cbt , cs in data:
            modedict[cbt].append(cs)
        for i in modedict.keys():
            modedict[i] = mode(modedict[i])
        for x in modedict:
            y = modedict[x]
            c.execute(""" UPDATE EncodedCars SET CarSeats = :y WHERE CarSeats = 0 AND CarBodyType = :x;""",
                {'y': y, 'x': x})
            conn.commit

def car_transmission_imputer(c,conn) -> sqlite3:
    modedict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
    with conn:
        c.execute(""" SELECT CarModel, CarTransmission FROM EncodedCars;""")
        data =  c.fetchall()
        for cm, ct in data:
            if cm != 0:
                modedict[cm].append(ct)
        for i in modedict.keys():
            modedict[i] = mode(modedict[i])
        for x in modedict:
            y = modedict[x]
            c.execute(""" UPDATE EncodedCars SET CarTransmission = :y WHERE CarTransmission = 0 AND CarModel = :x;""",
                {'y': y, 'x': x})
            conn.commit

def car_tax_imputer(c,conn) -> sqlite3:
    modedict = {2003:{1:{1:[],2:[]},2:{1:[],2:[]}, 3:{1:[],2:[]}, 4:{1:[],2:[]}, 5:{1:[],2:[]}, 6:{1:[],2:[]}, 7:{1:[],2:[]}, 8:{1:[],2:[]}, 9:{1:[],2:[]}},
                2004:{1:{1:[],2:[]},2:{1:[],2:[]}, 3:{1:[],2:[]}, 4:{1:[],2:[]}, 5:{1:[],2:[]}, 6:{1:[],2:[]}, 7:{1:[],2:[]}, 8:{1:[],2:[]}, 9:{1:[],2:[]}},
                2005:{1:{1:[],2:[]},2:{1:[],2:[]}, 3:{1:[],2:[]}, 4:{1:[],2:[]}, 5:{1:[],2:[]}, 6:{1:[],2:[]}, 7:{1:[],2:[]}, 8:{1:[],2:[]}, 9:{1:[],2:[]}},
                2006:{1:{1:[],2:[]},2:{1:[],2:[]}, 3:{1:[],2:[]}, 4:{1:[],2:[]}, 5:{1:[],2:[]}, 6:{1:[],2:[]}, 7:{1:[],2:[]}, 8:{1:[],2:[]}, 9:{1:[],2:[]}},
                2007:{1:{1:[],2:[]},2:{1:[],2:[]}, 3:{1:[],2:[]}, 4:{1:[],2:[]}, 5:{1:[],2:[]}, 6:{1:[],2:[]}, 7:{1:[],2:[]}, 8:{1:[],2:[]}, 9:{1:[],2:[]}},
                2008:{1:{1:[],2:[]},2:{1:[],2:[]}, 3:{1:[],2:[]}, 4:{1:[],2:[]}, 5:{1:[],2:[]}, 6:{1:[],2:[]}, 7:{1:[],2:[]}, 8:{1:[],2:[]}, 9:{1:[],2:[]}},
                2009:{1:{1:[],2:[]},2:{1:[],2:[]}, 3:{1:[],2:[]}, 4:{1:[],2:[]}, 5:{1:[],2:[]}, 6:{1:[],2:[]}, 7:{1:[],2:[]}, 8:{1:[],2:[]}, 9:{1:[],2:[]}},
                2010:{1:{1:[],2:[]},2:{1:[],2:[]}, 3:{1:[],2:[]}, 4:{1:[],2:[]}, 5:{1:[],2:[]}, 6:{1:[],2:[]}, 7:{1:[],2:[]}, 8:{1:[],2:[]}, 9:{1:[],2:[]}},
                2011:{1:{1:[],2:[]},2:{1:[],2:[]}, 3:{1:[],2:[]}, 4:{1:[],2:[]}, 5:{1:[],2:[]}, 6:{1:[],2:[]}, 7:{1:[],2:[]}, 8:{1:[],2:[]}, 9:{1:[],2:[]}},
                2012:{1:{1:[],2:[]},2:{1:[],2:[]}, 3:{1:[],2:[]}, 4:{1:[],2:[]}, 5:{1:[],2:[]}, 6:{1:[],2:[]}, 7:{1:[],2:[]}, 8:{1:[],2:[]}, 9:{1:[],2:[]}},
                2013:{1:{1:[],2:[]},2:{1:[],2:[]}, 3:{1:[],2:[]}, 4:{1:[],2:[]}, 5:{1:[],2:[]}, 6:{1:[],2:[]}, 7:{1:[],2:[]}, 8:{1:[],2:[]}, 9:{1:[],2:[]}},
                2014:{1:{1:[],2:[]},2:{1:[],2:[]}, 3:{1:[],2:[]}, 4:{1:[],2:[]}, 5:{1:[],2:[]}, 6:{1:[],2:[]}, 7:{1:[],2:[]}, 8:{1:[],2:[]}, 9:{1:[],2:[]}},
                2015:{1:{1:[],2:[]},2:{1:[],2:[]}, 3:{1:[],2:[]}, 4:{1:[],2:[]}, 5:{1:[],2:[]}, 6:{1:[],2:[]}, 7:{1:[],2:[]}, 8:{1:[],2:[]}, 9:{1:[],2:[]}}}
    with conn:
        c.execute(""" SELECT CarYear, CarModel, CarFuelType, CarTax FROM EncodedCars;""")
        data =  c.fetchall()
        for cy, cm, cft, ct in data:
            if cft != 3 and ct != "---":
                modedict[cy][cm][cft].append(ct)
        for a in range(2003,2016):
            for b in modedict[a]:
                for x in modedict[a][b]:
                    try:
                        MT = mode(modedict[a][b][x])
                    except:
                        MT = 0
                    c.execute(""" UPDATE EncodedCars SET CarTax = :MT WHERE CarYear = :a AND CarModel = :b AND CarFuelType = :x AND CarTax = "---" OR CarTax = 0;""",
                    {'MT':MT, 'a':a, 'b':b, 'x':x})
        c.execute(""" UPDATE EncodedCars SET CarTax = :MT WHERE CarTax = 0 OR CarTax = "---";""",
        {'MT':MT,})
        conn.commit
	
def car_millage_imputer(c,conn) -> sqlite3:
	with conn:
		c.execute(""" SELECT CarModel,CarYear,CarPrice,URL FROM EncodedCars WHERE CarMillage = 0 ;""")
		data =  c.fetchall()
		for cm, cy, cp, url in data:
			c.execute(""" SELECT CarMillage,CarPrice FROM EncodedCars WHERE CarModel = :cm AND CarYear = :cy;""",
					{"cm":cm, "cy":cy})
			data = c.fetchall()
			mm = [i[0] for i in data]
			mp = [i[-1] for i in data]
			cpd = round(cp/int(mean(mp)),2)
			mg = int(mean(mm)*cpd)
			c.execute(""" UPDATE EncodedCars Set CarMillage = :mg WHERE URL = :url;""",
					{"mg":mg, "url":url })
					
### Imputations ###


### Perpetuaily Running Functoions ###

def update_tsu(t1,c,conn) -> sqlite3:
	with conn:
		c.execute( """ SELECT UploadDate,URL FROM EncodedCars ORDER BY UploadDate DESC;""")
		data = c.fetchall()

	for TSU, URL in track(data):
		AdjustedTSU = str(t1 - datetime.fromisoformat(TSU)).replace('days,',':').replace('day,',':')
		with conn:
			c.execute(""" UPDATE EncodedCars SET TSU = :AdjustedTSU WHERE URL = :URL;""",
			{'AdjustedTSU':AdjustedTSU, 'URL': URL})

def url_gen(conn,c) -> sqlite3:
	url_list = []
	with conn:
		c.execute(""" SELECT URL FROM EncodedCars;""")
		for _ in c.fetchall():
			url = str(_).replace("('","").replace("',)","")
			url_list.append(url)
	return url_list

def ad_views(db_path,url) -> sqlite3:
	try:
		conn = sqlite3.connect(db_path)
		c = conn.cursor()
		lxml = request_url(url)
		if lxml.find("div", "icon icon-adexpired") == None:
			newViews = str(lxml.find("div", "InfoTitle__InfoTitleContainer-sc-qp6c10-0 iPMvez AdTitleBox__SInfoTitle-sc-1p2v1sf-0 bWrJlh").find("li", "InfoTitle__SubtitleItem-sc-qp6c10-4 MWEbJ").find_next("li", "InfoTitle__SubtitleItem-sc-qp6c10-4 MWEbJ").text).replace("views",'').replace(",",'')
		else:
			newViews = "SOLD"
		with conn:
			c.execute(""" UPDATE EncodedCars SET AdViews = :newViews  WHERE URL = :url ;""",
					{'newViews':newViews, 'url':url})
			conn.commit()
	except:
		return None

### Perpetuaily Running Functoions ###


### all following functions Scale individual Columns
### of the EncodedCars Table, These Functions use the MinMaxScaler
### Whiich is imported from the scikit-learn modual
### All revelent LEGENDS are provided in the seperate functions

def car_engine_size_scaler(conn,c,scaler) -> sqlite3:
	with conn:
		c.execute(""" DELETE FROM EncodedCars WHERE CarEngineSize = 0;""")
		c.execute(""" SELECT CarEngineSize FROM EncodedCars ORDER BY CarEngineSize ASC;""")
		data = []
		for _ in c.fetchall():
			data.append(_)
		data = np.array(data).reshape(-1,1)
		scaleddata = scaler.fit_transform(data)
		inverse = scaler.inverse_transform(scaleddata)
		return inverse
		# for i in scaleddata:
		# 	print(i)
		#inverse = scaler.inverse_transform(scaleddata)

def car_tax_scaler(conn,c,scaler) -> sqlite3:
	with conn:
		c.execute(""" DELETE FROM EncodedCars WHERE CarTax = 0;""")
		c.execute(""" SELECT CarTax FROM EncodedCars ORDER BY CarTax ASC;""")
		data = []
		for _ in c.fetchall():
			data.append(_)
		data = np.array(data).reshape(-1,1)
		scaleddata = scaler.fit_transform(data)
		inverse = scaler.inverse_transform(scaleddata)
		return inverse

def car_price_scaler(conn,c,scaler) -> sqlite3:
	with conn:
		c.execute(""" DELETE FROM EncodedCars WHERE CarTax = 0;""")
		c.execute(""" SELECT CarPrice FROM EncodedCars 
					WHERE NOT AdViews = "SOLD" 
					ORDER BY CarPrice DESC;""")
		data = []
		for _ in c.fetchall():
			data.append(_)
		data = np.array(data).reshape(-1,1)
		print(data)
		# for i in data:
		# 	print(i)
		scaleddata = scaler.fit_transform(data)
		inverse = scaler.inverse_transform(scaleddata)
		return inverse
		
def car_ad_scaler(conn,c,scaler) -> sqlite3:
	with conn:
		c.execute(""" SELECT AdViews FROM EncodedCars WHERE NOT AdViews ="SOLD" ORDER BY AdViews ASC;""")
		data = []
		for _ in c.fetchall()[5:-5]:
			data.append(_)
		data = np.array(data).reshape(-1,1)
		scaleddata = scaler.fit_transform(data)
		inverse = scaler.inverse_transform(scaleddata)
		return scaleddata

def TSU_scaler(conn,c,scaler) -> sqlite3:
	with conn:
		c.execute(""" SELECT TSU FROM EncodedCars 
					WHERE NOT AdViews ="SOLD" 
					ORDER BY UploadDate DESC;""")
		data = []
		for _ in c.fetchall()[5:-5]:
			TSU = str(_).replace("('","").replace("',)","")
			adjustedTSU = TSU.split(":")
			if len(adjustedTSU) <= 3 :
				data.append(TSU.replace(":",""))
			else:
				data.append(str(TSU).replace(" : ","0").replace(":",""))
		data = np.array(data).reshape(-1,1)
		scaleddata = scaler.fit_transform(data)
		inverse = scaler.inverse_transform(scaleddata)
		return scaleddata

	#print(car_engine_size_scaler(conn,c))
	#print(car_tax_scaler(conn,c))

class Compare:

	def __init__(self, url):
				self.data = url

	def Retrive(self):
		conn = sqlite3.connect("C:\Windows\System32\lillymay/Carmex.sqlite3")
		c = conn.cursor()
		with conn:
			c.execute(""" SELECT * FROM EncodedCars WHERE URL = :url;""",
			{"url":self.data})
			data = c.fetchone()
			if data == None:
				pass
			else:
				self.data = [i for i in data]
			c.execute(""" SELECT CarPrice, CarMillage
					FROM EncodedCars
					WHERE SellerType  = 3
					AND NOT URL = :url
					AND CarModel = :Model
					AND CarYear BETWEEN :FromYear AND :TooYear
					AND CarMillage > 100
					ORDER BY CarPrice ASC
					;""",
					{"url":self.data[0],"Model":self.data[10], "FromYear":self.data[11],
					"TooYear":self.data[11],"FuelType":self.data[14]})
		return c.fetchall()

	
	def Linear_Regression(self,data):
		x = []
		for i in data[0:-2]:
			i = str(i).replace("(","").replace(")","").split(",")
			x.append(int(i[0]))
			x.append(int(i[1]))
		x = np.array(x).reshape(-1,2)
		df = pd.DataFrame(x,columns =["Price","Millage"])
		reg = linear_model.LinearRegression()
		reg.fit(df[["Millage"]],df.Price)
		print(self.data[0])
		print("Predicted Price" ,reg.predict([[self.data[16]]])," Based from a sample size of",len(x))
		print("Asking Price ",self.data[-3])
		print("Car Millage ",self.data[16])
		print("  ")
		return df
	
	def Scatter_Plot(sellf,df):
		reg = linear_model.LinearRegression()
		reg.fit(df[["Millage"]],df.Price)
		plt.xlabel("KM")
		plt.ylabel("EURO")
		plt.scatter(df.Millage,df.Price,color="red",marker="+")
		plt.plot(df.Millage,reg.predict(df[["Millage"]]),color="blue")
		plt.show()

	def Valuation(self,df):
		print(df)
		mp  = int(mean(df.Price))
		mm  = int(mean(df.Millage))
		psd = int(pstdev(df.Price))
		msd = int((pstdev(df.Millage)))
		cp = int(self.data[-3])
		cm = int(self.data[16])
		if cp < mp-psd and cm < mm-msd:
			print("possible Winner here boiiiii",self.data[0])
			self.Scatter_Plot(df)

	def __str__(self):
			return str(self.__class__) + ": " + str(self.__dict__)


### Removed the db_paath vairaible for testing purposes
### DO NOT FORGET TO REPLACE db_path to run the .exe

def main(db_path,new_list):
	conn = create_connection(db_path)
	c = create_cursor(conn)
	### Encoding Functions ###
	seller_type_encoder(c,conn)
	print("ENCODED SELLER TYPE")
	car_fuel_encoder(c,conn)
	print("ENCODED FUEL TYPE")
	car_transmission_encoder(c,conn)
	print("ENCODED TRANSMISSION")
	seller_response_rate_encoder(c,conn)
	print("ENCODED SELLER RESPONSE RATE")
	seller_verification_encoder(c,conn)
	print("ENCODED VERIFICATION")
	seller_activeads_encoder(c,conn)
	print("ENCODED ACTIVEADS")
	seller_lifetimeads_encoder(c,conn)
	print("ENCODED LIFETIME ADS")
	car_bodytype_encoder(c,conn)
	print("ENCODED BODY TYPE")
	delete_new_cars(c,conn)
	print("ENCODED NEW CARS")
	car_colour_encoder(c,conn)
	print("ENCODED CAR COLOUR")
	CarSeats(c,conn)
	print("ENCODED CAR SEATS")
	car_model_encoder(c,conn)
	print("ENCODED CAR MODEL")
	engine_size_encoder(c,conn)
	print("ENCODED ENGINE SIZE")
	seller_DD_since_encoder(c,conn)
	print("ENCODED SELLER DONEDEALING SINCE")
	car_millage_encoder(c,conn)
	print("ENCODED CAR MILLAGE")
	car_NCT_encoder(c,conn)
	print("ENCODED NCT")
	car_price_encoder(c,conn)
	print("ENCODED CAR PRICE ")
	wanted_scrap_breaking(c,conn)
	print("REMOVED UNWANTED ADS")

	### Imputation Functions ###
	### Only Run Imputer functions after Encoder Functions ###
	car_body_type_imputer(c,conn)
	car_seats_imputer(c,conn)
	car_transmission_imputer(c,conn)
	car_tax_imputer(c,conn)
	car_millage_imputer(c,conn)
	print("IMPUTATION COMPLETE")

	### T1 = Current Time ###
	t1 = datetime(year = datetime.now().year,
				month = datetime.now().month,
				day = datetime.now().day,
				hour = datetime.now().hour,
				minute = datetime.now().minute)
	### T1 = Current Time ###
	update_tsu(t1,c,conn)
	print("TSU UPDATED")

	# with concurrent.futures.ThreadPoolExecutor() as executor:
	# 	results = [executor.submit(ad_views, db_path, x) for x in url_gen(conn,c)]
	# 	for f in concurrent.futures.as_completed(results):	
	# 		f.result()
	# print("AdViews Updated")

	for i in new_list:
		car1 = Compare(i)
		cars = car1.Retrive()
		if len(cars) > 0:
			car1.Valuation(car1.Linear_Regression(cars))
		else:
			pass

if __name__ == "__main__":
	main()


