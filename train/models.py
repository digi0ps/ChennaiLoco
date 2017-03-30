from django.db import models

# Create your models here.


class Station(models.Model):
	number = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=50, unique=True)
	majorStation = models.BooleanField(default=0)
	locality = models.CharField(max_length=50)
	pincode = models.IntegerField()

	def __str__(self):
		return name


class Train(models.Model):
	number = models.CharField(max_length=50)
	name = models.IntegerField(primary_key=True)
	avgTime = models.DecimalField(max_digits=5, decimal_places=2)
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
