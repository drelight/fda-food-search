import requests
import json
import config
import csv
from globals import HEADERS


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
    print(itemId)    

def main():    
    userSetup()
    url = getURL()
    data = parseResults(url)
    displaySearch(data)
    getNurtrition(data)

main()
