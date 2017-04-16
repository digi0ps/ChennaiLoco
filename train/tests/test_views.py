from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from train.views import check, result
from train.models import Train, Station, Route


class TestUrls(TestCase):

	def test_url_names(self):
		self.assertEqual(reverse("home"), "/")
		self.assertEqual(reverse("trains"), "/trains/")
		self.assertEqual(reverse("stations"), "/stations/")
		self.assertEqual(reverse("search"), "/search/")
		self.assertEqual(reverse("trainsearch"), "/search/train/")
		self.assertEqual(reverse("stationsearch"), "/search/station/")
		self.assertEqual(reverse("placessearch"), "/search/place/")

		self.assertEqual(reverse("train", args=[40001]), "/train/40001/")
		self.assertEqual(reverse("station", args=["mambalam"]), "/station/mambalam/")
		self.assertEqual(reverse("station", args=["chennai-beach"]), "/station/chennai-beach/")
		print("TestUrls.test_url_names succeeded")

	def test_url_exists(self):
		self.assertEqual(self.client.get("/").status_code, 200)
		self.assertEqual(self.client.get("/trains/").status_code, 200)
		self.assertEqual(self.client.get("/stations/").status_code, 200)
		self.assertEqual(self.client.get("/search/").status_code, 200)
		print("TestUrls.test_url_exists succeeded")


class TestTrainViews(TestCase):

	@classmethod
	def setUpTestData(cls):
		Train.objects.create(name="MSB1", number=12345)
		Train.objects.create(name="MSB2", number=12346)
		Train.objects.create(name="MSB3", number=12347)

	def test_train_exists(self):
		self.assertEqual(self.client.get("/train/12345/").status_code, 200)
		self.assertEqual(self.client.get("/train/12348/").status_code, 404)
		print("TestTrainViews.test_train_exists succeeded.")

	def test_train_template(self):
		resp = self.client.get("/train/12345/")
		self.assertTemplateUsed(resp, "train_detail.html")
		print("TestTrainViews.test_train_template succeeded.")

	def test_train_context(self):
		resp = self.client.get("/train/12345/")
		t = resp.context["train"]
		self.assertTrue(isinstance(t, Train))
		self.assertEqual(t.number, 12345)
		print("TestTrainViews.test_train_context succeeded.")


class TestStationViews(TestCase):

	@classmethod
	def setUpTestData(cls):
		Station.objects.create(name="Chennai Beach", code="CB", locality="Sample Locality", pincode="123456", majorStation=1)
		Station.objects.create(name="Chennai Central", code="CC", locality="Sample Locality", pincode="123456", majorStation=1)
		Station.objects.create(name="Mambalam", code="MBM", locality="Sample Locality", pincode="123456", majorStation=0)

	def test_station_exists(self):
		self.assertEqual(self.client.get("/station/chennai-central/").status_code, 200)
		self.assertEqual(self.client.get("/station/Mambalam/").status_code, 404)
		print("TestStationViews.test_station_exists succeeded.")

	def test_station_template(self):
		resp = self.client.get("/station/mambalam/")
		self.assertTemplateUsed(resp, "station_detail.html")

	def test_station_context(self):
		resp = self.client.get("/station/mambalam/")
		s = resp.context["station"]
		self.assertTrue(isinstance(s, Station))
		self.assertEqual(s.slug, "mambalam")
		print("TestTrainViews.test_staion_context succeeded.")


class TestSearchViews(TestCase):

	@classmethod
	def setUpTestData(cls):
		t = Train.objects.create(name="MSB1", number=12345)
		s1 = Station.objects.create(name="Chennai Beach", code="CB", locality="Sample Locality", pincode="123456", majorStation=1)
		s2 = Station.objects.create(name="Mambalam", code="MBM", locality="Sample Locality", pincode="123456", majorStation=0)
		Route.objects.create(train=t, station=s1, time="1030")
		Route.objects.create(train=t, station=s2, time="1130")

	def test_check_function(self):
		array = [x for x in range(1, 11)]
		self.assertTrue(check(array, 3, 8))
		self.assertFalse(check(array, 8, 3))
		print("TestCustomFunctions.test_check_function succeeded.")

	def test_result_class(self):
		r1 = Route.objects.all()[0]
		r2 = Route.objects.all()[1]
		t = Train.objects.first()
		res = result(train=t, f=r1, t=r2)

		self.assertTrue(isinstance(res, result))
		self.assertTrue(isinstance(res.train, Train))
		self.assertTrue(isinstance(res.f, Route))
		self.assertTrue(isinstance(res.t, Route))
		print("TestCustomFunctions.test_result_class succeeded.")

	def test_train_search(self):
		url = reverse("trainsearch")
		# Testing whether "get" redirects
		get = self.client.get(url, follow=True)
		self.assertEqual(get.status_code, 200)
		self.assertEqual(get.request["PATH_INFO"], reverse("search"))

		# Testing for post
		post = self.client.post(url, {"trainnumber": "12345"}, follow=True)
		self.assertEqual(post.request["PATH_INFO"], reverse("train", args=[12345]))
		self.assertEqual(post.status_code, 200)

		falsepost = self.client.post(url, {"trainnumber": "11111"}, follow=True)
		self.assertEqual(falsepost.request["PATH_INFO"], reverse("trainsearch"))
		self.assertEqual(falsepost.status_code, 404)
		print("TestCustomFunctions.test_train_search succeeded.")

	def test_station_search(self):
		url = reverse("stationsearch")
		# Testing whether "get" redirects
		get = self.client.get(url, follow=True)
		self.assertEqual(get.status_code, 200)
		self.assertEqual(get.request["PATH_INFO"], reverse("search"))

		# Testing for post
		post = self.client.post(url, {"stationname": "Mambalam"}, follow=True)
		self.assertEqual(post.request["PATH_INFO"], reverse("station", args=["mambalam"]))
		self.assertEqual(post.status_code, 200)

		post = self.client.post(url, {"stationname": "Chennai Beach"}, follow=True)
		self.assertEqual(post.request["PATH_INFO"], reverse("station", args=["chennai-beach"]))
		self.assertEqual(post.status_code, 200)

		falsepost = self.client.post(url, {"stationname": "stationthatdoesntexist"}, follow=True)
		self.assertEqual(falsepost.request["PATH_INFO"], reverse("stationsearch"))
		self.assertEqual(falsepost.status_code, 404)
		print("TestCustomFunctions.test_station_search succeeded.")

	def test_places_search(self):
		url = reverse("placessearch")
		# Testing whether "get" redirects
		get = self.client.get(url, follow=True)
		self.assertEqual(get.status_code, 200)
		self.assertEqual(get.request["PATH_INFO"], reverse("search"))

		# Testing for post
		post = self.client.post(url, {"fromstation": "Chennai Beach", "tostation": "Mambalam"})
		self.assertEqual(post.status_code, 200)
		self.assertEqual(len(post.context["results"]), 1)
		self.assertTrue(isinstance(post.context["from"], Station))
		self.assertTrue(isinstance(post.context["to"], Station))
		self.assertTemplateUsed(post, "searchresult.html")

		post = self.client.post(url, {"fromstation": "Chennai Beach", "tostation": "Chennai Beach"}, follow=True)
		self.assertEqual(post.status_code, 200)
		self.assertTrue(post.context["noresults"])

		falsepost = self.client.post(url, {"fromstation": "doesnt", "tostation": "exist"}, follow=True)
		self.assertEqual(falsepost.status_code, 404)
		print("TestCustomFunctions.test_places_search succeeded.")