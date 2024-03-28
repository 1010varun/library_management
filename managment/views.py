from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework import permissions

from .models import Book
from .serializers import BookSerializer



class BookList(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    books = Book.objects.all().order_by('title')
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

  def post(self, request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response(serializer.data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)



class BookDetail(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get_object(self, isbn):
    try:
      return Book.objects.get(isbn=isbn)
    except Book.DoesNotExist:
      return None

  def get(self, request, isbn):
    book = self.get_object(isbn)
    if not book:
      return Response(status=HTTP_404_NOT_FOUND)
    serializer = BookSerializer(book)
    return Response(serializer.data)

  def put(self, request, isbn):
    book = self.get_object(isbn)
    if not book:
      return Response(status=HTTP_404_NOT_FOUND)
    serializer = BookSerializer(book, data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

  def delete(self, request, isbn):
    book = self.get_object(isbn)
    if not book:
      return Response(status=HTTP_404_NOT_FOUND)
    book.delete()
    return Response(status=HTTP_204_NO_CONTENT)
