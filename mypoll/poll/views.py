from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView

from .models import Choice, Question

class IndexView(ListView):
    """Creata index view."""

    model = Question
    template_name = "poll/index.html"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(DetailView):
    """Create results view."""

    model = Question
    template_name = 'poll/results.html'

def detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if len(question.choice_set.all()) < 2:
        return render(request=request, template_name='poll/detail.html', context=dict(error_message2='You must create minimum two answer.'))
    return render(request=request, template_name='poll/detail.html', context=dict(question=question))

def vote(request, question_id):
    """Create vote view."""

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = dict(question=question, error_message='You did not answer.')
        return render(request=request, template_name='poll/detail.html', context=context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse(viewname='poll:results', args=[question.id]))


