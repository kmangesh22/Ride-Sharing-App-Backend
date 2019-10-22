from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import RideRequest
from .serializer import RideRequestSerializer
from bson import json_util
import json
from django.http import JsonResponse
from users.models import User
import smtplib
import os
# https://myaccount.google.com/lesssecureapps
# Create your views here.
from users.backend import authenticate
@api_view(['GET','POST'])
def request_ride(request):
    if authenticate(request):
        auth_res = authenticate(request)   
        if request.method == 'POST':
            if not request.data.get("start"):
                return Response({
                    "error":"Provide Start Location"
                },status=status.HTTP_400_BAD_REQUEST)
            if not request.data.get("destination"):
                return Response({
                    "error":"Provide Destination Location"
                },status=status.HTTP_400_BAD_REQUEST)
            if not request.data.get("start_time"):
                return Response({
                    "error":"Provide Start Time"
                },status=status.HTTP_400_BAD_REQUEST) 
            ride_request = RideRequest(start=request.data.get("start"),
                        destination=request.data.get("destination"),
                        start_time=request.data.get("start_time"),
                        status="Pending",
                        requester_id=auth_res[0].id)
            ride_request.save()
            return Response({
                "success":True
            },status=status.HTTP_201_CREATED)
        if request.method == 'GET':
            ride_requests = RideRequest.objects.all()
            serializer = RideRequestSerializer(ride_requests, many=True)
            return Response(serializer.data)                
    return Response("Forbidden", status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def pending_ride_requests(request):
    # if authenticate(request):
    res = []
    ride_requests = RideRequest.objects.filter(status="Pending").all()
    for request in ride_requests:
        res.append({
            "start":request["start"],
            "destination":request["destination"],
            "start_time":request["start_time"],
            "ride_request_id":str(request["id"]),
            "requester_name":request["requester_id"].name.first_name,
            "requester_contact_no":request["requester_id"].mobile_no
        })
    return Response(res)
    # return Response(res)                
    # return Response("Forbidden", status=status.HTTP_403_FORBIDDEN)

@api_view(['PUT'])
def offer_ride(request):
    if not request.data.get("id"):
        return Response({
            "error":"Provide request id"
        },status=status.HTTP_400_BAD_REQUEST)
    if not request.data.get("rider_id"):
        return Response({
            "error":"Provide Rider id"
        },status=status.HTTP_400_BAD_REQUEST)
    req = RideRequest.objects.get(id=request.data.get("id"))
    req.rider_id=User.objects.get(id=request.data.get("rider_id"))
    req.status = "Fullfilled"
    req.save()
    message = f"{req.rider_id.name.first_name} has Offerd you ride \n Contact number :- {req.rider_id.mobile_no}"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("kmangesh49@gmail.com", os.getenv("PASSWORD"))
    server.sendmail("kmangesh49@gmail.com", req.requester_id.email, message)
    return Response({"success":"ok"})
    

     
                