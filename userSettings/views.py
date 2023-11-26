from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserSettings
from django.contrib import messages
import pdb

def index(request):

    # Load currency data from the JSON file
    currency_data=[]
    filePath= os.path.join(settings.BASE_DIR,'currencies.json')
    with open(filePath, 'r') as json_file:
        data= json.load(json_file)
        for k,v in data.items():
            currency_data.append({'name':k,'value':v})
    
    
    # Check if UserSettings exist for the current user
    exists= UserSettings.objects.filter(user=request.user).exists()
    user_settings= None
        
    if exists:
        user_settings=UserSettings.objects.get(user=request.user)

    if request.method== 'GET':
        
        
        # pdb.set_trace()
            
        return render(request,'settings/index.html',{'currencies':currency_data, 'user_settings':user_settings})
    
    else:
        # Update or create UserSettings based on the selected currency
        currency = request.POST['currency']
        if exists:
            user_settings.currency=currency
            user_settings.save()
        else:
            UserSettings.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved')
        return render(request,'settings/index.html',{'currencies':currency_data,'user_settings':user_settings})