from datetime import date
from django.shortcuts import redirect
from .models import (
    TrustedUser,
    AppState
)

BASKETBALL_STR = 'Καλαθοσφαίριση'
VOLLEYBALL_STR = 'Πετοσφαίριση'
FOOTBALL_STR = 'Ποδόσφαιρο'
HANDBALL_STR = 'Χειροσφαίριση'
ISG_TRACK_STR = 'Στίβος'
ISG_SWIMMING_STR = 'Κολύμβηση'
ISG_TENNIS_STR = 'Αντισφαίριση'

MIN_AGE = 12
MAX_AGE = 18


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def get_school_year():
    month = date.today().month
    year = date.today().year

    if month < 9:
        school_year = f'{year - 1}-{year}'
    else:
        school_year = f'{year}-{year + 1}'

    return school_year


class SchoolTestMixin:
    def test_func(self):
        user = self.request.user
        trusted_users = TrustedUser.objects.filter(trusted_user=user, enabled=True)

        user_role = 'N/A'

        if trusted_users:
            user_role = trusted_users[0].user_role

        if user_role == 'ΣΧΟΛΕΙΟ':
            return True

        return False

    def handle_no_permission(self):
        return redirect('main:home')


class TeamSportMainListTestMixin:
    def test_func(self):
        if self.team_sport_ml.school != self.request.user:
            return False

        if self.team_sport_ml.locked:
            return False

        app_state_mode = AppState.objects.all().first().mode
        if self.team_sport_ml.mode != app_state_mode:
            return False

        return True

    def handle_no_permission(self):
        return redirect('main:home')


class StudentTeamSportMainListTestMixin:
    def test_func(self):

        team_sport_ml = self.team_sport_ml

        if team_sport_ml.school != self.request.user:
            return False

        if team_sport_ml.locked:
            return False

        app_state_mode = AppState.objects.all().first().mode
        if self.team_sport_ml.mode != app_state_mode:
            return False

        students_count = team_sport_ml.team_sport_students.all().count()

        limit = 0
        if team_sport_ml.team_sport.teamsportlimits:
            limit = team_sport_ml.team_sport.teamsportlimits.max_students_main_list

        if students_count >= limit:
            return False

        return True

    def handle_no_permission(self):
        return redirect('main:home')


class TeamSportPhaseListTestMixin:
    def test_func(self):
        if self.team_sport_pl.school != self.request.user:
            return False

        if self.team_sport_pl.locked:
            return False

        app_state_mode = AppState.objects.all().first().mode
        if self.team_sport_pl.mode != app_state_mode:
            return False

        return True

    def handle_no_permission(self):
        return redirect('main:home')


class IndividualSportsGroupPhaseTestMixin:
    def test_func(self):
        if self.individual_sports_group_phase.school != self.request.user:
            return False

        if self.individual_sports_group_phase.locked:
            return False

        app_state_mode = AppState.objects.all().first().mode
        if self.individual_sports_group_phase.mode != app_state_mode:
            return False

        return True

    def handle_no_permission(self):
        return redirect('main:home')


class IndividualSportListTestMixin:
    def test_func(self):
        if self.individual_sport_list.school != self.request.user:
            return False

        if self.individual_sport_list.locked:
            return False

        app_state_mode = AppState.objects.all().first().mode
        if self.individual_sport_list.mode != app_state_mode:
            return False

        return True

    def handle_no_permission(self):
        return redirect('main:home')


class DDE_TestMixin:
    def test_func(self):
        user = self.request.user
        trusted_users = TrustedUser.objects.filter(trusted_user=user, enabled=True)

        user_role = 'N/A'

        if trusted_users:
            user_role = trusted_users[0].user_role

        if user_role == 'ΔΔΕ':
            return True

        return False

    def handle_no_permission(self):
        return redirect('main:home')
