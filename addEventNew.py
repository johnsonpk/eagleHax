from __future__ import print_function
import httplib2
import os
import re, logging, Image, pytesseract, datetime
from PIL import Image
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/calendar']
#SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


event = {
  'summary': 'I was unable to get a summary.',
  'location': 'Unable to find a location',
  'description': 'I was unable to find a description.',
  'start': {
    'dateTime': '2016-04-20T07:00:00-05:00',
    'timeZone': 'America/Chicago',
  },
  'end': {
    'dateTime': '2016-04-20T12:00:00-05:00',
    'timeZone': 'America/Chicago',
  },
  'recurrence': [
    'RRULE:FREQ=MONTHLY;COUNT=1'
  ],
  'attendees': [
    {'email': 'paulj.96@gmail.com'},
    {'email': 'abhishah212@gmail.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'popup', 'minutes': 10},
    ],
  },
}
	


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def processDate(data):
    copy_of_data = data
    # print data
    '''
    keywordRegex = re.compile(r'(date|time)*')
    matching_keyword_objects = keywordRegex.search(data)
    print matching_keyword_objects.group()
    
    dateRegex = re.compile(r'((January|February|March|April|May|June|July|August|September|October|November|December|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)+.*\d\d)')
    matching_date_list = dateRegex.findall(data)
    print matching_date_list
    # first index is the best one (most specific)
    single_date = matching_date_list[0][0]
    print single_date
    
    # NEED TO CONVERT DATE/TIME INTO RFC3339 FORMAT
    '''
    dateRegex = re.compile(r'((?:(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?\s+(?:of\s+)?(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)|(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)\s+(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?)(?:\,)?\s*(?:\d{4})?|[0-3]?\d[-\./][0-3]?\d[-\./]\d{2,4})', re.IGNORECASE)
    matching_date_list = dateRegex.findall(data)
    # print matching_date_list
    single_date = matching_date_list[0].replace("\n", "")
    # print single_date
    
    monthDict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    monthDict = {"january":1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12}
    split_date = single_date.split()
    date = split_date[1]
    month = monthDict[split_date[0].lower()]
    
    # single value months (0-9)
    if len(str(month)) < 2:
        month = '0' + str(month)
    # print "date", date
    # print "month", month
    
    '''
    # time regex
    timeRegex = re.compile(r'(\d.*(PM|AM))')
    
    matching_time_list = timeRegex.findall(data)
    print "0"
    print matching_time_list
    
    time_span = matching_time_list[0][0]
    try:
        startTime = time_span.split('-')
        time_span = time_span.split('-')
    except:
        startTime = time_span.split('')
    
    print time_span
    '''
    # time regex
    timeRegex = re.compile(r'(\d{1,2}:\d{2} ?(?:[ap]\.?m\.?)?|\d[ap]\.?m\.?)', re.IGNORECASE)
    
    time_span = timeRegex.findall(data)
    
    # print "0"
    # print time_span

    
    
    # appropiate start and end times
    if len(time_span) == 2:
        startTime = time_span[0]
        endTime = time_span[1]
    else:
        startTime = time_span[0]
        endTime = None
    
    # print startTime
    # print endTime
    
    # begin to convert to rfc 3339 format
    # NEED TO ADD THE ABILITY TO HAVE MINUTES IN THE PROCESSING (SPLIT ON :)
    if 'pm' in startTime.lower():

        initial_time = int(startTime.lower().replace("pm", ""))
        initial_time = (initial_time + 12) % 24
        print(initial_time)
        # single value months (0-9)
        if len(str(initial_time)) < 2:
            initial_time = '0' + str(initial_time)
        # print initial_time
        #initial_time_number = int(initial_time.split())
        
    elif 'am' in startTime.lower():
        initial_time = startTime.lower().replace("am", "")
	initial_time = str((int(initial_time) + 5))
        # single value months (0-9)
        if len(str(initial_time)) < 2:
            initial_time = '0' + str(initial_time)
        # print initial_time
        
    else:
        pass
    
    # end time
    if 'pm' in endTime.lower():

        end_time = int(endTime.lower().replace("pm", ""))
        end_time = (end_time + 12) % 24
        
        # single value months (0-9)
        if len(str(end_time)) < 2:
            end_time = '0' + str(end_time)
        print(end_time)
        #end_time_number = int(end_time.split())
        
    elif 'am' in endTime.lower():
        end_time = endTime.lower().replace("am", "")
	end_time = str((int(end_time) + 5))

        # single value months (0-9)
        if len(str(end_time)) < 2:
            end_time = '0' + str(end_time)
        # print end_time
        
    else:
        pass
    
    
    
    # hardcoded the year
    # year, month, day, time, minute, month
    print(initial_time)
    try:
        start_date_rfc = datetime.datetime(2016, int(month), int(date), int(initial_time), 00, 00).strftime("%Y-%m-%dT%H:%M:%S-05:00")
    except:
        start_date_rfc = datetime.datetime(2016, int(month), int(date), int(initial_time), 00, 00).strftime("%Y-%m-%dT%H:%M:%S-05:00")
        
    
    print(start_date_rfc) 
    
    #2016-05-28T09:00:00-05:00
    
    # end date
    try:
        end_date_rfc = datetime.datetime(2016, int(month),int(date), int(end_time), 00, 00).strftime("%Y-%m-%dT%H:%M:%S-05:00")
    except:
        end_date_rfc = datetime.datetime(2016, int(month),int(date), int(end_time), 00, 00).strftime("%Y-%m-%dT%H:%M:%S-05:00")
    
    print(end_date_rfc)
    
    event['start']['dateTime'] = start_date_rfc
    event['end']['dateTime'] = end_date_rfc
    
def processDescription(data):
    numberRegex = re.compile(r'(((?:(?<![\d-])(?:\+?\d{1,3}[-.\s*]?)?(?:\(?\d{3}\)?[-.\s*]?)?\d{3}[-.\s*]?\d{4}(?![\d-]))|(?:(?<![\d-])(?:(?:\(\+?\d{2}\))|(?:\+?\d{2}))\s*\d{2}\s*\d{3}\s*\d{4}(?![\d-]))))', re.IGNORECASE)
    matching_number_list = numberRegex.findall(data)
    # print matching_number_list
    event['description'] = matching_number_list[0][0]

  
def processLocation(data):
    addressRegex = re.compile(r'(\d{1,4}[\w\s]{1,20}(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd)?.*[0-9]{5}(-[0-9]{4})?)', re.IGNORECASE)
    matching_address_list = addressRegex.findall(data)
    # print data
    # print 'lol'
    # print matching_address_list
    event['location'] = matching_address_list[0][0]
    
def processText(PlainText):
    
    processDate(PlainText)
    processLocation(PlainText)
    # title = processTitle(PlainText)
    processDescription(PlainText)




def main():
	"""Shows basic usage of the Google Calendar API.
	
	Creates a Google Calendar API service object and outputs a list of the next
	10 events on the user's calendar.
	"""
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)
	
	now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

	
	PlainText = pytesseract.image_to_string(Image.open('test.jpg'))


	processText(PlainText)

	calendarEvent = service.events().insert(calendarId='primary', body=event).execute()
	print('Event created: %s' % (calendarEvent.get('htmlLink')))

	print(calendarEvent)


# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/google-apps/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.

if __name__ == '__main__':
    main()
