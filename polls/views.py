from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from polls.models import Question
from polls.models import Choice


def index(request):
    """全てのQuestionモデルの一覧。"""
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    """特定Questionの詳細。"""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


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


def results(request, question_id):
    """投票結果。"""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
