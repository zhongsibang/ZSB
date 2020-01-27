from django.db import models
# Create your models here.

class User(models.Model):
    class Meta:
    ##在类中定义Meta类来定义table名称
        db_table = 'user'

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=48,null=False)
    mail = models.CharField(max_length=64,null=False,unique=True)
    password = models.CharField(max_length=258,null=False)
    isdelete = models.BooleanField(null=False)

    def __repr__(self):
        return "User {} {}".format(self.id,self.username)

    __str__ =  __repr__