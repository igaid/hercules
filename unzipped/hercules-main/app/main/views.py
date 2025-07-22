from django.shortcuts import render, reverse, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from .forms import (
    AppStateModeToggleForm,
    AppStateSchoolsEnabledToggleForm,
    SchoolRegistrationForm,
    SchoolRegistrationSubmitForm,
    TeamSportMainListForm,
    TeamSportMainListSubmitForm,
    StudentForTeamSportForm,
    TeamSportPhaseListForm,
    TeamSportPhaseListSubmitForm,
    IndividualSportsGroupPhaseForm,
    IndividualSportListForm,
    IndividualSportsGroupPhaseSubmitForm,
    StudentForIndividualSportForm,
    TeamSportMainListUnlockForm,
    TeamSportPhaseListUnlockForm,
    IndividualSportsGroupPhaseUnlockForm,
    SchoolRegistrationUnlockForm
)
from .models import (
    AppState,
    SchoolRegistration,
    TeamSport,
    TeamSportMainList,
    TeamSportPhaseList,
    IndividualSportsGroupPhase,
    IndividualSportList,
    IndividualSport,
    TrustedUser,
    Student,
    UnlockEntry)
from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalDeleteView,
    BSModalFormView
)
from django.contrib.auth import logout
from .common import (
    is_ajax,
    get_school_year,
    SchoolTestMixin,
    DDE_TestMixin,
    TeamSportMainListTestMixin,
    StudentTeamSportMainListTestMixin,
    TeamSportPhaseListTestMixin,
    IndividualSportListTestMixin,
    IndividualSportsGroupPhaseTestMixin
)
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    app_state = AppState.objects.all().first()

    user = request.user
    trusted_users = TrustedUser.objects.filter(trusted_user=user, enabled=True)

    user_role = 'N/A'

    if trusted_users:
        user_role = trusted_users[0].user_role

    school_year = AppState.objects.first().active_sch_year

    if app_state:
        home_message = app_state.home_message
    else:
        home_message = 'Welcome !!!'

    context = {'title': 'Αρχική σελίδα',
               'user_role': user_role,
               'home_message': home_message}

    if user_role == 'N/A':
        logout(request)

    if app_state:
        app_state_mode = app_state.mode
    else:
        app_state_mode = 'Σχολικά Πρωταθλήματα'

    if user_role == 'ΣΧΟΛΕΙΟ':
        school_registration_to_submit_count = SchoolRegistration.objects.filter(school=request.user,
                                                                                locked=False,
                                                                                school_year=school_year).count()
        school_registration_locked_count = SchoolRegistration.objects.filter(school=request.user,
                                                                             locked=True,
                                                                             school_year=school_year).count()

        team_sport_main_lists = TeamSportMainList.objects.filter(mode=app_state_mode,
                                                                 school=request.user,
                                                                 school_year=school_year)
        tsml_count = team_sport_main_lists.count()
        tsml_locked_count = team_sport_main_lists.filter(locked=True).count()

        team_sport_phase_lists = TeamSportPhaseList.objects.filter(mode=app_state_mode,
                                                                   school=request.user,
                                                                   school_year=school_year)
        tspl_count = team_sport_phase_lists.count()
        tspl_locked_count = team_sport_phase_lists.filter(locked=True).count()

        individual_sports_groups_phases = IndividualSportsGroupPhase.objects.filter(mode=app_state_mode,
                                                                                    school=request.user,
                                                                                    school_year=school_year)

        individual_sport_lists = IndividualSportList.objects.filter(mode=app_state_mode,
                                                                    school=request.user,
                                                                    school_year=school_year)

        isg_count = individual_sports_groups_phases.count()
        isg_locked_count = individual_sports_groups_phases.filter(locked=True).count()

        isl_count = individual_sport_lists.count()
        isl_locked_count = individual_sport_lists.filter(locked=True).count()

        context = {'title': 'Αρχική σελίδα',
                   'user_role': user_role,
                   'school_registration_to_submit_count': school_registration_to_submit_count,
                   'school_registration_locked_count': school_registration_locked_count,
                   'tsml_to_submit_count': tsml_count - tsml_locked_count,
                   'tsml_locked_count': tsml_locked_count,
                   'tspl_to_submit_count': tspl_count - tspl_locked_count,
                   'tspl_locked_count': tspl_locked_count,
                   'isg_to_submit_count': isg_count - isg_locked_count,
                   'isg_locked_count': isg_locked_count,
                   'isl_to_submit_count': isl_count - isl_locked_count,
                   'isl_locked_count': isl_locked_count,
                   'app_state_mode': app_state_mode}
    elif user_role == 'ΔΔΕ':
        if school_year != get_school_year():
            messages.warning(request, f"Προσοχή: Tο ενεργό σχολικό έτος {school_year} δεν είναι το τρέχον !!!")

        school_registrations_to_submit_count = SchoolRegistration.objects.filter(locked=False,
                                                                                 school_year=school_year).count()
        school_registrations_locked_count = SchoolRegistration.objects.filter(locked=True,
                                                                              school_year=school_year).count()

        team_sport_main_lists = TeamSportMainList.objects.filter(mode=app_state_mode, school_year=school_year)
        tsml_count = team_sport_main_lists.count()
        tsml_locked_count = team_sport_main_lists.filter(locked=True).count()

        team_sport_phase_lists = TeamSportPhaseList.objects.filter(mode=app_state_mode, school_year=school_year)
        tspl_count = team_sport_phase_lists.count()
        tspl_locked_count = team_sport_phase_lists.filter(locked=True).count()

        individual_sports_groups_phases = IndividualSportsGroupPhase.objects.filter(mode=app_state_mode,
                                                                                    school_year=school_year)

        individual_sport_lists = IndividualSportList.objects.filter(mode=app_state_mode,
                                                                    school_year=school_year)

        isg_count = individual_sports_groups_phases.count()
        isg_locked_count = individual_sports_groups_phases.filter(locked=True).count()

        isl_count = individual_sport_lists.count()
        isl_locked_count = individual_sport_lists.filter(locked=True).count()

        context = {'title': 'Αρχική σελίδα',
                   'user_role': user_role,
                   'school_registrations_to_submit_count': school_registrations_to_submit_count,
                   'school_registrations_locked_count': school_registrations_locked_count,
                   'tsml_to_submit_count': tsml_count - tsml_locked_count,
                   'tsml_locked_count': tsml_locked_count,
                   'tspl_to_submit_count': tspl_count - tspl_locked_count,
                   'tspl_locked_count': tspl_locked_count,
                   'isg_to_submit_count': isg_count - isg_locked_count,
                   'isg_locked_count': isg_locked_count,
                   'isl_to_submit_count': isl_count - isl_locked_count,
                   'isl_locked_count': isl_locked_count,
                   'app_state_mode': app_state_mode}

    return render(request, 'main/home.html', context)

    #
    #  Views for School and the Team Sport Main Lists
    #


