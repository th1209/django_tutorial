import datetime

from django.utils import timezone
from django.test import TestCase

from polls.models import Question


class QuestionMethodsTests(TestCase):
    def test_was_published_recently_with_old_question(self):
        """昨日より前の日付では、メソッドの実行結果が Falseとなるケース。"""
        time = timezone.now() - datetime.timedelta(days=2)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """最近の日付では、メソッドの実行結果が Trueとなるケース。"""
        time = timezone.now() - datetime.timedelta(hours=23)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)

    def test_was_published_recently_with_future_question(self):
        """未来の日付では、メソッドの実行結果が Falseとなるケース。"""
        time = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
