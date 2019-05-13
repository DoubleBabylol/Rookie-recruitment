from django.db import models
class jobinfo(models.Model):
	jobname = models.CharField(max_length=200)
	company = models.CharField(max_length=200)
	url = models.CharField(max_length=400)
	location = models.CharField(max_length=200)
	salary = models.CharField(max_length=200)

	def __str__(self):
		return "{}-{}".format(self.jobname, self.company)
 