class SchoolRegistrationView(SchoolTestMixin, UserPassesTestMixin, UpdateView):
    model = SchoolRegistration
    context_object_name = 'data'
    template_name = 'main/school/school_registration.html'
    form_class = SchoolRegistrationForm
    success_message = 'H Δήλωση Συμμετοχής στους Αγώνες αποθηκεύτηκε με επιτυχία.'
    success_url = reverse_lazy('main:school_registration')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_object(self, queryset=None):
        school_year = AppState.objects.first().active_sch_year
        school_registration = SchoolRegistration.objects.filter(school=self.request.user,
                                                                school_year=school_year).first()
        if not school_registration:
            school_registration = SchoolRegistration.objects.create(school=self.request.user,
                                                                    school_year=school_year)

        return school_registration

    def get_context_data(self, **kwargs):
        context = super(SchoolRegistrationView, self).get_context_data(**kwargs)

        context['user_role'] = 'ΣΧΟΛΕΙΟ'
        context['title'] = 'Δήλωση Συμμετοχής στους Αγώνες'

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        school_year = AppState.objects.first().active_sch_year
        school_registration = SchoolRegistration.objects.filter(school=self.request.user,
                                                                school_year=school_year).first()

        football_boys = school_registration.football_boys
        football_girls = school_registration.football_girls
        football_mix_1 = school_registration.football_mix_1
        football_mix_2 = school_registration.football_mix_2
        handball_boys = school_registration.handball_boys
        handball_girls = school_registration.handball_girls
        handball_mix_1 = school_registration.handball_mix_1
        handball_mix_2 = school_registration.handball_mix_2
        basketball_boys = school_registration.basketball_boys
        basketball_girls = school_registration.basketball_girls
        basketball_mix_1 = school_registration.basketball_mix_1
        basketball_mix_2 = school_registration.basketball_mix_2
        beach_volleyball_boys = school_registration.beach_volleyball_boys
        beach_volleyball_girls = school_registration.beach_volleyball_girls
        beach_volleyball_mix_1 = school_registration.beach_volleyball_mix_1
        beach_volleyball_mix_2 = school_registration.beach_volleyball_mix_2
        volleyball_boys = school_registration.volleyball_boys
        volleyball_girls = school_registration.volleyball_girls
        volleyball_mix_1 = school_registration.volleyball_mix_1
        volleyball_mix_2 = school_registration.volleyball_mix_2
        swimming_boys = school_registration.swimming_boys
        swimming_girls = school_registration.swimming_girls
        track_boys = school_registration.track_boys
        track_girls = school_registration.track_girls
        fencing_boys = school_registration.fencing_boys
        fencing_girls = school_registration.fencing_girls
        tennis_boys = school_registration.tennis_boys
        tennis_girls = school_registration.tennis_girls

        teams = int(football_boys) + int(football_girls) + int(football_mix_1) + int(football_mix_2) + \
                int(handball_boys) + int(handball_girls) + int(handball_mix_1) + int(handball_mix_2) + \
                int(basketball_boys) + int(basketball_girls) + int(basketball_mix_1) + int(basketball_mix_2) + \
                int(beach_volleyball_boys) + int(beach_volleyball_girls) + int(beach_volleyball_mix_1) + \
                int(beach_volleyball_mix_2) + \
                int(volleyball_boys) + int(volleyball_girls) + int(volleyball_mix_1) + int(volleyball_mix_2)

        individual = any([swimming_boys, swimming_girls, track_boys, track_girls, fencing_boys, fencing_girls,
                          tennis_boys, tennis_girls])

        if teams > 0 or individual:
            context['status'] = 'to_submit'

        return context

    def form_valid(self, form):
        # form.instance.locked = True
        # form.instance.submit_date_time = timezone.now()
        messages.success(self.request, 'Η Δήλωση Συμμετοχής στους Αγώνες του σχολείου σας αποθηκεύτηκε με επιτυχία.')

        return super().form_valid(form)


class SchoolRegistrationSubmitView(SchoolTestMixin, UserPassesTestMixin, BSModalFormView):
    model = SchoolRegistration
    form_class = SchoolRegistrationSubmitForm
    template_name = 'main/school/submit_school_registration.html'
    success_url = reverse_lazy('main:home')

    def get_context_data(self, **kwargs):
        context = super(SchoolRegistrationSubmitView, self).get_context_data(**kwargs)

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        return context

    def form_valid(self, form):
        school_year = AppState.objects.first().active_sch_year
        submit_date_time = timezone.now()
        school_registration = SchoolRegistration.objects.filter(school=self.request.user,
                                                                school_year=school_year)
        school_registration.update(locked=True, submit_date_time=submit_date_time)

        messages.success(self.request, "Η Δήλωση Συμμετοχής κλείδωσε με επιτυχία.")

        return super().form_valid(form)


class TeamSportMainListsView(SchoolTestMixin, UserPassesTestMixin, ListView):
    model = TeamSportMainList
    context_object_name = 'data'
    template_name = 'main/school_tsml/team_sport_main_lists.html'

    def get_queryset(self):
        school_year = AppState.objects.first().active_sch_year
        app_state_mode = AppState.objects.all().first().mode
        team_sport_main_lists = TeamSportMainList.objects.filter(mode=app_state_mode,
                                                                 school=self.request.user,
                                                                 school_year=school_year).order_by('id')

        # for item in team_sport_main_lists:
        #     item.students_count = item.team_sport_students.all().count()
        #     item.save()

        return team_sport_main_lists

    def get_context_data(self, **kwargs):
        context = super(TeamSportMainListsView, self).get_context_data(**kwargs)
        context['user_role'] = 'ΣΧΟΛΕΙΟ'
        context['title'] = 'Λίστες Ομάδων'

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        return context


class TeamSportMainListCreateView(SchoolTestMixin, UserPassesTestMixin, BSModalCreateView):
    template_name = 'main/school_tsml/create_team_sport_main_list.html'
    model = TeamSportMainList
    form_class = TeamSportMainListForm
    success_url = reverse_lazy('main:team_sport_main_lists')

    def get_context_data(self, **kwargs):
        context = super(TeamSportMainListCreateView, self).get_context_data(**kwargs)

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        return context

    def get_form(self):
        form = super(TeamSportMainListCreateView, self).get_form()

        app_state_mode = AppState.objects.all().first().mode

        form.fields['team_sport'].queryset = form.fields['team_sport'].queryset.filter(mode=app_state_mode,
                                                                                       enabled=True)

        return form

    def form_valid(self, form):
        if not is_ajax(self.request):
            team_sport_ml: TeamSportMainList = form.instance
            team_sport_ml.school = self.request.user
            team_sport_ml.school_year = AppState.objects.first().active_sch_year

            app_state_mode = AppState.objects.all().first().mode

            if app_state_mode == 'Σχολικά Πρωταθλήματα':
                messages.success(self.request, 'Η Λίστα Ομάδας δημιουργήθηκε με επιτυχία.')
            else:
                messages.success(self.request, 'Η Κατάσταση Συμμετοχής Ομάδας δημιουργήθηκε με επιτυχία.')

        return super().form_valid(form)


class TeamSportMainListDeleteView(TeamSportMainListTestMixin, UserPassesTestMixin, BSModalDeleteView):
    model = TeamSportMainList
    template_name = 'main/school_tsml/delete_team_sport_main_list.html'
    context_object_name = 'data'
    success_url = reverse_lazy('main:team_sport_main_lists')
    success_message = 'Η Λίστα Ομάδας διαγράφηκε με επιτυχία.'

    def get_context_data(self, **kwargs):
        context = super(TeamSportMainListDeleteView, self).get_context_data(**kwargs)

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        return context

    def dispatch(self, request, *args, **kwargs):
        self.team_sport_ml = TeamSportMainList.objects.get(pk=self.kwargs.get('pk'))

        return super().dispatch(request, *args, **kwargs)


class TeamSportMainListUpdateView(TeamSportMainListTestMixin, UserPassesTestMixin, BSModalUpdateView):
    model = TeamSportMainList
    template_name = 'main/school_tsml/update_team_sport_main_list.html'
    form_class = TeamSportMainListForm
    success_message = 'Η Λίστα Ομάδας ενημερώθηκε με επιτυχία.'
    success_url = reverse_lazy('main:team_sport_main_lists')

    def get_context_data(self, **kwargs):
        context = super(TeamSportMainListUpdateView, self).get_context_data(**kwargs)

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        return context

    def get_form(self):
        form = super(TeamSportMainListUpdateView, self).get_form()

        app_state_mode = AppState.objects.all().first().mode

        form.fields['team_sport'].queryset = form.fields['team_sport'].queryset.filter(mode=app_state_mode,
                                                                                       enabled=True)

        return form

    def dispatch(self, request, *args, **kwargs):
        self.team_sport_ml = TeamSportMainList.objects.get(pk=self.kwargs.get('pk'))

        return super().dispatch(request, *args, **kwargs)


