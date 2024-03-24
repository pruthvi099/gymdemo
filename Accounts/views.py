from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.urls import reverse
from django.contrib import auth, messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from datetime import datetime, timedelta

from Accounts.forms import LoginForm
from Members.models import MemberPlan, Member

# Create your views here.

@method_decorator(login_required, name='dispatch')
class Home(View):
    template_name = 'Accounts/home.html'

    def get(self, request):
        context = {
            'msg': 'Hello'
        }
        return render(request, self.template_name, context)
    
class Login(View):
    template_name = 'Accounts/login.html'

    def post(self, request):
        form =  LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = auth.authenticate(email=email, password=password)
            if user: 
                auth.login(request, user)
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('/')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('/')


        context = {
            'msg': 'Hello'
        }
        return redirect('Accounts:home')
    
    def get(self, request):
        if request.user.is_authenticated: return redirect("Accounts:home")

        context = {
            'form': LoginForm(),  
            'msg': 'Hello'
        }
        return render(request, self.template_name, context)
    
class Logout(View):
    def get(self, request):
        auth.logout(request)
        messages.success(request,'Logged Out Successfully!')
        return redirect('Accounts:login') 
    

class DashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'Accounts/dashboard.html'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponse(status=403) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Total active members
        total_active_members = Member.objects.filter(is_active=True).count()

        # Total inactive members
        total_inactive_members = Member.objects.filter(is_active=False).count()

        # Members renewed this month
        current_month = datetime.today().month
        current_year = datetime.today().year
        members_renewed_this_month = MemberPlan.objects.filter(startdate__month=current_month, startdate__year=current_year).count()

        # Total members paid this month
        members_paid_this_month = MemberPlan.objects.filter(startdate__month=current_month, startdate__year=current_year, is_paid=True).count()

        # Total members paid previous month
        previous_month = datetime.today().replace(day=1) - timedelta(days=1)
        previous_month_paid_members = MemberPlan.objects.filter(startdate__month=previous_month.month, startdate__year=previous_month.year, is_paid=True).count()

        unpaid_members = MemberPlan.objects.filter(is_paid=False).count()

        # Total inactive members
        inactive_members = Member.objects.filter(is_active=False).values()
        
        # Total invalid members
        invalid_members = Member.objects.filter(plan_validity=False).values().distinct()

        context['total_active_members'] = total_active_members
        context['total_inactive_members'] = total_inactive_members
        context['members_renewed_this_month'] = members_renewed_this_month
        context['members_paid_this_month'] = members_paid_this_month
        context['previous_month_paid_members'] = previous_month_paid_members
        context['unpaid_members'] = unpaid_members
        context['inactive_members'] = inactive_members
        context['invalid_members'] = invalid_members
        return context
        return context


