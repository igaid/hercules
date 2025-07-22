from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import UserAuthenticationForm
from main.models import TrustedUser, AppState
from django.contrib.auth import logout


@login_required()
def info(request):
    user = request.user
    trusted_users = TrustedUser.objects.filter(trusted_user=user, enabled=True)

    user_role = 'N/A'

    if trusted_users:
        user_role = trusted_users[0].user_role

    if user_role == 'N/A':
        logout(request)

    app_state_mode = AppState.objects.all().first().mode

    return render(request, 'users/info.html', {'title': 'Home',
                                               'user_role': user_role,
                                               'app_state_mode': app_state_mode})


class UserAuthenticationView(LoginView):
    authentication_form = UserAuthenticationForm
