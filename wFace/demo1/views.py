from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import base64
import os
from django.conf import settings
import face_recognition
import random
from django.http import JsonResponse
import sys
from demo1.models import User
from django.core import serializers
import json
import numpy as np
import requests

class JsonEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
            np.int16, np.int32, np.int64, np.uint8,
            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, 
            np.float64)):
            return float(obj)
        elif isinstance(obj,(np.ndarray,)): #### This is the fix
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def index(request):
	context = {
		'some_context': "context_answer",
	}
	return render(request, 'demo2/index.html', context)
	
@csrf_exempt
def video(request):
	context = {
		'some_context': "context_answer",
	}
	return render(request, 'demo1/videoupload.html', context)	
	
@csrf_exempt
def register(request):
	context = {
		'some_context': "context_answer",
	}
	if request.method == 'POST': # If the form has been submitted...
		print("this is a post request")
		return render(request, 'demo2/index.html', context)
	else:
		return render(request, 'demo2/Registerationpage.html', context)
	
@csrf_exempt
def doregister(request):
	context = {
		'some_context': "context_answer",
	}
	if request.method == 'POST': # If the form has been submitted...
		img1 = request.POST.get("img1", " ")
		img2 = request.POST.get("img2", " ")
		img3 = request.POST.get("img3", " ")
		img4 = request.POST.get("img4", " ")
		img5 = request.POST.get("img5", " ")
		name = request.POST.get("name", " ")
		email = request.POST.get("email", " ")	
		address = request.POST.get("address", " ")	
		
		URL = "http://127.0.0.1:5000/predict"				
		r = requests.post(url = URL, json={"image":img1})
		if r.status_code == 200:
			data = r.json()
			if(data['status'] == 'success'):		
				id = data['id']
				if id == 'unknown':
					print("successful registration begins")
				else:
					return JsonResponse({'ret':'fail', 'msg':'User already exists'})					
		else:
			return JsonResponse({'ret':'fail', 'msg':'internal error'})				
		
		URL = "http://127.0.0.1:5000/create"
		PARAMS = {'address':'address'} 
		r = requests.get(url = URL, params = PARAMS) 
		
		if r.status_code != 200:
			return JsonResponse({'ret':'fail', 'msg':'internal error'})	
		
		id = '';
		data = r.json() 
		print(data)
		if(data['status'] == 'success'):
			images = [img1, img2, img3, img4, img5]
			for image in images:
				id = data['id']
				URL = "http://127.0.0.1:5000/update"				
				r = requests.post(url = URL, json={"id": id, 
												   "image":image})
				if r.status_code != 200:
					return JsonResponse({'ret':'fail', 'msg':'internal error'})	
		else:
			return JsonResponse({'ret':'fail', 'msg':'internal error'})			
		
		URL = "http://127.0.0.1:5000/train"		
		PARAMS = {'address':'address'} 	
		r = requests.get(url = URL, params = PARAMS) 

		if r.status_code != 200:
			return JsonResponse({'ret':'fail', 'msg':'internal error'})
		else:
			user = User(userName= name, email = email, address = address, encoded=id)
			user.save();	
			return JsonResponse({'ret':'success', 'msg':'Successful registration'})				
		
@csrf_exempt
def login(request):
	context = {
		'some_context': "context_answer",
	}
	return render(request, 'demo2/Loginpage.html', context)		

@csrf_exempt	
def dologin(request):
	if request.method == 'POST': # If the form has been submitted...
		image = request.POST.get("image", " ")
		if image:
			URL = "http://127.0.0.1:5000/predict"				
			r = requests.post(url = URL, json={"image":image})
			if r.status_code == 200:
				data = r.json()
				if(data['status'] == 'success'):
					id = data['id']
					print(id)
					user = User.objects.get(encoded=id)
					name = user.userName;
					email = user.email;
					address = user.address;					
					return JsonResponse({'ret':'success', "name": name, "email": email, "address": address, 'msg':'Successfully logged in'})
				else:
					return JsonResponse({'ret':'fail', 'msg':'User does not exists'})	
			else:
				return JsonResponse({'ret':'fail', 'msg':'Internal error'})						

# Create your views here.
