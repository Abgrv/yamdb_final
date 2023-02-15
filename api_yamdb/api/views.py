from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from api.filters import TitleFilter
from api.mixins import MixinViewSet
from reviews.models import Category, Genre, Review, Title
from users.permissions import (IsAdmin, IsAdminOrReadOnly,
                               IsReadOnlyOrIsAuthorOrIsModerator)

from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, RegistrationSerializer,
                          ReviewSerializer, TitleCreateSerializer,
                          TitleSerializer, TokenSerializer, UserSerializer)

User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class GenreViewSet(MixinViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(MixinViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsReadOnlyOrIsAuthorOrIsModerator
    ]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(
            author=self.request.user, title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsReadOnlyOrIsAuthorOrIsModerator
    ]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        return review.comments.select_related('author').all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        permission_classes=(IsAuthenticated,),
        serializer_class=UserSerializer,
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegistrationApiView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        """Функция создания нового пользователя"""
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(password='', confirmation_code='')

        username = request.data.get('username')
        email = request.data.get('email')
        user = get_object_or_404(User, username=username, email=email)

        confirmation_code = default_token_generator.make_token(user)

        user.password = confirmation_code
        user.confirmation_code = confirmation_code
        user.save()
        try:
            send_mail(
                'Код подтверждения',
                confirmation_code,
                settings.EMAIL_HOST_USER,
                [email]
            )
        except SMTPException as e:
            return Response({'error': e},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetTokenApiView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        serializer = TokenSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(
            User,
            username=username,
        )

        if confirmation_code == user.confirmation_code:
            token = AccessToken.for_user(user)
            token_data = {'token': str(token)}
            return Response(token_data, status=status.HTTP_200_OK)
        return Response(
            'Введен неверный код подтверждения',
            status=status.HTTP_400_BAD_REQUEST
        )
