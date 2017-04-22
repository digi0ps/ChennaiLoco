from django.test import TestCase
from train.models import Train, Route, Station
TRAIN_FIELDS = ['route', 'number', 'name', 'stations']
STATION_FIELDS = ['stations', 'route', 'review', 'location', 'code', 'name', 'locality', 'pincode', 'line', 'majorStation', 'slug']
ROUTE_FIELDS = ['id', 'train', 'station', 'time']


class TestModelCreation(TestCase):

	def test_create_train(self):
		t = Train.objects.create(number=40001, name="MSB")
		self.assertTrue(isinstance(t, Train))
		print("TestModelCreation.test_create_train succeeded.")

	def test_create_station(self):
		s = Station.objects.create(name="Sample Station", code="SXS", locality="Sample Place", pincode="123456", majorStation=1)
		self.assertTrue(isinstance(s, Station))
		print("TestModelCreation.test_create_station succeeded.")

	def test_create_route(self):
		t = Train.objects.create(number=40001, name="MSB")
		s1 = Station.objects.create(name="Mambalam", code="MBM", locality="Mambalam", pincode=600098, majorStation=1)
		s2 = Station.objects.create(name="Ashok Pillar", code="ASK", locality="Ashok Pillar", pincode=600097, majorStation=1)
		r = Route.objects.create(train=t, station=s1, time="1010")
		self.assertTrue(isinstance(r, Route))
		print("TestModelCreation.test_create_route succeeded.")


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
		Station.objects.create(name="Sample Station", code="SXS", locality="Sample Place", pincode="123456", majorStation=1)

	def test_field_names(self):
		fields = Station._meta.get_fields()
		field_names = [f.name for f in fields]
		print(field_names)
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


class TestRouteModel(TestCase):
	@classmethod
	def setUpTestData(cls):
		t = Train.objects.create(number=40001, name="MSB")
		s1 = Station.objects.create(name="Mambalam", code="MBM", locality="Mambalam", pincode=600098, majorStation=1)
		s2 = Station.objects.create(name="Ashok Pillar", code="ASK", locality="Ashok Pillar", pincode=600097, majorStation=1)
		Route.objects.create(train=t, station=s1, time="1010")
		Route.objects.create(train=t, station=s2, time="1020")

	def test_field_names(self):
		fields = Route._meta.get_fields()
		field_names = [f.name for f in fields]
		self.assertEqual(field_names, ROUTE_FIELDS)
		print("TestRouteModel.test_field_names succeeded.")

	def test_str_name(self):
		route = Route.objects.first()
		expected_str = "%s at %s" % ("MSB", "Mambalam")
		self.assertEqual(str(route), expected_str)
		print("TestRouteModel.test_str_name succeeded.")

	def test_station_cascade(self):
		s1 = Station.objects.all()[0]
		self.assertTrue(Route.objects.filter(station=s1).exists())
		s1.delete()
		self.assertFalse(Route.objects.filter(station=s1).exists())
		self.assertEqual(Route.objects.count(), 1)
		print("TestRouteModel.test_station_cascade succeeded.")

	def test_train_cascade(self):
		t = Train.objects.first()
		self.assertTrue(Route.objects.filter(train=t).exists())
		t.delete()
		self.assertFalse(Route.objects.filter(train=t).exists())
		self.assertEqual(Route.objects.count(), 0)
		print("TestRouteModel.test_train_cascade succeeded.")
