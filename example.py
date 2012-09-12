import foursquare_api as fs 
import matplotlib.pyplot as plt #for plotting data
from datetime import *
from pandas import * #for dataframe
import json #for manipulating API responses
from credentials import *#credentials.py should define consumer_secret and consumer_key
#-----------------------------------
#get your own consumer key and secret after registering an app here: 
#https://foursquare.com/developers/apps

#NOTE: the redirect_uri you specify here must match what was specified when you registered your app 
myfs=fs.Foursquare(consumer_key,consumer_secret,redirect_uri='http://localhost:8080/foursquare_callback')
user_info = myfs.get_user_info(sample_user_id)#replace sample_user_id with the ID you want
print user_info

