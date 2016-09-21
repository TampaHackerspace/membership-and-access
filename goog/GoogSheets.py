'''
Created on Sep 18, 2016

@author: tbirch
'''
from _Goog import Goog
from GoogAuth import GoogAuth

from apiclient import discovery
import httplib2


class GoogSheets(Goog):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        Goog.__init__(self, params)
        Goog.Config.update(GoogSheets.Config)
        Goog.Config.update(params)
        ga = GoogAuth(params)
        self.cred = ga.get_credentials('sheets.readonly')
    
    #------------------------------------------------------------------------------ 
    def get_goog_data(self, sheet_id, sheet_range):
        '''
        Load information from Google Sheet
        '''
        http = self.cred.authorize(httplib2.Http())
#        service = discovery.build('sheets', 'v4',
#                                  http=http, discoveryServiceUrl=GoogSheets.Config["GOOG_DISCOVERY_URL"])
        service = discovery.build('sheets', 'v4', http=http)
        result = service.spreadsheets().values().get(spreadsheetId=sheet_id,
                                                     range=sheet_range).execute()
        member_data = result.get('values',[])
        
        return member_data  