from django.test import TestCase

# Models test

from train.models import Train, Route, Station
TRAIN_FIELDS = ['route', 'number', 'name', 'stations']
STATION_FIELDS = ['stations', 'route', 'code', 'name', 'locality', 'pincode', 'line', 'majorStation', 'slug']


class TestTrainModel(TestCase):
	@classmethod
	def setUpTestData(cls):
		Train.objects.create(number=40001, name="MSB")

	def test_field_names(self):
		fields = Train._meta.get_fields()
		field_names = [f.name for f in fields]
		self.assertEqual(field_names, TRAIN_FIELDS)
		print("TestTrainModel.test_field_names succeeded.")

	def test_str_name(self):
		train = Train.objects.first()
		self.assertEqual(str(train), str(train.number))
		print("TestTrainModel.test_str_name succeeded.")

	def test_absolute_url(self):
		train = Train.objects.first()
		abs_url = train.get_absolute_url()
		self.assertEqual(abs_url, "/train/" + str(train.number) + "/")
		print("TestTrainModel.test_absolute_url succeeded.")

	def test_attribute_type(self):
		train = Train.objects.first()
		self.assertEqual(type(train.number), int)
		self.assertEqual(type(train.name), str)
		print("TestTrainModel.test_attribute_type succeeded.")


class TestStationModel(TestCase):
	@classmethod
	def setUpTestData(cls):
		Station.objects.create(name="Sample Station", code="SXS", locality="Sample Place", pincode=123456, majorStation=1)

	def test_field_names(self):
		fields = Station._meta.get_fields()
		field_names = [f.name for f in fields]
		self.assertEqual(field_names, STATION_FIELDS)
		print("TestStationModel.test_field_names succeeded.")

	def test_str_name(self):
		station = Station.objects.first()
		self.assertEqual(str(station), station.name)
		print("TestStationModel.test_str_name succeeded.")

	def test_slug_field(self):
		station = Station.objects.first()
		slug = station.name.lower().replace(" ", "-")
		self.assertEqual(station.slug, slug)
		print("TestStationModel.test_slug_field succeeded.")

	def test_absolute_url(self):
		station = Station.objects.first()
		abs_url = station.get_absolute_url()
		self.assertEqual(abs_url, "/station/" + station.slug + "/")
		print("TestStationModel.test_absolute_url succeeded.")

	def test_attribute_type(self):
		station = Station.objects.first()
		self.assertEqual(type(station.code), str)
		self.assertEqual(type(station.name), str)
		self.assertEqual(type(station.locality), str)
		self.assertEqual(type(station.pincode), str)
		self.assertEqual(type(station.majorStation), bool)
		print("TestStationModel.test_attribute_type succeeded.")
