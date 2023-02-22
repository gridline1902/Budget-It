from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todolist", null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
        

class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    amount = models.FloatField(blank=True, null=True)
    needs = models.FloatField(blank=True, null=True)
    wants = models.FloatField(blank=True, null=True)
    savings = models.FloatField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.amount} {self.needs} {self.wants} {self.savings}"
