# myapp/management/commands/populate_user_profiles.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import UserProfile

class Command(BaseCommand):
    help = 'Populate user profiles'

    def handle(self, *args, **options):
        # Create UserProfile instances
        user1 = User.objects.create(username='user3', email='user1@example.com')
        user_profile1 = UserProfile.objects.create(user=user1)

        user2 = User.objects.create(username='user4', email='user2@example.com')
        user_profile2 = UserProfile.objects.create(user=user2)

        # Save instances to the database
        user_profile1.save()
        user_profile2.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated user profiles'))