class TeamSportMainListSubmitView(TeamSportMainListTestMixin, UserPassesTestMixin, BSModalUpdateView):
    model = TeamSportMainList
    form_class = TeamSportMainListSubmitForm
    template_name = 'main/school_tsml/submit_team_sport_main_list.html'
    success_url = reverse_lazy('main:team_sport_main_lists')

    def get_context_data(self, **kwargs):
        context = super(TeamSportMainListSubmitView, self).get_context_data(**kwargs)

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        return context

    def form_valid(self, form):
        if not is_ajax(self.request):
            team_sport_ml: TeamSportMainList = form.instance
            team_sport_ml.locked = True
            team_sport_ml.submit_date_time = timezone.now()

            app_state_mode = AppState.objects.all().first().mode

            if app_state_mode == 'Σχολικά Πρωταθλήματα':
                messages.success(self.request, 'Η Λίστα Ομάδας κλείδωσε με επιτυχία.')
            else:
                messages.success(self.request, 'Η Κατάσταση Συμμετοχής Ομάδας κλείδωσε με επιτυχία.')

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        self.team_sport_ml = TeamSportMainList.objects.get(pk=self.kwargs.get('pk'))

        team_sport_ml = self.team_sport_ml

        students_count = team_sport_ml.team_sport_students.all().count()

        min_limit = 0

        if team_sport_ml.team_sport.teamsportlimits:
            min_limit = team_sport_ml.team_sport.teamsportlimits.min_students_main_list

        if students_count < min_limit:
            return redirect("main:home")

        return super().dispatch(request, *args, **kwargs)


class TeamSportMainListStudentsView(TeamSportMainListTestMixin, UserPassesTestMixin, ListView):
    model = TeamSportMainList
    context_object_name = 'data'
    template_name = 'main/school_tsml/team_sport_main_list_students.html'

    def get_queryset(self):
        return TeamSportMainList.objects.get(pk=self.kwargs.get('pk')).team_sport_students.all()

    def get_context_data(self, **kwargs):
        context = super(TeamSportMainListStudentsView, self).get_context_data(**kwargs)
        team_sport_ml = TeamSportMainList.objects.get(pk=self.kwargs.get('pk'))

        students_count = team_sport_ml.team_sport_students.all().count()

        min_limit = 0
        max_limit = 0
        if team_sport_ml.team_sport.teamsportlimits:
            min_limit = team_sport_ml.team_sport.teamsportlimits.min_students_main_list
            max_limit = team_sport_ml.team_sport.teamsportlimits.max_students_main_list

        if students_count == max_limit:
            messages.info(self.request, "Η Λίστα είναι πλήρης !!!")
            context['hide_create_student_btn'] = 'True'

        if students_count < min_limit:
            messages.info(self.request, "Δεν έχει συμπληρωθεί ο ελάχιστος αριθμός μαθητών !!!")
            context['hide_submit_btn'] = 'True'

        context['user_role'] = 'ΣΧΟΛΕΙΟ'
        context['title'] = f'{team_sport_ml.team_sport} - {team_sport_ml.gender} ({team_sport_ml.school_year})'
        context['team_sport_ml_id'] = self.kwargs.get('pk')

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        return context

    def dispatch(self, request, *args, **kwargs):
        self.team_sport_ml = TeamSportMainList.objects.get(pk=self.kwargs.get('pk'))

        return super().dispatch(request, *args, **kwargs)


class StudentForTeamSportMainListCreateView(StudentTeamSportMainListTestMixin, UserPassesTestMixin, BSModalCreateView):
    template_name = 'main/school_tsml/create_student_for_team_sport_main_list.html'
    model = Student
    form_class = StudentForTeamSportForm
    success_message = 'Ο μαθητής δημιουργήθηκε με επιτυχία.'

    def dispatch(self, request, *args, **kwargs):
        self.team_sport_ml: TeamSportMainList = get_object_or_404(TeamSportMainList, pk=kwargs['team_sport_ml_pk'])

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(StudentForTeamSportMainListCreateView, self).get_form_kwargs()
        kwargs['team_sport_ml_id'] = self.team_sport_ml.id

        return kwargs

    def form_valid(self, form):
        student: Student = form.instance
        student.school = self.request.user
        student.school_year = AppState.objects.first().active_sch_year
        student.team_sport_main_list = self.team_sport_ml

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("main:team_sport_main_list_students", kwargs={"pk": self.team_sport_ml.id})


class StudentForTeamSportMainListUpdateView(TeamSportMainListTestMixin, UserPassesTestMixin, BSModalUpdateView):
    model = Student
    template_name = 'main/school_tsml/update_student_for_team_sport_main_list.html'
    form_class = StudentForTeamSportForm
    success_message = 'Ο μαθητής ενημερώθηκε με επιτυχία.'

    def dispatch(self, request, *args, **kwargs):
        self.team_sport_ml: TeamSportMainList = get_object_or_404(TeamSportMainList, pk=kwargs['team_sport_ml_pk'])

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(StudentForTeamSportMainListUpdateView, self).get_object(queryset=queryset)

    def get_form_kwargs(self):
        kwargs = super(StudentForTeamSportMainListUpdateView, self).get_form_kwargs()
        kwargs['team_sport_ml_id'] = self.team_sport_ml.id

        return kwargs

    def get_success_url(self):
        return reverse("main:team_sport_main_list_students", kwargs={"pk": self.team_sport_ml.id})


class StudentForTeamSportMainListDeleteView(TeamSportMainListTestMixin, UserPassesTestMixin, BSModalDeleteView):
    model = Student
    template_name = 'main/school_tsml/delete_student_for_team_sport_main_list.html'
    context_object_name = 'data'
    success_message = 'Ο μαθητής διαγράφηκε με επιτυχία.'

    def dispatch(self, request, *args, **kwargs):
        self.team_sport_ml: TeamSportMainList = get_object_or_404(TeamSportMainList, pk=kwargs['team_sport_ml_pk'])

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("main:team_sport_main_list_students", kwargs={"pk": self.team_sport_ml.id})

    #
    #  Views for School and the Team Sport Phase Lists
    #


class TeamSportPhaseListsView(SchoolTestMixin, UserPassesTestMixin, ListView):
    model = TeamSportPhaseList
    context_object_name = 'data'
    template_name = 'main/school_tspl/team_sport_phase_lists.html'

    def get_queryset(self):
        school_year = AppState.objects.first().active_sch_year
        app_state_mode = AppState.objects.all().first().mode
        team_sport_phase_lists = TeamSportPhaseList.objects.filter(mode=app_state_mode,
                                                                   school=self.request.user,
                                                                   school_year=school_year).order_by('id')

        for item in team_sport_phase_lists:
            team_sport_ml = item.team_sport_main_list
            team_sport_ml.students_count = team_sport_ml.team_sport_students.all().count()
            team_sport_ml.save()

            if item.phase == '1η':
                item.students_count = team_sport_ml.team_sport_students.filter(plays_in_phase_1=True).count()
            elif item.phase == '2η':
                item.students_count = team_sport_ml.team_sport_students.filter(plays_in_phase_2=True).count()
            else:
                item.students_count = team_sport_ml.team_sport_students.filter(plays_in_phase_3=True).count()
            item.save()

        return team_sport_phase_lists

    def get_context_data(self, **kwargs):
        context = super(TeamSportPhaseListsView, self).get_context_data(**kwargs)
        context['user_role'] = 'ΣΧΟΛΕΙΟ'
        context['title'] = 'Καταστάσεις Συμμετοχής Ομάδων'

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        messages.info(self.request,
                      "Πρέπει να υποβάλετε μια Λίστα Ομάδας για μπορέσετε να δημιουργήσετε μια Κατάσταση Συμμετοχής Ομάδας !!! ")

        school_year = AppState.objects.first().active_sch_year
        team_sport_mls = TeamSportMainList.objects.filter(mode=app_state_mode,
                                                          school=self.request.user,
                                                          school_year=school_year,
                                                          locked=True)

        if len(team_sport_mls) == 0:
            context['hide_create_phase_list_btn'] = 'True'

        return context


