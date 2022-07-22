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
    def __init__(self,depart,arrive,date,people, dest):
        self.start = depart
        self.stop = arrive
        self.date = date
        self.mate = people
        self.dest = dest
c1 = volare
c1.start = 'LIS'

### Insert Functions That will be used
locations=pd.read_csv('lab_3_api_and_webscrape\Project 3\locations.csv')
cunt=pd.read_csv('lab_3_api_and_webscrape\Project 3\IATA.csv')
cunt = cunt[['Country','IATA']]

def ama ():
    amadeus = Client(
    client_id='nPw0aTw26KfiG0npH6XcoEKYCJ7N8zbf',
    client_secret = 'dLqHifawmuDizlVZ'
    )
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode='LIS',
            destinationLocationCode=c1.stop,
            departureDate=c1.date,
            adults=c1.mate
        )
        flight_retrieve(response.data)
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

	querystring = {"query":c1.dest,"country":c1.stop}
	
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
    bot1 = 'Hello and welcome to Vacation Bot 1.0. I am your personal digital travel agent and I am here to help you get the best experience out of your next outdoor vacation.\n'
    talk_speed(bot1,0.0001)
    bot2 = 'Lets start by you telling me your name\n'
    talk_speed(bot2,0.0001)
    name = input('>    ')
    bot3 = 'Nice to meet you '+name+'. Please tell me when you plan to go on vacation\n'
    talk_speed(bot3,0.0001)
    year = (input('Year(YYYY)>   ')).strip()
    month = (input('Month(MM)>   ')).strip()
    day = (input('Day(DD)>   ')).strip()
    date=year+'-'+month+'-'+day
    c1.date=date
    c1.date=date
    bot4 = "Alright now lets see what activities we have available for you today\n"
    talk_speed(bot4,0.0001)
    waiting(0.5)
    print((locations['Activities'].unique()))
    print()
    bot5="\nRight now we're a bit limited on options, so these are the only things we have available. Please tell me which one interests you.\n"
    talk_speed(bot5,0.0001)
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
    bot = 'How many people are travelling with you (insert a interger)'
    talk_speed(bot,0.001)
    c1.mate=1+int(input('>   '))
    bot6='Alright, here are some personal recomendations for Countries you might like to visit...\n'
    talk_speed(bot6,0.0001)
    waiting(0.3)
    print(p)
    waiting(0.2)
    bot7='Do any of these interest you?'
    talk_speed(bot7,0.0001)
    resp = input('Yes or No:  ').strip().lower()
    if resp == 'yes':
        app_data(p,activity)
    if resp == 'no':
        print('How about these countries')
        p=list((locations['Countries'].loc[locations['Activities']==activity]).unique())
        p=rd.choices(p, k=10)
        waiting(0.2)
        print(p)
        print()
        resp = input('Yes or No:  ').strip().lower()
        if resp == 'yes':
            app_data(p,activity)
        elif resp == 'no':
            print('How about these countries')
            p=list((locations['Countries'].loc[locations['Activities']==activity]).unique())
            p=rd.choices(p, k=10)
            waiting(0.2)
            print(p)
            resp = input('Yes or No:  ').strip().lower()
            if resp == 'yes':
                app_data(p,activity)
    while resp not in ['yes','no']:
        print("I didnt get that")
        resp = (input('Yes or No:  ')).strip().lower()
        if resp == 'yes':
            app_data(p,activity)
        if resp == 'no':
            print('How about these countries')
            p=list((locations['Countries'].loc[locations['Activities']==activity]).unique())
            p=rd.choices(p, k=10)
            waiting(0.2)
            print(p)
            if resp == 'yes':
                app_data(p,activity)
            if resp == 'no':
                print('How about these countries')
                p=list((locations['Countries'].loc[locations['Activities']==activity]).unique())
                p=rd.choices(p, k=10)
                waiting(0.2)

def app_data(z,act):
    print(z)
    country = input('Which of these countries interests you?').strip().lower().capitalize()
    while country not in z:
        print('error: try again')
        country = input('Which of these countries interests you').strip().lower().capitalize()
    q = locations
    bot = 'Alright based on your decisions I think its best you go to '+c1.dest+'. Now let us begin to plan your trip...'
    talk_speed(bot,0.001)
    waiting(1)
    bot1 = "Ive got eveything I need. You are going to "+c1.dest+', '+ c1.stop



app_title()
