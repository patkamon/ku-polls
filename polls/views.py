"""Views of different kind of pages."""
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from .models import Choice, Question, Vote
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

logger = logging.getLogger('polls')


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    # to cover more complex cases:
    # http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
    ip = request.META.get('REMOTE_ADDR')
    logger.info(f"{user} logged in from {ip}")

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    logger.info(f'logout user: {user} via ip: {ip}')

@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, request, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    logger.warning(f"Invalid login attempt for {credentials} from {ip}")



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

@login_required(login_url='/accounts/login/')
def vote(request, question_id):
    """Make choice be able to vote."""
    user = request.user
    # run this get_object_or_404 if fail return 404 page
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice_id = request.POST['choice']
        selected_choice = question.choice_set.get(pk=choice_id)

    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        vote = get_vote_for_user(user, question)
        # Always return an HttpResponseRedirect after successfully dealing
        if not vote:
            vote = Vote(user=user, choice=selected_choice)
        else:
            vote.choice = selected_choice
        vote.save()
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        logger = logging.getLogger('polls')
        logger.info(f'{user} vote {vote.choice} in question {question}')
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def get_vote_for_user(user_a, question):
    try:
        vote = Vote.objects.filter(user=user_a).filter(choice__question=question)
        if vote.count() == 0:
            return None
        else:
            return vote[0]
    except Vote.DoesNotExist:
        return None


def resultData(request, obj):
    """To return the data of that polls question."""
    votedata = []

    question = Question.objects.get(id=obj)
    votes = question.choice_set.all()

    for i in votes:
        votedata.append({i.choice_text: i.votes})
    return JsonResponse(votedata, safe=False)