class TeamSportPhaseListCreateView(SchoolTestMixin, UserPassesTestMixin, BSModalCreateView):
    template_name = 'main/school_tspl/create_team_sport_phase_list.html'
    model = TeamSportPhaseList
    form_class = TeamSportPhaseListForm
    success_message = 'Η Κατάσταση Συμμετοχής Ομάδας δημιουργήθηκε με επιτυχία.'
    success_url = reverse_lazy('main:team_sport_phase_lists')

    def get_form(self):
        form = super(TeamSportPhaseListCreateView, self).get_form()

        school_year = AppState.objects.first().active_sch_year
        app_state_mode = AppState.objects.all().first().mode
        form.fields['team_sport_main_list'].queryset = form.fields['team_sport_main_list'].queryset.filter(
            mode=app_state_mode, school=self.request.user, school_year=school_year, locked=True)

        return form

    def form_valid(self, form):
        team_sport_pl: TeamSportPhaseList = form.instance
        team_sport_pl.school = self.request.user
        team_sport_pl.school_year = AppState.objects.first().active_sch_year

        return super().form_valid(form)


class TeamSportPhaseListDeleteView(TeamSportPhaseListTestMixin, UserPassesTestMixin, BSModalDeleteView):
    model = TeamSportPhaseList
    template_name = 'main/school_tspl/delete_team_sport_phase_list.html'
    context_object_name = 'data'
    success_url = reverse_lazy('main:team_sport_phase_lists')
    success_message = 'Η Κατάσταση Συμμετοχής Ομάδας διαγράφηκε με επιτυχία.'

    def dispatch(self, request, *args, **kwargs):
        self.team_sport_pl = TeamSportPhaseList.objects.get(pk=self.kwargs.get('pk'))

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        team_sport_students = TeamSportPhaseList.objects.get(
            pk=self.kwargs.get('pk')).team_sport_main_list.team_sport_students.all()
        if self.team_sport_pl.phase == '1η':
            team_sport_students.update(plays_in_phase_1=False)
        elif self.team_sport_pl.phase == '2η':
            team_sport_students.update(plays_in_phase_2=False)
        else:
            team_sport_students.update(plays_in_phase_3=False)

        return super().form_valid(form)


class TeamSportPhaseListUpdateView(TeamSportPhaseListTestMixin, UserPassesTestMixin, BSModalUpdateView):
    model = TeamSportPhaseList
    template_name = 'main/school_tspl/update_team_sport_phase_list.html'
    form_class = TeamSportPhaseListForm
    success_message = 'Η Κατάσταση Συμμετοχής Ομάδας ενημερώθηκε με επιτυχία.'
    success_url = reverse_lazy('main:team_sport_phase_lists')

    def get_form(self):
        form = super(TeamSportPhaseListUpdateView, self).get_form()

        school_year = AppState.objects.first().active_sch_year
        app_state_mode = AppState.objects.all().first().mode
        form.fields['team_sport_main_list'].queryset = form.fields['team_sport_main_list'].queryset.filter(
            mode=app_state_mode, school=self.request.user, school_year=school_year, locked=True)

        return form

    def dispatch(self, request, *args, **kwargs):
        self.team_sport_pl = TeamSportPhaseList.objects.get(pk=self.kwargs.get('pk'))

        return super().dispatch(request, *args, **kwargs)


class TeamSportPhaseListSubmitView(TeamSportPhaseListTestMixin, UserPassesTestMixin, BSModalUpdateView):
    model = TeamSportPhaseList
    form_class = TeamSportPhaseListSubmitForm
    template_name = 'main/school_tspl/submit_team_sport_phase_list.html'
    success_message = 'Η Κατάσταση Συμμετοχής Ομάδας κλείδωσε με επιτυχία.'
    success_url = reverse_lazy('main:team_sport_phase_lists')

    def form_valid(self, form):
        team_sport_pl: TeamSportPhaseList = form.instance
        team_sport_pl.locked = True
        team_sport_pl.submit_date_time = timezone.now()

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        self.team_sport_pl = TeamSportPhaseList.objects.get(pk=self.kwargs.get('pk'))

        team_sport_pl = self.team_sport_pl

        min_limit = 0
        team_sport_ml = team_sport_pl.team_sport_main_list
        if team_sport_ml.team_sport.teamsportlimits:
            min_limit = team_sport_ml.team_sport.teamsportlimits.min_students_phase_list

        if team_sport_pl.phase == '1η':
            students_count = team_sport_ml.team_sport_students.filter(plays_in_phase_1=True).count()
        elif team_sport_pl.phase == '2η':
            students_count = team_sport_ml.team_sport_students.filter(plays_in_phase_2=True).count()
        else:
            students_count = team_sport_ml.team_sport_students.filter(plays_in_phase_3=True).count()

        if students_count < min_limit:
            return redirect("main:home")

        return super().dispatch(request, *args, **kwargs)


class TeamSportPhaseListStudentsView(TeamSportPhaseListTestMixin, UserPassesTestMixin, ListView):
    model = TeamSportPhaseList
    context_object_name = 'data'
    template_name = 'main/school_tspl/team_sport_phase_list_students.html'

    def get_queryset(self):
        return TeamSportPhaseList.objects.get(pk=self.kwargs.get('pk')).team_sport_main_list.team_sport_students.all()

    def get_context_data(self, **kwargs):
        context = super(TeamSportPhaseListStudentsView, self).get_context_data(**kwargs)
        team_sport_pl = TeamSportPhaseList.objects.get(pk=self.kwargs.get('pk'))
        context['user_role'] = 'ΣΧΟΛΕΙΟ'
        context['title'] = f'{team_sport_pl.team_sport_main_list.team_sport}-' \
                           f'{team_sport_pl.team_sport_main_list.gender} ({team_sport_pl.school_year})' \
                           f' - {team_sport_pl.phase} Φάση'
        context['phase'] = team_sport_pl.phase
        context['team_sport_pl_id'] = self.kwargs.get('pk')

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        min_limit = 0
        max_limit = 0
        team_sport_ml = team_sport_pl.team_sport_main_list
        if team_sport_ml.team_sport.teamsportlimits:
            min_limit = team_sport_ml.team_sport.teamsportlimits.min_students_phase_list
            max_limit = team_sport_ml.team_sport.teamsportlimits.max_students_phase_list

        if team_sport_pl.phase == '1η':
            students_count = team_sport_ml.team_sport_students.filter(plays_in_phase_1=True).count()
        elif team_sport_pl.phase == '2η':
            students_count = team_sport_ml.team_sport_students.filter(plays_in_phase_2=True).count()
        else:
            students_count = team_sport_ml.team_sport_students.filter(plays_in_phase_3=True).count()

        if students_count < min_limit:
            context['hide_submit_btn'] = 'True'

        if (self.request.method != 'POST'):
            messages.info(self.request, f'Πρέπει να επιλέξετε από {min_limit} μέχρι και {max_limit} μαθητές.')

        return context

    def dispatch(self, request, *args, **kwargs):
        self.team_sport_pl = TeamSportPhaseList.objects.get(pk=self.kwargs.get('pk'))

        team_sport_ml = self.team_sport_pl.team_sport_main_list

        min_limit = 0
        max_limit = 0
        if team_sport_ml.team_sport.teamsportlimits:
            min_limit = team_sport_ml.team_sport.teamsportlimits.min_students_phase_list
            max_limit = team_sport_ml.team_sport.teamsportlimits.max_students_phase_list

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ids = list()
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                ids.append(int(key))

        team_sport_ml = self.team_sport_pl.team_sport_main_list

        max_limit = 0
        if team_sport_ml.team_sport.teamsportlimits:
            max_limit = team_sport_ml.team_sport.teamsportlimits.max_students_phase_list

        if len(ids) > max_limit:
            messages.error(request, f'Οι επιλογές σας ήταν παραπάνω από το αποδεκτό όριο ({max_limit}).')

            return redirect("main:team_sport_phase_list_students", pk=self.team_sport_pl.id)

        team_sport_students = self.team_sport_pl.team_sport_main_list.team_sport_students.all()
        if self.team_sport_pl.phase == '1η':
            team_sport_students.update(plays_in_phase_1=False)
        elif self.team_sport_pl.phase == '2η':
            team_sport_students.update(plays_in_phase_2=False)
        else:
            team_sport_students.update(plays_in_phase_3=False)

        for student_id in ids:
            student = Student.objects.get(pk=student_id)
            if self.team_sport_pl.phase == '1η':
                student.plays_in_phase_1 = True
            elif self.team_sport_pl.phase == '2η':
                student.plays_in_phase_2 = True
            else:
                student.plays_in_phase_3 = True

            student.save()

        messages.success(request, 'Η Κατάσταση Συμμετοχής αποθηκεύτηκε με επιτυχία.')

        return redirect("main:team_sport_phase_list_students", pk=self.team_sport_pl.id)

    #
    #  Views for School and the Individual Sport Lists
    #


