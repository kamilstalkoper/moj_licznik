#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.generic import ListView, DetailView, View, FormView

from ..forms import AddUserForm


@method_decorator(staff_member_required(login_url='authentication:auth_login'),
                  name='dispatch')
class UsersListView(ListView):
    context_object_name = 'users'
    http_method_names = [u'get', ]
    model = User
    page_kwarg = 'strona'
    paginate_by = 10
    template_name = 'backend/accounts/users_list.html'

    def get_queryset(self):
        return User.objects.all().exclude(id=self.request.user.id)


class SearchUsersView(UsersListView):
    search_phrase = None

    def get(self, request, *args, **kwargs):
        self.search_phrase = escape(request.GET.get('q', ''))
        return super(SearchUsersView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SearchUsersView, self).get_context_data(**kwargs)
        if not self.search_phrase:
            return context

        context.update({
            'is_searched': True,
            'search_phrase': self.search_phrase,
        })
        return context

    def get_queryset(self):
        qs = super(SearchUsersView, self).get_queryset()
        if not self.search_phrase:
            return qs

        return qs.filter(
            Q(username__icontains=self.search_phrase) |
            Q(email__icontains=self.search_phrase) |
            Q(first_name__icontains=self.search_phrase) |
            Q(last_name__icontains=self.search_phrase)
        )


@method_decorator(staff_member_required(login_url='authentication:auth_login'),
                  name='dispatch')
class ShowUserProfileView(DetailView):
    template_name = 'backend/accounts/user_profile.html'
    http_method_names = [u'get', ]
    context_object_name = 'editing_user'
    model = User
    pk_url_kwarg = 'user_id'

    def get_queryset(self):
        return User.objects.all().exclude(id=self.request.user.id)


@method_decorator(staff_member_required(login_url='authentication:auth_login'),
                  name='dispatch')
class ChangeUserStatusView(View):
    http_method_names = [u'post', ]

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        if user_id is not None and user_id != self.request.user.id:
            user = User.objects.filter(id=user_id).first()
            if user is not None:
                user.is_active = not user.is_active
                user.save()

        return redirect('backend:show_user_profile_view', user_id=user_id)


@method_decorator(staff_member_required(login_url='authentication:auth_login'),
                  name='dispatch')
class AddUserView(FormView):
    form_class = AddUserForm
    template_name = 'backend/accounts/add_user.html'
    http_method_names = [u'get', u'post']

    def form_valid(self, form):
        user = form.save()
        user = authenticate(
            username=user.username, password=form.cleaned_data.get('password1'))
        return redirect('backend:show_user_profile_view', user_id=user.id)
