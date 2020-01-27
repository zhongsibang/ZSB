from django.db import models
from user.models import User
# Create your models here.

class Post(models.Model):
    class META:
        db_table = 'post'

    id = models.AutoField(primary_key=True)
    posttitle = models.CharField(max_length=200,null=False)
    postdate = models.DateTimeField(null=False)
    #作者外键
    postauthor = models.ForeignKey(User,on_delete=models.CASCADE) #字段名？

    def __repr__(self):
        return "<<<Post {} {} {}".format(self.id,self.posttitle,self.postauthor)

    __str__ = __repr__

class Content(models.Model):
    class META:
        db_table = 'content'
    post = models.OneToOneField(Post,on_delete=models.CASCADE)  #一对一外键
    content = models.TextField(null=False)

    def __repr__(self):
        return "<<<Content {} {} {} ".format(self.pk,self.post.id,self.content[:20])

    __str__ =__repr__
