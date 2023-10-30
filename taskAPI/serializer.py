from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):
    unit = serializers.CharField(max_length=255)
    villa_count = serializers.IntegerField()

    class Meta:
        model = Project
        fields = ['unit', 'villa_count']


class AllSerializer(serializers.Serializer):
    unit = serializers.CharField(max_length=255)
    utype = serializers.CharField(max_length=255)
    unit_type_count = serializers.IntegerField()

    class Meta:
        model = Project
        fields = ['unit', 'unit_type_count']


class SearchSerializer(serializers.Serializer):
    unit = serializers.CharField(max_length=255)
    utype = serializers.CharField(max_length=255)
    beds = serializers.IntegerField()
    area = serializers.FloatField()
    price = serializers.IntegerField()
    date = serializers.DateField()

    class Meta:
        model = Project
        fields = ['unit', 'utype', 'beds', 'area', 'price', 'date']
