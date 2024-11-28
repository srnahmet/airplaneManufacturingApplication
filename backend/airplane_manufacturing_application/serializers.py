from rest_framework import serializers
from .models import Airplane, Part, Team, Employee, AirplaneType, PartType

class DatatableParamsSerializer(serializers.Serializer):
    start = serializers.IntegerField(default=0)
    length = serializers.IntegerField(default=10)
    search_value = serializers.CharField(default='', required=False)
    order_column = serializers.CharField(default='id')
    order_dir = serializers.ChoiceField(choices=['asc', 'desc'], default='asc')


class PartTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartType
        fields = ['id', 'name']

class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ['id', 'name']

class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type = AirplaneTypeSerializer()
    class Meta:
        model = Airplane
        fields = ['id', 'create_date', 'airplane_type']

class PartSerializer(serializers.ModelSerializer):
    airplane_type_name = AirplaneTypeSerializer(source='airplane_type', read_only=True)
    part_type_name = PartTypeSerializer(source='part_type', read_only=True)
    airplane_name = AirplaneSerializer(source='airplane', read_only=True)

    class Meta:
        model = Part
        fields = ['id', 'airplane_type', 'airplane_type_name', 'part_type', 'part_type_name', 'airplane', 'airplane_name', 'create_date']

class TeamSerializer(serializers.ModelSerializer):
    part_type_name = PartTypeSerializer(source='part_type', read_only=True)
    # employee_count = serializers.IntegerField(source='total_employees', read_only=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'part_type', 'part_type_name', 'employee_count']

class EmployeeSerializer(serializers.ModelSerializer):
    team_name = TeamSerializer(source='team', read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'name', 'team', 'team_name']
