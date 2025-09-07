from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('accounts.urls', namespace='accounts')),
    path('user/files/', include(('file.urls', 'files'),namespace='user-files')),
    path('user/folders/', include(('folder.urls', 'folders'), namespace='user-folders')),

    path('group/', include('group.urls', namespace='groups')),

    path('group/<int:group_id>/files/', include(('file.urls', 'files'), namespace='group-files')),
    path('group/<int:group_id>/folders/', include(('folder.urls', 'folders'), namespace='group-folders')),


    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
