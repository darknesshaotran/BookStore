from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.registerForm,name="register"),
    path('register/addUser/', views.registerMember, name='addUser'),
    path('login/', views.loginn.as_view(), name='login'),
    path('logoutUser/', views.logoutUser, name='logout'),
    path('', views.homePage, name='home'),
    path('update_item_cart/<int:userId>/<int:bookId>',views.UpdateItemCart,name='updateItemCart'),
    path('cart/',views.cart,name='cart'),
    path('UpItem/<int:userId>/<int:bookId>',views.upItem,name='up'),
    path('DownItem/<int:userId>/<int:bookId>',views.downItem,name='down'),
    path('checkout/',views.checkout,name='checkout'),
    path('ordered/<int:userId>',views.ordered,name='ordered'), 
    path('history',views.history,name="history"),
    path('history/<int:orderID>',views.detail,name="detail"),
    path('profile',views.profile,name="profile"),
    path('profile/updateForm',views.UpdateProfileForm,name="updateprofileForm"),
    path('profile/update',views.UpdateProfile,name="updateprofile"),
    path('profile/changepassForm',views.changepassForm,name="changepassForm"),
    path('profile/change',views.changePass,name="changePass"),
    path('detail/<int:bookID>',views.detailProduct,name="detailProduct"),
    
    

]