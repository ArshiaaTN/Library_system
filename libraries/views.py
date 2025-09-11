from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Library
from .forms import LibraryForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Library
from books.forms import BookForm

def library_detail(request, pk):
    library = get_object_or_404(Library, pk=pk)
    books = library.books.all()

    query = request.GET.get('q')
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(authors__first_name__icontains=query) |
            Q(authors__last_name__icontains=query)
        ).distinct()

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            library.books.add(book)
            return redirect('library_detail', pk=library.pk)
    else:
        form = BookForm()

    return render(request, 'libraries/library_detail.html', {
        'library': library,
        'form': form,
        'books': books,
        'query': query,
    })


def add_library(request):
    if request.method == 'POST':
        form = LibraryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('library_list')
    else:
        form = LibraryForm()
    return render(request, 'libraries/add_library.html', {'form': form})

def library_list(request):
    libraries = Library.objects.all()
    return render(request, 'libraries/library_list.html', {'libraries': libraries})

from django.shortcuts import get_object_or_404, redirect

def add_book_to_library(request, library_pk):
    library = get_object_or_404(Library, pk=library_pk)
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            library.books.add(book)
            return redirect('library_detail', pk=library.pk)
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form, 'library': library})

