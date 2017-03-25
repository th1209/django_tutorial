from django.conf.urls import url
from polls import views


# アプリ名。複数アプリを区別する場合は必須。
# 単一アプリしか使わない場合でも、付けておいたほうが無難だろう。
app_name = 'polls'
urlpatterns = [
    # 以下は、汎用ビューを使う場合のURL対応表。
    # 以下のポイントに注目。
    # * 汎用ビューでDBモデルを引く場合、必ず?P<pk>という名前付きパターンを使うこと。
    # * 対応するビューの関数名は、'(クラス名.as_view())'で指定。
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),

    # * 以下コメントアウトは、汎用ビューを使う以前のurl対応表。
    # * 正規表現上の()で括った箇所はキャプチャされ、viewsのメソッドに引数として渡される。
    #   また、?P<question_id>の部分が特異かと思うが、これはdjangoの名前付きパターンと呼ばれるものである(以下に構文を示す)。
    #   (?P<name>pattern)
    # url(r'^$', views.index, name='index'),
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]