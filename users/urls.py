from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register('', views.EmailViewset, basename='email')

urlpatterns = router.urls