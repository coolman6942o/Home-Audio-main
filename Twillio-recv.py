# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC9798d4a2551c7b813978b18afb5ba5b4'
auth_token = 'd0b5c1524912f89ae37ddfa85340b63c'
client = Client(account_sid, auth_token)

messages = client.messages.list(limit=20,)
    
for msg in messages:
        print(f"From: {msg.from_}, To: {msg.to}, Date Sent: {msg.date_sent}, Status: {msg.status}")
        print(f"Message: {msg.body}")
        
        print("-" * 50)
        