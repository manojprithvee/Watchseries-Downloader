import json,requests
a=requests.post('https://api.parse.com/1/push', data=json.dumps({
       "where": {
         "deviceType": "android"
       },
       "data": {
         "alert": "Your suitcase has been filled with tiny robots!",
         "title":"manoj"
       }
     }), headers={
       "X-Parse-Application-Id": "<enter app id>",
       "X-Parse-REST-API-Key": "<enter Restapi key>",
       "Content-Type": "application/json"
     })

print a.text