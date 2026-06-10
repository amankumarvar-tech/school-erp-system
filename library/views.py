from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
import datetime
from .models import Book, BookCategory, BookIssue
from student_mgmt.models import Student
from teacher_mgmt.models import Teacher

@login_required
def library_dashboard(request):
    total_books = Book.objects.filter(is_active=True).count()
    total_copies = sum(Book.objects.filter(is_active=True).values_list('total_copies', flat=True))
    issued_count = BookIssue.objects.filter(status='issued').count()
    overdue_count = BookIssue.objects.filter(status='issued', due_date__lt=datetime.date.today()).count()
    recent_issues = BookIssue.objects.select_related('book','student','teacher').order_by('-issue_date')[:10]
    overdue_books = BookIssue.objects.filter(status='issued', due_date__lt=datetime.date.today()).select_related('book','student','teacher')[:8]
    categories = BookCategory.objects.all()
    context = {
        'total_books': total_books, 'total_copies': total_copies,
        'issued_count': issued_count, 'overdue_count': overdue_count,
        'recent_issues': recent_issues, 'overdue_books': overdue_books,
        'categories': categories,
    }
    return render(request, 'library/dashboard.html', context)

@login_required
def book_list(request):
    query = request.GET.get('q','')
    category_id = request.GET.get('category','')
    books = Book.objects.filter(is_active=True).select_related('category')
    if query:
        books = books.filter(Q(title__icontains=query)|Q(author__icontains=query)|Q(isbn__icontains=query))
    if category_id:
        books = books.filter(category_id=category_id)
    categories = BookCategory.objects.all()
    return render(request, 'library/book_list.html', {'books': books, 'query': query, 'categories': categories, 'category_id': category_id})

@login_required
def book_add(request):
    categories = BookCategory.objects.all()
    if request.method == 'POST':
        copies = int(request.POST.get('total_copies', 1))
        Book.objects.create(
            title=request.POST['title'],
            author=request.POST['author'],
            isbn=request.POST.get('isbn',''),
            publisher=request.POST.get('publisher',''),
            publication_year=request.POST.get('publication_year') or None,
            category_id=request.POST.get('category') or None,
            total_copies=copies,
            available_copies=copies,
            shelf_location=request.POST.get('shelf_location',''),
            price=request.POST.get('price',0),
            description=request.POST.get('description',''),
        )
        messages.success(request, 'Book added to library!')
        return redirect('book_list')
    return render(request, 'library/book_add.html', {'categories': categories})

@login_required
def issue_book(request):
    books = Book.objects.filter(is_active=True, available_copies__gt=0)
    students = Student.objects.filter(is_active=True)
    teachers = Teacher.objects.filter(is_active=True)
    if request.method == 'POST':
        book_id = request.POST['book']
        borrower_type = request.POST['borrower_type']
        due_date = request.POST['due_date']
        book = get_object_or_404(Book, pk=book_id)
        if book.available_copies <= 0:
            messages.error(request, 'No copies available!')
            return redirect('issue_book')
        issue = BookIssue(book=book, borrower_type=borrower_type, due_date=due_date,
                         issued_by=request.user.get_full_name() or request.user.username)
        if borrower_type == 'student':
            issue.student_id = request.POST['student']
        else:
            issue.teacher_id = request.POST['teacher']
        issue.save()
        book.available_copies -= 1
        book.save()
        messages.success(request, f'Book "{book.title}" issued successfully!')
        return redirect('issue_list')
    return render(request, 'library/issue_book.html', {'books': books, 'students': students, 'teachers': teachers})

@login_required
def return_book(request, issue_id):
    issue = get_object_or_404(BookIssue, pk=issue_id)
    if request.method == 'POST':
        today = datetime.date.today()
        issue.return_date = today
        issue.status = 'returned'
        if today > issue.due_date:
            days_late = (today - issue.due_date).days
            issue.fine_amount = days_late * 2  # ₹2 per day fine
        issue.save()
        issue.book.available_copies += 1
        issue.book.save()
        messages.success(request, f'Book returned! Fine: ₹{issue.fine_amount}')
        return redirect('issue_list')
    return render(request, 'library/return_book.html', {'issue': issue})

@login_required
def issue_list(request):
    status = request.GET.get('status', '')
    issues = BookIssue.objects.select_related('book','student','teacher').order_by('-issue_date')
    if status:
        issues = issues.filter(status=status)
    # Auto-mark overdue
    today = datetime.date.today()
    issues.filter(status='issued', due_date__lt=today).update(status='overdue')
    return render(request, 'library/issue_list.html', {'issues': issues, 'status': status})
