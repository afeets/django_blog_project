from django.shortcuts import render
from django.contrib import messages # return messages back to user
# Create your views here.
from django.contrib.auth.mixins import (LoginRequiredMixin,PermissionRequiredMixin)

from django.urls import reverse
from django.views import generic
from django.shortcuts import get_object_or_404
from groups.models import Group,GroupMember
from . import models

# Class based views
class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields = ('name','description') # fields that can be edited
    model = Group

class SingleGroup(generic.DetailView):
    model = Group

class ListGroups(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            # Get groupmember objects where user is equal to current user and group is equal to group
            GroupMember.objects.create(user=self.request.user,group=group)
        except:
            messages.warning(self.request,('You are already a member'))
        else:
            messages.success(self.request,('You are now a member'))

        return super().get(request,*args,**kwargs)

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        try:
            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,'Sorry you are not in this group')
        else:
            membership.delete()
            messages.success(self.request,'You have now left the group')

        return super().get(request,*args,**kwargs)
