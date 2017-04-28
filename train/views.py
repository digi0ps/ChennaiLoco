from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Models Import
from train.models import Train, Station, Route, Review

# REST API Import
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from train.serializers import StationSerializer, TrainSerailizer

# Forms Import
from train.forms import AuthForm, ReviewForm


# Custom Class definition


class result:
	# Train, Route(First station), Route(Second station)
	def __init__(self, train, f, t):
		self.train = train
		self.f = f
		self.t = t


# Custom Functions definition


def check(array, first, second):
	"""
	Checks if two items are present in a list of items one after the other
	"""
	# Position variables for the first item and second item
	f_pos, s_pos = [-1, -1]
	l = len(array)
	for i in range(0, l):
		if array[i] == first:
			f_pos = i
		elif array[i] == second:
			s_pos = i
	# Returns true only if position of second item greater than first item
	# And both are not in their default values
	if s_pos > -1 and f_pos > -1 and s_pos > f_pos:
		return True
	else:
		return False


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
	positive = Review.objects.filter(station=station, category="positive").order_by("-score")
	neutral = Review.objects.filter(station=station, category="neutral").order_by("-score")
	negative = Review.objects.filter(station=station, category="negative").order_by("-score")
	route = Route.objects.select_related('train').filter(station=station)
	return render(request, "station_detail.html", {
		"station": station,
		"trainroutes": route,
		"positives": positive,
		"negatives": negative,
		"neutrals": neutral,
		}
	)


def search_view(request):
	return render(request, "search.html")


def train_search_view(request):
	if request.method == "POST" and request.POST:
		number = int(request.POST["trainnumber"])
		train = get_object_or_404(Train, number=number)
		url = train.get_absolute_url()
		return HttpResponseRedirect(url)
	else:
		return HttpResponseRedirect(reverse("search"))


def station_search_view(request):
	if request.method == "POST" and request.POST:
		name = request.POST["stationname"]
		name = name.replace(" ", "-").lower()
		station = get_object_or_404(Station, slug=name)
		url = station.get_absolute_url()
		return HttpResponseRedirect(url)
	else:
		return HttpResponseRedirect(reverse("search"))


def places_search_view(request):
	if request.method == "POST" and request.POST:
		from_station = request.POST["fromstation"].replace(" ", "-").lower()
		to_station = request.POST["tostation"].replace(" ", "-").lower()
		# get  the two station objects
		f = get_object_or_404(Station, slug=from_station)
		t = get_object_or_404(Station, slug=to_station)

		# Trains list containig result objects
		results = list()
		trains = Train.objects.all().prefetch_related('stations')
		for train in trains:
			stations = train.stations.all()
			check_result = check(stations, f, t)
			if check_result:
				f_route = Route.objects.filter(train=train, station=f).select_related('station')[0]
				t_route = Route.objects.filter(train=train, station=t).select_related('station')[0]
				r = result(train, f_route, t_route)
				results.append(r)
				return render(request, "searchresult.html", {
					"results": results,
					"from": f,
					"to": t,
				})
			else:
				return render(request, "searchresult.html", {
					"noresults": 1,
					"from": f,
					"to": t,
				})
	else:
		return HttpResponseRedirect(reverse("search"))


class train_api(APIView):
	def get(self, request):
		trains = Train.objects.all()
		serializer = TrainSerailizer(trains, many=True)
		return Response(serializer.data)


class station_api(APIView):
	def get(self, request, format="json"):
		stations = Station.objects.all()
		serializer = StationSerializer(stations, many=True)
		return Response(serializer.data)


def auth_view(request):
	if request.user.is_authenticated:
		logout(request)
		return HttpResponseRedirect(reverse('home'))

	if request.method == "POST" and request.POST:
		userdetails = AuthForm(request.POST)
		if userdetails.is_valid():
			cd = userdetails.cleaned_data
			print(cd)
			user = authenticate(username=cd["username"], password=cd["password"])
			if user is not None:
				login(request, user)
				return HttpResponseRedirect(reverse('home'))
			else:
				return render(request, "auth.html", {"form": userdetails, "failed": 1})

	elif request.method == "GET":
		form = AuthForm()
		return render(request, "auth.html", {"form": form})


def register_view(request):
	if request.method == "POST" and request.POST:
		userdetails = AuthForm(request.POST)
		if userdetails.is_valid():
			cd = userdetails.cleaned_data
			user = User.objects.create_user(username=cd["username"], password=cd["password"])
			login(request, user)
			return HttpResponseRedirect(reverse("home"))
		else:
			return render(request, "auth.html", {"form": userdetails, "invalid": 1})


def review_view(request, slug):
	if request.method == "POST" and request.POST:
		review = ReviewForm(request.POST)
		if review.is_valid():
			cd = review.cleaned_data
			station = get_object_or_404(Station, slug=slug)
			r = Review.objects.create(station=station, rating=cd["rating"], feedback=cd["feedback"], user=request.user)
			return HttpResponseRedirect(station.get_absolute_url())
		else:
			return render(request, "station_detail.html", {"station": station, "invalid": 1})
