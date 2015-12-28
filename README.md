# slackinder
A slack bot to interact with tinder
# requirements
slackclient
https://github.com/slackhq/python-slackclient
pip install slackclient

pynder
https://github.com/charliewolf/pynder
pip install pynder

# installation
Edit the ./plugins/tindbot.py file and add the appropriate values for the tinder account you want to use
FBTOKEN = <insert token here>
FBID = <insert ID here>

These instructions are good for locating and grabbing the tokens you need from facebook for your tinder account: 
https://gist.github.com/rtt/10403467

# usage
Type the following commands to interact with your bot

## tindmatch
Causes the bot to retrieve a current match - displaying photo and age of the match

## swiperight
'like' the current match

## swipeleft
'dislike' the current match

## tindscore
Get a listing of the matches that have liked you back
This gives you a number and a name.
Use the number to reference other actions in the bot

## tindmsg [match number] [message]
 
