from django.shortcuts import render, redirect
from . import models
from datetime import datetime
from django.views.generic import TemplateView
from . import form
from django.contrib import messages
from django.http import HttpResponse
import json
from django.db.models import Sum
import pusher

# Create your views here.



class Vote_main(TemplateView):
    def get(self, request):
        today=datetime.now().date()
        polls_ing = models.Poll.objects.filter(end_date__gte=today).order_by('-id')
        polls_end = models.Poll.objects.filter(end_date__lt=today).order_by('-id')
        context = {"polls_ing":polls_ing,"polls_end":polls_end}
        return render(request, 'vote/index.html',context)

class Add_candi(TemplateView):
    def get(self, request):
        f = form.FormCandi()
        return render(request,'vote/add_candi.html',{'form':f})

    def post(self,request):
        f = form.FormCandi(request.POST)
        if f.is_valid():
            new_name = f.cleaned_data['name']
            new_area = f.cleaned_data['area']
            try:
                existing_user = models.Candidate.objects.get(name=new_name, area=new_area)
            except:
                existing_user = None
            if existing_user == None:
                new_candi = f.save()
                messages.info(request,'success!')
                return redirect('vote:main_view')
            else:
                messages.info(request,'duplicate!_change_name_or_area')
                return redirect('vote:add_candi')
                
        else:
            return render(request,'vote:add_candi')

class Add_poll(TemplateView):
    def get(self, request):
        f = form.FormPoll()
        return render(request,'vote/add_poll.html',{'form':f})

    def post(self,request):
        f = form.FormPoll(request.POST)
        if f.is_valid():
            new_start = f.cleaned_data['start_date']
            new_end = f.cleaned_data['end_date']
            new_area = f.cleaned_data['area']
            
            if new_end < new_start :
                messages.info(request,'we_must_start_date_<=_end_date')
                return redirect('vote:add_poll')

            ###중복 체크###
            try:
                existing_poll = models.Poll.objects.get(area = new_area, start_date__lte=new_start, end_date__gte=new_end)
            except:
                existing_poll = None
            
            if existing_poll==None:
                try:
                    existing_poll = models.Poll.objects.get(area = new_area, start_date__range=[new_start,new_end])
                except:
                    existing_poll = None

            if existing_poll==None:
                try:
                    existing_poll = models.Poll.objects.get(area = new_area, end_date__range=[new_start,new_end])
                except:
                    existing_poll = None

            if existing_poll==None:
                try:
                    existing_poll = models.Poll.objects.get(area = new_area, start_date__gte=new_start, end_date__lte=new_end)
                except:
                    existing_poll = None

            if existing_poll == None:
                new_poll = f.save()
                messages.info(request,'success!')
                return redirect('vote:main_view')
            else:
                messages.info(request,'duplicate!_change_start_date_or_end_date')
                return redirect('vote:add_poll')
                
        else:
            return render(request,'vote:add_poll')

class Candi_to_poll(TemplateView):
    def get(self, request):
        candis = models.Candidate.objects.all().order_by('-area')
        context={"candis":candis}
        return render(request,'vote/canditopoll.html',context)

    def post(self,request):
        f_c = request.POST['candi']
        f_p = request.POST['poll']

        new_c = models.Candidate.objects.get(id=f_c)
        new_p = models.Poll.objects.get(id=f_p)
        
        if new_c.area != new_p.area:
            messages.info(request,'please_check_your_area')
            return redirect('vote:candi_to_poll')

        try:
            duple_check = models.Vote.objects.get(can_for__id=f_c, poll_for__id=f_p)
        except:
            duple_check=None

        if duple_check==None:
            vote = models.Vote.objects.create(can_for=new_c, poll_for=new_p, vote_count=0)
            vote.save()
            messages.info(request,'success_registered')
            return redirect('vote:main_view')
        else:
            messages.info(request,'already_registered')
            return redirect('vote:candi_to_poll')

class Vote_area(TemplateView):
    def get(self, request, area, id):
        votes = models.Vote.objects.filter(poll_for__id=id)
        list_candis =[]
        
        for vote in votes:
            candi = models.Candidate.objects.get(id=vote.can_for.id)
            list_candis.append(candi)

        poll = models.Poll.objects.get(id=id)
        today = datetime.now().date()
        if poll.end_date < today:
            vote_valid=False
        else:
            vote_valid=True

        context={"candis":list_candis, "poll_id":id, "vote_valid":vote_valid}
        return render(request,'vote/votes.html',context)

class Vote_select(TemplateView):
    def __pusher(self):
        pusher_client = pusher.Pusher(
            app_id='685009',
            key='dd24723fdc03c087279d',
            secret='56202d89d190f70d4d58',
            cluster='ap3',
            ssl=True
            )

        pusher_client.trigger('my-channel', 'my-event', {'message': 'push'})

    def get(self, request, id, poll_id):
        vote = models.Vote.objects.get(can_for__id=id, poll_for__id=poll_id)
        vote.vote_count=vote.vote_count+1
        vote.save()
        
        messages.info(request,'Success!')
        votes = models.Vote.objects.filter(poll_for__id=poll_id)

        context={"votes":votes}
        # ▲투표 완료
        # ▼Noti, pusher
        can = models.Candidate.objects.get(id=id)
        msg = can.name+"님이 1표를 받았습니다."
        message = models.Noti.objects.create(message = msg)
        self.__pusher()

        return render(request,'vote/finish.html',context)

class View_result(TemplateView):
    def get(self, request, poll_id):
        votes = models.Vote.objects.filter(poll_for__id=poll_id)
        print('hhhhhhhhhhhhhhhhhhhhhhh')
        context={"votes":votes}
        return render(request,'vote/finish.html',context)

class Vote_admin(TemplateView):
    def get(self, request):
        return render(request,'vote/admin.html')

def getPoll(self,id):
    candi = models.Candidate.objects.get(id=id)
    area = candi.area

    today=datetime.now()
    polls = models.Poll.objects.filter(area=area, start_date__gt=today)
    list_polls={}
    for po in polls:
        string = po.area + " ( " + str(po.start_date) + " ~ " + str(po.end_date) + " ) "
        list_polls[po.id] = string

    if len(list_polls)==0:
        string="Nothing"
        list_polls[0] = string
    
    return HttpResponse(json.dumps(list_polls), content_type="application/json")


def getNoti(self):
    notis = models.Noti.objects.all()[:10]
    list_notis={}
    for noti in notis:
        list_notis[noti.id] = noti.message

    if len(list_notis)==0:
        string="Nothing"
        list_notis[0] = string
    
    return HttpResponse(json.dumps(list_notis), content_type="application/json")




