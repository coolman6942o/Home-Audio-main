from twilio.rest import Client
account_sid = 'AC9798d4a2551c7b813978b18afb5ba5b4'
auth_token = 'd0b5c1524912f89ae37ddfa85340b63c'
client = Client(account_sid, auth_token)
message = client.messages.create(
  from_='+14159643653',
  body='Hello This is the KGB and I demand $100k or He dies ',
  to='+61477033909'
)
print(message.sid)
