import requests
import json

IG_ACCESS_TOKEN = 'IGAAQSspJjZBBRBZAE9KZAWtYem5Pcmg2VFM1S1FBY0pKTVhrSk15U2kxcDNtdkhOZAHRpcjh0UEFzSHcyZAEI1Sll4aWc5SG1MWjB1M21wOFFGcXVXdFdXTy02Q2hQenE2UXNmNE5nMWpSanZAuRk1oa2VFSHlkYzB0VktaZAkl3OHcwdwZDZD'

CONVO_ID = 17842015820359855
IG_APP_SECRET = '772cd8074aa00e6fc9965875e765477b'

CHAT_ID_1 = 'aWdfZAG06MzQwMjgyMzY2ODQxNzEwMzAxMjQ0MjU5NzUwNDY2MDM0Mjc0NTE1'
CHAT_ID_2 = 'aWdfZAG06MzQwMjgyMzY2ODQxNzEwMzAxMjQ0MjU5NzkwMDE2ODYzNjUyNzY1'

MESSAGE_ID ='aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDExMjg2MDQyMzQ3OjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTc1MDQ2NjAzNDI3NDUxNTozMTk2NDc5MDE5MDMwNTA5MDY1NDcwNTgxNTc1MDk2NzI5NgZDZD' 

def get_message(id):
    r = requests.get(f"https://graph.instagram.com/v21.0/{id}", params={'fields': 'id,from,to,message', 'access_token': IG_ACCESS_TOKEN})
    return r

def get_conversation(id):
    r = requests.get(f"https://graph.instagram.com/v21.0/{id}", params={'fields': 'messages', 'access_token': IG_ACCESS_TOKEN})
    return r

def get_conversations(id):
    r = requests.get(f"https://graph.instagram.com/v21.0/me/conversations", params={'fields': 'messages', 'access_token': IG_ACCESS_TOKEN})
    return r

r = get_message(MESSAGE_ID)

print(r)
print(r.json())
