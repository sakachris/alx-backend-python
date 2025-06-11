from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import render
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
