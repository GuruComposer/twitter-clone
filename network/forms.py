from django.forms import ModelForm
from network.models import Post
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Row, HTML, Column, Field

class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs['class']='post-form-text-area'
        self.fields["text"].widget.attrs["placeholder"] = "Enter a tweet..."
        self.fields["text"].widget.attrs["rows"] = "2"
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'index'
        self.helper.form_show_labels = False
        self.helper.label_class = 'col-lg-2'

        self.helper.add_input(Submit('submit', 'Submit'))