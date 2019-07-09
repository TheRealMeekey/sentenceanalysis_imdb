from django import forms
from imdb.models import SentimentAnalysis


class SentimentAnalysisForm(forms.ModelForm):
    class Meta:
        model = SentimentAnalysis
        fields = ('review',)

    def __init__(self, *args, **kwargs):
        super(SentimentAnalysisForm, self).__init__(*args, **kwargs)
        self.fields['review'].widget.attrs.update({'class': 'materialize-textarea'})
