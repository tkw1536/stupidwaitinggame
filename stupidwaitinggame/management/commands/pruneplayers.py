from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Removes all players with zero points from the database'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        UserModel = get_user_model()

        # Remove all the users with a profile score of 0
        # (unless they're staff)
        pruned, _ = UserModel.objects.filter(profile__score=0, is_staff=False).delete()
        print("Deleted {} user(s) with a score of 0. ".format(pruned))

        # Remove all the users without a profile
        # (unless they're staff)
        pruned, _ = UserModel.objects.filter( profile__isnull=True, is_staff=False).delete()
        print("Deleted {} user(s) without a profile. ".format(pruned))

        count = UserModel.objects.count()
        print("There are still {} user(s) in the database. ".format(count))

        
