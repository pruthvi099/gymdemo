from django.shortcuts import render, redirect
from django.views.generic import View, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from django.contrib import auth, messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from dateutil import relativedelta
from datetime import datetime
from django.views.decorators.http import require_POST
from django.http import HttpResponse

from Members.models import Enquiry, Member, MemberPlan
from Members.forms import EnquiryForm, MemberForm, MemberPlanForm


# Create your views here.

def calculate_age(dob):
    """
    Calculate age from date of birth (DOB).
    :param dob: Date of birth in the format 'YYYY-MM-DD'
    :return: Age in years
    """
    # Get current date
    current_date = datetime.now().date()

    # Convert DOB string to datetime object
    try: dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
    except: dob_date = dob

    # Calculate age
    age = current_date.year - dob_date.year - ((current_date.month, current_date.day) < (dob_date.month, dob_date.day))

    return age

@method_decorator(login_required, name='dispatch')
class Enquiries(View):
    template_name = 'Members/enquiriesall.html'

    def get(self, request):
        enquiries = list(Enquiry.objects.filter().values())
        context = {
            'enquiries': enquiries,
            'active_tab': 'enquiry',

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
            form_obj.age = calculate_age(form_obj.birthday)
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
            'active_tab': 'enquiry',

        }
        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
class AllMembers(View):
    template_name = 'Members/membersall.html'

    def get(self, request):
        enquiries = list(Member.objects.filter(is_active=True).values())
        context = {
            'enquiries': enquiries,
            'active_tab': 'members',

        }
        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
class AddMember(View):
    template_name = 'Members/addmember.html'

    def post(self, request):
        form = MemberForm(request.POST, prefix='member')

        if form.is_valid():
            form_obj = form.save(commit=False)

            form_obj.gender = request.POST['genderRadio']
            form_obj.age = calculate_age(form_obj.birthday)
            form_obj.is_active = True
            form_obj.createdby_id = request.user.id

            form_obj.save()
            messages.success(request, "Uploaded Member successFully !")
        else:
            print(form.errors)
            messages.error(request, "Uploading Member Failed !")

        return redirect("Members:members")
    
    def get(self, request):
        context = {
            'form': MemberForm(prefix='member'),
            'active_tab': 'members',
        }
        return render(request, self.template_name, context)
    
@method_decorator(login_required, name='dispatch')
class AddMemberfromEnquiry(View):
    template_name = 'Members/addmember.html'

    def post(self, request):
        enq_id = request.POST.get('enq_id', '')

        if enq_id == '': 
            messages.error(request, "Cant find Enquiry !")
            return redirect("Members:enquiries")
        
        full_enquiry = Enquiry.objects.get(id=enq_id)
        print(full_enquiry.age)

        form = Member.objects.create( **{
            'name': full_enquiry.name,
            'mobile': full_enquiry.mobile,
            'age' : full_enquiry.age,
            'gender': full_enquiry.gender,
            'location': full_enquiry.location,
            'birthday' : full_enquiry.birthday,

            'is_enquiry' : True, 
            'enquiry' : full_enquiry,
        })
        
        form.save()

        messages.success(request, "Uploaded Member successFully !")

        return redirect("Members:members")
    
@method_decorator(login_required(login_url='/'), name='dispatch')
class MemberDetailView(DetailView):
    model = Member
    template_name = 'Members/member-detail.html'  # Your template name for member details
    context_object_name = 'member'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = self.get_object()  
        
        related_plans = MemberPlan.objects.filter(member=member)
        context['memberplans'] = related_plans
        return context

@method_decorator(login_required, name='dispatch')
class PlanCreateView(CreateView):
    model = MemberPlan
    form_class = MemberPlanForm
    template_name = 'Members/addmemberplan.html'  

    def get_success_url(self):
        return reverse('Members:member-detail', kwargs={'pk': self.object.member.pk})

    def get_initial(self):
        initial = super().get_initial()
        member_id = self.request.GET.get('member_id')
        if member_id:
            member = get_object_or_404(Member, id=member_id)
            initial['member'] = member

        initial['startdate'] = now().date()
        return initial
    
    def form_valid(self, form):
        duration = form.instance.plan.duration 
        form.instance.startdate = form.instance.startdate
        endDate = (form.instance.startdate + relativedelta.relativedelta(months=duration))
        form.instance.enddate = endDate
        form.instance.createdby_id = self.request.user.id

        if form.instance.is_active and form.instance.is_paid:
            member = Member.objects.get(id= form.instance.member.id)
            member.plan_validity = True
            member.save()

        # Perform additional validations here
        if not form.is_valid():
            messages.error(self.request, "Error: Member must be active to create a paid plan.")
            print(form.errors)
            return self.form_invalid(form)

        # If all validations pass, save the form
        response = super().form_valid(form)
        print(form)
        # Send success message
        messages.success(self.request, _("Plan created successfully."))
        return redirect(reverse('Members:member-detail',kwargs={'pk':form.instance.member.id}))
    
class MemberPlanUpdateView(UpdateView):
    model = MemberPlan
    form_class = MemberPlanForm
    template_name = 'Members/addmemberplan.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete'] = True
        return context   
    
    def get_success_url(self):
        return reverse('Members:member-detail', kwargs={'pk': self.object.member.pk})
    
@require_POST
def delete_member_plan(request, pk):
    member_plan = get_object_or_404(MemberPlan, pk=pk)
    member_pk = member_plan.member.pk
    member_plan.delete()
    next_url = request.POST.get('next', '')
    return redirect(next_url)


class UpdateAllPlans(View):
    def get(self, request):
        member_plans = MemberPlan.objects.filter(is_active=True)
        # print(member_plans)
        for plan in member_plans:
            print(plan.enddate < datetime.now().date())
            if plan.enddate < datetime.now().date():
                plan.is_active = False
                member = plan.member
                member.plan_validity = False

                plan.save()
                member.save()
        
        return HttpResponse(status=200) 
    
@method_decorator(login_required, name='dispatch')
class DeactivateMemberView(View):
    def get(self, request, member_id):
        member = get_object_or_404(Member, id=member_id)
        
        member.is_active = False
        member.save()

        messages.success(request, _("Member Deactivated successfully."))
        return redirect('Members:member-detail', pk=member_id)
    
@method_decorator(login_required, name='dispatch')
class ActivateMemberView(View):
    def get(self, request, member_id):
        member = get_object_or_404(Member, id=member_id)
        
        member.is_active = True
        member.save()

        messages.success(request, _("Member Activated successfully."))
        return redirect('Members:member-detail', pk=member_id)