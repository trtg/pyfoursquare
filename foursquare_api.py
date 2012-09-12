from rauth.service import OAuth2Service #see https://github.com/litl/rauth for more info
import shelve #for persistent caching of tokens, hashes,etc.
import time
import datetime 
#get your own consumer key and secret after registering a desktop app here: 
#https://dev.Foursquare.com/apps/new
#for more details on the API: https://wiki.Foursquare.com/display/API/Foursquare+Resource+Access+API

class Foursquare:
    def __init__(self,consumer_key,consumer_secret,redirect_uri='',debug=0,cache_name='tokens.dat'):
        #cache stores tokens and hashes on disk so we avoid
        #requesting them every time.
        self.redirect_uri = redirect_uri
        self.cache=shelve.open(cache_name,writeback=False)
        self.debug=debug        
        self.oauth=OAuth2Service(
                name='foursquare',
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token_url='https://foursquare.com/oauth2/access_token',
                authorize_url='https://foursquare.com/oauth2/authorize')

        self.access_token = self.cache.get('foursquare_access_token',None)
        
        #If this is our first time running- get a new token
        if (self.access_token is None):
            got_access_token=self.get_access_token()
            if( not got_access_token):
                print "Error: Unable to get access token"
                    

    def dbg_print(self,txt):
        if self.debug==1:
            print txt

    def get_access_token(self):
        #the pin you want here is the string that appears after 'code=' on the page served
        #by the authorize_url
        #NOTE: the redirect_uri you specify here must match what was specified when you registered your 
        #foursquare app or you will receive an error indicating callback URI mismatch at this point
        authorize_url=self.oauth.get_authorize_url(redirect_uri=self.redirect_uri,response_type='code')

        print 'Visit this URL in your browser: ' + authorize_url
        code_string = raw_input('Enter the string after "code=" from the URL in your browser: ')

        data=dict(code=code_string,
                grant_type='authorization_code',
                redirect_uri = self.redirect_uri)
        response=self.oauth.get_access_token('POST', data=data)

        print "get_access_token response is ",response.content
        self.access_token=response.content.get('access_token',None)
        self.cache['foursquare_access_token']=self.access_token
        if not(self.access_token): 
            print "Unable to get an access token "
            return False
        else:
            return True

    
    def get_user_info(self,user_id=None):
        """Returns user profile info such as height, unit preference, timezone, stride length,etc. """
        #set user_id=='self' to get details of the acting user
        if user_id is None:
            user_id='self'
        params={}
        #foursquare inexplicably expects an argument named 'oauth_token' instead of access_token
        #params=dict(access_token=self.access_token)
        response=self.oauth.get(
                'https://api.foursquare.com/v2/users/%s?oauth_token=%s' % (user_id,self.access_token),
                params=params)
        return response.content