class IndividualSportsGroupPhaseListView(SchoolTestMixin, UserPassesTestMixin, ListView):
    model = IndividualSportsGroupPhase
    context_object_name = 'data'
    template_name = 'main/school_isgp/individual_sports_group_phases.html'

    def get_context_data(self, **kwargs):
        context = super(IndividualSportsGroupPhaseListView, self).get_context_data(**kwargs)
        context['user_role'] = 'ΣΧΟΛΕΙΟ'
        school_year = AppState.objects.first().active_sch_year
        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        context['title'] = 'Καταστάσεις Συμμετοχής Ατομικών Αθλημάτων'

        individual_sports_groups_phases = IndividualSportsGroupPhase.objects.filter(mode=app_state_mode,
                                                                                    school=self.request.user,
                                                                                    school_year=school_year).order_by(
            'id')

        for individual_sports_group_phase in individual_sports_groups_phases:
            individual_sports_lists = individual_sports_group_phase.individual_sport_lists.all()

            students_count = 0
            for individual_sports_list in individual_sports_lists:
                students_count += individual_sports_list.individual_sport_students.all().count()

            individual_sports_group_phase.students_count = students_count
            individual_sports_group_phase.save()

        context['data'] = individual_sports_groups_phases

        return context


class IndividualSportsGroupPhaseCreateView(SchoolTestMixin, UserPassesTestMixin, BSModalCreateView):
    template_name = 'main/school_isgp/create_individual_sports_group_phase.html'
    model = IndividualSportsGroupPhase
    form_class = IndividualSportsGroupPhaseForm
    success_message = 'Το Άθλημα δημιουργήθηκε με επιτυχία.'
    success_url = reverse_lazy('main:individual_sports_groups_phases')

    def get_form(self):
        form = super(IndividualSportsGroupPhaseCreateView, self).get_form()

        app_state_mode = AppState.objects.all().first().mode

        form.fields['individual_sports_group'].queryset = form.fields['individual_sports_group'].queryset.filter(
            mode=app_state_mode, enabled=True).order_by('id')

        return form

    def form_valid(self, form):
        individual_sports_group_phase: IndividualSportsGroupPhase = form.instance
        individual_sports_group_phase.school = self.request.user
        individual_sports_group_phase.school_year = AppState.objects.first().active_sch_year

        return super().form_valid(form)


class IndividualSportsGroupPhaseDeleteView(IndividualSportsGroupPhaseTestMixin, UserPassesTestMixin, BSModalDeleteView):
    model = IndividualSportsGroupPhase
    template_name = 'main/school_isgp/delete_individual_sports_group_phase.html'
    context_object_name = 'data'
    success_url = reverse_lazy('main:individual_sports_groups_phases')
    success_message = 'Το Άθλημα διαγράφηκε με επιτυχία.'

    def dispatch(self, request, *args, **kwargs):
        self.individual_sports_group_phase = IndividualSportsGroupPhase.objects.get(pk=self.kwargs.get('pk'))

        return super().dispatch(request, *args, **kwargs)


class IndividualSportsGroupPhaseUpdateView(IndividualSportsGroupPhaseTestMixin, UserPassesTestMixin, BSModalUpdateView):
    model = IndividualSportsGroupPhase
    template_name = 'main/school_isgp/update_individual_sports_group_phase.html'
    form_class = IndividualSportsGroupPhaseForm
    success_message = 'Το Άθλημα ενημερώθηκε με επιτυχία.'
    success_url = reverse_lazy('main:individual_sports_groups_phases')

    def get_form(self):
        form = super(IndividualSportsGroupPhaseUpdateView, self).get_form()

        app_state_mode = AppState.objects.all().first().mode

        form.fields['individual_sports_group'].queryset = form.fields['individual_sports_group'].queryset.filter(
            mode=app_state_mode, enabled=True).order_by('id')

        return form

    def dispatch(self, request, *args, **kwargs):
        self.individual_sports_group_phase = IndividualSportsGroupPhase.objects.get(pk=self.kwargs.get('pk'))

        return super().dispatch(request, *args, **kwargs)


class IndividualSportsGroupPhaseSubmitView(IndividualSportsGroupPhaseTestMixin, UserPassesTestMixin, BSModalFormView):
    model = IndividualSportsGroupPhase
    form_class = IndividualSportsGroupPhaseSubmitForm
    template_name = 'main/school_isgp/submit_individual_sports_group_phase.html'
    success_url = reverse_lazy('main:individual_sports_groups_phases')

    def get_context_data(self, **kwargs):
        context = super(IndividualSportsGroupPhaseSubmitView, self).get_context_data(**kwargs)

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        return context

    def form_valid(self, form):
        submit_date_time = timezone.now()
        self.individual_sports_group_phase.locked = True
        self.individual_sports_group_phase.submit_date_time = submit_date_time
        self.individual_sports_group_phase.save()

        individual_sport_lists = self.individual_sports_group_phase.individual_sport_lists.all()
        individual_sport_lists.update(locked=True, submit_date_time=submit_date_time)

        messages.success(self.request,
                         "Η Κατάσταση Συμμετοχής Ατομικού Αθλήματος κλείδωσε με επιτυχία.")

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        self.individual_sports_group_phase = IndividualSportsGroupPhase.objects.get(pk=self.kwargs.get('pk'))

        if self.individual_sports_group_phase.locked:
            return redirect('main:individual_sports_groups_phases')

        individual_sport_lists = self.individual_sports_group_phase.individual_sport_lists.all()

        empty_lists = False
        for item in individual_sport_lists:
            if item.individual_sport_students.all().count() == 0:
                empty_lists = True
                break

        if empty_lists:
            return redirect('main:individual_sports_groups_phases')

        return super().dispatch(request, *args, **kwargs)


class IndividualSportListsView(IndividualSportsGroupPhaseTestMixin, UserPassesTestMixin, ListView):
    model = IndividualSportList
    context_object_name = 'data'
    template_name = 'main/school_isl/individual_sport_lists.html'

    def get_queryset(self):
        individual_sport_lists = IndividualSportList.objects.filter(
            individual_sports_group_phase=self.individual_sports_group_phase).order_by('id')

        return individual_sport_lists

    def get_context_data(self, **kwargs):
        context = super(IndividualSportListsView, self).get_context_data(**kwargs)
        context['user_role'] = 'ΣΧΟΛΕΙΟ'

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        context['title'] = f'Κατάσταση Συμμετοχής: ' \
                           f'{self.individual_sports_group_phase.individual_sports_group} - ' \
                           f'Φάση {self.individual_sports_group_phase.phase}'

        context['isgp_id'] = self.individual_sports_group_phase.id

        isl_count = self.individual_sports_group_phase.individual_sport_lists.all().count()

        if self.individual_sports_group_phase.locked:
            context['status'] = 'submitted'
            messages.info(self.request, "Η Κατάσταση Συμμετοχής έχει υποβληθεί στη ΔΔΕ !!!")
        else:
            if isl_count > 0:
                individual_sport_lists = self.individual_sports_group_phase.individual_sport_lists.all()

                empty_lists = False
                for item in individual_sport_lists:
                    if item.individual_sport_students.all().count() == 0:
                        empty_lists = True
                        break

                if not empty_lists:
                    context['status'] = 'to_submit'
                    messages.warning(self.request, "Η Κατάσταση Συμμετοχής δεν έχει υποβληθεί στη ΔΔΕ !!!")
                else:
                    context['status'] = 'empty_lists'
                    messages.warning(self.request, "Υπάρχουν αγωνίσματα χωρίς μαθητές !!!")
            else:
                context['status'] = 'empty'
                messages.info(self.request, "Δεν υπάρχουν αγωνίσματα για να γίνει υποβολή !!!")

        return context

    def dispatch(self, request, *args, **kwargs):
        self.individual_sports_group_phase = IndividualSportsGroupPhase.objects.get(pk=self.kwargs.get('pk'))

        return super().dispatch(request, *args, **kwargs)


