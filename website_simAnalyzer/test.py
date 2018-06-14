import requests
import json


register_request = requests.get('http://localhost:8000/server/user?mail=testmail1&password=testPassword&action=register')
print(register_request.json())

login_request = requests.get('http://localhost:8000/server/user?mail=testmail1&password=testPassword&action=login')
print(login_request.json())

update_request = requests.get('http://localhost:8000/server/user?mail=testmail1&password=testPassword&action=update&prefered_book=a&similar_book=b')
print(update_request.json())

#context = {
#            'method': 'POST',
#            'mail': 'testmail',
#            'password': 'testpassword',
#            'action': 'test'
#        }
#json_data = json.dumps(context)
#headers = {'content-type': 'application/json'}
#r = requests.post('http://localhost:8000/server/user', data=json_data, headers=headers)
#print(r.text)
#?mail=testmail&password=testPassword&action=test
#print(r.text)
