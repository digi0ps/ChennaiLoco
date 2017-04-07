from django.shortcuts import render
from django.views.generic import ListView, DetailView


# Models Import
from train.models import Train, Station, Route


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


class train_detail(DetailView):
	model = Train
	context_object_name = "train"
	template_name = "train_detail.html"


class station_detail(DetailView):
	model = Station
	context_object_name = "station"
	template_name = "station_detail.html"
