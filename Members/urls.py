from django.urls import path
from Members.views import *

urlpatterns = [
    path('enquiries', Enquiries.as_view(), name='enquiries'),
    path('addenquiry', AddEnquiry.as_view(), name='addenquiry'),
    path('members', AllMembers.as_view(), name='members'),
    path('addmember', AddMember.as_view(), name='addmember'),
    path('addmemberfromenq', AddMemberfromEnquiry.as_view(), name='addmemberfromenq'),
    path('member/<int:pk>/', MemberDetailView.as_view(), name='member-detail'),
    path('plan/create/', PlanCreateView.as_view(), name='memberplancreate'),
    path('member/<int:member_id>/deactivate/', DeactivateMemberView.as_view(), name='deactivate-member'),
    path('member/<int:member_id>/activate/', ActivateMemberView.as_view(), name='activate-member'),
    path('plan/<int:pk>/edit/', MemberPlanUpdateView.as_view(), name='member_plan_edit'),
    path('plan/<int:pk>/delete/', delete_member_plan, name='delete_member_plan'),
    path('updateAllPlans', UpdateAllPlans.as_view(), name='updateAllPlans'),
]

app_name = 'Members'
