#!/usr/bin/env python
# encoding: utf-8

from django.contrib.auth.models import AbstractUser

from django.db import models

from app.subapps.structure.models import Meter


class User(AbstractUser):
    meter = models.ForeignKey(Meter)
