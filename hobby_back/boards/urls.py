from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('hobby/', views.postHobby_list.as_view()),
    path('hobby/<int:pk>/', views.postHobby_detail.as_view()),
    path('free/', views.postFree_list.as_view()),
    path('free/<int:pk>/', views.postFree_detail.as_view()),
    path('notice/', views.notice_list.as_view()),
    path('notice/<int:pk>/', views.notice_detail.as_view()),
    path('faq/', views.faq_list.as_view()),
    path('faq/<int:pk>/', views.faq_detail.as_view()),
    path('img/', views.img_list.as_view()),
    path('img/<int:pk>/', views.img_detail.as_view()),
    path('free/<int:pk>/comment', views.commentFree_list.as_view()),
    path('free/<int:pk>/comment/<int:comment_pk>', views.commentFree_detail)
]

urlpatterns = format_suffix_patterns(urlpatterns)
