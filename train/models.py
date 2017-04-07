from django.db import models
from django.template.defaultfilters import slugify
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
		else:
			return str(self.number)

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


class Route(models.Model):
	train = models.ForeignKey(Train, on_delete=models.CASCADE)
	station = models.ForeignKey(Station, on_delete=models.CASCADE)
	arrival = models.IntegerField()
	departure = models.IntegerField()

	def __str__(self):
		return self.train.name + " at " + self.station.name