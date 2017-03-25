from django.shortcuts import get_object_or_404
from django.shortcuts import render
# from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
# from django.template import loader
from django.views import generic
from polls.models import Question
from polls.models import Choice


# 以下のいくつかのクラスは、汎用ビューと呼ばれる、よく使われる処理をクラス化したもの。
# 使いこなすにはもう少し勉強が必要そうなので、要調査。以下のQiitaの記事が導入に易しそう。
# [Djangoにおけるクラスベース汎用ビューの入門と使い方サンプル](http://qiita.com/felyce/items/7d0187485cad4418c073)

# 以下はListViewを継承した汎用ビュー。
# ListViewは、あるオブジェクトの一覧を表示するという汎用的な役割を持つ。
class IndexView(generic.ListView):
    # 汎用ビューでは、ビューがどのDBモデルを扱うのか知る必要がある。
    # 汎用ビューにこれを教えるには、以下のmodelプロパティを定義することで行う。
    #model = Question
    # 汎用ビューでは、決められたテンプレート名を使う。
    # ListViewの場合は、'(app name)/(model name)_list.html'という形式。
    # 以下のtemplate_nameプロパティを定義すると、代わりにプロパティで指定したテンプレートを作ってくれる。
    template_name = 'polls/index.html'
    # ListViewでは、'(model name)_list'という名称のオブジェクト配列変数が自動的に生成される。
    # 以下ではその変数名を上書いている。
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """このメソッドをオーバーライドすることで、
        取得するDBモデルリストの結果を上書きできる。
        """
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    # DetailViewの場合は、'(app name)/(model name)_detail.html'という形式のテンプレートを使う。
    # ここでも、template_nameプロパティを定義することで、挙動を上書いている。
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# 以下コメントアウトは、汎用ビューを定義する前のビュー関数。

# def index(request):
#     """全てのQuestionモデルの一覧。"""
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))


# def detail(request, question_id):
#     """特定Questionの詳細。"""
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})


# def results(request, question_id):
#     """投票結果。"""
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    """投票時の処理。投票数の加算処理、必要なViewへの転送を行う。"""
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POSTでPOSTの値を取れる(必ず文字列なので注意)。
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # POST下データなので、リダイレクトする
        # また、以下のreverse関数はURLの逆引きと呼ばれるもので、URLに付けた名称から、対応するviewのメソッドを呼び出す際に使う。
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
