from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect,render
from .models import Notification
@login_required
def inbox(request): return render(request,"notifications/inbox.html",{"notifications":request.user.notifications.all()[:50]})
@login_required
def mark_read(request,pk):
    n=get_object_or_404(Notification,pk=pk,recipient=request.user); n.is_read=True; n.save(update_fields=["is_read"]); return redirect("notifications:inbox")
