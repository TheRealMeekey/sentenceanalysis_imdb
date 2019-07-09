import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from nltk.classify import NaiveBayesClassifier

# Считываем обзоры
train = []
for line in open('reviews/movie_reviews/full_train.txt', 'r'):
    train.append(line.strip())

test = []
for line in open('reviews/movie_reviews/full_test.txt', 'r'):
    test.append(line.strip())

# Форматируем обзоры
REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\d+)")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
NO_SPACE = ""
SPACE = " "


def preprocess_reviews(reviews):
    '''
    Принимает список отзывов и возвращает отформатированый список отзывов
    :param reviews: array
    :return: array
    '''
    reviews = [REPLACE_NO_SPACE.sub(NO_SPACE, line.lower()) for line in reviews]
    reviews = [REPLACE_WITH_SPACE.sub(SPACE, line) for line in reviews]

    return reviews


train_clean = preprocess_reviews(train)
test_clean = preprocess_reviews(test)

# Векторизуем обзоры
cv = CountVectorizer(binary=True)
cv.fit(train_clean)
X = cv.transform(train_clean)
X_test = cv.transform(test_clean)

# Классафицируем. Логистическая регрессия
target = [1 if i < 12500 else 0 for i in range(25000)]

X_train, X_val, y_train, y_val = train_test_split(
    X, target, train_size=0.75
)

final_model = LogisticRegression(C=0.05)
final_model.fit(X, target)
# print("Final: %s"
#       % accuracy_score(target, final_model.predict(X_test)))

# Final: 0.88128

# определение позитивных/негативных слов
feature_to_coef = {
    word: coef for word, coef in zip(
        cv.get_feature_names(), final_model.coef_[0]
    )
}

# Создаем словарь из позитивных и негативных слов
positivs = []
for best_positive in sorted(feature_to_coef.items(), key=lambda x: x[1], reverse=True)[:25]:
    positivs.append(best_positive)

pos = dict(positivs)

negativs = []
for best_negative in sorted(feature_to_coef.items(), key=lambda x: x[1])[:25]:
    negativs.append(best_negative)

neg = dict(negativs)


def word_feats(words):
    '''
    Принимает список на вход, возвращает словарь формата {word:True}
    :param words: array
    :return: dict
    '''
    return dict([(word, True) for word in words])


# Приводим слова из словоря к формату ({'w': True, 'o': True, 'r': True, 'd': True}, 'pos')
positive_features = [(word_feats(p), 'pos') for p in pos]
negative_features = [(word_feats(n), 'neg') for n in neg]

word_set = positive_features + negative_features

classifier = NaiveBayesClassifier.train(word_set)
