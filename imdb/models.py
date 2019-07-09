from django.db import models


class SentimentAnalysis(models.Model):
    REVIEW_TYPE = (
        ('Positive', 'Положительный'),
        ('Negative', 'Негативный'),
        ('Neutral', 'Нейтральный')
    )

    review = models.TextField()
    result = models.CharField(choices=REVIEW_TYPE, max_length=32)

    def __str__(self):
        return '{}'.format(self.result)
