from django.shortcuts import render, get_object_or_404, redirect
from imdb.ml_model import classifier, word_feats
from imdb.models import SentimentAnalysis
from imdb.forms import SentimentAnalysisForm


def review_list(request):
    reviews = SentimentAnalysis.objects.all()
    return render(request, 'imdb/reviews_list.html', {'reviews': reviews})


def review_new(request):
    if request.method == "POST":
        form = SentimentAnalysisForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            review.result = check_result(review.id)
            review.save()
            return redirect('review_list')
    else:
        form = SentimentAnalysisForm()
    return render(request, 'imdb/create_reviews.html', {'form': form})


def check_result(review):
    review = get_object_or_404(SentimentAnalysis, pk=review)
    text = review.review
    sentence = text.lower().strip()
    words = sentence.split(' ')
    p_rating = 0
    n_rating = 0
    for word in words:
        classResult = classifier.classify(word_feats(word))
        if classResult == 'neg':
            n_rating = n_rating + 1
        if classResult == 'pos':
            p_rating = p_rating + 1

    if float(p_rating) / len(words) > float(n_rating) / len(words):
        result = 'Positive'
    elif float(p_rating) / len(words) < float(n_rating) / len(words):
        result = 'Negative'
    else:
        result = 'Neutral'
    return result
