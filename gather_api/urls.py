from django.conf.urls import url, include
from rest_framework.authtoken import views as rest_auth
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from gather_api import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'nodes', views.NodeViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'connections', views.ConnectionViewSet)
router.register(r'messages', views.MessageViewSet)

schema_view = get_schema_view(title='Pastebin API')


# The API URLs are now determined automatically by the router.
urlpatterns = [

    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^api-token-auth/', rest_auth.obtain_auth_token),
    url(r'^schema/$', schema_view),
    url(r'^', include(router.urls))
]
