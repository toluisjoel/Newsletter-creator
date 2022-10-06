from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register('', views.PostViewset,basename='post')

urlpatterns = router.urls