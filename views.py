from django.shortcuts import render

# Creating view for generating text using gpt and another for fetching weather data.

from django.http import JsonResponse
import openai
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from .models import ApiResponse
openai.api_key = "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"
weather_api_url = "https://openweathermap.org/find?q="
weather_api_key = "9961ae2a5e636c6160bbbe940a671c98"

@csrf_exempt
def generate_text(request):
    if request.method=='GET':
        prompt=request.GET.get("prompt","")
        response=openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=50,
        )

        json_data = {
            "generated_text": response.choices[0].text,
            # Other JSON fields
        }
        api_response = ApiResponse(response_data=json_data)
        api_response.save()
        return JsonResponse({"generated_text": response.choices[0].text})
        #return render(request, 'index.html')

@csrf_exempt
def get_weather(request):
    if request.method=='GET':
        city=request.GET.get("city","")
        weather_api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}"
        params={
            "q":city,
            "appid":weather_api_key,
        }
        response=requests.get(weather_api_url,params=params)
        data=response.json()
        
        api_response = ApiResponse(response_data=data)
        api_response.save()

        return JsonResponse({"weather_data":data})

def get_json_from_database(request):
    responses = ApiResponse.objects.all()

    # Serialize the data to JSON and return it as a response
    data = [{"response_data": response.response_data} for response in responses]
    return JsonResponse(data, safe=False)
