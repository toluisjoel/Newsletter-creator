from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register('news', views.PostViewset, basename='news')
router.register('subscribers', views.SubscriberViewset, basename='email')

urlpatterns = router.urls
