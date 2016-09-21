'''
Created on Sep 18, 2016

@author: tabinfl
'''

from fuzzywuzzy import fuzz

from goog.GoogSheets import GoogSheets

class Member(object):
    '''
    Extract THS member information from a big hairy pile of Google Sheets
    '''
    
    Members = {}
    LastNames = {}
    gconfig={}
    
    
    #------------------------------------------------------------------------------ 
    def __init__(self, params):
        '''
        Constructor - get OAuth2 credentials & populate Members dict
        '''        

        self.gconfig.update(params);
        self._load_goog_data(self.gconfig["GOOG_MEMBERS_SHEET"], params["GOOG_MEMBERS_RANGE"])
    
        
        for (fullname, memberdata) in self.Members.iteritems():
            lname = memberdata["Last Name"]
            if self.LastNames.has_key(lname):
                self.LastNames[lname].append(fullname)
            else:
                self.LastNames[lname] = [fullname]
        return None
        
    #------------------------------------------------------------------------------ 
       
    def lookup(self, fullname=None, firstname=None, lastname=None):
        '''
        Find & return a single member record
        '''
        if fullname and self.Members.has_key(fullname):
            return self.Members[fullname]
        else:
            if self.LastNames.has_key(lastname):
                for try_name in self.LastNames[lastname]:
                    if fuzz.ratio(fullname, try_name) > 75:
                        return self.Members[try_name]
            return None
        
#===============================================================================
# Helpers below
#===============================================================================

    def _load_goog_data(self, sheet_id, sheet_range):
        '''
        Load membership information from Google Sheet
        '''    
        self.gs = GoogSheets(self.gconfig)
        member_data = self.gs.get_goog_data(sheet_id, sheet_range)
        
        fields = member_data.pop(0)
        for row in member_data:
            row_dict = {}
            for i in range(len(fields)):
                if len(row) <= i:
                    continue
                row_dict[fields[i]] = row[i]
            fullname = row_dict["First Name"] + " " + row_dict["Last Name"]
            self.Members[fullname] = row_dict
            
        return self.Members  
#------------------------------------------------------------------------------
