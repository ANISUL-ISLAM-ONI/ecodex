from oscar.apps.catalogue.models import Product
from django.core import serializers
import pandas as pd
import json
import re

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score


products = Product.objects.all()
data = serializers.serialize('json', products, fields=('title', 'description', 'product_class', 'rating'))
datadic = json.loads(data)
dataactual = list()
for prod in datadic :
    dataactual.append({'product_id' : prod['pk'], 'titledescription' : prod['fields']['title'] + ' ' + re.sub('<.*?>', '', prod['fields']['description'])})

df = pd.DataFrame(dataactual)

vectorizer = TfidfVectorizer(stop_words='english')

X1 = vectorizer.fit_transform(df['titledescription'])


def include_cluster(i):
    li = list()
    for ind in order_centroids[i, :10]:
        li.append(terms[ind])
    return li

true_k = 4
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X1)
print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()

#for i in range(true_k):
#    print_cluster(i)

def show_recommendations(product):
    Y = vectorizer.transform([product])
    prediction = model.predict(Y)
    return include_cluster(prediction[0])

