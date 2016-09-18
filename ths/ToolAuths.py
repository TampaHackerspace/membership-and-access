'''
Created on Sep 18, 2016

@author: tbirch
'''
from _GoogSheets import GoogSheets

class ToolAuths(object):
    '''
    classdocs
    '''

    Config = {
        "GOOG_SHOP_SHEET" : '1R-H9d-XOLUWo7H1HpnLOAkWaHHMAvinwpQ84oA0GG1w',
    }

    def __init__(self, params):
        '''
        Get tool signoffs from Google Sheets
        '''
        GoogSheets.__init__(self, params)
        