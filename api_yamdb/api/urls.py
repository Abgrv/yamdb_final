from django.urls import include, path
from rest_framework import routers
from . import views

router_v1 = routers.DefaultRouter()
router_v1.register('categories', views.CategoryViewSet, basename='categories')
router_v1.register('genres', views.GenreViewSet, basename='genre')
router_v1.register('titles', views.TitleViewSet, basename='title')
router_v1.register('users', views.UsersViewSet, basename='users')

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/',
         views.UserRegistrationApiView.as_view(), name='registration'),
    path('v1/auth/token/', views.GetTokenApiView.as_view(), name='token')
]
