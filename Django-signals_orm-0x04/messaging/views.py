# messaging/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from .models import Message


@login_required
def delete_user(request):
    user = request.user
    logout(request)  # Logs out before deletion
    user.delete()
    return redirect("account_deleted")  # Create this template/page


@login_required
def inbox(request):
    messages = (
        Message.objects.filter(
            receiver=request.user, parent_message__isnull=True
        )  # Top-level messages
        .select_related("sender", "receiver")
        .prefetch_related("replies__sender")  # Replies + sender info
        .order_by("-timestamp")
    )
    return render(request, "messaging/inbox.html", {"messages": messages})


@require_POST
@login_required
def send_message(request):
    receiver_id = request.POST.get("receiver_id")
    content = request.POST.get("content")
    parent_message_id = request.POST.get("parent_message_id")  # optional

    if not (receiver_id and content):
        return redirect("inbox")  # or return an error

    try:
        receiver = User.objects.get(id=receiver_id)
    except User.DoesNotExist:
        return redirect("inbox")  # or return an error

    parent_message = None
    if parent_message_id:
        try:
            parent_message = Message.objects.get(id=parent_message_id)
        except Message.DoesNotExist:
            parent_message = None  # silently ignore

    Message.objects.create(
        sender=request.user,
        receiver=receiver,
        content=content,
        parent_message=parent_message,
    )

    return HttpResponseRedirect("/messaging/inbox/")


@login_required
def unread_messages(request):
    unread_msgs = Message.unread.unread_for_user(request.user)
    return render(request, "messaging/unread.html", {"unread_messages": unread_msgs})
