from django.shortcuts import render, get_object_or_404
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


def train_view(request, pk):
	train = get_object_or_404(Train, pk=pk)
	route = Route.objects.select_related('station').filter(train=train)
	return render(request, "train_detail.html", {"train": train, "route": route})


def station_view(request, slug):
	station = get_object_or_404(Station, slug=slug)
	route = Route.objects.select_related('train').filter(station=station)
	return render(request, "station_detail.html", {"station": station, "trainroutes": route})
