from django.contrib.auth import get_user_model
from rest_framework import serializers

from activities.models import Activity, Entity,users
from measurements.models import Measurement
from measurements.serializers import MeasurementSaveSerializer
from projects.models import UserParticipation


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = users
        fields = ('id', 'username', 'password', 'email','githubid','bitbucket','svn','urls')

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            githubid=validated_data['githubid'],
            bitbucket=validated_data['bitbucket'],
            svn=validated_data['svn'],
            urls=validated_data['urls']
        )
        user.set_password(validated_data['password'])
        user.save()
        participation, created = UserParticipation.objects.get_or_create(user=user, project=None)
        participation.save()
        return user


class ActivitySerializer(serializers.ModelSerializer):
    measurements = MeasurementSaveSerializer(many=True)

    class Meta:
        model = Activity
        fields = ('id', 'comments', 'measurements', 'participation', 'entity')

    def create(self, validated_data):
        measurements_data = validated_data.pop('measurements')
        activity = Activity.objects.create(**validated_data)
        for measurement_data in measurements_data:
            max_length = Measurement._meta.get_field('value').max_length
            measurement_data['value'] = measurement_data['value'][:max_length]
            Measurement.objects.create(activity=activity, **measurement_data)
        return activity


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ('id', 'name', 'group')

    def create(self, validated_data):
        activity = Activity.objects.create(**validated_data)
        return activity
