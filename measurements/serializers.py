<<<<<<< HEAD
from rest_framework import serializers

from measurements.models import Measurement

=======
from measurements.models import Measurement

from rest_framework import serializers

>>>>>>> b08e6a3e8b2c2dd9bc6e05534b8e9593d0bb7dab

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('id', 'name', 'value', 'type', 'activity')


class MeasurementSaveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ('name', 'value', 'type')
        model = Measurement
