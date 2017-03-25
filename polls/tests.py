import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from polls.models import Question


class QuestionMethodsTests(TestCase):
    """DBモデルクラスに対する、簡単なテスト例。"""
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


def create_question(question_text, days):
    """テスト用のDBモデル ファクトリメソッド。"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(
        question_text=question_text,
        pub_date=time
    )


class QuestionViewTests(TestCase):
    """ビューに対する、簡単なテスト例。"""
    def test_index_view_with_no_questions(self):
        """indexに対する、モデルを0件取得するケースのテスト。"""
        # ビューのテストでは、Clientクラスを使う。
        # また、reverseメソッドを使うことで、viewの関数名の変更に強いテストになっていることにも注目。
        response = self.client.get(reverse('polls:index'))
        # 若干トリッキーだが、assertContainsメソッドで、レスポンスで返る値や、そのステータスコードをチェックできる。
        # 詳しくは、以下URLを参照すること。
        # https://docs.djangoproject.com/en/1.10/topics/testing/tools/
        self.assertContains(response, "No polls are available.", status_code=200)

    def test_index_view_with_questions(self):
        """indexに対する、複数モデルを取得するケースのテスト。"""
        create_question(question_text="1day ago question.", days=-1)
        create_question(question_text="2days ago question.", days=-2)
        create_question(question_text="Today question.", days=0)
        create_question(question_text="Tomorrow question.", days=1)

        response = self.client.get(reverse('polls:index'))
        # モデルは日付の降順で取れるし、明日以降のインスタンスは含まれない
        # (assertQuerySetEqualで、DBモデルのリストのチェックができる。__str__メソッドを定義しておけば、文字列形式でテストができる点にも注目。)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Today question.>', '<Question: 1day ago question.>', '<Question: 2days ago question.>', ]
        )

    def test_detail_view_with_today_question(self):
        """detailに対する、本日のモデルケースを取得しようとする処理のテスト。"""
        question = create_question(question_text="Today question.", days=0)
        response = self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertContains(response, question.question_text, status_code=200)

    def test_detail_view_with_future_question(self):
        """detailに対する、未来のモデルケースを取得しようとする処理のテスト。"""
        question = create_question(question_text="Tomorrow question.", days=1)
        response = self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertEqual(response.status_code, 404)