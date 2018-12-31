from django.shortcuts import render, redirect
from . import models
from datetime import datetime
from django.views.generic import TemplateView
from . import form
from django.contrib import messages
from django.http import HttpResponse
import json

# Create your views here.
class Vote_main(TemplateView):
    def get(self, request):
        polls = models.Poll.objects.all()
        context = {"polls":polls}
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
        candis = models.Candidate.objects.all()
        today=datetime.now()
        polls = models.Poll.objects.filter(end_date__gte=today)
        context={"candis":candis, "polls":polls}
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


# class Vote_area(TemplateView):
#     def get(self, request, area, id):
#         votes=models.Vote.objects.filter(poll_for__id=id)
#         print(votes)

def getPoll(self,id):
    candi = models.Candidate.objects.get(id=id)
    area = candi.area
    polls = models.Poll.objects.filter(area=area)
    list_polls={}
    for po in polls:
        string = po.area + " ( " + str(po.start_date) + " ~ " + str(po.end_date) + " ) "
        list_polls[po.id] = string

    if len(list_polls)==0:
        string="Nothing"
        list_polls[0] = string
    
    return HttpResponse(json.dumps(list_polls), content_type="application/json")