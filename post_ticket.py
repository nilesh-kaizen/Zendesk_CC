import os

import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

all_tickets = []
TICKETFROMID = 'https://zccbuff.zendesk.com/api/v2/tickets/'

load_dotenv()
user = os.getenv('user')
password = os.getenv('password')

'''
We are fetching all tickets in a single API call using below method.
Paging through tickets after fetching all tickets will reduce the API calls.
URL - will have URL of Zendesk API to fetch all tickets
'''


def fetch_tickets(URL):
    response = requests.get(URL, auth=HTTPBasicAuth(user, password))
    if response.status_code != 200:
        return response.status_code
    data = response.json()
    all_tickets.extend(data['tickets'])
    return all_tickets


'''
We are fetching ticket for individual ID.
ID - Unique ID of the ticket
'''


def fetch_ticket_from_url(ID):
    URL = TICKETFROMID + str(ID) + '.json'
    response = requests.get(URL, auth=HTTPBasicAuth(user, password))
    if response.status_code != 200:
        return response.status_code
    data = response.json()
    return data


class PostTicket:
    pass
