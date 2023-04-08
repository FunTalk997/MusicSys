from django.urls import path

from API import views

urlpatterns = [
    path('music/', views.MusicView.as_view()),
    path('music/detail/', views.MusicById.as_view()),

    path('collect/', views.CollectView.as_view()),

    path('comment/', views.CommentView.as_view()),
    path('music/comment/', views.CommentByMusicId.as_view()),

    path('user/', views.UserView.as_view()),
    path('userLogin/', views.UserLoginView.as_view()),
    path('userInfo/', views.UserInfoView.as_view()),
    path('userPwd/', views.UserPwdView.as_view()),

    path('adminLogin/', views.AdminLoginView.as_view()),
    path('adminPwd/', views.AdminPwdView.as_view()),

    path('carousel/', views.CarouselView.as_view()),
    path('newSongs/', views.NewSongsView.as_view()),
    path('topSongs/', views.TopSongsView.as_view()),

    path('upload/', views.UploadView.as_view())
]
