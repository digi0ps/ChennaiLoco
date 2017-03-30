from django.db import models

# Create your models here.


class Station(models.Model):
	number = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=50)
	majorStation = models.BooleanField(default=0)
	locality = models.CharField(max_length=50)
	pincode = models.IntegerField()

	class meta:
		ordering = ["-number"]

	def __str__(self):
		if self.name:
			return self.name
		else:
			return str(self.number)


class Train(models.Model):
	number = models.IntegerField(unique=True)
	name = models.CharField(max_length=50)
	stations = models.ManyToManyField(
		Station,
		related_name="stations",
		through="Status",
	)

	def __str__(self):
		return str(self.number)


class Status(models.Model):
	train = models.ForeignKey(Train, on_delete=models.CASCADE)
	station = models.ForeignKey(Station, on_delete=models.CASCADE)
	arrival = models.IntegerField()
	departure = models.IntegerField()

	def __str__(self):
		return self.train.name + " at " + self.station.name