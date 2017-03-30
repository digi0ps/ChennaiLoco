from django.shortcuts import render
from django.views.generic import ListView


# Models Import
from train.models import Train, Station, Status


def home_view(request):
	return render(request, "home.html")


class train_list(ListView):
	model = Train
	context_object_name = "trains"
	template_name = "trains_list.html"


class station_list(ListView):
	model = Station
	context_object_name = "stations"
	template_name = "stations_list.html"
