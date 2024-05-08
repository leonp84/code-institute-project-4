from .models import Board
from django import forms


class CreateBoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'description', 'colour',]
