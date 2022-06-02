from re import X
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from django.http import HttpResponse, JsonResponse
import slack
from .models import userInformation

# Create your views here.

@csrf_exempt
def events(request):#function that recieves events from Slack API

    client = slack.WebClient(token=settings.BOT_USER_ACCESS_TOKEN) #makes connection with our bot using access tokens
    json_dict = json.loads(request.body.decode('utf-8')) #reads the json file sent by Slack API
    
    if json_dict['token'] != settings.VERIFICATION_TOKEN: #Authenticates verification token
        return HttpResponse(status=403)
    
    if 'type' in json_dict: #authenticates the URL
        if json_dict['type'] == 'url_verification':
            response_dict = {"challenge": json_dict['challenge']}
            return JsonResponse(response_dict, safe=False)
    
    if 'event' in json_dict: #Checks if the response includes any events in the payload
        event_msg = json_dict['event'] #reads event message
        
        if ('subtype' in event_msg) and (event_msg['subtype'] == 'bot_message'): #If the event correspondes to any bot message, it bypasses and does nothing 
            return HttpResponse(status=200)
   
        #Below code checks and enters the user info in database
        if event_msg['type'] == 'app_mention': #Checks if bot is mentioned in a chat
            user = event_msg['user']
            channel = event_msg['channel']
            text = event_msg['text']

            userData = client.users_info(user = user) #Using slack api to retrieve the user information
            userI = str(userData['user']['id']) #unique id associated with slack user
            userN = str(userData['user']['name']) #gets the user name of the user
            fullN = str(userData['user']['real_name']) #gets the real name of the user
            em = str(userData['user']['profile']['email'])
                
            if userInformation.objects.filter(userId = userI): #Check if the user exists in the database or not
                passwordCheck = userInformation.objects.values_list("password").get(userId = userI)
                if passwordCheck[0] == None:
                    client.chat_postMessage(channel=channel, text="%s, Please set your password by sending me a DM :Slightly_Smiling_face:.\nNote: Use <SetPassword 'Enter your password here'> to set password" %fullN)
                    return HttpResponse(status=200)
                else:
                    client.chat_postMessage(channel=channel, text="%s, Hello :wave:" %fullN)
                    return HttpResponse(status=200)

         
            else:#Enters the userinfo in database since it does not exists.
                temp = userInformation(userId = userI, userName = userN, fullName = fullN, email = em)
                temp.save()
                client.chat_postMessage(channel=channel, text=client.chat_postMessage(channel=channel, text="%s, Please set your password by sending me a DM :Slightly_Smiling_face:.\nNote: Use <SetPassword 'Enter your password here'> to set password" %fullN))
                return HttpResponse(status=200)
                
            
            

        if event_msg['type'] == 'message': #Checks if any message is initiated. If so, it saves the message information in database
            user = event_msg['user']
            channel = event_msg['channel']
            text = event_msg['text']
            userData = client.users_info(user = user) #Using slack api to retrieve the user information
            
            if str(channel) == 'D03J308DT8Q':
                if "setpassword" in text.lower(): #used to set password for users
                    
                    userI = str(userData['user']['id']) #unique id associated with slack user
                    fullN = str(userData['user']['real_name']) #gets the real name of the user
                    passwordCheck = userInformation.objects.values_list("password").get(userId = userI)
                    
                    if passwordCheck[0] == None or passwordCheck[0] == 'None':
                        temporary = userInformation.objects.values_list().get(userId = userI)
                        temporary = userInformation.objects.get(id = temporary[0])
                        temporary.password = str((text.split())[-1])
                        temporary.save()
                        client.chat_postMessage(channel=channel, text="%s, Your Password is Saved :tada:"%fullN)
                        return HttpResponse(status=200)

                    else:
                        client.chat_postMessage(channel=channel, text="Password Exist.\nNote: to update password <UpdatePassword 'Enter your Previous Password Here' 'Enter New Password Here'> to set password f")
                        return HttpResponse(status=200)
                
                
                if "updatepassword" in text.lower(): #used to update password for users
                    
                    userI = str(userData['user']['id']) #unique id associated with slack user
                    fullN = str(userData['user']['real_name']) #gets the real name of the user
                    passwordCheck = userInformation.objects.values_list("password").get(userId = userI)
                    
                    if passwordCheck[0] == str((text.split())[-2]):
                        temporary = userInformation.objects.values_list().get(userId = userI)
                        temporary = userInformation.objects.get(id = temporary[0])
                        temporary.password = str((text.split())[-1])
                        temporary.save()
                        client.chat_postMessage(channel=channel, text="%s, Your Password is Updated :tada:"%fullN)
                        return HttpResponse(status=200)
                    
                    else:
                        client.chat_postMessage(channel=channel, text="%s, Your Password is Incorrect :disappointed:"%fullN)
                        return HttpResponse(status=200)

            

    
    return HttpResponse(status=200)