from django.urls import path
from .views import PostList, PostDetail, create_news, PostCreate, PostUpdate, PostDelete

urlpatterns = [path('', PostList.as_view()),
            path('<int:pk>', PostDetail.as_view(), name= 'news'),
            path('create/', create_news, name='news'),
            path('create2/', PostCreate.as_view(), name='post_create'),
            path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
            path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]