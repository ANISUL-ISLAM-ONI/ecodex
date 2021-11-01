'''
def seethecontent(product):
    print(product)
    print(type(product))
    print(product.id)
    print(product.title)
    print(type(product.title))
    print(product.description)
    print(type(product.description))
'''

def include_cluster(i, terms, order_centroids):
    li = list()
    for ind in order_centroids[i, :10]:
        li.append(terms[ind])
    return li

def show_recommendations(product, vectorizer, model, terms, order_centroids):
    Y = vectorizer.transform([product])
    prediction = model.predict(Y)
    return include_cluster(prediction[0], terms, order_centroids)


def seethecontent(primaryproduct):
    from oscar.apps.catalogue.models import Product, ProductRecommendation
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

    true_k = 0
    if(products.count() < 4):
        true_k = products.count()
    else:
        true_k = 4
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X1)
    # print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()

    clusterlist = show_recommendations(primaryproduct.title, vectorizer, model, terms, order_centroids) + show_recommendations(re.sub('<.*?>', '', primaryproduct.description), vectorizer, model, terms, order_centroids)
    # print(li)
    temppro = Product.objects.filter(title__contains=clusterlist[0]) | Product.objects.filter(description__contains=clusterlist[0])
    for i in range(1, len(clusterlist)):
        temppro = temppro | Product.objects.filter(title__contains=clusterlist[i]) | Product.objects.filter(description__contains=clusterlist[0])

    # print(temppro)
    for pro in temppro:
        if(pro != primaryproduct):
            try:
                ProductRecommendation(primary=primaryproduct, recommendation=pro, ranking=1).save()
            except:
                pass

