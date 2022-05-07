from django import forms
from tasktell.common.mixins import FormBootstrapMixin
from tasktell.main.models import Project


class ProjectCreateForm(FormBootstrapMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()

    class Meta:
        model = Project
        fields = ('name', 'type', 'logo', 'description')
        widgets = {
            'type': forms.RadioSelect(
                choices=Project.TYPE_CHOICES,
                attrs={'class': 'oke'}
            )
        }


class PublicProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ()
