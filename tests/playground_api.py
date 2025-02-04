import requests
import json

real_msg = """{"object": "instagram",
  "entry": [
    {
      "time": 1737678111582,
      "id": "17841411286042347",
      "messaging": [
        {
          "sender": {
            "id": "640673465068123"
          },
          "recipient": {
            "id": "17841411286042347"
          },
          "timestamp": 1737678110615,
          "message": {
            "mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDExMjg2MDQyMzQ3OjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTc5MDAxNjg2MzY1Mjc2NTozMjA1NDUwMzM4OTAxODcxOTM1
NjI2ODI1OTcyODk0OTI0OAZDZD",
            "text": "Hey"
          }
        }
      ]
    }
  ]
}"""

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

def get_conversations():
    r = requests.get(f"https://graph.instagram.com/v21.0/me/conversations", params={'fields': 'messages', 'access_token': IG_ACCESS_TOKEN})
    return r

def send_message(sender_id, recipient_id, content):
    r = requests.post(f"https://graph.instagram.com/v22.0/{sender_id}/messages", 
                  headers={"Authorization": f"Bearer {IG_ACCESS_TOKEN}", "Content-Type":"application/json"},           
                  params={'access_token': IG_ACCESS_TOKEN}, 
                  json={"recipient":{"id":recipient_id}, "message": {"text": content}})
    return r

client_id = 640673465068123 
evenlift_id = 17841411286042347

print(f"Sending to client_id {client_id} from {evenlift_id} content: content")

random_id = 915479490737573
r = requests.get(f"https://graph.instagram.com/v22.0/{evenlift_id}", 
                  headers={"Authorization": f"Bearer {IG_ACCESS_TOKEN}", "Content-Type":"application/json"},           
                 params={'access_token': IG_ACCESS_TOKEN, 'fields':"id,username"}
                 )

# r = requests.post(f"https://graph.instagram.com/v22.0/{evenlift_id}/messages", 
#                   headers={"Authorization": f"Bearer {IG_ACCESS_TOKEN}", "Content-Type":"application/json"},           
#                   params={'access_token': IG_ACCESS_TOKEN}, 
#                   json={"recipient":{"id":client_id}, "message": {"text": "Return message fro. evenlift"}})
# r = get_conversations()
# r = get_message(MESSAGE_ID)

print(r)
print(r.json())