class IndividualSportListCreateView(IndividualSportsGroupPhaseTestMixin, UserPassesTestMixin, BSModalCreateView):
    template_name = 'main/school_isl/create_individual_sport_list.html'
    model = IndividualSportList
    form_class = IndividualSportListForm
    success_message = 'Το Αγώνισμα δημιουργήθηκε με επιτυχία.'

    def get_form_kwargs(self):
        kwargs = super(IndividualSportListCreateView, self).get_form_kwargs()
        kwargs['individual_sports_group_phase_id'] = self.individual_sports_group_phase.id

        return kwargs

    def get_form(self):
        form = super(IndividualSportListCreateView, self).get_form()

        app_state_mode = AppState.objects.all().first().mode

        form.fields['individual_sport'].queryset = form.fields['individual_sport']. \
            queryset.filter(mode=app_state_mode,
                            individual_sports_group=self.individual_sports_group_phase.individual_sports_group,
                            enabled=True).order_by('id')

        individual_sport_lists = IndividualSportList.objects.filter(
            individual_sports_group_phase=self.individual_sports_group_phase)

        individual_sports = list()
        for item in individual_sport_lists:
            individual_sports.append(item.individual_sport.id)

        form.fields['individual_sport'].queryset = form.fields['individual_sport'].queryset.exclude(
            pk__in=individual_sports)

        return form

    def form_valid(self, form):
        individual_sport_list: IndividualSportList = form.instance
        individual_sport_list.school = self.request.user
        individual_sport_list.school_year = AppState.objects.first().active_sch_year
        individual_sport_list.individual_sports_group_phase = self.individual_sports_group_phase

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("main:individual_sports_lists", kwargs={"pk": self.individual_sports_group_phase.id})

    def dispatch(self, request, *args, **kwargs):
        self.individual_sports_group_phase = IndividualSportsGroupPhase.objects.get(pk=self.kwargs.get('pk'))

        return super().dispatch(request, *args, **kwargs)


class IndividualSportListDeleteView(IndividualSportListTestMixin, UserPassesTestMixin, BSModalDeleteView):
    model = IndividualSportList
    template_name = 'main/school_isl/delete_individual_sport_list.html'
    context_object_name = 'data'
    success_message = 'Το Αγώνισμα διαγράφηκε με επιτυχία.'

    def get_success_url(self):
        return reverse("main:individual_sports_lists",
                       kwargs={"pk": self.individual_sport_list.individual_sports_group_phase.id})

    def dispatch(self, request, *args, **kwargs):
        self.individual_sport_list = IndividualSportList.objects.get(pk=self.kwargs.get('pk'))

        return super().dispatch(request, *args, **kwargs)


class IndividualSportListUpdateView(IndividualSportListTestMixin, UserPassesTestMixin, BSModalUpdateView):
    model = IndividualSportList
    template_name = 'main/school_isl/update_individual_sport_list.html'
    form_class = IndividualSportListForm
    success_message = 'Το Αγώνισμα ενημερώθηκε με επιτυχία.'

    def get_success_url(self):
        return reverse("main:individual_sports_lists",
                       kwargs={"pk": self.individual_sport_list.individual_sports_group_phase.id})

    def get_form_kwargs(self):
        kwargs = super(IndividualSportListUpdateView, self).get_form_kwargs()
        kwargs['individual_sports_group_phase_id'] = self.individual_sport_list.individual_sports_group_phase.id

        return kwargs

    def get_form(self):
        form = super(IndividualSportListUpdateView, self).get_form()

        app_state_mode = AppState.objects.all().first().mode

        form.fields['individual_sport'].queryset = form.fields['individual_sport'].queryset.filter(
            mode=app_state_mode, enabled=True).order_by('id')

        return form

    def dispatch(self, request, *args, **kwargs):
        self.individual_sport_list = IndividualSportList.objects.get(pk=self.kwargs.get('pk'))

        return super().dispatch(request, *args, **kwargs)


class IndividualSportListStudentsView(IndividualSportListTestMixin, UserPassesTestMixin, ListView):
    model = IndividualSportList
    context_object_name = 'data'
    template_name = 'main/school_isl/individual_sport_list_students.html'

    def get_queryset(self):
        return IndividualSportList.objects.get(pk=self.kwargs.get('pk')).individual_sport_students.all()

    def get_context_data(self, **kwargs):
        context = super(IndividualSportListStudentsView, self).get_context_data(**kwargs)
        individual_sport_list: IndividualSportList = IndividualSportList.objects.get(pk=self.kwargs.get('pk'))
        context['next_id'] = individual_sport_list.individual_sports_group_phase.id
        context['user_role'] = 'ΣΧΟΛΕΙΟ'
        context['title'] = f'Φάση {individual_sport_list.individual_sports_group_phase.phase} - ' \
                           f'{individual_sport_list.individual_sport}'
        context['individual_sport_list_id'] = self.kwargs.get('pk')

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        return context

    def dispatch(self, request, *args, **kwargs):
        self.individual_sport_list = IndividualSportList.objects.get(pk=self.kwargs.get('pk'))

        return super().dispatch(request, *args, **kwargs)


class StudentForIndividualSportListCreateView(IndividualSportListTestMixin, UserPassesTestMixin, BSModalCreateView):
    template_name = 'main/school_isl/create_student_for_individual_sport_list.html'
    model = Student
    form_class = StudentForIndividualSportForm
    success_message = 'Ο μαθητής δημιουργήθηκε με επιτυχία.'

    def dispatch(self, request, *args, **kwargs):
        self.individual_sport_list: IndividualSportList = get_object_or_404(IndividualSportList,
                                                                            pk=kwargs['individual_sport_list_pk'])

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(StudentForIndividualSportListCreateView, self).get_form_kwargs()
        kwargs['individual_sport_list_id'] = self.individual_sport_list.id

        return kwargs

    def form_valid(self, form):
        student: Student = form.instance
        student.school = self.request.user
        student.school_year = AppState.objects.first().active_sch_year
        student.individual_sport_list = self.individual_sport_list

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("main:individual_sport_list_students", kwargs={"pk": self.individual_sport_list.id})


class StudentForIndividualSportListUpdateView(IndividualSportListTestMixin, UserPassesTestMixin, BSModalUpdateView):
    model = Student
    template_name = 'main/school_isl/update_student_for_individual_sport_list.html'
    form_class = StudentForIndividualSportForm
    success_message = 'Ο μαθητής ενημερώθηκε με επιτυχία.'

    def dispatch(self, request, *args, **kwargs):
        self.individual_sport_list: IndividualSportList = get_object_or_404(IndividualSportList,
                                                                            pk=kwargs['individual_sport_list_pk'])

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(StudentForIndividualSportListUpdateView, self).get_form_kwargs()
        kwargs['individual_sport_list_id'] = self.individual_sport_list.id

        return kwargs

    def get_success_url(self):
        return reverse("main:individual_sport_list_students", kwargs={"pk": self.individual_sport_list.id})


