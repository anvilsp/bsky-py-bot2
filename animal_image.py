# This script includes the functions to get animal images and the corresponding raw image
# Program by Ava Vazquez

import random, requests

animal_types = ["dog", "cat", "bunny", "duck", "lizard"]

def get_random_animal():
    global animal_types
    return random.choice(animal_types)

def check_if_animal(animal):
    # check if there's an animal in the array
    global animal_types
    if animal in animal_types:
        return True
    return False

def get_animal_url(animal = None):
    global animal_types

    if not animal in animal_types or animal == None:
        # get a random animal if nothing is specified
        animal = get_random_animal()
    try:
        match animal:
            case "dog":
                response = requests.get("https://dog.ceo/api/breeds/image/random")
                # url is under 'message' in json
                return response.json()['message']
            case "cat":
                response = requests.get("https://api.thecatapi.com/v1/images/search")
                # returns an array with a dict of values, so get the 0th index and then the url value
                return response.json()[0]['url']
            case "bunny":
                response = requests.get("https://api.bunnies.io/v2/loop/random/?media=gif,png")
                return response.json()['media']['poster']
            case "duck":
                response = requests.get("https://random-d.uk/api/v2/random?type=jpg")
                return response.json()['url']
            case "lizard":
                response = requests.get("https://nekos.life/api/v2/img/lizard")
                return response.json()['url']
    except Exception as e:
        print("Error loading from API.")
        exit()

def get_image(url):
    try:
        # get and return the raw data from the image at the given URL
        image_data = requests.get(url)
        return image_data.content
    except Exception as e:
        print("Error downloading image.")
        exit()