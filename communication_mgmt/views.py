from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Notice, Message, Event

@login_required
def notice_list(request):
    notices = Notice.objects.filter(is_active=True).order_by('-published_at')
    return render(request, 'communication_mgmt/notice_list.html', {'notices': notices})

@login_required
def notice_add(request):
    from student_mgmt.models import Class
    classes = Class.objects.all()
    if request.method == 'POST':
        Notice.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            audience=request.POST.get('audience', 'all'),
            priority=request.POST.get('priority', 'medium'),
            expiry_date=request.POST.get('expiry_date') or None,
            published_by=request.user,
        )
        messages.success(request, 'Notice posted successfully!')
        return redirect('notice_list')
    return render(request, 'communication_mgmt/notice_add.html', {'classes': classes})

@login_required
def notice_delete(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        notice.is_active = False
        notice.save()
        messages.success(request, 'Notice removed.')
    return redirect('notice_list')

@login_required
def message_list(request):
    received = Message.objects.filter(receiver=request.user).order_by('-sent_at')
    sent = Message.objects.filter(sender=request.user).order_by('-sent_at')
    unread_count = received.filter(is_read=False).count()
    # mark as read
    received.filter(is_read=False).update(is_read=True)
    return render(request, 'communication_mgmt/messages.html', {
        'received': received, 'sent': sent, 'unread_count': unread_count
    })

@login_required
def message_send(request):
    users = User.objects.exclude(id=request.user.id).order_by('username')
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver')
        subject = request.POST.get('subject', '').strip()
        content = request.POST.get('content', '').strip()
        if receiver_id and subject and content:
            Message.objects.create(
                sender=request.user,
                receiver_id=receiver_id,
                subject=subject,
                content=content,
            )
            messages.success(request, 'Message sent successfully!')
            return redirect('message_list')
        else:
            messages.error(request, 'Please fill all fields.')
    return render(request, 'communication_mgmt/message_send.html', {'users': users})

@login_required
def events_list(request):
    from django.utils import timezone
    upcoming = Event.objects.filter(event_date__gte=timezone.now().date()).order_by('event_date')
    past = Event.objects.filter(event_date__lt=timezone.now().date()).order_by('-event_date')[:10]
    return render(request, 'communication_mgmt/events.html', {'upcoming': upcoming, 'past': past})

@login_required
def event_add(request):
    if request.method == 'POST':
        Event.objects.create(
            name=request.POST['name'],
            description=request.POST.get('description', ''),
            event_date=request.POST['event_date'],
            end_date=request.POST.get('end_date') or None,
            venue=request.POST.get('venue', ''),
            organized_by=request.POST.get('organized_by', ''),
            is_holiday=request.POST.get('is_holiday') == 'on',
        )
        messages.success(request, 'Event added!')
        return redirect('events_list')
    return render(request, 'communication_mgmt/event_add.html')
