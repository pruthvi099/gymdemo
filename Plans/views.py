from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse
from django.contrib import auth, messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from Plans.models import Plan
from Members.forms import EnquiryForm

# Create your views here.

@method_decorator(login_required, name='dispatch')
class AllPlans(View):
    template_name = 'Plans/allview.html'

    def get(self, request):
        plans = list(Plan.objects.filter().values())
        context = {
            'plans': plans,
            'active_tab': 'plans',

        }
        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
class AddEnquiry(View):
    template_name = 'Members/addenquiry.html'

    def post(self, request):
        form = EnquiryForm(request.POST)

        if form.is_valid():
            form_obj = form.save(commit=False)

            form_obj.gender = request.POST['genderRadio']
            form_obj.createdby_id = request.user.id

            form_obj.save()
            messages.success(request, "Uploaded Enquiry successFully !")
        else:
            print(form.errors)
            messages.error(request, "Uploading Enquiry Failed !")

        return redirect("Members:enquiries")
    
    def get(self, request):
        context = {
            'form': EnquiryForm(),
            'active_tab': 'plans',

        }
        return render(request, self.template_name, context)