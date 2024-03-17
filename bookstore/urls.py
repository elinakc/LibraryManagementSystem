from django.urls import path
from . import views


urlpatterns = [
     
    path('Books/', views.BookListCreateAPIView.as_view(), name='book_list'),
    path('Books/<int:pk>/', views.BookRetriveUpdateDestroyAPIView.as_view(), name='book_detail'),
    
    path('Borrow/', views.BorrowListCreateAPIView.as_view(), name='borrow_list'),
    path('Borrow/<int:pk>/', views.BorrowRetrieveUpdateDestroyAPIView.as_view(), name='borrow_detail'),
    
    path('Profile/', views.UserProfileListCreateAPIView.as_view(), name='userprofile_list'),
    path('Profile/<int:pk>/', views.UserProfileRetrieveUpdateDestroyAPIView.as_view(), name='userprofile_detail'),
    
    
    path('users/', views.UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view(), name='user-retrieve-update-destroy'),
    
    path('login/', views.UserLoginAPIView.as_view(), name='user-login'),
    path('register/', views.UserRegistrationAPIView.as_view(), name='user-register'),
    
    path('borrow_book/', views.borrow_book.as_view(), name='borrow_book'),
    path('borrowed_booklist/', views.borrowListView.as_view(), name='borrowed_books_list'),
    
    path('return_book/', views.return_book.as_view(), name='return_book'),
    
    path('filter_books/', views.bookListAPIView.as_view(), name='book-list'),
    
]
