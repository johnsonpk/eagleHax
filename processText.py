import re, logging, Image, pytesseract
from PIL import Image
logging.basicConfig(level=logging.DEBUG, format= "%(asctime)s - %(levelname)s - %(message)s")
#print(pytesseract.image_to_string(Image.open('test.jpg')))
#print(pytesseract.image_to_string(Image.open('test-european.jpg'), lang='fra'))

data = pytesseract.image_to_string(Image.open('test.jpg'))

def processText():
    pass


def addEvent():
    pass



