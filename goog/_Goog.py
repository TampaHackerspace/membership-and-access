'''
Created on Sep 18, 2016

@author: tbirch
'''

class Goog(object):
    '''
    classdocs
    '''
    Config = {
        "GOOG_DISCOVERY_URL" :  'https://www.googleapis.com/$api/v$apiVersion',        
        "GOOG_SCOPE_BASE" :          'https://www.googleapis.com/auth/',
   
        "GOOGLE_APPLICATION_CREDENTIALS" : None,
        "GOOG_SECRET_FILE" : None,
        "GOOG_APP_NAME" : None
    }


    def __init__(self, params):
        '''
        Constructor
        '''
        Goog.Config.update(params)
