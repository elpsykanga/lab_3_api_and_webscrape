import re
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import amadeus
from amadeus import Client, ResponseError
import sys
import random as rd


class volare:
    def __init__(self,name,depart,arrive,date,people):
        self.name = name
        self.start = depart
        self.stop = arrive
        self.date = date
        self.mate = people
c1 = volare


### Insert Functions That will be used
locations=pd.read_csv('lab_3_api_and_webscrape\Project 3\locations.csv')
cunt=pd.read_csv('lab_3_api_and_webscrape\Project 3\IATA.csv')

def ama ():
    amadeus = Client(
    client_id='nPw0aTw26KfiG0npH6XcoEKYCJ7N8zbf',
    client_secret = 'dLqHifawmuDizlVZ'
    )
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=c1.start,
            destinationLocationCode=c1.stop,
            departureDate=c1.date,
            adults=c1.mate
        )
        print(response.data)
    except ResponseError as error:
        print(error)


def flight_retrieve(x):
    flights=x[0:5]
    tripdf = pd.DataFrame()
    for i in range(len(flights)):
        trip = {}
        volo=flights[i]
        flight=volo['itineraries'][0]
        e = re.sub('PT','',flight['duration'])
        e = re.sub('H',' Hours ',e)
        trip['duration'] = re.sub('M',' Min',e)
        q=flight['segments'][0]
        trip['airline']=q['carrierCode']
        q=q['departure']
        trip['from']=q['iataCode']
        trip['leave at']=re.sub('T',' at ',q['at'])
        q=flight['segments'][0]
        q = q['arrival']
        trip['to']=q['iataCode']
        trip['arrive at']=re.sub('T',' at ',q['at'])
        cost=volo['price']
        trip['price']=cost['total']
        listing=pd.DataFrame([trip]).T
        tripdf=pd.concat(objs=[listing,tripdf],axis=1,)
    tripdf.columns=[1,2,3,4,5]
    return(tripdf)


def get_id(df):
	url = "https://airbnb19.p.rapidapi.com/api/v1/searchDestination"

	querystring = {"query":'tbd',"country":df ['Country']}
	
	headers = {
	"X-RapidAPI-Key": "4756e43d86msh629b4ee18cb5f4cp1b8e99jsncc91f7430291",
	"X-RapidAPI-Host": "airbnb19.p.rapidapi.com"}
												

	response = requests.request("GET", url, headers=headers, params=querystring)
	time.sleep(3)
	data = response.json()
	try:
		return data['data'][0]['id']
	except:
		return df['City']

def get_place_info(idlist,citylist):
	li = []
	notgood = []
	for ind in range(len(idlist[0])):
		print(idlist[0][ind])
		url = "https://airbnb19.p.rapidapi.com/api/v1/searchPropertyByPlace"

		querystring = {"id":idlist[0][ind],"totalRecords":"10","currency":"EUR","adults":"1"}

		headers = {
		"X-RapidAPI-Key": "4756e43d86msh629b4ee18cb5f4cp1b8e99jsncc91f7430291",
		"X-RapidAPI-Host": "airbnb19.p.rapidapi.com"}


		response = requests.request("GET", url, headers=headers, params=querystring)
		time.sleep(3)

		data2 = response.json()
		
		try:
			for i in range(10):
				city = data2['data'][i]['city']
				rating = data2['data'][i]['avgRating']
				price = data2['data'][i]['price']

				li.append({ 'City': citylist[ind], 'Rating':rating, 'Price': price})
		except:
				notgood.append(citylist[ind])
	return pd.DataFrame(li),notgood

def waiting(t):
    time.sleep(t)
    print('.')
    print()
    time.sleep(t)
    print('.')
    print()
    time.sleep(t)
    print('.')
    print()

def talk_speed(dialog, speed):
    for character in dialog:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(speed)

def app_title():
    print()
    print()
    print()
    print('#######################################')
    print('############# VACATION BOT ############')
    print('################ v.1 ##################')
    print('#######################################')
    waiting(0.5)
    app_start()


def app_start():
    bot2 = 'Please tell me when you want to go on vacation.(YYYY-MM-DD)\n'
    talk_speed(bot2,0.0001)
    year = (input('Year()>   ')).strip()
    month = (input('Month>   ')).strip()
    day = (input('Year>   ')).strip()
    date=year+'-'+month+'-'+day
    c1.date=date
    bot4 = "Pick an outdoor activity\n"
    talk_speed(bot4,0.0001)
    waiting(0.5)
    print((locations['Activities'].unique()))
    print()
    activity = input('>    ').strip().lower().capitalize()
    if activity == ['Hiking', 'Cycling','Surfing']:
        print('Good choice!!')
    while activity not in ['Hiking', 'Cycling','Surfing']:
        print('error: I never said that')
        activity = input('>    ').strip().lower().capitalize()
        if activity == ['Hiking', 'Cycling','Surfing']:
            print('Good choice!!')
    p=list((locations['Countries'].loc[locations['Activities']==activity]).unique())
    p=rd.choices(p, k=10)
    waiting(0.4)
    bot6='Alright, here are some personal recomendations for Countries you might like to visit...\n'
    talk_speed(bot6,0.0001)
    waiting(0.3)
    print(p)
    waiting(3)
    bot7='Do any of these interest you?'
    talk_speed(bot7,0.0001)
    resp = input('Yes or No:  ').lower()
    if resp == 'yes':
        app_data(p)



def app_data(z):
    print(z)
    



app_title()
