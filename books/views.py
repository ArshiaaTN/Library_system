from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Author
from .forms import BookForm
from django.shortcuts import render
from .models import Book, Author
from .forms import BookSearch

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})

def book_list(request):
    form = BookSearch(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query', '').strip()
        if query:
            books = books.filter(
                title__icontains=query
         ) | books.filter(
                authors__first_name__icontains=query
            ) | books.filter(
                authors__last_name__icontains=query
            )
            books = books.distinct()

    return render(request, 'books/book_list.html', {'books': books, 'form': form})

def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('library_detail', pk=book.libraries.first().pk if book.libraries.exists() else 'library_list')
    else:
        initial_authors = ', '.join([f"{a.first_name} {a.last_name}" for a in book.authors.all()])
        form = BookForm(instance=book, initial={'authors_input': initial_authors})
    return render(request, 'books/edit_book.html', {'form': form, 'book': book})

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        library_pk = book.libraries.first().pk if book.libraries.exists() else None
        book.delete()
        return redirect('library_detail', pk=library_pk if library_pk else 'library_list')
    return render(request, 'books/delete_book.html', {'book': book})