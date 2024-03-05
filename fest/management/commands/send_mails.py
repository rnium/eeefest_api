from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandError
from fest.models import Registration
from fest.utils import send_confirmation_email

baseUrl = "https://www.seceeefest.tech"


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        count = 0
        for reg in Registration.objects.filter(is_approved=True, is_email_sent=False):
            try:
                send_confirmation_email(baseUrl, reg)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed. Reg. Id: {reg.id}, error: {e}"))
                continue
            count += 1
            reg.is_email_sent = True
            reg.save()
        self.stdout.write(self.style.SUCCESS(f"Done, total emails sent: {count}"))