class StudentForIndividualSportListDeleteView(IndividualSportListTestMixin, UserPassesTestMixin, BSModalDeleteView):
    model = Student
    template_name = 'main/school_isl/delete_student_for_individual_sport_list.html'
    context_object_name = 'data'
    success_message = 'Ο μαθητής διαγράφηκε με επιτυχία.'

    def dispatch(self, request, *args, **kwargs):
        self.individual_sport_list: IndividualSportList = get_object_or_404(IndividualSportList,
                                                                            pk=kwargs['individual_sport_list_pk'])

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("main:individual_sport_list_students", kwargs={"pk": self.individual_sport_list.id})

    #
    #  Views for DDE
    #


class DDE_SchoolRegistrationsView(DDE_TestMixin, UserPassesTestMixin, ListView):
    model = SchoolRegistration
    context_object_name = 'data'
    template_name = 'main/dde/school_registrations.html'

    def get_queryset(self):
        school_year = AppState.objects.first().active_sch_year
        school_registrations = SchoolRegistration.objects.filter(school_year=school_year,
                                                                 locked=True).order_by('id')

        return school_registrations

    def get_context_data(self, **kwargs):
        context = super(DDE_SchoolRegistrationsView, self).get_context_data(**kwargs)
        context['user_role'] = 'ΔΔΕ'
        context['title'] = 'Δηλώσεις Συμμετοχής στους Αγώνες'

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        return context


class DDE_TeamSportMainListsView(DDE_TestMixin, UserPassesTestMixin, ListView):
    model = TeamSportMainList
    context_object_name = 'data'
    template_name = 'main/dde/team_sport_main_lists.html'

    def get_queryset(self):
        school_year = AppState.objects.first().active_sch_year
        app_state_mode = AppState.objects.all().first().mode
        team_sport_main_lists = TeamSportMainList.objects.filter(mode=app_state_mode,
                                                                 school_year=school_year,
                                                                 locked=True).order_by('id')

        return team_sport_main_lists

    def get_context_data(self, **kwargs):
        context = super(DDE_TeamSportMainListsView, self).get_context_data(**kwargs)
        context['user_role'] = 'ΔΔΕ'
        context['title'] = 'Λίστες Ομάδων'

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        return context


class DDE_TeamSportPhaseListsView(DDE_TestMixin, UserPassesTestMixin, ListView):
    model = TeamSportPhaseList
    context_object_name = 'data'
    template_name = 'main/dde/team_sport_phase_lists.html'

    def get_queryset(self):
        school_year = AppState.objects.first().active_sch_year
        app_state_mode = AppState.objects.all().first().mode
        team_sport_phase_lists = TeamSportPhaseList.objects.filter(mode=app_state_mode,
                                                                   school_year=school_year,
                                                                   locked=True).order_by('id')

        for item in team_sport_phase_lists:
            team_sport_ml = item.team_sport_main_list
            team_sport_ml.students_count = team_sport_ml.team_sport_students.all().count()
            team_sport_ml.save()

            if item.phase == '1η':
                item.students_count = team_sport_ml.team_sport_students.filter(plays_in_phase_1=True).count()
            elif item.phase == '2η':
                item.students_count = team_sport_ml.team_sport_students.filter(plays_in_phase_2=True).count()
            else:
                item.students_count = team_sport_ml.team_sport_students.filter(plays_in_phase_3=True).count()
            item.save()

        return team_sport_phase_lists

    def get_context_data(self, **kwargs):
        context = super(DDE_TeamSportPhaseListsView, self).get_context_data(**kwargs)
        context['user_role'] = 'ΔΔΕ'
        context['title'] = 'Καταστάσεις Συμμετοχής Ομάδων'

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        return context


class DDE_IndividualSportListsView(DDE_TestMixin, UserPassesTestMixin, ListView):
    model = IndividualSportList
    context_object_name = 'data'
    template_name = 'main/dde/individual_sport_lists.html'

    def get_queryset(self):
        school_year = AppState.objects.first().active_sch_year
        app_state_mode = AppState.objects.all().first().mode
        individual_sport_lists_all = IndividualSportList.objects.filter(mode=app_state_mode, school_year=school_year,
                                                                        locked=True)
        data = list()
        for i in range(1, 4):
            individual_sport_lists = individual_sport_lists_all.filter(
                individual_sports_group_phase__phase=f'{i}η').order_by('id')

            individual_sports = set()
            individual_sports_qs = individual_sport_lists.values('individual_sport').distinct()

            for individual_sport in individual_sports_qs:
                individual_sports.add(individual_sport['individual_sport'])

            individual_sports = sorted(individual_sports)

            for individual_sport in individual_sports:
                is_dict = dict()

                students_count = 0
                isl = individual_sport_lists.filter(individual_sport=individual_sport)
                for item in isl:
                    students_count += item.individual_sport_students.all().count()

                is_dict['school_year'] = school_year
                is_dict['sport'] = individual_sport
                is_dict['phase'] = f'{i}η'
                is_dict['sport_name'] = IndividualSport.objects.get(id=individual_sport).individual_sport
                is_dict['students_count'] = students_count

                data.append(is_dict)

        return data

    def get_context_data(self, **kwargs):
        context = super(DDE_IndividualSportListsView, self).get_context_data(**kwargs)
        context['user_role'] = 'ΔΔΕ'
        context['title'] = 'Αγωνίσματα'

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        return context


class DDE_IndividualSportsGroupsPhasesView(DDE_TestMixin, UserPassesTestMixin, ListView):
    model = IndividualSportsGroupPhase
    context_object_name = 'data'
    template_name = 'main/dde/individual_sports_groups_phases.html'

    def get_queryset(self):
        school_year = AppState.objects.first().active_sch_year
        app_state_mode = AppState.objects.all().first().mode
        individual_sports_groups_phases = IndividualSportsGroupPhase.objects.filter(mode=app_state_mode,
                                                                                    school_year=school_year,
                                                                                    locked=True).order_by('id')

        return individual_sports_groups_phases

    def get_context_data(self, **kwargs):
        context = super(DDE_IndividualSportsGroupsPhasesView, self).get_context_data(**kwargs)
        context['user_role'] = 'ΔΔΕ'
        context['title'] = 'Καταστάσεις Συμμετοχής Ατομικών Αθλημάτων'

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        return context


class TeamSportMainListUnlockView(DDE_TestMixin, UserPassesTestMixin, BSModalUpdateView):
    model = TeamSportMainList
    form_class = TeamSportMainListUnlockForm
    template_name = 'main/dde/unlock_team_sport_main_list.html'
    success_url = reverse_lazy('main:dde_team_sport_main_lists')

    def get_context_data(self, **kwargs):
        context = super(TeamSportMainListUnlockView, self).get_context_data(**kwargs)

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        return context

    def form_valid(self, form):
        if not is_ajax(self.request):
            team_sport_ml: TeamSportMainList = form.instance
            team_sport_ml.locked = False

            phases = team_sport_ml.team_sport_phases.all()

            app_state_mode = AppState.objects.all().first().mode
            if app_state_mode == 'Σχολικά Πρωταθλήματα':
                UnlockEntry.objects.create(dde_user=self.request.user,
                                           list_to_unlock=f'Λίστα Ομάδας {team_sport_ml} για το {team_sport_ml.school.last_name}',
                                           unlock_date_time=timezone.now())

                for phase in phases:
                    UnlockEntry.objects.create(dde_user=self.request.user,
                                               list_to_unlock=f'[Διαγραφή] Κατάσταση Συμμετοχής Ομάδας {phase} για το {phase.school.last_name}',
                                               unlock_date_time=timezone.now())
                    phase.delete()

                messages.success(self.request, 'Η Λίστα Ομάδας ξεκλείδωσε με επιτυχία.')
            else:
                UnlockEntry.objects.create(dde_user=self.request.user,
                                           list_to_unlock=f'Κατάσταση Συμμετοχής Ομάδας {team_sport_ml} για το {team_sport_ml.school.last_name}',
                                           unlock_date_time=timezone.now())

                messages.success(self.request, 'Η Κατάσταση Συμμετοχής Ομάδας ξεκλείδωσε με επιτυχία.')

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        self.team_sport_ml = TeamSportMainList.objects.get(pk=self.kwargs.get('pk'))

        return super().dispatch(request, *args, **kwargs)


