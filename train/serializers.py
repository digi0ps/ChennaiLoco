from rest_framework import serializers
from train.models import Train, Station


class TrainSerailizer(serializers.ModelSerializer):
	class Meta:
		model = Train
		fields = ('name', 'number')


class StationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Station
		fields = ('code', 'name')
