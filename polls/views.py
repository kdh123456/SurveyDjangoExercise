from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404

from .models import Question, Choice
from django.views import generic

'''def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')  # 템플릿 불러오기
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context) # 내용과 템플릿 한꺼 번에 넘겨주기


def detail(request, question_id):
    #try:
       # question= Question.objects.order_by(pk=question_id)
   # except Question.DoesNotExist:
       # raise Http404("Question does not exist!!!")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question}) # 내용과 템플릿 한꺼 번에 넘겨주기


def results(request, question_id):
    question = get_object_or_404(Question, pk= question_id)
    return render(request, 'polls/results.html', {'question': question})'''


def votes(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html',{
            'question' : question,
            'error_message':"You didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions!"""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'