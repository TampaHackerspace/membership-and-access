from __future__ import print_function

import time

import demjson
from slackclient import SlackClient

import ths.Member

ConfigFile = '/Users/tbirch/GitHub/membership-and-access/config/config.json'
ConfigLocal = '/Users/tbirch/GitHub/membership-and-access/config/local/config.json'

SlackTeam = dict()
SlackChans = dict()

config = demjson.decode_file(ConfigFile)
config.update(demjson.decode_file(ConfigLocal))

config["MessageID"] = 1

#===============================================================================
# Startup functions
#===============================================================================

def build_slack_lists():
    user_list = sc.api_call("users.list")
    if user_list['ok']:
        for u in user_list['members']:
            SlackTeam[u['id']] = u
    else:
        print("Something wrong with user list.")

    chan_list = sc.api_call("channels.list")
    if chan_list['ok']:
        for c in chan_list['channels']:
            SlackChans[c['id']] = c

    else:
        print("Something wrong with channel list.")

#------------------------------------------------------------------------------ 
def got_hello(msg):
    if msg:
        ev = msg['type']
        if ev == "hello":
            print("Got hello")
            return True
    raise
    return False
#===============================================================================
# Utiity functions
#===============================================================================
def get_or_add_user(uid):
    if SlackTeam.has_key(uid):
        u = SlackTeam[uid]
    else:
        u = sc.api_call('users.info', user=uid)
        if u["ok"]:
            SlackTeam[uid] = u["user"]
            u = u["user"]
        else:
            u = {"name" : uid}
    return u

#===============================================================================
# Parse message event looking for magic words
#===============================================================================
def handle_message(msg):
    u = get_or_add_user(msg["user"])
    if u.has_key("name"):
        uname = u["name"]
        txt = msg["text"]
        loc = txt.find(config["MAGIC_WORDS"])
        if loc < 0:
            return
        
        loc = loc + len(config["MAGIC_WORDS"])
        words = txt[loc:].split()
        target = words[0].strip();
        if target[0:2] != "<@":
            print("Sorry, ", uname, ", I can't do that.", sep="")
        target = target[2:len(target)-1]

        if (msg["user"] != config["OWNER_UID"]):
            
            send_txt = uname," is not the boss of me!"
            print(send_txt)
            
            config["MessageID"] = config["MessageID"] + 1
            sc.rtm_send_message(msg["channel"], send_txt)
            return

        target_user = get_or_add_user(target)
        target_profile =  target_user["profile"]
        target_name = target_profile["real_name"]
        member = mem.lookup(fullname=target_name, firstname=target_profile["first_name"], lastname=target_profile["last_name"])
        if member:
            print(member)
            send_txt = member["First Name"] + " " + member["Last Name"] + " is a member."
        else:
            send_txt = "I don't see " + target_name + " in the member list."
        config["MessageID"] = config["MessageID"] + 1
        sc.rtm_send_message(msg["channel"], send_txt)


    else:
        uname = msg["user"]
    
    if SlackChans.has_key(msg["channel"]):
        c = SlackChans[msg["channel"]]
    else:
        c = sc.api_call("channels.info", channel=msg["channel"])
        if c["ok"]:
            SlackChans[msg["channel"]] = c["channel"]
            c = c["channel"]
        else:
            c = { "channel" : msg["channel"]}
    
    if c.has_key("name"):
        cname = c["name"]
    else:
        cname = msg["channel"]

    print(uname, "in channel", cname, "says:")
    print("    ", msg['text'])
    
#===============================================================================
# The main deal
#===============================================================================
mem = ths.Member(config["GOOG"])

sc = SlackClient(config['BOT_TOKEN'])
slack_ok = sc.rtm_connect()
if slack_ok:
    print("Connected to Slack, building user/channel lists")
    build_slack_lists()
else:
    print ("Could not connect to Slack")


if slack_ok:
    msg_list = sc.rtm_read()
    try:
        got_hello(msg_list.pop(0))
    except:
        print("That's odd, no 'hello' from Slack")

    while True:
        msg_list = sc.rtm_read()
        for msg in msg_list:
            if msg.has_key("ok"):
                # response to something we sent
                if msg["ok"]:
                    print("Sent OK:\n",msg)
                else:
                    print("ERROR sendingn",msg)
                continue
            
            ev = msg["type"]

            if ev == "message":
                handle_message(msg)    
 
            elif ev == "presence_change":
                u = get_or_add_user(msg["user"])
                print(u['name'], "is now", msg['presence'])
                
            elif ev == "reconnect_url":
                pass    # unsupported type - discard              
                
            else:
                for key,val in msg.iteritems():
                    print("Got:", key, "|", val)
 
        time.sleep(config['SLACKPOLL_DELAY'])
