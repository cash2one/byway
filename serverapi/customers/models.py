# -*- coding: utf-8 -*-

from django.utils import timezone
from django.db import models
from django.forms.models import model_to_dict
from django.contrib.auth.models import User

from util.response_util import *


ISOTIMEFORMAT = '%Y-%m-%d %X'

HTTP_SCHEMA = 'http://'
HOST_URL = 'api.byway.net.cn'
API_VERSION = 'v1'


# Create your models here.
class Customer(models.Model):
	mail = models.CharField(max_length=40)
	phone = models.CharField(max_length=20)
	name = models.CharField(max_length=50)
	icon = models.CharField(default='/media/usericon/default.jpg', max_length=100)
	password = models.CharField(max_length=50)
	score = models.IntegerField(default=0)
	token = models.CharField(max_length=255, null=True)
	status = models.IntegerField(default=0)

	def signup_customer(self):
		customer_by_mail = self.get_customer_by_mail()
		customer_by_phone = self.get_customer_by_phone()
		if customer_by_mail is None and customer_by_phone is None:
			self.save()
			# 检查是否和auth_user冲突
			if not User.objects.filter(id=self.id):
				return True
			else:
				self.delete()
				return False
		else:
			return False

	def get_customer_by_mail(self):
		try:
			customer = Customer.objects.get(mail=self.mail)
		except Exception, e:
			return None
		else:
			return customer

	def get_customer_by_phone(self):
		try:
			customer = Customer.objects.get(phone=self.phone)
		except Exception, e:
			return None
		else:
			return customer

	def to_dict(self):
		customer_dict = dict()
		customer_dict['name'] = self.name
		customer_dict['mail'] = self.mail
		customer_dict['phone'] = self.phone
		customer_dict['icon'] = BASE_SCHEMES + API_BASE + self.icon
		customer_dict['score'] = self.score
		customer_dict['token'] = self.token
		customer_dict['status'] = self.status
		return customer_dict


class Ship(models.Model):
	customer_id = models.ForeignKey(Customer)
	receiver_name = models.CharField(max_length=50)
	phone = models.CharField(max_length=20)
	dormitory_no = models.IntegerField(default=0)
	room_no = models.IntegerField(default=0)
	address = models.CharField(max_length=255, default='')

	def to_dict(self):
		ship_dict = model_to_dict(self)
		return ship_dict