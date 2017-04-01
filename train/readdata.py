# Reads data from data/*.txt and moves them to data base

# TODO: Define Function for reading with an argument for specifying the model
# TODO: Fetch the model and the text file based on the argument passed
from train.models import Train, Station, Status

EXT = ".txt"
DIR = "train/data/"
COLDIV = ":"
ROWDIV = "\n"
MODELS = ["train", "station", "status"]


def get_data_from_file(name):
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
	dataset = [d.strip() for d in dataset.split(ROWDIV) if d != "" and d != " "]

	return dataset


def train_data():
	print("\tChecking whether data file exists and reading from it.")
	dataset = get_data_from_file("train")
	if not dataset:
		return "Error: Null dataset."

	print("\tDeleting Train Objects.")
	Train.objects.all().delete()

	print("\tInserting new data.")

	for data in dataset:
		data = data.split(":")
		data[1] = int(data[1])
		t = Train()
		t.name, t.number = data
		t.save()
		print("\nSaved train " + str(t.number))

	print("\tInsertion done.\n\tQuiting...")


def station_data():
	print("\tChecking whether data file exists and reading from it.")
	dataset = get_data_from_file("station")
	if not dataset:
		return "Error: Null dataset."

	print("\tDeleting Station Objects.")
	Station.objects.all().delete()

	print("\tInserting new data.")

	for data in dataset:
		data = data.split(":")
		data[1] = int(data[1])
		s = Station()
		s.name, s.code, s.locality, s.pincode = data
		s.save()
		print("\nSaved station " + s.name)

	print("\tInsertion done.\tQuiting...")