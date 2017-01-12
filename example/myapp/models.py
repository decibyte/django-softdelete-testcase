from django.db import models

from softdelete.models import SoftDeleteManager, SoftDeleteObject


class Parent(SoftDeleteObject):
    name = models.CharField(max_length=100)

    objects = SoftDeleteManager()


class Child(SoftDeleteObject):
    parent = models.OneToOneField(Parent)
    name = models.CharField(max_length=100)

    objects = SoftDeleteManager()
