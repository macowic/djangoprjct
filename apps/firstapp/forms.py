from cProfile import label
from django import forms 

from firstapp.models import Homework

class HomeworkForm(forms.ModelForm):

    class Meta:
        
        IMAGE_FILE_TYPES = (
        'png',
        'jpg',
        'jpeg',
        ) 

        title = forms.CharField(
            max_length=100,
            label = 'Тема')
        subject = forms.CharField(
            max_length=50,
            label = 'Предмет')
        logo = forms.ImageField(
            label='Логотип',
            max_length=255
        )
        
        model = Homework
        fields = [
            'title',
            'subject', 'logo'
        ]