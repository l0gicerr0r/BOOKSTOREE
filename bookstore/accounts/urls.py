
# from django.contrib import admin
# from django.urls import path
# from accounts.views import register_view, login_view, logout_view,user_home, landing_page,borrow_book
# from . import views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('register/', register_view, name='register'),
#     path('login/', login_view, name='login'),
#     path('logout/', logout_view, name='logout'),
  
#     path('user-home/', views.user_home, name='user_home'),
#     path('', landing_page, name='landing'),  # Landing page
    
   
#   # User home after login
#     path('', user_home, name='user_home'),
#     path('borrow/<str:book_title>/', borrow_book, name='borrow_book'),
# ]








# # userrrr login pageee  homeeeeeeeeee

from django.contrib import admin
from django.urls import path
from accounts.views import register_view, login_view, logout_view, user_home, landing_page,borrow_book
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication Routes
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Pages
    path('', landing_page, name='landing'),  # Default home page before login
    path('user-home/', user_home, name='user_home'),  # User home after login

    # Borrow book route
    # path('borrow/<str:book_title>/', borrow_book, name='borrow_book'),
    # path('borrow/<str:book_id>/', borrow_book, name='borrow_book'),
    path('borrow/<str:book_id>/', borrow_book, name='borrow_book'),
    


    path('borrow/', views.display_borrowed_books, name='display_borrowed_books'),


    



]

