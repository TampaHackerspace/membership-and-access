'''
Created on Sep 18, 2016

@author: tbirch
'''

import os

from apiclient import discovery
import httplib2

from oauth2client import client
from oauth2client import tools
import oauth2client

class GoogSheets(object):
    '''
    classdocs
    '''
    Config = {        
        "GOOG_SCOPE" : 'https://www.googleapis.com/auth/spreadsheets.readonly',
        "GOOG_DISCOVERY_URL" : 'https://sheets.googleapis.com/$discovery/rest?version=v4',
    
        "GOOGLE_APPLICATION_CREDENTIALS" : None,
        "GOOG_SECRET_FILE" : None,
        "GOOG_APP_NAME" : None
    }

    def __init__(self, params):
        '''
        Constructor
        '''
        GoogSheets.Config.update(params)

    #------------------------------------------------------------------------------ 
    def get_credentials(self):
        """Gets user credentials from storage.
    
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
    
        Returns:
            credentials, the obtained credential.
        """
        flags = None
        try:
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None
            
        credential_dir = '.'
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, GoogSheets.Config["GOOGLE_APPLICATION_CREDENTIALS"])
    
        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(GoogSheets.Config["GOOG_SECRET_FILE"], GoogSheets.Config["GOOG_SCOPE"])
            flow.user_agent = GoogSheets.Config["GOOG_APP_NAME"]
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                #credentials = tools.run(flow, store)
                raise
            print('Storing credentials to ' + credential_path)
        return credentials
    
    #------------------------------------------------------------------------------ 
    def get_goog_data(self, cred, sheet_id, sheet_range):
        '''
        Load information from Google Sheet
        '''
        http = cred.authorize(httplib2.Http())
        service = discovery.build('sheets', 'v4',
                                  http=http, discoveryServiceUrl=GoogSheets.Config["GOOG_DISCOVERY_URL"])
        
        result = service.spreadsheets().values().get(spreadsheetId=sheet_id,
                                                     range=sheet_range).execute()
        member_data = result.get('values',[])
        
        return member_data  