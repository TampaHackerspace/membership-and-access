'''
Created on Sep 18, 2016

@author: tbirch
'''
from _Goog import Goog
from GoogAuth import GoogAuth

import datetime

from apiclient import discovery
import httplib2

class GoogCal(Goog):
    '''
    classdocs
    '''
    
    def __init__(self, params):
        '''
        Constructor
        '''
        Goog.__init__(self)
        Goog.Config.update(params)
        ga = GoogAuth(params)
        self.cred = ga.get_credentials('calendar.readonly')

    #------------------------------------------------------------------------------ 
    def get_cal_list(self):
        '''
        Load information from Google Calendar
        '''
        http = self.cred.authorize(httplib2.Http())
        service = discovery.build('calendar',
                                  'v3',
                                  http=http)
 
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        cals = service.calendarList()
        calsResult = cals.list(
#            calendarId='primary',
#            timeMin=now,
#            maxResults=10, singleEvents=True,
#            orderBy='startTime'
            ).execute()
        calendars = calsResult.get('items', [])
    
        if not calendars:
            print('No calendars found.')
        for c in calendars:
            print(c)
#            start = event['start'].get('dateTime', event['start'].get('date'))
 #           print(start, event['summary'])
        
        return c  