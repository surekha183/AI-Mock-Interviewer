from django import forms
from .roles import INTERVIEW_ROLES

LEVEL_CHOICES = [
    ("Fresher", "Fresher"),
    ("1-2 Years", "1-2 Years"),
    ("2-5 Years", "2-5 Years"),
    ("5-10 Years", "5-10 Years"),
    ("10+ Years", "10+ Years"),
]


DOMAIN_CHOICES = [
    (domain, domain)
    for domain in INTERVIEW_ROLES.keys()
]


class InterviewForm(forms.Form):

    domain = forms.ChoiceField(
        choices=DOMAIN_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "domain"
            }
        )
    )

    role = forms.ChoiceField(
        choices=[],
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "role"
            }
        )
    )

    experience = forms.ChoiceField(
        choices=LEVEL_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        first_domain = list(INTERVIEW_ROLES.keys())[0]

        self.fields["role"].choices = [
            (role, role)
            for role in INTERVIEW_ROLES[first_domain]
        ]

        if "domain" in self.data:

            selected = self.data.get("domain")

            if selected in INTERVIEW_ROLES:

                self.fields["role"].choices = [
                    (role, role)
                    for role in INTERVIEW_ROLES[selected]
                ]