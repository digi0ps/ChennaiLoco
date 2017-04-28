from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import re
# Create your models here.
POSITIVE = ["good", "nice", "beatiful", "amazing", "awesome", "best", "cool", "clean", "neat"]
NEGATIVE = ["bad", "worst", "dirty", "ugly", "unhelpful"]
POINT, THRESHOLD = [2, 3]


def find_category(x, y):
	if x and y:
		return "Mixed"
	elif x and not y:
		return "positive"
	elif not x and y:
		return "negative"
	else:
		return "neutral"


def calc_score(message, rating):
	# Input: The message to be analysed
	# Operations: Calculates the score and finds the category
	# Output: (score, category)
	# Remove all the punctaution characters
	message = re.sub(r'[.!\-@#]', '', message)
	# Lower the message and split it into words
	message = message.lower().split(" ")
	score, pflag, nflag = [0, 0, 0]
	for word in message:
		if word in POSITIVE:
			score += 2
			pflag = 1
		elif word in NEGATIVE:
			score -= 2
			nflag = 1

	category = find_category(pflag, nflag)
	score = score * rating
	return (score, category)


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


class Review(models.Model):
	station = models.ForeignKey(Station, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	rating = models.IntegerField()
	feedback = models.CharField(max_length=500)
	score = models.IntegerField(default=0, blank=True)
	category = models.CharField(max_length=10, blank=True)

	def __str__(self):
		return self.station.name + ": " + self.feedback[:30]

	def save(self, *args, **kwargs):
		tup = calc_score(self.feedback, self.rating)
		self.score = tup[0]
		self.category = tup[1]
		print(tup)
		super(Review, self).save(*args, **kwargs)


class Location(models.Model):
	station = models.ForeignKey(Station, on_delete=models.CASCADE)
	lat = models.DecimalField(max_digits=10, decimal_places=7)
	lng = models.DecimalField(max_digits=10, decimal_places=7)

	def __str__(self):
		return self.station.name