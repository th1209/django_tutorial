from django.contrib import admin

from polls.models import Question
from polls.models import Choice


# 以下は、Choiceクラスを、Questionクラス上の管理ページで編集するための設定。
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


# 以下のように、'(モデル名)Admin'というクラスを定義して、
# registerメソッドの第二引数に渡すと、管理フォーム上での設定を詳細に制御できる。
class QuestionAdmin(admin.ModelAdmin):
    # 以下プロパティで、表示するカラムの種類や順番を制御できる。
    fields = ['question_text', 'pub_date']
    # 詳細にカラムの設定をしたい場合、fieldsプロパティの代わりに、
    # fieldsetsプロパティを使う。
    # fieldsets = [
    #     (None,               {'fields': ['question_text']}),
    #     ('Date information', {'fields': ['pub_date']}),
    # ]
    # プロパティinlinesに、'(モデル名)Inline'クラスを指定すると、
    # 対象の従属モデルを管理ページ上で表示できる。
    inlines = [ChoiceInline]
    # 以下で、表示するカラムを制御する。
    # 特筆すべきは、カスタムメソッドも、まるでカラム(プロパティ)のように表示できること!
    # カスタムメソッドを管理ページ上で表示するためには、別途モデルクラスにプロパティ追加が必要なので、models.pyも要チェック。
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    # 以下のプロパティを設定すると、対象のカラムに関するフィルタを追加できる。
    list_filter = ['pub_date']
    # 以下のプロパティで、対象のカラムで検索ができるようになる。
    # (裏でLIKE句による検索が走るので、パフォーマンスには要注意。)
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
