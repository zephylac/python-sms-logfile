import sys
from twilio.rest import TwilioRestClient

accountSID = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
authToken = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
myTwilioNumber = 'xxxxxxxxxxxx'
myCellPhone = 'xxxxxxxxxxxxx'

def send(msg):
        client = TwilioRestClient(accountSID, authToken)
        client.messages.create(
                to = myCellPhone,
                from_ = myTwilioNumber,
                body = msg
        )
