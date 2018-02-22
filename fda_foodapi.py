import requests
import json
import config

def parseTerms(terms):

    print(terms)


API_KEY = 'Ta7LL6tQ7R28M66t4euBYPwK4O3GW5LBaoa6Vdbk'
BASE_URL = 'https://api.nal.usda.gov/ndb/search/?format=json&q=&sort=n&max=25&offset=0&api_key={0}'.format(config.api_key)

searchTerm = input("Enter the food you want to search for: ").split()
maxResults = input("What are the maximum number of results you would like: ")
if len(searchTerm) > 1:
    searchTerm = '+'.join(searchTerm)
    searchURL = 'https://api.nal.usda.gov/ndb/search/?format=json&q={0}&sort=n&max={1}&offset=0&api_key={2}'.format(searchTerm, maxResults, config.api_key)
    
else:
    searchURL = 'https://api.nal.usda.gov/ndb/search/?format=json&q={0}&sort=n&max={1}&offset=0&api_key={2}'.format(searchTerm[0], maxResults, config.api_key)
    
print(searchURL)



