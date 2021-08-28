"""xix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.apps import apps
from django.conf import settings, urls
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import views
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog
from oscar.views import handler403, handler404, handler500

from apps.sitemaps import base_sitemaps

admin.autodiscover()

urlpatterns = [
    # Include admin as convenience. It's unsupported and only included
    # for developers.
    path('admin/', admin.site.urls),

    # i18n URLS need to live outside of i18n_patterns scope of Oscar
    path('i18n/', include(urls.i18n)),

    # include a basic sitemap
    path('sitemap.xml', views.index,
        {'sitemaps': base_sitemaps}),
    path('sitemap-<slug:section>.xml', views.sitemap,
        {'sitemaps': base_sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
]

# Prefix Oscar URLs with language codes
urlpatterns += i18n_patterns(
    path('', include(apps.get_app_config('oscar').urls[0])),
    path('dashboard/stores/', apps.get_app_config('stores_dashboard').urls),
    path('stores/', apps.get_app_config('stores').urls),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
)

if settings.DEBUG:
    import debug_toolbar

    # Server statics and uploaded media
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Allow error pages to be tested
    urlpatterns += [
        path('403', handler403, {'exception': Exception()}),
        path('404', handler404, {'exception': Exception()}),
        path('500', handler500),
        path('__debug__/', include(debug_toolbar.urls)),
    ]
