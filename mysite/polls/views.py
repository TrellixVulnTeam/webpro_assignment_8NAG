from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.db import connection
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from polls.models import Poll, Question, Answer, Comment
from .forms import PollForm, CommentForm, ChangePasswordForm, NewUserForm


def my_login(request):
	context = {}

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user:
			login(request, user)

			next_url = request.POST.get('next_url')
			if next_url:
				return redirect(next_url)
			else:
				return redirect('index')
		else:
			context['username'] = username
			context['password'] = password
			context['error'] = 'Wrong username or password!'

	next_url = request.GET.get('next')
	if next_url:
		context['next_url'] = next_url
	return render(request, 'polls/login.html', context=context)

def my_logout(request):
	logout(request)
	return redirect('login')

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
	#print(request.user)
	#print(request.user.email)
	return render(request, 'polls/index.html', context=context)

@login_required
@permission_required('polls.view_poll')
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

@login_required
@permission_required('polls.add_poll')
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

@login_required
def create_comments(request, poll_id):
	if request.method == 'POST':
		form = CommentForm(request.POST)
		poll = Poll.objects.get(pk=poll_id)
		if form.is_valid():
			Comment.objects.create(
				poll=poll,
				title=form.cleaned_data.get('title'),
				body=form.cleaned_data.get('body'),
				email=form.cleaned_data.get('email'),
				tel=form.cleaned_data.get('tel')
			)
	else:
		form = CommentForm()
	
	context = {
		'form': form,
		'poll_id': poll_id
	}

	return render(request, 'polls/create-comment.html', context=context)

@login_required
def change_password(request):
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST, user=request.user)
		if form.is_valid():
			u = request.user
			u.set_password(form.cleaned_data.get('new_pw'))
			u.save()
	else:
		form = ChangePasswordForm(user=request.user)

	context = {
		'form': form
	}

	return render(request, 'polls/change_password.html', context=context)

def newuser(request):

	if request.method == 'POST':
		form = NewUserForm(request.POST)
		if form.is_valid():
			Profile.objects.create(
				user=form.cleaned_data.get('user')
			)
	else:
		form = NewUserForm()
	
	context = {
		'form': form
	}
	
	return render(request, 'polls/register.html', context=context)