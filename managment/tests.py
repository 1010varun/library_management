from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Book

class BookListTestCase(APITestCase):

    def setUp(self):
        self.book1 = Book.objects.create(title="Harry Potter", authors="J. K. Rowling", isbn="9780261102694")
        self.book2 = Book.objects.create(title="The Hitchhiker's Guide to the Galaxy", authors="Douglas Adams", isbn="9780345391803")
        self.url = reverse('book-list')

    def test_get_all_books(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], self.book2.title)

    def test_empty_list(self):
        Book.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)



class BookDetailTestCase(APITestCase):

    def setUp(self):
        self.book = Book.objects.create(title="Sample Book Title", authors="varun", isbn="9780316203761")
        self.url = reverse('book-detail', args=[self.book.isbn])

    def test_get_book_by_isbn(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.book.title)

    def test_not_found(self):
        invalid_isbn = "1234567890"
        url = reverse('book-detail', args=[invalid_isbn])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class BookCreateTestCase(APITestCase):

    def test_create_book(self):
        data = {
            "title": "A Brief History of Time",
            "authors": "Stephen Hawking",
            "isbn": "9780553896848",
        }
        response = self.client.post(reverse('book-list'), data=data)
        self.assertEqual(response.status_code, 201)  # Created
        self.assertEqual(Book.objects.count(), 1)
        created_book = Book.objects.get()
        self.assertEqual(created_book.title, data['title'])

    def test_missing_required_field(self):
        data = {"authors": "J. K. Rowling"}  # Missing title
        response = self.client.post(reverse('book-list'), data=data)
        self.assertEqual(response.status_code, 400)  # Bad Request
        self.assertEqual(Book.objects.count(), 0)  # No book created