class TeamSportPhaseListUnlockView(DDE_TestMixin, UserPassesTestMixin, BSModalUpdateView):
    model = TeamSportPhaseList
    form_class = TeamSportPhaseListUnlockForm
    template_name = 'main/dde/unlock_team_sport_phase_list.html'
    success_message = 'Η Κατάσταση Συμμετοχής Ομάδας ξεκλείδωσε με επιτυχία.'
    success_url = reverse_lazy('main:dde_team_sport_phase_lists')

    def form_valid(self, form):
        team_sport_pl: TeamSportPhaseList = form.instance
        team_sport_pl.locked = False

        if not is_ajax(self.request):
            UnlockEntry.objects.create(dde_user=self.request.user,
                                       list_to_unlock=f'Κατάσταση Συμμετοχής Ομάδας {team_sport_pl} για {team_sport_pl.school.last_name}',
                                       unlock_date_time=timezone.now())

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        self.team_sport_pl = TeamSportPhaseList.objects.get(pk=self.kwargs.get('pk'))

        return super().dispatch(request, *args, **kwargs)


class IndividualSportsGroupPhaseUnlockView(DDE_TestMixin, UserPassesTestMixin, BSModalFormView):
    model = IndividualSportsGroupPhase
    form_class = IndividualSportsGroupPhaseUnlockForm
    template_name = 'main/dde/unlock_individual_sports_group_phase.html'
    success_url = reverse_lazy('main:dde_individual_sports_groups_phases')

    def get_context_data(self, **kwargs):
        context = super(IndividualSportsGroupPhaseUnlockView, self).get_context_data(**kwargs)

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        return context

    def form_valid(self, form):
        if not is_ajax(self.request):
            individual_sports_group_phase = IndividualSportsGroupPhase.objects.get(pk=self.kwargs.get('pk'))
            individual_sports_group_phase.locked = False
            individual_sports_group_phase.save()

            individual_sport_lists = individual_sports_group_phase.individual_sport_lists.all()
            individual_sport_lists.update(locked=False)

            UnlockEntry.objects.create(dde_user=self.request.user,
                                       list_to_unlock=f'{individual_sports_group_phase} για {individual_sports_group_phase.school.last_name}',
                                       unlock_date_time=timezone.now())

            messages.success(self.request, 'Η Κατάσταση Συμμετοχής Ατομικού Αθλήματος ξεκλείδωσε με επιτυχία.')

        return super().form_valid(form)


class SchoolRegistrationUnlockView(DDE_TestMixin, UserPassesTestMixin, BSModalFormView):
    model = SchoolRegistration
    form_class = SchoolRegistrationUnlockForm
    template_name = 'main/dde/unlock_school_registration.html'
    success_url = reverse_lazy('main:dde_school_registrations')

    def get_context_data(self, **kwargs):
        context = super(SchoolRegistrationUnlockView, self).get_context_data(**kwargs)

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode
        context['school'] = self.school_registration.school.last_name

        return context

    def form_valid(self, form):
        self.school_registration.locked = False
        self.school_registration.save()

        if not is_ajax(self.request):
            UnlockEntry.objects.create(dde_user=self.request.user,
                                       list_to_unlock=f'Δήλωση Συμμετοχής Ομάδας για {self.school_registration.school.last_name}',
                                       unlock_date_time=timezone.now())

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        self.school_registration = SchoolRegistration.objects.get(pk=self.kwargs.get('pk'))

        return super().dispatch(request, *args, **kwargs)


def dde_lists_for_printing(request):
    user = request.user
    trusted_users = TrustedUser.objects.filter(trusted_user=user, enabled=True)

    user_role = 'N/A'

    if trusted_users:
        user_role = trusted_users[0].user_role

    if user_role != 'ΔΔΕ':
        return redirect("main:home")

    app_state_mode = AppState.objects.all().first().mode

    context = {'title': 'Εκτυπώσεις',
               'user_role': user_role,
               'app_state_mode': app_state_mode}

    return render(request, 'main/dde/lists_for_printing.html', context)


class AppStateModeToggleView(DDE_TestMixin, UserPassesTestMixin, UpdateView):
    model = AppState
    form_class = AppStateModeToggleForm
    template_name = 'main/dde/toggle_mode.html'
    success_url = reverse_lazy('main:home')

    def get_context_data(self, **kwargs):
        context = super(AppStateModeToggleView, self).get_context_data(**kwargs)
        context['user_role'] = 'ΔΔΕ'
        context['title'] = 'Αλλαγή λειτουργίας εφαρμογής'

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        return context

    def form_valid(self, form):
        messages.success(self.request, 'Η αλλαγή λειτουργίας έγινε με επιτυχία.')

        app_state_mode = form.instance.mode
        app_state_se = form.instance.schools_enabled

        TeamSport.objects.update(enabled=False)
        TeamSport.objects.filter(mode=app_state_mode).update(enabled=True)
        IndividualSport.objects.update(enabled=False)
        IndividualSport.objects.filter(mode=app_state_mode).update(enabled=True)

        if app_state_se == 'Τα σχολεία είναι ενεργοποιημένα':
            if app_state_mode == 'Σχολικά Πρωταθλήματα':
                TrustedUser.objects.filter(school_type='ΛΥΚΕΙΟ').update(enabled=True)
                TrustedUser.objects.filter(school_type='ΓΥΜΝΑΣΙΟ').update(enabled=False)
            else:
                TrustedUser.objects.filter(school_type='ΛΥΚΕΙΟ').update(enabled=False)
                TrustedUser.objects.filter(school_type='ΓΥΜΝΑΣΙΟ').update(enabled=True)

        return super().form_valid(form)

    def get_object(self, queryset=None):
        return AppState.objects.all().first()


class AppStateSchoolsEnabledToggleView(DDE_TestMixin, UserPassesTestMixin, UpdateView):
    model = AppState
    form_class = AppStateSchoolsEnabledToggleForm
    template_name = 'main/dde/toggle_schools_enabled.html'
    success_url = reverse_lazy('main:home')

    def get_context_data(self, **kwargs):
        context = super(AppStateSchoolsEnabledToggleView, self).get_context_data(**kwargs)
        context['user_role'] = 'ΔΔΕ'
        context['title'] = 'Αλλαγή λειτουργίας εφαρμογής'

        app_state_mode = AppState.objects.all().first().mode
        context['app_state_mode'] = app_state_mode

        return context

    def form_valid(self, form):
        app_state_mode = form.instance.mode
        app_state_se = form.instance.schools_enabled

        if app_state_se == 'Τα σχολεία είναι ενεργοποιημένα':
            if app_state_mode == 'Σχολικά Πρωταθλήματα':
                TrustedUser.objects.filter(school_type='ΛΥΚΕΙΟ').update(enabled=True)
                TrustedUser.objects.filter(school_type='ΓΥΜΝΑΣΙΟ').update(enabled=False)
            else:
                TrustedUser.objects.filter(school_type='ΛΥΚΕΙΟ').update(enabled=False)
                TrustedUser.objects.filter(school_type='ΓΥΜΝΑΣΙΟ').update(enabled=True)

            messages.success(self.request, 'Η ενεργοποίηση των σχολείων έγινε με επιτυχία.')
        else:
            TrustedUser.objects.filter(user_role='ΣΧΟΛΕΙΟ').update(enabled=False)

            messages.success(self.request, 'Η απενεργοποίηση των σχολείων έγινε με επιτυχία.')

        return super().form_valid(form)

    def get_object(self, queryset=None):
        return AppState.objects.all().first()
