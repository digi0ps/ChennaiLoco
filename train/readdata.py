# Reads data from data/*.txt and moves them to data base

# TODO: Define Function for reading with an argument for specifying the model
# TODO: Fetch the model and the text file based on the argument passed
from train.models import Train, Station, Route, Location
from ChennaiLoco.secret_settings import API_KEY
import googlemaps
import re

# Constants - if you want to change anything change here

EXT = ".txt"
DIR = "train/data/"
COLDIV = ":"
ROWDIV = "\n"
BLOCKDIV = ";"
MODELS = ["train", "station", "route"]
POSITIVE = ["good", "nice", "beatiful", "amazing", "awesome", "best", "cool", "clean", "neat"]
NEGATIVE = ["bad", "worst", "dirty", "ugly", "unhelpful"]
POINT, THRESHOLD = [2, 3]


def get_data_from_file(name, splitter=ROWDIV):
	"""
	name -> Name of the file
	splitter -> The splitting variable used to split the data
	function -> Return data from the respective file. 
	"""
	filename = DIR + name + EXT

	# Reading the file
	try:
		datafile = open(filename)
	except FileNotFoundError:
		return "Error: File not found."

	dataset = datafile.read()
	datafile.close()
	del datafile

	# Splitting the data by line -> if the element not equal to whitespace -> also stripping white space from strings
	dataset = [d.strip() for d in dataset.split(splitter) if d != "" and d != " "]

	return dataset


def train_data():
	print("Checking whether data file exists and reading from it.")
	dataset = get_data_from_file("train")
	if not dataset:
		return "Error: Null dataset."

	print("Deleting Train Objects.")
	Train.objects.all().delete()

	print("Inserting new data.")

	for data in dataset:
		data = data.split(COLDIV)
		data[1] = int(data[1])
		t = Train()
		t.name, t.number = data
		t.save()
		print("Saved train " + str(t.number))

	print("Insertion done.\nQuiting...")


def station_data():
	print("Checking whether data file exists and reading from it.")
	dataset = get_data_from_file("station")
	if not dataset:
		return "Error: Null dataset."

	print("Deleting Station Objects.")
	Station.objects.all().delete()

	print("Inserting new data.")

	for data in dataset:
		data = data.split(COLDIV)
		s = Station()
		s.name, s.code, s.locality, s.pincode, s.line = data
		s.save()
		print("Saved station " + s.name)

	print("Insertion done.Quiting...")


def route_data():
	dataset = get_data_from_file("route", BLOCKDIV)
	if not dataset:
		return "Errro: Null dataset."

	print("Deleteing Route objects.")
	Route.objects.all().delete()

	print("Inserting new data.")
	for datas in dataset:
		datas = [d for d in datas.split(ROWDIV) if d != "" and d != " "]
		for data in datas:
			if COLDIV not in data:
				"""
				This is the train number, so am getting the train using
				a try except and assigning it to the train variable.
				"""
				try:
					print(data)
					t = Train.objects.get(number=int(data))
				except:
					return "Train does not exist - " + data
			else:
				"""
				This is the station + the time taken to arrive/depart theier
				"""
				data = data.split(COLDIV)
				try:
					print(data[0])
					s = Station.objects.get(code=data[0])
				except:
					return "Station does not exist - " + data[0]
				r = Route()
				r.train = t
				r.station = s
				r.time = data[1][0:2] + ":" + data[1][2:4]
				r.save()
				print("Saved route " + str(r.train.number) + " - " + r.station.code)
	print("Insertion done. Quiting.")


def location_data():
	Location.objects.all().delete()
	maps = googlemaps.Client(key=API_KEY)
	stations = Station.objects.all()
	for station in stations:
		print("Fethcing geocode for " + station.name)
		result = maps.geocode(station.name + " Railway Station")
		if result:
			l = Location()
			l.station = station
			l.lat = result[0]["geometry"]["location"]["lat"]
			l.lng = result[0]["geometry"]["location"]["lng"]
			l.save()
		else:
			print("ERROR: Geocode not found for " + station.name)




def find_category(x, y):
	if x and y:
		return "Mixed"
	elif x and not y:
		return "Positive"
	elif not x and y:
		return "Negative"
	else:
		return "Neutral"


def calc_score(message):
	# Input: The message to be analysed
	# Operations: Calculates the score and finds the category
	# Output: (score, category)
	# Remove all the punctaution characters
	message = re.sub(r'[.!\-@#]', '', message)
	# Lower the message and split it into words
	message = message.lower().split(" ")
	score, pflag, nflag = [0,0,0]
	for word in message:
		if word in POSITIVE:
			score += 2
			pflag = 1
		elif word in NEGATIVE:
			score -= 2
			nflag = 1

	category = find_category(pflag, nflag)
	return (score, category)


def populate_db():
	print("Entering Train data")
	train_data()
	print("Entering Station data")
	station_data()
	print("Entering all route info")
	route_data()
	print("Entering all location info")
	location_data()
	return "Database populated. Quiting."
