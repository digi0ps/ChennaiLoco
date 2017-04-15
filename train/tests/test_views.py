from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from train import views
from train.models import Train


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
		print("test_url_names succeeded")

	def test_url_exists(self):
		self.assertEqual(self.client.get("/").status_code, 200)
		self.assertEqual(self.client.get("/trains/").status_code, 200)
		self.assertEqual(self.client.get("/stations/").status_code, 200)
		self.assertEqual(self.client.get("/search/").status_code, 200)
		print("test_url_exists succeeded")


class TestTrainViews(TestCase):

	@classmethod
	def setUpTestData(cls):
		Train.objects.create(name="MSB1", number=12345)
		Train.objects.create(name="MSB2", number=12346)
		Train.objects.create(name="MSB3", number=12347)

	def test_train_exists(self):
		self.assertEqual(self.client.get("/train/12345/").status_code, 200)
		self.assertEqual(self.client.get("/train/12348/").status_code, 404)
		print("test_train_exists succeeded.")

	def test_train_template(self):
		resp = self.client.get("/train/12345")
		# self.assertTemplateUsed(resp, "train_detail.html")

	def test_train_context(self):
		resp = self.client.get("/train/12345")
		# print(resp.context["train"])