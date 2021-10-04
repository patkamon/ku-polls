"""Views of different kind of pages."""
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from .models import Choice, Question
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages


# Create your views here.
def index(request):
    """Contain list of polls."""
    latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[::-1]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    """Show detail of polls, handle when polls not able to vote."""
    question = get_object_or_404(Question, pk=question_id)
    if question.can_vote():
        return render(request, 'polls/detail.html', {'question': question})
    messages.error(request, "You try to access poll that does not allow")
    return HttpResponseRedirect(reverse('polls:index'))


def results(request, question_id):
    """Show the results of polls."""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    """Make choice be able to vote."""
    # run this get_object_or_404 if fail return 404 page
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def resultData(request, obj):
    """To return the data of that polls question."""
    votedata = []

    question = Question.objects.get(id=obj)
    votes = question.choice_set.all()

    for i in votes:
        votedata.append({i.choice_text: i.votes})
    print(votedata)
    return JsonResponse(votedata, safe=False)
