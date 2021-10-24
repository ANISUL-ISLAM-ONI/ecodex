from oscar.apps.catalogue.models import Product
from django.core import serializers
import pandas as pd
import json
import re

products = Product.objects.all()
data = serializers.serialize('json', products, fields=('title', 'description', 'product_class', 'rating'))
datadic = json.loads(data)
dataactual = list()
for prod in datadic :
    dataactual.append({'product_id' : prod['pk'], 'title' : prod['fields']['title'], 'description' : re.sub('<.*?>', '', prod['fields']['description']), 'product_class' : prod['fields']['product_class'], 'rating' : float(0.0 if prod['fields']['rating'] is None else prod['fields']['rating']),})

df = pd.DataFrame(dataactual)
