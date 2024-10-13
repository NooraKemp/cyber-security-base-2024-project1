from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import connection
from .models import Note

@login_required
def index(request):
  user = User.objects.get(username=request.user)
  notes = Note.objects.filter(owner=request.user)
  context = {'notes':notes, 'user':user}
  return render(request, 'notes/index.html', context)

# Flaw 1 CSRF: GET request
# Flaw 3 Broken access control: User parameter can be modified in URL (line 18)
@login_required
def addnote(request):
  user = User.objects.get(username=request.GET.get('user'))
  noteText = request.GET.get('noteText')
  note = Note(owner=user, note=noteText)
  note.save()
  return redirect('/')

# Flaw 1 fix: Use POST request instead of GET
# Flaw 3 fix: User is now logged in user (user = User.objects.get(username=request.user))
# @login_required
# def addnote(request):
#     if request.method == 'POST':
#         user = User.objects.get(username=request.user)
#         noteText = request.POST.get('noteText')
#         note = Note(owner=user, note=noteText)
#         note.save()
#     return redirect('/')

@login_required
def deletenote(request):
  if request.method == 'POST':
    noteId = request.POST.get('noteId')
    if noteId:
      with connection.cursor() as cursor:
        # Flaw 2: SQL Injection Vulnerability
        cursor.execute(f"DELETE FROM notes_note WHERE id = {noteId} AND owner_id = {request.user.id}")
  return redirect('/')

# Flaw 2 fix:
# @login_required
# def deletenote(request):
#   if request.method == 'POST':
#         noteId = request.POST.get('noteId')
#         if noteId:
#             note = get_object_or_404(Note, pk=noteId)
#             if note.owner == request.user:
#                 note.delete()
#   return redirect('/')
