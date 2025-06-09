from django.urls import path

from .views import (AuthorCreateView, AuthorListView, AuthorUpdateView,
                    BookCreateView, BookDeleteView, BookDetailView,
                    BooksListView, BookUpdateView, RecommendBookView,
                    ReviewBookView)

app_name = "library"

urlpatterns = [
    path("books/", BooksListView.as_view(), name="books_list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("books/new/", BookCreateView.as_view(), name="book_create"),
    path("books/<int:pk>/edit/", BookUpdateView.as_view(), name="book_edit"),
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="book_delete"),
    path("authors/", AuthorListView.as_view(), name="authors_list"),
    path("authors/create", AuthorCreateView.as_view(), name="authors_create"),
    path("authors/<int:pk>/edit/", AuthorUpdateView.as_view(), name="authors_update"),
    path("books/review/<int:pk>/", ReviewBookView.as_view(), name="book_review"),
    path(
        "books/recommend/<int:pk>/", RecommendBookView.as_view(), name="book_recommend"
    ),
]
