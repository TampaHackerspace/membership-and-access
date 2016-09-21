'''
Created on Sep 18, 2016

@author: tbirch
'''
from _Goog import Goog
import os

from oauth2client import client
from oauth2client import tools
import oauth2client

class GoogAuth(Goog):
    '''
    classdocs
    '''
    
    def __init__(self, params):
        '''
        Constructor
        '''
        Goog.__init__(self, params)
        Goog.Config.update(params)

    #------------------------------------------------------------------------------ 
    def get_credentials(self, scope):
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
        credential_path = os.path.join(credential_dir, Goog.Config["GOOGLE_APPLICATION_CREDENTIALS"])
    
        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            scope = Goog.Config["GOOG_SCOPE_BASE"] + scope
            flow = client.flow_from_clientsecrets(Goog.Config["GOOG_SECRET_FILE"], scope)
            flow.user_agent = Goog.Config["GOOG_APP_NAME"]
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                #credentials = tools.run(flow, store)
                raise
            print('Storing credentials to ' + credential_path)
        return credentials
    
