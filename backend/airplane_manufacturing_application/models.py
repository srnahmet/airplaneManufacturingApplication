from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now



# Uçak Modeli: Uçak tipi
class AirplaneType(models.Model):
    name = models.CharField(max_length=50,default=None)

    def __str__(self):
        return self.name
    
# Uçak Modeli
class Airplane(models.Model):
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE, related_name="airplane_types", default=None)
    create_date = models.DateTimeField(default=now, verbose_name="Oluşturulma Tarihi")

    def __str__(self):
        return self.name

# PartType Modeli: Parça türü
class PartType(models.Model):
    name = models.CharField(max_length=50,default=None)

    def __str__(self):
        return self.name

# Part Modeli
class Part(models.Model):
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE,default=None)  # Parçanın ait olduğu uçak tipi
    part_type = models.ForeignKey(PartType, on_delete=models.CASCADE,default=None)  # Parçanın türü 
    create_date = models.DateTimeField(default=now) # Parça oluşturma tarihi
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE,null=True,default=None)  # Part yalnızca bir Airplane ile ilişkili

    def __str__(self):
        return f"{self.part_type.name} - {self.airplane_type.name}"

# Team Modeli
class Team(models.Model):
    name = models.CharField(max_length=100,default=None)
    is_assembly_team = models.BooleanField(default=False) # Takım montaj takımı mı?
    part_type = models.ForeignKey(PartType, on_delete=models.CASCADE, null=True, blank=True)  # Her takım yalnızca belirli bir türde parça üretir, montaj takımı için belirtilmez

    def __str__(self):
        return self.name
    
    @property
    def employee_count(self):
        return self.employee.count()

# Employee Modeli
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='employee', null=True) # Her çalışan bir takıma atanabilir

    def __str__(self):
        return self.name
