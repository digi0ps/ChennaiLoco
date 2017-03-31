# Reads data from data/*.txt and moves them to data base

# TODO: Define Function for reading with an argument for specifying the model
# TODO: Fetch the model and the text file based on the argument passed
from train.models import Train, Station, Status

EXT = ".txt"
DIR = "train/data/"
COLDIV = ":"
ROWDIV = "\n"
MODELS = ["train", "station", "status"]


def read_data(target):

	# Initalizing files and models
	if target not in MODELS:
		return "Error: Wrong argument."

	filename = DIR + target + EXT
	# Reading the file
	try:
		datafile = open(filename)
	except FileNotFoundError:
		return "Error: File not found."

	dataset = datafile.read()
	datafile.close()
	del datafile
	# Splitting the data by line -> if the element not equal to whitespace -> also stripping white space from strings
	dataset = [d.strip() for d in dataset.split(ROWDIV) if d != "" and d != " "]
	# Delete all existing objects

	# Main magic
	for data in dataset:
		data = data.split(":")
		print(data)
		data[1] = int(data[1])
		if target == "train":
			# [name, number]
			Train.objects.all().delete()
			t = Train()
			t.name, t.number = data
			t.save()
		elif target == "station":
			# [name, code, locality, pincode]
			Station.objects.all().delete()
			s = Station()
			s.name, s.code, s.locality, s.pincode = data
			s.save()
