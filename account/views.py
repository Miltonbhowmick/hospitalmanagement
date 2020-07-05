from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout 
# Create your views here.
from . import models
from django.http import HttpResponse

