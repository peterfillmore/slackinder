#!/usr/local/bin/python
import time
import pynder
import re

import logging

#setup logging
logger = logging.getLogger('TINDBOT')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('tindbot.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


FBTOKEN = "INSERTTOKEN"
FBID = "INSERTID"

crontable = []
outputs = []

mysession = pynder.Session(FBID, FBTOKEN)
users = mysession.nearby_users()

#print users
tindercounter=0
currentmatches = list() #store the list of matches into an easy list
matchkey = 0

#regex for matching tindmsgs
tindmsgregex = re.compile('tindmsg ([0-9]*)', re.IGNORECASE) #get the corresponding match number
tindrecregex = re.compile('tindreceive ([0-9]*)', re.IGNORECASE)
tindmsgsendregex = re.compile('tindmsg [0-9]* ([a-z0-9\s]*)', re.IGNORECASE) #get text from after the number

def stripusername(username):
#function to strip out unicode junk from the username
    return username[2:-1]

def process_message(data):
    global tindercounter 
    global mysession 
    global users
    global currentmatches 
    try: 
        if (data['text'].lower().startswith("tindmatch")): 
            try: 
                photo = users[tindercounter].get_photos()[0]
                name = users[tindercounter].name
                age = str(users[tindercounter].age)
                outputs.append([data['channel'], photo])
                outputs.append([data['channel'], "Name:"+ name + "("+age+")"])
                logger.info("tindbot found: "+name+" photo:"+photo) 
            except:
                outputs.append([data['channel'], "Ran out of matches - generating more!"])
                users = mysession.nearby_users()
                print users 
                tindercounter=0
                logger.info("tindbot generated more potential matches") 
                pass 
        if (data['text'].lower().startswith("swiperight")): 
            outputs.append([data['channel'], "tindbot Liked "])
            outputs.append([data['channel'], users[tindercounter].name])
            users[tindercounter].like()
            if tindercounter<len(users): 
                tindercounter +=1
            else:
                users = mysession.nearby_users()
                tindercounter=0
                logger.info("tindbot Liked:"+users[tindercounter].name) 
        if (data['text'].lower().startswith("swipeleft")): 
            outputs.append([data['channel'], "tindbot Disliked "])
            outputs.append([data['channel'], users[tindercounter].name])
            users[tindercounter].dislike()
            if tindercounter<len(users): 
                tindercounter +=1
            else:
                users = mysession.nearby_users()
                tindercounter=0
            logger.info("tindbot Disliked:"+users[tindercounter].name) 
        if (data['text'].lower().startswith("tindscore")): 
            currentmatches = list() #clear the current dictionary
            matchkey = 0 
            for match in mysession.matches():
                currentmatches.append([stripusername(str(match)), match]) 
                outputs.append([data['channel'], str(matchkey)+" "+stripusername(str(match))])
                outputs.append([data['channel'], match.user.thumbnails[0]])
                matchkey += 1
                logger.info("tindbot matched:"+str(matchkey)+" "+stripusername(str(match)))
        if (data['text'].lower().startswith("tindmsg")):
            tindmsgindex = int(tindmsgregex.search(data['text']).groups(1)[0]) 
            try: 
                match = currentmatches[tindmsgindex][1] #get the match we're messaging
                mymsg = tindmsgsendregex.search(data['text']).groups(1)[0] 
                match.message(mymsg)
                outputs.append([data['channel'], "tindbot sent:'"+mymsg+"' To "+currentmatches[tindmsgindex][0]])
                logger.info("tindbot sent:"+mymsg+" To "+currentmatches[tindmsgindex][0]) 
            except:
                outputs.append([data['channel'], "I'm broken - probably just run tindscore to fix me"])
        if (data['text'].lower().startswith("tindreceive")):
            tindrecindex = int(tindrecregex.search(data['text']).groups(1)[0]) 
            try: 
                match = currentmatches[tindrecindex][1] 
                outputs.append([data['channel'], match.user.name])
                print match.messages 
                for message in match.messages: 
                    outputs.append([data['channel'], str(message)])
            except:
                outputs.append([data['channel'], "I'm broken - probably just run tindscore to fix me"])
        if (data['text'].lower().startswith("tinddump")):
            try: 
                for match in mysession.matches():
                    for message in match.messages: 
                        outputs.append([data['channel'], str(match) + ":"])
                        outputs.append([data['channel'], str(message)])
            except: 
                outputs.append([data['channel'], "Something broke - hopefully i'm still working"])
    except KeyError:
        pass
