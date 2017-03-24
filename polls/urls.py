from django.conf.urls import url
from polls import views

app_name = 'polls'
urlpatterns = [
    # 正規表現上の()で括った箇所はキャプチャされ、viewsのメソッドに引数として渡される。
    # また、?P<question_id>の部分が特異かと思うが、これはdjangoの名前付きパターンと呼ばれるものである(以下に構文を示す)。
    # (?P<name>pattern)
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]