from django.db import models
from django.contrib.auth.models import User

COLOURS = (
    (0, 'Black'),
    (1, 'Blue'),
    (2, 'Green'),
)


class Board(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="boards")
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True)
    colour = models.IntegerField(choices=COLOURS, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"{self.title} | Owner: {self.author}"
