from django import forms
from .models import Review

BAD_WORDS = ['malo', 'mugroso', 'estupido','wey']

class ReviewSimpleForm(forms.Form):
    rating = forms.IntegerField(
        min_value=1, max_value=5,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Califica del 1 al 5',
            'class': 'form-control'
        })
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Escribe tu reseña aquí...',
            'class': 'form-control',
            'rows': 4
        })
    )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text',]
        widgets = {
            'rating': forms.NumberInput(attrs={
                'placeholder': 'Calificación del 1 al 5',
                'class': 'form-control',
            }),
            'text': forms.Textarea(attrs={
                'placeholder': 'Escribe tu reseña',
                'class': 'form-control',
                'rows': 4
            })
        }
        
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 0 or rating > 5:
            raise forms.ValidationError(
                "La calificación debe estar entre 1 y 5."
            )
        return rating
    
    def clean_text(self):
        text = self.cleaned_data['text']
        for palabra in BAD_WORDS:
            if palabra in text.lower():
                raise forms.ValidationError(f'La reseña tiene una palabra prohibida: {palabra}')
        return text
    
    def clean(self):
        clean_data = super().clean()
        rating = clean_data.get("rating")
        text = clean_data.get("text") or " "
        
        if rating == 1 and len(text) < 10:
            raise forms.ValidationError(
                "Si la califación es de 1 estrella, por favor explica mejor tu experiencia ")