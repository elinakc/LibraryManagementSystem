from rest_framework import serializers

from .models import Books, Borrow, UserProfile
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser


# Serializer for books
class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = "__all__"
        
    


# SERIALIZER FOR BORROW
class BorrowSerializers(serializers.ModelSerializer):
  book_name = serializers.CharField(source ='book.book_name', read_only=True)
  borrow_username = serializers.CharField(source = 'user.username', read_only=True)
  
  
  class Meta:
        model = Borrow
        fields = "__all__"
        


# SERIALIZER FOR USERPROFILE
class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"




# SERIALIZER FOR USERLOGIN AND FOR USERREGISTRATION

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email"]
        
class UserRegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(max_length= 200, write_only = True)
  username = serializers.CharField(max_length = 200, write_only = True)
  
  class Meta:
        model = CustomUser
        fields = ["id", "username", "password","email" ]
        
  def validate(self, attrs):
        if attrs['password'] != attrs['password']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

  def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        UserProfile.objects.create(user=user)  # Create a corresponding user profile
        return user

      
        
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required")

        user = CustomUser.objects.filter(username=username).first()

        print(user)
        
        if user is None:
            raise serializers.ValidationError("User doesnot exist.")

        if not password == user.password:
            raise serializers.ValidationError("Incorrect password")

        self.user = user
        return data

    def login(self):
        refresh = RefreshToken.for_user(self.user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }




