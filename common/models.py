from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
from costant.constant import CATEGORY

User = get_user_model()


class Province(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return f"id:{self.id}--name:{self.name}"

    class Meta:
        ordering = ["-id"]


class City(models.Model):
    name = models.CharField(max_length=500, unique=True)
    province = models.ForeignKey(Province, related_name="cities", related_query_name="city", on_delete=models.CASCADE)

    def __str__(self):
        return f"id:{self.id}--name:{self.name}"

    class Meta:
        ordering = ["-id"]


class Category(models.Model):
    name = models.CharField(max_length=500, choices=CATEGORY)
    fa_name=models.CharField(max_length=500)

    def __str__(self):
        return f"id:{self.id}--name:{self.name}"

    def save(self,*args,**kwargs):
        self.fa_name=self.get_name_display()
        super(Category, self).save()


    class Meta:
        ordering = ["-id"]



class Skill(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return f"id{self.id}___name:{self.name}"

    class Meta:
        ordering = ["-id"]
