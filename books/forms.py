from django import forms
from .models import Book, Author

class BookForm(forms.ModelForm):
    authors_input = forms.CharField(
        label="Authors",
        help_text="Enter author names separated by commas"
    )

    class Meta:
        model = Book
        fields = ['title', 'price', 'published_date', 'category']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_authors_input(self):
        names = self.cleaned_data['authors_input'].split(',')
        authors = []
        for name in names:
            name = name.strip()
            try:
                first_name, last_name = name.split(' ', 1)
            except ValueError:
                raise forms.ValidationError(f"Author '{name}' must include first and last name")
            try:
                author = Author.objects.get(first_name=first_name, last_name=last_name)
            except Author.DoesNotExist:
                raise forms.ValidationError(f"Author '{name}' does not exist")
            authors.append(author)
        return authors

    def save(self, commit=True):
        book = super().save(commit=False)
        if commit:
            book.save()
        authors = self.cleaned_data['authors_input']
        book.authors.set(authors)
        return book

class BookSearch(forms.Form):
    query = forms.CharField(
        label='Search',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Book title or author name'})
    )