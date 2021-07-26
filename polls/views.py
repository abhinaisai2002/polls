import json
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.core import serializers
from datetime import datetime
# Create your views here.
@login_required(login_url='users:login')
def polls_view(request):
    if request.method == 'POST':
        title =request.POST.get('description')
        options =request.POST.getlist('option')
        poll = Poll( title = title,creator = request.user )
        poll.save()
        for option in options:
            pollOptions = PollsOptions(pollOption=option,poll=poll)
            pollOptions.save()
    polls = Poll.objects.all().order_by('date').reverse()
    DATA=[]
    for poll in polls:
        data = {}
        data['poll'] = poll
        try:
            data['status'] = VotedBy.objects.get(poll=poll,polled_by = request.user)
        except:
            data['status'] = None
        DATA.append(data)

    pageNumber = request.GET.get('page')
    paginator = Paginator(DATA, 10)
    pagePolls = paginator.get_page(pageNumber)
    context = {
        'DATA':pagePolls,
    }
    return render(request,'polls/polls.html',context)

def submit_poll_view(request):
    if request.method == 'POST':
        print(request)
        pollId = request.POST.get('pollId')
        optionId = request.POST.get('optionId')
        poll = Poll.objects.get(id = pollId)
        polloption = PollsOptions.objects.get(id = optionId)
        print(polloption)
        print(polloption.pollOptionVotes)
        polloption.pollOptionVotes += 1
        polloption.save()
        polled_by = VotedBy(poll=poll,polled_by = request.user,polledOpt=polloption )
        polled_by.save()

        DATA = []
        total_votes = 0
        for option in poll.pollsoptions_set.all():
            data = {}
            data['pollOption'] = option.pollOption
            data['votes'] = option.pollOptionVotes
            data['id'] = option.id
            total_votes += option.pollOptionVotes
            DATA.append(data)
        return JsonResponse({'data': DATA, 'total_votes': total_votes,'polledOpt' : polloption.pollOption})


def get_poll_data(request):
    if request.method == 'GET':
        pollId = request.GET.get('pollId')
        poll = Poll.objects.get(id=pollId)
        DATA= []
        total_votes = 0
        for option in poll.pollsoptions_set.all():
            data={}
            data['pollOption'] = option.pollOption
            data['votes'] = option.pollOptionVotes
            data['id'] = option.id
            total_votes += option.pollOptionVotes
            DATA.append(data)
    return JsonResponse({'data':DATA,'total_votes':total_votes})

def top_polls(request):
    d = []
    polls = Poll.objects.all()
    for poll in polls:
        dt={}
        totalVotes = poll.pollsoptions_set.all().aggregate(Sum('pollOptionVotes'))
        dt['title'] = poll.title
        dt['votes'] = totalVotes['pollOptionVotes__sum']
        dt['id'] = poll.id
        dt['creator'] = poll.creator.username
        d.append(dt)
    d.sort(key = lambda x : x['votes'],reverse=True)
    return JsonResponse({'topPolls':d[:5]})


def comment_view(request):
    if request.method == 'POST':
        pollId = request.POST.get('pollid')
        comment = request.POST.get('text')
        poll = Poll.objects.get(id = pollId)
        comment = CommentBy(poll=poll,comment = comment,comment_by = request.user)
        comment.save()
        date = comment.date
        x = date.strftime("%B %d, %Y, %I:%M %p")
        data = {
            'user' : comment.comment_by.username,
            'date' : x,
            'text' : comment.comment
        }
    return JsonResponse({'comment' : data})


@login_required(login_url='users:login')
def poll_view(request,id):
    poll = Poll.objects.get(id = id)
    try:
        status = VotedBy.objects.get(poll=poll, polled_by=request.user)
    except:
        status = None
    comments = CommentBy.objects.filter(poll = poll).order_by('date').reverse()

    context = {
        'poll' : poll,
        'status' : status,
        'comments' : comments
    }
    return render(request,'polls/poll.html',context)

def search_view(request):
    pollname = request.GET.get('name')
    if pollname == '':
        return JsonResponse({'data':[]})
    print(pollname)
    polls = Poll.objects.filter(title__contains = pollname)
    
    data=[]
    for poll in polls:
        data.append([poll.title,poll.id])
    if data == []:
        return JsonResponse({'data': [['no match found','-1']]})
    return JsonResponse({'data':data})
