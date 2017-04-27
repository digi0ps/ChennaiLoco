from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# Create your models here.


class Station(models.Model):
	code = models.CharField(max_length=10, primary_key=True)
	name = models.CharField(max_length=50, unique=True)
	locality = models.CharField(max_length=50)
	pincode = models.CharField(max_length=6)
	line = models.CharField(max_length=10)
	majorStation = models.BooleanField(default=0)
	slug = models.SlugField(max_length=50, unique=True, null=True)

	class meta:
		ordering = ["-number"]

	def __str__(self):
		if self.name:
			return self.name

	def get_absolute_url(self):
		return "/station/%s/" % self.slug

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Station, self).save(*args, **kwargs)


class Train(models.Model):
	number = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=50)
	stations = models.ManyToManyField(
		Station,
		related_name="stations",
		through="Route",
	)

	def __str__(self):
		return str(self.number)

	def get_absolute_url(self):
		return "/train/%i/" % self.number


class Route(models.Model):
	train = models.ForeignKey(Train, on_delete=models.CASCADE)
	station = models.ForeignKey(Station, on_delete=models.CASCADE)
	time = models.CharField(max_length=5)

	def __str__(self):
		return self.train.name + " at " + self.station.name

d = User.objects.get(username="digi")


class Review(models.Model):
	station = models.ForeignKey(Station, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE, default=d)
	rating = models.IntegerField()
	feedback = models.CharField(max_length=500)
	score = models.IntegerField(blank=True)
	category = models.CharField(max_length=10, blank=True)

	def __str__(self):
		return self.station.name + ": " + self.feedback[:30]


class Location(models.Model):
	station = models.ForeignKey(Station, on_delete=models.CASCADE)
	lat = models.DecimalField(max_digits=10, decimal_places=7)
	lng = models.DecimalField(max_digits=10, decimal_places=7)

	def __str__(self):
		return self.station.name