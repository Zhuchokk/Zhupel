from django.db import models
from django.utils import timezone
import json
from random import choice


class Article(models.Model):
    header = models.CharField(max_length=256)
    text = models.TextField()
    pub_date = models.DateField()
    comment_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    themes = models.CharField(max_length=256, default='["без темы"]')
    secret_key = models.CharField(max_length=32, default="none")

    def __str__(self):
        return self.header[:25]

    def set_themes(self, x):
        self.themes = json.dumps(x)

    def get_themes(self):
        return json.loads(self.themes)

    @staticmethod
    def new_key():
        dictionary = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_!@'
        key = ''
        for _ in range(32):
            key += choice(dictionary)
        return key


class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=80, default="noname")
    email = models.EmailField(default="no email")
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now())
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.article)