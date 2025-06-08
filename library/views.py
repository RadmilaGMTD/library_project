from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Author, Book
from .forms import AuthorForm, BookForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .services import BookService


class ReviewBookView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, id=pk)

        if not request.user.has_perm("library.can_review_book"):
            return HttpResponseForbidden("У вас нет прав для рецензирования книги.")

        book.review = request.POST.get("review")
        book.save()
        return redirect("library:book_detail", pk=pk)


class RecommendBookView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, id=pk)

        if not request.user.has_perm("library.can_recommend_book"):
            return HttpResponseForbidden("У вас нет прав для рекомендации  книги.")

        book.recommend = True
        book.save()
        return redirect("library:book_detail", pk=pk)


class AuthorListView(ListView):
    model = Author
    template_name = "library/authors_list.html"
    context_object_name = "authors"

    def get_queryset(self):
        queryset = cache.get("authors_queryset")
        if not queryset:
            queryset = super().get_queryset()
            cache.set("authors_queryset", queryset, 60 * 15)

        return queryset


class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = "library/author_form.html"
    success_url = reverse_lazy("library:authors_list")


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = "library/author_form.html"
    success_url = reverse_lazy("library:authors_list")


class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "library/book_form.html"
    success_url = reverse_lazy("library:books_list")
    permission_required = "library.add_book"


class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "library/book_form.html"
    success_url = reverse_lazy("library:books_list")
    permission_required = "library.change_book"


@method_decorator(cache_page(60 * 15), name="dispatch")
class BooksListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = "library/books_list.html"
    context_object_name = "books"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(publication_date__year__gt=1900)


@method_decorator(cache_page(60 * 15), name="dispatch")
class BookDetailView(DetailView):
    model = Book
    template_name = "library/book_detail.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author_books_count"] = Book.objects.filter(
            author=self.object.author
        ).count()
        book_id = self.object.id
        context["average_rating"] = BookService.calculate_average_rating(book_id)
        context["is_popular"] = BookService.is_popular(book_id)
        return context


class BookDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    model = Book
    template_name = "library/books_confirm_delete.html"
    success_url = reverse_lazy("library:books_list")
    permission_required = "library.delete_book"
