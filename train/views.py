from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect

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


def search_view(request):
	return render(request, "search.html")


def train_search_view(request):
	if request.method == "POST" and request.POST:
		number = int(request.POST["trainnumber"])
		train = get_object_or_404(Train, number=number)
		url = train.get_absolute_url()
		return HttpResponseRedirect(url)


def station_search_view(request):
	if request.method == "POST" and request.POST:
		name = request.POST["stationname"]
		name = name.replace(" ", "-").lower()
		print(name)
		station = get_object_or_404(Station, slug=name)
		url = station.get_absolute_url()
		return HttpResponseRedirect(url)


def check_two_stations(array, first, second):
	"""
	Checks if two items are present in a list of items one after the other
	"""
	# l Position variables for the first item and second item
	f_pos, s_pos = -1
	for i in range(0, l):
		if array[i] == f:
			f_pos = i
		elif array[i] == s:
			s_pos = i
	# Returns true only if position of second item greater than first item
	# And both are not in their default values
	if s_pos > -1 and f_pos > -1 and s_pos > f_pos:
		return True
	else:
		return Flase


def places_search_view(request):
	if request.method == "POST" and request.POST:
		from_station = request.POST["fromstation"].replace(" ", "-").lower()
		to_staiton = request.POST["tostation"].replace(" ", "-").lower()
		# get  the two station objects
		f = get_object_or_404(Station, slug=from_station)
		t = get_object_or_404(Station, slug=to_station)

		trains = Trains.objects.all().select_related('stations')
		for train in trains:
			stations = train.stations.all()
			check = check_two_stations(stations, f, t)
			print(check)
