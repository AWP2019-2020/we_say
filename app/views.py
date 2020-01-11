from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView

from app.models import User, Poll, Vote, Theme


def index(request):
    if request.GET.get('sort') == '1':
        posts = Poll.objects.all().order_by("-created_at")[:10]
    elif request.GET.get('sort') == '2':
        posts = Poll.objects.all().annotate(num_voters=Count('votes')).order_by('-num_voters')[:10]
    else:
        posts = Poll.objects.all().order_by("-created_at")[:10]

    return render(request, 'home.html', context={'polls':posts})

def themePage(request, theme_key):
    if request.GET.get('sort') == '1':
        posts = Poll.objects.filter(theme_id=theme_key).order_by("-created_at")[:10]
    elif request.GET.get('sort') == '2':
        posts = Poll.objects.filter(theme_id=theme_key).annotate(num_voters=Count('votes')).order_by('-num_voters')[:10]
    else:
        posts = Poll.objects.filter(theme_id=theme_key).order_by("-created_at")[:10]

    return render(request, 'home.html', context={'polls':posts})

class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    model = User

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(username=data['username'],
                                        password=data['password1'])
        return redirect('home')


class LoginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self):
        form = AuthenticationForm()
        return {'form': form}

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'],
                                password=data['password'])
            login(request, user)
            return redirect(reverse_lazy('home'))
        else:
            return render(request, "login.html", {"form": form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('home'))

class VoteView(View):
    def get(self, request, *args, **kwargs):
        vote = Vote.objects.filter(poll_id=kwargs['pk'], user=request.user).first()
        if not vote:
            vote = Vote.objects.create(poll_id=kwargs['pk'], option=kwargs['rez'], user=request.user)
        else:
            vote.option=kwargs['rez']
            vote.save()
        # return redirect(reverse_lazy('home'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class CancelVote(View):
    def get(self, request, *args, **kwargs):
        vote = Vote.objects.filter(poll_id=kwargs['pk'], user=request.user).first()
        if vote:
            vote.delete()
        # return redirect(reverse_lazy('home'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class CreatePoll(CreateView):
    model = Poll
    fields = ['question', 'text', 'theme']
    template_name = 'createpoll.html'

    def form_valid(self, form):
        Poll.objects.create(
            created_by=self.request.user,
            **form.cleaned_data
        )
        return redirect(reverse_lazy('home'))

class UserProfile(View):
    def get(self, request, *args, **kwargs):
        user_profile = User.objects.filter(id=kwargs['pk']).first()

        return render(request, 'userprofile.html', context={'user_profile':user_profile})

class EditProfile(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'editprofile.html'

    def form_valid(self, form):
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']

        self.object.save()

        return redirect(reverse_lazy('userProfile', kwargs={'pk':self.object.id}))