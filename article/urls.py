from rest_framework import routers
from article import views


app_name = "article"

router = routers.DefaultRouter()
router.register(r'article', views.ArticleView, basename='article')

urlpatterns = router.urls
