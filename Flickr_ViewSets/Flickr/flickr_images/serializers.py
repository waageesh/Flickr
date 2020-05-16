from .models import *
from rest_framework import serializers

class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = UploadImages
		fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):
	class Meta:
		model = UploadImages
		fields = '__all__'