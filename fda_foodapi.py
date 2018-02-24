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

def foodSearch():
    searchTerm = input("Enter the food you want to search for: ").split()
    maxResults = input("What are the maximum number of results you would like: ")

    if len(searchTerm) > 1:
        searchTerm = '+'.join(searchTerm)
        searchURL = 'https://api.nal.usda.gov/ndb/search/?format=json&q={0}&sort=n&max={1}&offset=0&api_key={2}'.format(searchTerm, maxResults, config.api_key)
        
    else:
         searchURL = 'https://api.nal.usda.gov/ndb/search/?format=json&q={0}&sort=n&max={1}&offset=0&api_key={2}'.format(searchTerm[0], maxResults, config.api_key)
    
    return searchURL

def searchResults(url):
    response = requests.get(url)
    data = json.loads(response.text)
    data = data['list']['item']
    return data

def displaySearch(data):
    for index, item in enumerate(data):
        print('{0}) {1}'.format(index+1,item['name']))

def getNutrition(data):
    selection = int(input('Enter the food you would like the nutrition content for: '))
    index = selection - 1
    item_id = data[index]['ndbno']
    nutr_url = ('https://api.nal.usda.gov/ndb/nutrients/?format=json&api_key={0}&nutrients='
                '{1}&nutrients={2}&nutrients={3}&nutrients={4}&nutrients={5}&nutrients={6}&ndbno={7}'.format(config.api_key, nu['kcal'], 
                nu['fat'], nu['protein'], nu['carbs'], nu['fiber'], nu['sugars'], item_id))
    response = requests.get(nutr_url)
    nutr_data = json.loads(response.text)
    return nutr_data
    
def parseNutrition(nutr_data):
    nutrparse = nutr_data
    food_name = nutrparse['report']['foods'][0]['name']
    serving_size = nutrparse['report']['foods'][0]['measure']
    nutrient_list = nutrparse['report']['foods'][0]['nutrients']
    #Need a way to make this more memory efficient parsing, maybe a regex?
    for i in nutrient_list:
        if i['nutrient_id'] == '208':
            calories = i['value']
        elif i['nutrient_id'] == '291':
            fiber = i['value']
        elif i['nutrient_id'] == '203':
            protein = i['value']
        elif i['nutrient_id'] == '269':
            sugars = i['value']
        elif i['nutrient_id'] == '204':
            fat = i['value']
        elif i['nutrient_id'] == '205':
            carbs = i['value']
    keys = ['food_name', 'serving_size','calories','fiber','protein','sugars','fat','carbs']
    values = [food_name,serving_size,calories,fiber,protein,sugars,fat,carbs]
    nutr_dict = dict(zip(keys,values))
    return nutr_dict

def test():
    search_url = 'https://api.nal.usda.gov/ndb/search/?format=json&q={0}&sort=n&max={1}&offset=0&api_key={2}'.format('Mcdonald', '60', config.api_key)
    user_file = 'Patrick_data.csv'
    nutr_url = ('https://api.nal.usda.gov/ndb/nutrients/?format=json&api_key={0}&nutrients='
                '{1}&nutrients={2}&nutrients={3}&nutrients={4}&nutrients={5}&nutrients={6}&ndbno={7}'.format(config.api_key, nu['kcal'], 
                nu['fat'], nu['protein'], nu['carbs'], nu['fiber'], nu['sugars'], '21228'))
    response = requests.get(nutr_url)
    nutr_data = json.loads(response.text)
    return nutr_data

def main():    
    userSetup()
    search_url = foodSearch()
    search_data = searchResults(search_url)
    displaySearch(search_data)
    nutr_data = getNutrition(search_data)
    results = parseNutrition(nutr_data)
    print(results)


    


main()
