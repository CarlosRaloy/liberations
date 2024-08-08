"""
== template_django URL's Configuration ==

Note: Configuration on paths example:
path('my_path/', include([file urls.py of my app], [Name app]), namespace = [any_name])),
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include(('aplications.releases.urls', 'releases'), namespace='settings')),
                  path('users/', include(('aplications.users.urls', 'users'), namespace='users')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
