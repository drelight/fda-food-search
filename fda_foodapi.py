import requests
import json
import config
import csv

HEADERS = ['Date', 'Food Name', 'Serving Size', 'Calories', 'Fat', 'Protein', 'Carbohydrates']

def userSetup():
    name = input("What is your name: ")
    response = int(input("Is this your first time using the program input 1 for yes or 2 for no: "))
    if response is 1:
        return
    elif response is 2:
        with open('{}_data.csv'.format(name), 'w+') as csvfile:
            write = csv.writer(csvfile)
            write.writerow(HEADERS)
    else:
        print("Please enter valid input")
        userSetup()


#searchTerm = input("Enter the food you want to search for: ").split()
#maxResults = input("What are the maximum number of results you would like: ")
searchTerm = 'Ground Beef'.split()
maxResults = 20
if len(searchTerm) > 1:
    searchTerm = '+'.join(searchTerm)
    searchURL = 'https://api.nal.usda.gov/ndb/search/?format=json&q={0}&sort=n&max={1}&offset=0&api_key={2}'.format(searchTerm, maxResults, config.api_key)
    
else:
    searchURL = 'https://api.nal.usda.gov/ndb/search/?format=json&q={0}&sort=n&max={1}&offset=0&api_key={2}'.format(searchTerm[0], maxResults, config.api_key)
    
response = requests.get(searchURL)

data = json.loads(response.text)

data = data['list']['item']

for index, item in enumerate(data):
    print('{0}) {1}'.format(index+1,item['name']))

    
userSetup()


