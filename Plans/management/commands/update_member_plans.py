from django.core.management.base import BaseCommand
from datetime import datetime
from Members.models import MemberPlan

class Command(BaseCommand):
    help = 'Updates the status of active member plans'

    def handle(self, *args, **options):
        member_plans = MemberPlan.objects.filter(is_active=True, end_date__lt=datetime.now())
        for plan in member_plans:
            plan.is_active = False
            plan.save()
        self.stdout.write(self.style.SUCCESS('Successfully updated member plans status'))