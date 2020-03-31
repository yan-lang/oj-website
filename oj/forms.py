from bootstrap_modal_forms.forms import BSModalForm
from django.core.exceptions import ValidationError
from django.forms import FileField, FileInput

from .models import Submission


class RestrictedFileField(FileField):
    """ max_upload_size:
                2.5MB - 2621440
                5MB - 5242880
                10MB - 10485760
                20MB - 20971520
                50MB - 5242880
                100MB 104857600
                250MB - 214958080
                500MB - 429916160
    """

    def __init__(self, *, allowed_types=None, max_length=None, allow_empty_file=False, **kwargs):
        super().__init__(max_length=max_length, allow_empty_file=allow_empty_file, **kwargs)
        self.allowed_types = allowed_types

    def clean(self, data, initial=None):
        data = super().clean(data, initial)
        file_name: str = data.name
        if self.allowed_types is not None and not file_name.endswith(tuple(self.allowed_types)):
            raise ValidationError(['This file type is not allowed.'])

        return data


class SubmissionForm(BSModalForm):
    class Meta:
        model = Submission
        fields = ['submitted_file']

    submitted_file = RestrictedFileField(max_length=20971520, allowed_types=['.zip', '.jar'])
