from __future__ import annotations

from django.db import models
from django.contrib.auth import get_user_model
import random

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from django.contrib.auth.models import User

from datetime import timedelta, datetime
from django.utils import timezone

DAY_IN_SECONDS = 86400
HALF_A_DAY_IN_SECONDS = DAY_IN_SECONDS // 2
WORDS = ["Advance", "Gain", "Upgrade", "Progress", "Improve", "Develop", "Expand", "Grow", "Explore", "Rise"]

class UserProfile(models.Model):
    score: int = models.IntegerField(default=0)
    user: User = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="profile")

    last_click: datetime = models.DateTimeField(auto_now_add=True)
    next_click: datetime = models.DateTimeField(auto_now_add=True)
    button_text: str = models.CharField(max_length=32, default="Begin")

    def click(self) -> [int, datetime]:
        now = timezone.now()
        if now < self.next_click:
            return self.score, self.next_click
        
        point_score = max(((self.next_click - self.last_click) - (now - self.next_click)).total_seconds(), 1)
        next_click_in_seconds = round(min((1.1 + random.random() * 0.1) ** self.score, min(DAY_IN_SECONDS - point_score, HALF_A_DAY_IN_SECONDS)))

        self.score += point_score
        self.next_click = now + timedelta(seconds=next_click_in_seconds)
        self.last_click = now

        normal_weight = 0.99 / len(WORDS)

        self.button_text = random.choices(WORDS + ["CORONA"], [normal_weight] * len(WORDS) + [0.01])[0]
        self.save()

        return self.score, self.next_click
