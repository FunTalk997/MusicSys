from django.db import models


# Create your models here.
class AdminModel(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    addTime = models.DateTimeField()
    loginTime = models.DateTimeField()

    class Meta:
        db_table = 'admin'


class UserModel(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    iconUrl = models.CharField(max_length=255)
    addTime = models.DateTimeField()
    loginTime = models.DateTimeField()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'email': self.email,
            'iconUrl': self.iconUrl,
            'addTime': self.addTime,
            'loginTime': self.loginTime
        }


class MusicModel(models.Model):
    id = models.AutoField(primary_key=True)
    songName = models.CharField(max_length=255)
    singer = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    songTime = models.IntegerField()
    lyric = models.TextField()
    lyricist = models.CharField(max_length=255)
    picUrl = models.CharField(max_length=255)
    songUrl = models.CharField(max_length=255)
    addTime = models.DateTimeField()

    class Meta:
        db_table = 'music'


class CollectModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserModel', on_delete=models.CASCADE)
    music = models.ForeignKey('MusicModel', on_delete=models.CASCADE)
    addTime = models.DateTimeField()

    class Meta:
        db_table = 'collect'


class CommentModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserModel', on_delete=models.CASCADE)
    music = models.ForeignKey('MusicModel', on_delete=models.CASCADE)
    comment = models.TextField()
    addTime = models.DateTimeField()

    class Meta:
        db_table = 'comment'
