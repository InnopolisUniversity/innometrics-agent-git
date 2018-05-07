from django.contrib.auth import get_user_model
from rest_framework import serializers
from commit.models import users
from activities.models import Activity, Entity
from measurements.models import Measurement
from measurements.serializers import MeasurementSaveSerializer
from projects.models import UserParticipation


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    githubid = serializers.CharField(write_only=True,required=False)
    bitbucket = serializers.CharField(write_only=True,required=False)
    svn = serializers.CharField(write_only=True,required=False)
    urls = serializers.CharField(write_only=True,required=False)
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'email','githubid','bitbucket','svn','urls')

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        if 'githubid' in validated_data.keys():
            githubid=validated_data['githubid']
            if users.objects.filter(user=user).exists():
                users.objects.filter(user=user).update(githubid=githubid)
            else:
                users(user=user).save()
                users.objects.filter(user=user).update(githubid=githubid)
        if 'bitbucket' in validated_data.keys():
            bitbucket=validated_data['bitbucket']
            if users.objects.filter(user=user).exists():
                users.objects.filter(user=user).update(bitbucket=bitbucket)
            else:
                users(user=user).save()
                users.objects.filter(user=user).update(bitbucket=bitbucket)
        if 'svn' in validated_data.keys():
            svn = validated_data['svn']
            if users.objects.filter(user=user).exists():
                users.objects.filter(user=user).update(svn=svn)
            else:
                users(user=user).save()
                users.objects.filter(user=user).update(svn=svn)
        if 'urls' in validated_data.keys():
            svn = validated_data['svn']
            urls= validated_data['urls']
            if users.objects.filter(user=user).exists():
                users.objects.filter(user=user).update(svn=svn,urls=urls)
            else:
                users(user=user).save()
                users.objects.filter(user=user).update(svn=svn,urls=urls)
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
