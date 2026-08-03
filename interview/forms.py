from django import forms

ROLE_CHOICES = [
    ("Python Developer", "Python Developer"),
    ("Data Analyst", "Data Analyst"),
    ("Software Engineer", "Software Engineer"),
    ("Django Developer", "Django Developer"),
    ("SQL Developer", "SQL Developer"),
]

LEVEL_CHOICES = [
    ("Fresher", "Fresher"),
    ("1-2 Years", "1-2 Years"),
]


class InterviewForm(forms.Form):

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    experience = forms.ChoiceField(
        choices=LEVEL_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"})
    )