import re, logging, Image, pytesseract
from PIL import Image
logging.basicConfig(level=logging.DEBUG, format= "%(asctime)s - %(levelname)s - %(message)s")
#print(pytesseract.image_to_string(Image.open('test.jpg')))
#print(pytesseract.image_to_string(Image.open('test-european.jpg'), lang='fra'))

PlainText = pytesseract.image_to_string(Image.open('test.jpg'))

def processDate(data):
    copy_of_data = data
    print data
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
    
    
    
    # appropiate start and end times
    if len(time_span) == 2:
        startTime = time_span[0]
        endTime = time_span[1]
    else:
        startTime = time_span[0]
        endTime = None
    
    print startTime
    print endTime
    
    

#processDate(PlainText)





def processText(PlainText):
    pass
    # date = processDate(PlainText)
    # location = processLocation(PlainText)
    # title = processTitle(PlainText)
    # description  = processDescription(PlainText)
   
def processLocation(data):
    pass


def addEvent():
    pass



