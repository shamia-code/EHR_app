from django.contrib import admin
# Use include() to add paths from the catalog application
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('patients.urls')),
    path('accounts/', include('accounts.urls')),
]