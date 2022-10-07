from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register('news', views.PostViewset, basename='news')
router.register('emails', views.EmailViewset, basename='email')

urlpatterns = router.urls
