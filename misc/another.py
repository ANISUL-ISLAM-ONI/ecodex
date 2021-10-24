from oscar.apps.catalogue.models import Product, ProductRecommendation

primary_product = Product.objects.all()[0]
recommended_product = Product.objects.all()[1]

recom = ProductRecommendation()

recom.primary = recommended_product

recom.recommendation = recommended_product

recom.ranking = 1

recom.save()


