from django import forms
from django.forms import widgets
from django.forms import ModelForm

from Members.models import Enquiry, Member, MemberPlan
from Plans.models import Plan

class EnquiryForm(ModelForm):
    class Meta:
        model = Enquiry
        exclude = ['created', 'gender', 'age']
        widgets = {
            "name": widgets.TextInput(attrs={"class": "form-control form-control-lg"}),
            "location": widgets.TextInput(attrs={"class": "form-control form-control-lg"}),
            "birthday": forms.DateTimeInput(attrs={'class':'form-control form-control-lg', 'data-target': '#datetimepicker', 'type':"date"}),
            "mobile": widgets.NumberInput(attrs={"class": "form-control form-control-lg"}),
        }

class MemberForm(ModelForm):
    is_enquiry = forms.ChoiceField(choices=[(True, 'Yes'), (False, 'No')], widget=widgets.RadioSelect(attrs={"class": "form-control "}), required=False)
    enquiry = forms.ModelChoiceField(queryset=Enquiry.objects.filter(), required=False, widget=widgets.Select(attrs={"class": "form-control form-control-lg"}))
    class Meta:
        model = Member
        exclude = ['created', 'gender', 'age']
        widgets = {
            "name": widgets.TextInput(attrs={"class": "form-control form-control-lg"}),
            "location": widgets.TextInput(attrs={"class": "form-control form-control-lg"}),
            "birthday": forms.DateTimeInput(attrs={'class':'form-control form-control-lg', 'data-target': '#datetimepicker', 'type':"date"}),
            "mobile": widgets.NumberInput(attrs={"class": "form-control form-control-lg"}),
        }

    def clean(self):
        enquiry = self.data.get('member-enquiry_id')
        if enquiry is not None:
            obj = Enquiry.objects.filter(id=enquiry)
            if obj.exists():
                enquiryobj = obj[0]
            else: enquiryobj = None
        else: enquiryobj = None
        self.cleaned_data['enquiry'] = enquiryobj
        print(enquiryobj)
        
        return super().clean()
    
class MemberPlanForm(forms.ModelForm):
    member = forms.ModelChoiceField(queryset=Member.objects.filter(), required=False, widget=widgets.Select(attrs={"class": "form-control "}))
    plan = forms.ModelChoiceField(queryset=Plan.objects.filter(), required=False, widget=widgets.Select(attrs={"class": "form-control "}))
    is_active = forms.ChoiceField(choices=[(True, 'Yes'), (False, 'No')], widget=widgets.RadioSelect(attrs={"class": "input-group-prepend"}), required=False)
    is_paid = forms.ChoiceField(choices=[(True, 'Yes'), (False, 'No')], widget=widgets.RadioSelect(attrs={"class": "input-group-prepend"}), required=False)
    class Meta:
        model = MemberPlan
        fields = ['is_active', 'is_paid', 'member', 'plan', 'startdate', 'paymentdate']
        widgets = {
            "startdate": forms.DateTimeInput(attrs={'class':'form-control', 'data-target': '#datetimepicker', 'type':"date"}),
            "paymentdate": forms.DateTimeInput(attrs={'class':'form-control', 'data-target': '#datetimepicker', 'type':"date"}),
        }


    # is_enquiry = models.BooleanField(null=True, blank=True)
    # plan_validity = models.BooleanField(null=True, blank=True)
    # enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, null=True, blank=True)

    # created = models.DateTimeField(auto_now_add=True)
    # createdby = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
# <input type="date" data-target="#datetimepicker" class="form-control" value=""/>