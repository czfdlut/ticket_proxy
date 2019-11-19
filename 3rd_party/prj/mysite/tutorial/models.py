from django.db import models

# Create your models here.
class OrderTicket(models.Model):
    uid = models.CharField(max_length=128)
    merchantCode = models.CharField(max_length=128)
    merchantName = models.CharField(max_length=128)
    bizNo = models.CharField(max_length=128)
    bizName = models.CharField(max_length=128)
    bizBrief = models.CharField(max_length=255)
    bizTime = models.CharField(max_length=128)
    orderDate = models.CharField(max_length=128)
    orderNo = models.CharField(max_length=128)
    ticketPrices = models.CharField(max_length=128)
    payType = models.CharField(max_length=128)
    mobile = models.CharField(max_length=128)
    requestID = models.CharField(max_length=128)
    orderTicketFlow = models.CharField(max_length=128)
    updateTime = models.CharField(max_length=128)
    status = models.CharField(max_length=128)
    errmsg = models.CharField(max_length=128)
