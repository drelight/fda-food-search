import requests
import json
import config
import csv
from globals import HEADERS
from globals import NUTRIENT_IDS as nu


def userSetup():
    name = input("What is your name: ")
    response = int(input("Is this your first time using the program input 1 for no or 2 for yes: "))
    if response is 1:
        return
    elif response is 2:
        with open('{}_data.csv'.format(name), 'w+') as csvfile:
            write = csv.writer(csvfile)
            write.writerow(HEADERS)
    else:
        print("Please enter valid input")
        userSetup()

def getURL():

    searchTerm = input("Enter the food you want to search for: ").split()
    maxResults = input("What are the maximum number of results you would like: ")

    if len(searchTerm) > 1:
        searchTerm = '+'.join(searchTerm)
        searchURL = 'https://api.nal.usda.gov/ndb/search/?format=json&q={0}&sort=n&max={1}&offset=0&api_key={2}'.format(searchTerm, maxResults, config.api_key)
        
    else:
         searchURL = 'https://api.nal.usda.gov/ndb/search/?format=json&q={0}&sort=n&max={1}&offset=0&api_key={2}'.format(searchTerm[0], maxResults, config.api_key)
    
    return searchURL

def parseResults(url):
    response = requests.get(url)
    data = json.loads(response.text)
    data = data['list']['item']
    return data

def displaySearch(data):
    for index, item in enumerate(data):
        print('{0}) {1}'.format(index+1,item['name']))

def getNurtrition(data):
    selection = int(input('Enter the food you would like the nutrition content for: '))
    index = selection - 1
    itemId = data[index]['ndbno']
    nutrURL = ('https://api.nal.usda.gov/ndb/nutrients/?format=json&api_key={0}&nutrients='
                '{1}&nutrients={2}&nutrients={3}&nutrients={4}&nutrients={5}&nutrients={6}&ndbno={7}'.format(config.api_key, nu['kcal'], 
                nu['fat'], nu['protein'], nu['carbs'], nu['fiber'], nu['sugars'], itemId))
    response = requests.get(nutrURL)
    nutr_data = json.loads(response.text)
    return nutr_data
    
def parseNutrition(nutr_data):
    nutrparse = nutr_data
    food_name = nutrparse['report']['foods'][0]['name']
    serving_size = nutrparse['report']['foods'][0]['measure']
    nutrient_list = nutrparse['report']['foods'][0]['nutrients']
    return food_name, serving_size, nutrient_list


def main():    
    userSetup()
    url = getURL()
    data = parseResults(url)
    displaySearch(data)
    nutr_data = getNurtrition(data)
    print(parseNutrition(nutr_data))

main()
