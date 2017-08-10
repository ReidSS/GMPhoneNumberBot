import requests
import urllib
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

contact_info = {'test user':'5558675309', 'test usertwo': '5555555555'}


at = "AuthTokenHere" #auth token
botID = "BotIDHere" # Bot ID
groupID = 0000000 # Group ID


# Finds the closest match to a name in the contact info dictionary
def find_closest(name):
    highest = 0
    highestMatch = ""
    for key in contact_info:
        if fuzz.token_sort_ratio(key , name) > highest:
            highest = fuzz.token_sort_ratio(key , name)
            highestMatch = key

    return highestMatch

# Uses the find_closest function to search through the contact info dictionary
def search(name):
    try:
        return name + ": " + contact_info[name]
    except KeyError:
        closest_match = find_closest(name)
        if closest_match != "None":
            
            return closest_match  + ": " + contact_info[closest_match]
        else:
            return "Could not find a number for " + name

# adds a contact to the contact_info dictionary
def add_name(name, number):
    contact_info[name] = str(number)    

        
def post_message(bot_id, text):
    response = requests.post('https://api.groupme.com/v3/bots/post?token=72207070408d0134bb444d3c79b35b3a&bot_id=' + str(bot_id) + '&text=' + str(text))
    #data = response.json()
    print response


#post_message(botID, "yo")
def like_message(conversation_id, message_id):
    response = requests.post('https://api.groupme.com/v3/messages/' + str(conversation_id) + '/' + str(message_id) + '/like?token=72207070408d0134bb444d3c79b35b3a')
    
    print response


    

def get_latest_message(group_id):
    response = requests.get('https://api.groupme.com/v3/groups/' + str(group_id) + '?token=72207070408d0134bb444d3c79b35b3a')
    data = response.json()

    text = data['response']['messages']['preview']['text']

    should_i_talk = fuzz.token_sort_ratio(text, "what is number?")
    add_contact = fuzz.token_sort_ratio(text, "add a number")
    bus = fuzz.token_sort_ratio(text, "what time does the bus leave?")

    if should_i_talk > 60:
        post_message(botID, search(data['response']['messages']['preview']['text']))
        print 'posting'
        print should_i_talk


    elif add_contact > 75:
        print 'adding a contact'
        post_message(botID, "if you want to add a contact to the list, text Reid your name and number, 2179189339")

    elif bus > 87:
        post_message(botID, 'The buses leave at 4:00 P.M.')



i = 0
while i < 1:
    get_latest_message(groupID)
