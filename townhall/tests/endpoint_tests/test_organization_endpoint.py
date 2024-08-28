import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from myapi import models as townhall_models
from datetime import datetime
from django.utils import timezone

