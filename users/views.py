from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView, DetailView, UpdateView, ListView

from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm
from users.models import User


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def get_success_url(self):
        return reverse_lazy('users:login', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Регистрация прошла успешно')
        return response


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('films:home')

    def form_valid(self, form):
        from django.contrib.auth import login
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, f'Добро пожаловать, {user.email}!')
        return super().form_valid(form)


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Ждем вас снова!.')
        return super().dispatch(request, *args, **kwargs)


class ProfileView(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['ratings'] = Interaction.objects.filter(
    #         user=self.object
    #     ).select_related('film')
    #     return context


def my_profile_redirect(request):
    return redirect(reverse('users:profile', kwargs={'pk': request.user.pk}))


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.pk})

    def test_func(self):
        return self.get_object() == self.request.user

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Ваш профиль успешно обновлен!')
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Класс для отображения списка пользователей.
    """
    model = User
    permission_required = "users.view_user"
    context_object_name = "users"
