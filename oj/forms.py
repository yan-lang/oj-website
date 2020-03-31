from .models import Submission
from bootstrap_modal_forms.forms import BSModalForm


class SubmissionForm(BSModalForm):
    class Meta:
        model = Submission
        fields = ['submitted_file']
