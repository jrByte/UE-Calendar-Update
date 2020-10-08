# UE-Calendar-Update
This is an automated web scraping script. This will automatically log into University of Applied Sciences and download all the classes for that month. This program will then write this data into a CV file that can be exported to the desired calendar.

## Table of Contents

* [General info](#general-info)
* [Requirements](#requirements)
* [Technologies](#technologies)
* [Future](#Future)

## General Info

### Requirements:
The program only requries you to type in your username and password in the following box.

'''
def __init__(self, username="", password=""):
  self.username = username
  self.password = password
  self.dict = {}
'''

## Technologies: 

Project was ceated with:
* Python version: 3.7
* unicodecsv version: 0.14.1
* beautifulsoup4 version: 4.9.0
* requests version: 2.23.0

## Future:

From trial and error this is temporarily the best solution. Future changes can be made by using google calendar api. Currently the libraries aren't working with my python version.
