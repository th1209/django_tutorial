import datetime

from django.utils import timezone
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """インスタンスが昨日〜今日の間に作られたものなら、Trueを返す。"""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # 以下のプロパティは、管理サイト上でwas_published_recentlyメソッドを管理サイト上でカラムとして扱うための設定。
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    # was_published_recently.short_description = 'Published'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
