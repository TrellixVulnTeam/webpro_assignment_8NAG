from django.shortcuts import render
from django.db.models import Count
from django.http import HttpResponse
from polls.models import Poll, Question, Answer

from .forms import PollForm

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

	if request.method == 'POST':
		for question in poll.question_set.all():
			name = 'choice' + str(question.id)
			choice_id = request.POST.get(name)
			if choice_id:
				try:
					ans = Answer.objects.get(question_id=question.id)
					ans.choice_id = choice_id
					ans.save()
				except Answer.DoesNotExist:
					Answer.objects.create(choice_id=choice_id, question_id=question.id)
			# print(choice_id)

	print(request.GET)

	return render(request, 'polls/detail.html', { 'poll': poll })
 
def create(request):
	if request.method == 'POST':
		# title = request.POST.get('title')
		# question_list = request.POST.getlist('questions[]')
		form = PollForm(request.POST)

		if form.is_valid():
			poll = Poll.objects.create(
				title=form.cleaned_data.get('title'),
				start_date=form.cleaned_data.get('start_date'),
				end_date=form.cleaned_data.get('end_date')			
			)

			for i in range(1, form.cleaned_data.get('no_question') + 1):
				Question.objects.create(
					text='QQQ' + str(i),
					type='01',
					poll=poll
				)
	else:
		# answers = request.GET.get('answers')
		# answer_list = request.GET.getlist('answers[]')
		form = PollForm() 
	
	context = {'form':form}
	return render(request, 'polls/create.html', context=context)