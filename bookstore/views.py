import datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Books, Borrow , UserProfile, CustomUser
from .serializers import BookSerializers,UserProfileSerializers
from .serializers import BorrowSerializers
from .serializers import UserSerializer
from .serializers import UserLoginSerializer, UserRegisterSerializer
from django.contrib.auth import login
from datetime import datetime
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BookFilter


# Create your views here.

#Logical View for Books
class BookListCreateAPIView(generics.ListCreateAPIView):
  queryset = Books.objects.all()
  serializer_class = BookSerializers
  # permission_classes  = [IsAuthenticated]
  
class BookRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Books.objects.all()
  serializer_class = BookSerializers
  # permission_classes = [IsAuthenticated]
  


#LOGICAL VIEW FOR BORROW

class BorrowListCreateAPIView(generics.ListCreateAPIView):
  queryset = Borrow.objects.all()
  serializer_class = BorrowSerializers
  # permission_classes = [IsAuthenticated]
  
class BorrowRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Borrow.objects.all()
  serializer_class = BorrowSerializers
  # permission_classes = [IsAuthenticated]
  
  
#FOR BORROWBOOK  
  
class borrow_book(APIView):
  def post(self, request):
    book_id = request.data.get('book_id')
    user_id = request.data.get('user_id')
    due_date = request.data.get('due_date')

    try:
        book = Books.objects.get(id=book_id)
    except Books.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    if book.quantity <= 0:
        return Response({'error': 'Book not available for borrowing'}, status=status.HTTP_400_BAD_REQUEST)

    # Decrement book quantity
    book.quantity -= 1
    book.save()

    borrow = Borrow.objects.create(user_id=user_id, book=book, due_date=due_date)
    serializer = BorrowSerializers(borrow)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  
# FOR RETURN BOOK

class return_book(APIView):
  def post(self, request):
  
    borrow_id = request.data.get('borrow_id')

    try:
        borrow = Borrow.objects.get(id=borrow_id)
    except Borrow.DoesNotExist:
        return Response({'error': 'Borrow record not found'}, status=status.HTTP_404_NOT_FOUND)

    if borrow.returned_date is not None:
        return Response({'error': 'Book already returned'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    current_date = timezone.now().date()

    # Calculate fine if the book is returned late
    if current_date > borrow.due_date:
        days_late = (current_date - borrow.due_date).days
        fine_amount = days_late *10 # Define FINE_PER_DAY as your fine amount per day

        # Apply the fine to the user's account or handle it as per your system's logic
        # For example, deducting the fine from the user's balance
        borrow.user.balance -= fine_amount
        borrow.user.save()

        # You can also store the fine amount in the borrow record if needed
        borrow.fine_amount = fine_amount


    # Increment book quantity
    borrow.book.quantity += 1
    borrow.book.save()

    borrow.returned_date = datetime.now().date()
    borrow.save()

    serializer = BorrowSerializers(borrow)
    return Response(serializer.data, status=status.HTTP_200_OK)

  
#For BORROWED BOOKLIST

class borrowListView(APIView):
  def get(self, request, *args, **kwargs):
    user_id = request.query_params.get('user_id')
    book_id = request.query_params.get('book_id')
   
    
    
    borrow_book = Borrow.objects.all()
    
    if user_id:
      borrowed_book = borrow_book.filter(borrower_id= user_id)
      
    if book_id:
      borrowed_book = borrowed_book.filter(book_id= book_id)
      
    serializer =  BorrowSerializers(borrow_book, many=True)
    return Response(serializer.data) 
  
 
#For filtering
class bookListAPIView(generics.ListAPIView):
  queryset = Books.objects.all()
  serializer_class = BookSerializers
  filter_backends = [DjangoFilterBackend]
  filterset_class = BookFilter
  
#LOGICAL VIEW FOR USERPROFILE
class UserProfileListCreateAPIView(generics.ListCreateAPIView):
  queryset = UserProfile.objects.all()
  serializer_class = UserProfileSerializers
  permission_classes = [IsAuthenticated]
  
class UserProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = UserProfile.objects.all()
  serializer_class = UserProfileSerializers
  permission_classes = [IsAuthenticated]
  
  
  
  
#LOGICAL VIEW FOR CUSTOMUSER 
class UserListCreateAPIView(generics.ListCreateAPIView):
  queryset = CustomUser.objects.all()
  serializer_class = UserSerializer
  permission_classes = [IsAuthenticated]  # Adjust permissions as needed

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Adjust permissions as needed
 
    
#FOR LOGIN   
class UserLoginAPIView(APIView):
  def post(self, request):
    serializers = UserLoginSerializer(data = request.data)
    serializers.is_valid(raise_exception=True)
    user = serializers.user
    login(request, user)
    
    response = Response(serializers.login())
    response.set_cookie(key='access_token', value=serializers.data['access'], httponly=True)
    return response


#FOR REGISTRATION
class UserRegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        print(f'sdddddd{request.data}')
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    