'''
Created on Sep 18, 2016

@author: tabinfl
'''

from fuzzywuzzy import fuzz

from _GoogSheets import GoogSheets

class Member(GoogSheets):
    '''
    Extract THS member information from a big hairy pile of Google Sheets
    '''
    
    Config = {
        "GOOG_MEMBERS_SHEET" : '1tYz8RiHH5_VGNaec_4SvNUYD5-gyeMiPKtD4tjcKk5M',
        "GOOG_MEMBERS_RANGE" : '2016!A2:Y110'
    }
    
    Members = {}
    LastNames = {}
    
    
    #------------------------------------------------------------------------------ 
    def __init__(self, params):
        '''
        Constructor - get OAuth2 credentials & populate Members dict
        '''
        GoogSheets.__init__(self, params)
        
        cred = self.get_credentials()
        self._load_goog_data(cred,
                             Member.Config["GOOG_MEMBERS_SHEET"],
                             Member.Config["GOOG_MEMBERS_RANGE"], )
        
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



    def _load_goog_data(self, cred, sheet_id, sheet_range):
        '''
        Load membership information from Google Sheet
        '''
    
        member_data = self.get_goog_data(cred, sheet_id, sheet_range)
        
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
#import MySQLdb as mysql
#===============================================================================
# 
# def _setup_mysql_conn():
#     '''
#     Sets up MySQL database connection - prototype membership DB
#     '''
#     self.db = mysql.connect(host=config['DBHOST'],user=config['DBUSER'],passwd=config['DBPASS'],db=config['DBNAME'])
# 
#     if self.db:
#         print ("Connected to database")
#         self.dbcur = self.db.cursor()
#     else:
#         print("Can't connect to database")
# 
# def _lookup_mysql_member_byslack(target_addr):
#     '''
#     Fetches single member by Slack handle from prototype MySQL database
#     '''
#     dbcur = self.dbcur
#     sql = "select online_accts.member_id, DATE_FORMAT(members.joindate, '%d %b %Y') from online_accts, members where online_accts.platform = 'slack' and online_accts.address = '{}' and members.member_id = online_accts.member_id".format(target_addr)
#     n = dbcur.execute(sql)
#     if n > 0:
#         rows = dbcur.fetchone()
#         (member_id, join_date) = rows
#         print (target_addr,"is a member since", join_date)
# 
#         dbcur.fetchall()
# 
#         sql = "select tool_name, DATE_FORMAT(auth_date, '%d %b %Y') from tool_auths, tools where tools.tool_id = tool_auths.tool_id and member_id = {}".format(int(member_id))
#         n = dbcur.execute(sql)
#         if n > 0:
#             rows = dbcur.fetchall()
#             for r in rows:
#                 (tool_name, auth_date) = r
#                 print("    ",tool_name,"on","{}".format(auth_date))
#         else:
#             print("NO tools authoried.")
#     else:
#         print(target_addr, "is NOT in the membership db.")
#===============================================================================
#------------------------------------------------------------------------------  
