# ajust_pj/urls.py に以下を追加
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ajust_app.urls')),
]