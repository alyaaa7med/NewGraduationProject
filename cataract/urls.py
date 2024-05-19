from  rest_framework_nested import routers
from accounts.urls import router

from .views import CataractDiseaseView 



user_retina_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
user_retina_router.register(r'retina_images', CataractDiseaseView, basename='retina-image')


urlpatterns = user_retina_router.urls 