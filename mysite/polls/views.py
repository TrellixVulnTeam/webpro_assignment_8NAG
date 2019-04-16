from django.shortcuts import render
from django.db.models import Count
from django.http import HttpResponse
from polls.models import Poll, Question

def index(request):
	#poll_list = Poll.objects.all()
	poll_list = Poll.objects.annotate(question_count=Count('question'))
	print(poll_list.query)
	# for poll in poll_list:
	# 	question_list = Question.objects.filter(poll_id=poll.id).count()
	# 	poll.question_count = question_count

	context = {
		'page_title': "My Polls", 
		'poll_list': poll_list
	}
	
	return render(request, 'polls/index.html', context=context)

def detail(request, poll_id):

	poll = Poll.objects.get(pk=poll_id)

	return render(request, 'polls/detail.html', { 'poll': poll })
