from .models import (
    AppState,
    SchoolRegistration,
    TeamSportMainList,
    TeamSportPhaseList,
    IndividualSportList,
    IndividualSportsGroupPhase,
    Student)
from bootstrap_modal_forms.forms import BSModalModelForm
from .common import (
    get_school_year,
    MIN_AGE,
    MAX_AGE
)
from django.core.exceptions import ValidationError
from datetime import date
from django.shortcuts import get_object_or_404
from django.forms import HiddenInput, ModelForm
from crispy_forms.helper import FormHelper

MAX_TEAMS_GENERIC = 2
MAX_TEAMS_BASKETBALL = 3


class SchoolRegistrationSubmitForm(BSModalModelForm):
    class Meta:
        model = SchoolRegistration
        fields = ['school']
        widgets = {'school': HiddenInput(), }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['school'].disabled = True
        self.fields['school'].initial = self.request.user


class SchoolRegistrationForm(ModelForm):
    class Meta:
        model = SchoolRegistration
        fields = ['football_boys',
                  'football_girls',
                  'football_mix_1',
                  'football_mix_2',
                  'football_mix_school',
                  'handball_boys',
                  'handball_girls',
                  'handball_mix_1',
                  'handball_mix_2',
                  'handball_mix_school',
                  'basketball_boys',
                  'basketball_girls',
                  'basketball_mix_1',
                  'basketball_mix_2',
                  'basketball_mix_school',
                  'beach_volleyball_boys',
                  'beach_volleyball_girls',
                  'beach_volleyball_mix_1',
                  'beach_volleyball_mix_2',
                  'beach_volleyball_mix_school',
                  'volleyball_boys',
                  'volleyball_girls',
                  'volleyball_mix_1',
                  'volleyball_mix_2',
                  'volleyball_mix_school',
                  'swimming_boys',
                  'swimming_girls',
                  'track_boys',
                  'track_girls',
                  'fencing_boys',
                  'fencing_girls',
                  'tennis_boys',
                  'tennis_girls'
                  ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        school_year = AppState.objects.first().active_sch_year
        school_registration = SchoolRegistration.objects.filter(school=self.request.user,
                                                                school_year=school_year).first()

        app_state_mode = AppState.objects.all().first().mode
        if app_state_mode == 'Σχολικά Πρωταθλήματα':
            self.fields['football_mix_1'].disabled = True
            self.fields['football_mix_2'].disabled = True
            self.fields['football_mix_school'].disabled = True
            self.fields['handball_mix_1'].disabled = True
            self.fields['handball_mix_2'].disabled = True
            self.fields['handball_mix_school'].disabled = True
            self.fields['basketball_mix_1'].disabled = True
            self.fields['basketball_mix_2'].disabled = True
            self.fields['basketball_mix_school'].disabled = True
            self.fields['beach_volleyball_mix_1'].disabled = True
            self.fields['beach_volleyball_mix_2'].disabled = True
            self.fields['beach_volleyball_mix_school'].disabled = True
            self.fields['volleyball_mix_1'].disabled = True
            self.fields['volleyball_mix_2'].disabled = True
            self.fields['volleyball_mix_school'].disabled = True
            self.fields['swimming_boys'].disabled = True
            self.fields['swimming_girls'].disabled = True
            self.fields['fencing_boys'].disabled = True
            self.fields['fencing_girls'].disabled = True
            self.fields['tennis_boys'].disabled = True
            self.fields['tennis_girls'].disabled = True

        if school_registration.locked:
            self.fields['football_boys'].disabled = True
            self.fields['football_girls'].disabled = True
            self.fields['football_mix_1'].disabled = True
            self.fields['football_mix_2'].disabled = True
            self.fields['football_mix_school'].disabled = True
            self.fields['handball_boys'].disabled = True
            self.fields['handball_girls'].disabled = True
            self.fields['handball_mix_1'].disabled = True
            self.fields['handball_mix_2'].disabled = True
            self.fields['handball_mix_school'].disabled = True
            self.fields['basketball_boys'].disabled = True
            self.fields['basketball_girls'].disabled = True
            self.fields['basketball_mix_1'].disabled = True
            self.fields['basketball_mix_2'].disabled = True
            self.fields['basketball_mix_school'].disabled = True
            self.fields['beach_volleyball_boys'].disabled = True
            self.fields['beach_volleyball_girls'].disabled = True
            self.fields['beach_volleyball_mix_1'].disabled = True
            self.fields['beach_volleyball_mix_2'].disabled = True
            self.fields['beach_volleyball_mix_school'].disabled = True
            self.fields['volleyball_boys'].disabled = True
            self.fields['volleyball_girls'].disabled = True
            self.fields['volleyball_mix_1'].disabled = True
            self.fields['volleyball_mix_2'].disabled = True
            self.fields['volleyball_mix_school'].disabled = True
            self.fields['swimming_boys'].disabled = True
            self.fields['swimming_girls'].disabled = True
            self.fields['track_boys'].disabled = True
            self.fields['track_girls'].disabled = True
            self.fields['fencing_boys'].disabled = True
            self.fields['fencing_girls'].disabled = True
            self.fields['tennis_boys'].disabled = True
            self.fields['tennis_girls'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        football_boys = cleaned_data.get('football_boys')
        football_girls = cleaned_data.get('football_girls')
        football_mix_1 = cleaned_data.get('football_mix_1')
        football_mix_2 = cleaned_data.get('football_mix_2')
        football_mix_school = cleaned_data.get('football_mix_school')
        handball_boys = cleaned_data.get('handball_boys')
        handball_girls = cleaned_data.get('handball_girls')
        handball_mix_1 = cleaned_data.get('handball_mix_1')
        handball_mix_2 = cleaned_data.get('handball_mix_2')
        handball_mix_school = cleaned_data.get('handball_mix_school')
        basketball_boys = cleaned_data.get('basketball_boys')
        basketball_girls = cleaned_data.get('basketball_girls')
        basketball_mix_1 = cleaned_data.get('basketball_mix_1')
        basketball_mix_2 = cleaned_data.get('basketball_mix_2')
        basketball_mix_school = cleaned_data.get('basketball_mix_school')
        beach_volleyball_boys = cleaned_data.get('beach_volleyball_boys')
        beach_volleyball_girls = cleaned_data.get('beach_volleyball_girls')
        beach_volleyball_mix_1 = cleaned_data.get('beach_volleyball_mix_1')
        beach_volleyball_mix_2 = cleaned_data.get('beach_volleyball_mix_2')
        beach_volleyball_mix_school = cleaned_data.get('beach_volleyball_mix_school')
        volleyball_boys = cleaned_data.get('volleyball_boys')
        volleyball_girls = cleaned_data.get('volleyball_girls')
        volleyball_mix_1 = cleaned_data.get('volleyball_mix_1')
        volleyball_mix_2 = cleaned_data.get('volleyball_mix_2')
        volleyball_mix_school = cleaned_data.get('volleyball_mix_school')
        swimming_boys = cleaned_data.get('swimming_boys')
        swimming_girls = cleaned_data.get('swimming_girls')
        track_boys = cleaned_data.get('track_boys')
        track_girls = cleaned_data.get('track_girls')
        fencing_boys = cleaned_data.get('fencing_boys')
        fencing_girls = cleaned_data.get('fencing_girls')
        tennis_boys = cleaned_data.get('tennis_boys')
        tennis_girls = cleaned_data.get('tennis_girls')

        app_state_mode = AppState.objects.all().first().mode

        if int(football_boys) > MAX_TEAMS_GENERIC:
            self.add_error('football_boys', f"Η τιμή πρέπει να είναι μέχρι και {MAX_TEAMS_GENERIC}.")
        if int(football_girls) > MAX_TEAMS_GENERIC:
            self.add_error('football_girls', f"Η τιμή πρέπει να είναι μέχρι και {MAX_TEAMS_GENERIC}.")
        if app_state_mode != 'Σχολικά Πρωταθλήματα':
            if int(football_mix_1) > 0 and int(football_boys) + int(football_girls) > 0:
                self.add_error('football_mix_1', f"Έχετε δηλώσει Ομάδες Αγοριών ή/και Κοριτσιών.")
            if int(football_mix_1) > 2 * MAX_TEAMS_GENERIC:
                self.add_error('football_mix_1', f"Η τιμή πρέπει να είναι μέχρι και {2 * MAX_TEAMS_GENERIC}.")
            if int(football_mix_2) > MAX_TEAMS_GENERIC:
                self.add_error('football_mix_2', f"Η τιμή πρέπει να είναι μέχρι και {MAX_TEAMS_GENERIC}.")
            if int(football_mix_2) > 0 and football_mix_school == '---':
                self.add_error('football_mix_school', f"Έχετε δηλώσει Μικτή Ομάδα (ΣΜΕΑ + Γενικής).")
            if int(football_mix_2) == 0 and football_mix_school != '---':
                self.add_error('football_mix_2', f"Έχετε δηλώσει Σχολείο για Μικτή Ομάδα (ΣΜΕΑ + Γενικής).")

        if int(handball_boys) > MAX_TEAMS_GENERIC:
            self.add_error('handball_boys', f"Η τιμή πρέπει να είναι μέχρι και {MAX_TEAMS_GENERIC}.")
        if int(handball_girls) > MAX_TEAMS_GENERIC:
            self.add_error('handball_girls', f"Η τιμή πρέπει να είναι μέχρι και {MAX_TEAMS_GENERIC}.")
        if app_state_mode != 'Σχολικά Πρωταθλήματα':
            if int(handball_mix_1) > 0 and int(handball_boys) + int(handball_girls) > 0:
                self.add_error('handball_mix_1', f"Έχετε δηλώσει Ομάδες Αγοριών ή/και Κοριτσιών.")
            if int(handball_mix_1) > 2 * MAX_TEAMS_GENERIC:
                self.add_error('handball_mix_1', f"Η τιμή πρέπει να είναι μέχρι και {2 * MAX_TEAMS_GENERIC}.")
            if int(handball_mix_2) > MAX_TEAMS_GENERIC:
                self.add_error('handball_mix_2', f"Η τιμή πρέπει να είναι μέχρι και {MAX_TEAMS_GENERIC}.")
            if int(handball_mix_2) > 0 and handball_mix_school == '---':
                self.add_error('handball_mix_school', f"Έχετε δηλώσει Μικτή Ομάδα (ΣΜΕΑ + Γενικής).")
            if int(handball_mix_2) == 0 and handball_mix_school != '---':
                self.add_error('handball_mix_2', f"Έχετε δηλώσει Σχολείο για Μικτή Ομάδα (ΣΜΕΑ + Γενικής).")

        if int(basketball_boys) > MAX_TEAMS_BASKETBALL:
            self.add_error('basketball_boys', f"Η τιμή πρέπει να είναι μέχρι και {MAX_TEAMS_BASKETBALL}.")
        if int(basketball_girls) > MAX_TEAMS_BASKETBALL:
            self.add_error('basketball_girls', f"Η τιμή πρέπει να είναι μέχρι και {MAX_TEAMS_BASKETBALL}.")
        if app_state_mode != 'Σχολικά Πρωταθλήματα':
            if int(basketball_mix_1) > 0 and int(basketball_boys) + int(basketball_girls) > 0:
                self.add_error('basketball_mix_1', f"Έχετε δηλώσει Ομάδες Αγοριών ή/και Κοριτσιών.")
            if int(basketball_mix_1) > 2 * MAX_TEAMS_BASKETBALL:
                self.add_error('basketball_mix_1', f"Η τιμή πρέπει να είναι μέχρι και {2 * MAX_TEAMS_BASKETBALL}.")
            if int(basketball_mix_2) > MAX_TEAMS_BASKETBALL:
                self.add_error('basketball_mix_2', f"Η τιμή πρέπει να είναι μέχρι και {MAX_TEAMS_BASKETBALL}.")
            if int(basketball_mix_2) > 0 and basketball_mix_school == '---':
                self.add_error('basketball_mix_school', f"Έχετε δηλώσει Μικτή Ομάδα (ΣΜΕΑ + Γενικής).")
            if int(basketball_mix_2) == 0 and basketball_mix_school != '---':
                self.add_error('basketball_mix_2', f"Έχετε δηλώσει Σχολείο για Μικτή Ομάδα (ΣΜΕΑ + Γενικής).")

        if int(beach_volleyball_boys) > MAX_TEAMS_GENERIC:
            self.add_error('beach_volleyball_boys', f"Η τιμή πρέπει να είναι μέχρι και {MAX_TEAMS_GENERIC}.")
        if int(beach_volleyball_girls) > MAX_TEAMS_GENERIC:
            self.add_error('beach_volleyball_girls', f"Η τιμή πρέπει να είναι μέχρι και {MAX_TEAMS_GENERIC}.")
        if app_state_mode != 'Σχολικά Πρωταθλήματα':
            if int(beach_volleyball_mix_1) > 0 and int(beach_volleyball_boys) + int(beach_volleyball_girls) > 0:
                self.add_error('beach_volleyball_mix_1', f"Έχετε δηλώσει Ομάδες Αγοριών ή/και Κοριτσιών.")
            if int(beach_volleyball_mix_1) > 2 * MAX_TEAMS_GENERIC:
                self.add_error('beach_volleyball_mix_1', f"Η τιμή πρέπει να είναι μέχρι και {2 * MAX_TEAMS_GENERIC}.")
            if int(beach_volleyball_mix_2) > MAX_TEAMS_GENERIC:
                self.add_error('beach_volleyball_mix_2', f"Η τιμή πρέπει να είναι μέχρι και {MAX_TEAMS_GENERIC}.")
            if int(beach_volleyball_mix_2) > 0 and beach_volleyball_mix_school == '---':
                self.add_error('beach_volleyball_mix_school', f"Έχετε δηλώσει Μικτή Ομάδα (ΣΜΕΑ + Γενικής).")
            if int(beach_volleyball_mix_2) == 0 and beach_volleyball_mix_school != '---':
                self.add_error('beach_volleyball_mix_2', f"Έχετε δηλώσει Σχολείο για Μικτή Ομάδα (ΣΜΕΑ + Γενικής).")

        if int(volleyball_boys) > MAX_TEAMS_GENERIC:
            self.add_error('volleyball_boys', f"Η τιμή πρέπει να είναι μέχρι και {MAX_TEAMS_GENERIC}.")
        if int(volleyball_girls) > MAX_TEAMS_GENERIC:
            self.add_error('volleyball_girls', f"Η τιμή πρέπει να είναι μέχρι και {MAX_TEAMS_GENERIC}.")
        if app_state_mode != 'Σχολικά Πρωταθλήματα':
            if int(volleyball_mix_1) > 0 and int(volleyball_boys) + int(volleyball_girls) > 0:
                self.add_error('volleyball_mix_1', f"Έχετε δηλώσει Ομάδες Αγοριών ή/και Κοριτσιών.")
            if int(volleyball_mix_1) > 2 * MAX_TEAMS_GENERIC:
                self.add_error('volleyball_mix_1', f"Η τιμή πρέπει να είναι μέχρι και {2 * MAX_TEAMS_GENERIC}.")
            if int(volleyball_mix_2) > MAX_TEAMS_GENERIC:
                self.add_error('volleyball_mix_2', f"Η τιμή πρέπει να είναι μέχρι και {MAX_TEAMS_GENERIC}.")
            if int(volleyball_mix_2) > 0 and volleyball_mix_school == '---':
                self.add_error('volleyball_mix_school', f"Έχετε δηλώσει Μικτή Ομάδα (ΣΜΕΑ + Γενικής).")
            if int(volleyball_mix_2) == 0 and volleyball_mix_school != '---':
                self.add_error('volleyball_mix_2', f"Έχετε δηλώσει Σχολείο για Μικτή Ομάδα (ΣΜΕΑ + Γενικής).")

        if app_state_mode != 'Σχολικά Πρωταθλήματα':
            teams = int(football_boys) + int(football_girls) + int(football_mix_1) + int(football_mix_2) + \
                    int(handball_boys) + int(handball_girls) + int(handball_mix_1) + int(handball_mix_2) + \
                    int(basketball_boys) + int(basketball_girls) + int(basketball_mix_1) + int(basketball_mix_2) + \
                    int(beach_volleyball_boys) + int(beach_volleyball_girls) + int(beach_volleyball_mix_1) + \
                    int(beach_volleyball_mix_2) + \
                    int(volleyball_boys) + int(volleyball_girls) + int(volleyball_mix_1) + int(volleyball_mix_2)
        else:
            teams = int(football_boys) + int(football_girls) + \
                    int(handball_boys) + int(handball_girls) + \
                    int(basketball_boys) + int(basketball_girls) + \
                    int(beach_volleyball_boys) + int(beach_volleyball_girls) + \
                    int(volleyball_boys) + int(volleyball_girls)

        individual = any([swimming_boys, swimming_girls, track_boys, track_girls, fencing_boys, fencing_girls,
                          tennis_boys, tennis_girls])

        if teams == 0 and not individual:
            raise ValidationError("Πρέπει να υποβάλετε τουλάχιστον μία ομάδα ή ένα ατομικό άθλημα.")


class TeamSportMainListForm(BSModalModelForm):
    class Meta:
        model = TeamSportMainList
        fields = ['mode', 'team_sport', 'gender', 'pt_teacher']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mode'].disabled = True
        self.fields['mode'].initial = AppState.objects.all().first().mode

        if self.instance.pk:
            students_count = TeamSportMainList.objects.get(pk=self.instance.pk).team_sport_students.count()

            if students_count > 0:
                self.fields['team_sport'].disabled = True
                self.fields['gender'].disabled = True

    def clean(self):
        cleaned_data = super().clean()

        clean_school_year = AppState.objects.first().active_sch_year
        clean_team_sport = self.cleaned_data['team_sport']
        clean_gender = self.cleaned_data['gender']
        app_state_mode = AppState.objects.all().first().mode

        conflicts = TeamSportMainList.objects.filter(mode=app_state_mode,
                                                     school=self.request.user,
                                                     school_year=clean_school_year,
                                                     team_sport=clean_team_sport,
                                                     gender=clean_gender).exclude(pk=self.instance.pk)

        if any(conflicts):
            raise ValidationError('Η λίστα αυτή υπάρχει ήδη !!!', code='invalid')

        return cleaned_data


class TeamSportMainListSubmitForm(BSModalModelForm):
    class Meta:
        model = TeamSportMainList
        fields = ['team_sport', 'gender', 'pt_teacher']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['team_sport'].disabled = True
        self.fields['gender'].disabled = True
        self.fields['pt_teacher'].disabled = True


class StudentForTeamSportForm(BSModalModelForm):
    class Meta:
        model = Student
        fields = ['mode', 'plays_in', 'registry_no', 'last_name', 'first_name', 'father_name', 'mother_name',
                  'year_of_birth', 'gender', 'school_class']

    def __init__(self, *args, **kwargs):
        self.team_sport_ml: TeamSportMainList = get_object_or_404(TeamSportMainList, pk=kwargs.pop('team_sport_ml_id'))
        super().__init__(*args, **kwargs)
        self.fields['mode'].disabled = True
        self.fields['mode'].initial = AppState.objects.all().first().mode
        self.fields['plays_in'].disabled = True
        self.fields['plays_in'].initial = 'Ομαδικό Άθλημα'

        if self.team_sport_ml.gender == 'Αγόρια':
            self.fields['gender'].initial = 'Αγόρι'
        else:
            self.fields['gender'].initial = 'Κορίτσι'
        self.fields['gender'].disabled = True

    def clean_year_of_birth(self):
        try:
            clean_year = int(self.cleaned_data['year_of_birth'])
        except ValueError:
            raise ValidationError("Το έτος πρέπει να είναι αριθμός.")

        cur_year = date.today().year

        if cur_year - clean_year < MIN_AGE or cur_year - clean_year > MAX_AGE:
            raise ValidationError("Η ηλικία του μαθητή πρέπει να είναι μεταξύ 12 και 18.")

        return clean_year

    def clean(self):
        cleaned_data = super().clean()

        clean_school_year = AppState.objects.first().active_sch_year
        clean_registry_no = self.cleaned_data['registry_no']
        app_state_mode = AppState.objects.all().first().mode

        conflicts = Student.objects.filter(mode=app_state_mode,
                                           plays_in='Ομαδικό Άθλημα',
                                           school=self.request.user,
                                           school_year=clean_school_year,
                                           registry_no=clean_registry_no).exclude(pk=self.instance.pk)

        if any(conflicts):
            raise ValidationError('Ο μαθητής υπάρχει ήδη !!!', code='invalid')

        return cleaned_data


class TeamSportPhaseListForm(BSModalModelForm):
    class Meta:
        model = TeamSportPhaseList
        fields = ['mode', 'team_sport_main_list', 'phase', 'pt_teacher']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mode'].disabled = True
        self.fields['mode'].initial = AppState.objects.all().first().mode

    def clean(self):
        cleaned_data = super().clean()

        clean_school_year = AppState.objects.first().active_sch_year
        clean_team_sport_ml = self.cleaned_data['team_sport_main_list']
        clean_phase = self.cleaned_data['phase']
        app_state_mode = AppState.objects.all().first().mode

        conflicts = TeamSportPhaseList.objects.filter(mode=app_state_mode,
                                                      school=self.request.user,
                                                      school_year=clean_school_year,
                                                      team_sport_main_list=clean_team_sport_ml,
                                                      phase=clean_phase).exclude(pk=self.instance.pk)

        if any(conflicts):
            raise ValidationError('Η κατάσταση αυτή υπάρχει ήδη !!!', code='invalid')

        return cleaned_data


class TeamSportPhaseListSubmitForm(BSModalModelForm):
    class Meta:
        model = TeamSportPhaseList
        fields = ['team_sport_main_list', 'phase', 'pt_teacher']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['team_sport_main_list'].disabled = True
        self.fields['phase'].disabled = True
        self.fields['pt_teacher'].disabled = True


class IndividualSportsGroupPhaseForm(BSModalModelForm):
    class Meta:
        model = IndividualSportsGroupPhase
        fields = ['mode', 'individual_sports_group', 'phase', 'pt_teacher']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mode'].disabled = True
        self.fields['mode'].initial = AppState.objects.all().first().mode

        if AppState.objects.all().first().mode != 'Σχολικά Πρωταθλήματα':
            self.fields['phase'].disabled = True
            self.fields['phase'].initial = '1η'

        if self.instance.pk:
            individual_sport_lists_count = IndividualSportsGroupPhase.objects.get(
                pk=self.instance.pk).individual_sport_lists.count()

            if individual_sport_lists_count > 0:
                self.fields['individual_sports_group'].disabled = True
                # self.fields['phase'].disabled = True

    def clean(self):
        cleaned_data = super().clean()

        clean_school_year = AppState.objects.first().active_sch_year
        clean_individual_sports_group = self.cleaned_data['individual_sports_group']
        clean_phase = self.cleaned_data['phase']
        app_state_mode = AppState.objects.all().first().mode

        conflicts = IndividualSportsGroupPhase.objects.filter(mode=app_state_mode,
                                                              school=self.request.user,
                                                              school_year=clean_school_year,
                                                              individual_sports_group=clean_individual_sports_group,
                                                              phase=clean_phase).exclude(pk=self.instance.pk)

        if any(conflicts):
            raise ValidationError('Η κατάσταση αυτή υπάρχει ήδη !!!', code='invalid')

        return cleaned_data


class IndividualSportListForm(BSModalModelForm):
    class Meta:
        model = IndividualSportList
        fields = ['mode', 'individual_sport', 'pt_teacher']

    def __init__(self, *args, **kwargs):
        self.individual_sports_group_phase = get_object_or_404(IndividualSportsGroupPhase,
                                                               pk=kwargs.pop('individual_sports_group_phase_id'))
        super().__init__(*args, **kwargs)
        self.fields['mode'].disabled = True
        self.fields['mode'].initial = AppState.objects.all().first().mode

    def clean(self):
        cleaned_data = super().clean()
        clean_individual_sport = self.cleaned_data['individual_sport']

        conflicts = IndividualSportList.objects.filter(individual_sport=clean_individual_sport,
                                                       individual_sports_group_phase=self.individual_sports_group_phase).exclude(
            pk=self.instance.pk)

        if any(conflicts):
            raise ValidationError('Η κατάσταση αυτή υπάρχει ήδη !!!', code='invalid')

        return cleaned_data


class IndividualSportsGroupPhaseSubmitForm(BSModalModelForm):
    class Meta:
        model = IndividualSportsGroupPhase
        fields = ['school']
        widgets = {'school': HiddenInput(), }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['school'].disabled = True
        self.fields['school'].initial = self.request.user


class StudentForIndividualSportForm(BSModalModelForm):
    class Meta:
        model = Student
        fields = ['mode', 'plays_in', 'registry_no', 'last_name', 'first_name', 'father_name', 'mother_name',
                  'year_of_birth', 'gender', 'school_class', 'individual_sport_plays_in_phase']

    def __init__(self, *args, **kwargs):
        self.individual_sport_list: IndividualSportList = get_object_or_404(IndividualSportList,
                                                                            pk=kwargs.pop('individual_sport_list_id'))
        super().__init__(*args, **kwargs)
        self.fields['mode'].disabled = True
        self.fields['mode'].initial = AppState.objects.all().first().mode
        self.fields['plays_in'].disabled = True
        self.fields['plays_in'].initial = 'Ατομικό Άθλημα'
        self.fields['individual_sport_plays_in_phase'].disabled = True
        self.fields[
            'individual_sport_plays_in_phase'].initial = self.individual_sport_list.individual_sports_group_phase.phase

    def clean_year_of_birth(self):
        try:
            clean_year = int(self.cleaned_data['year_of_birth'])
        except ValueError:
            raise ValidationError("Το έτος πρέπει να είναι αριθμός.")

        cur_year = date.today().year

        if cur_year - clean_year < MIN_AGE or cur_year - clean_year > MAX_AGE:
            raise ValidationError("Η ηλικία του μαθητή πρέπει να είναι μεταξύ 12 και 18.")

        return clean_year

    def clean(self):
        cleaned_data = super().clean()

        clean_school_year = AppState.objects.first().active_sch_year
        clean_registry_no = self.cleaned_data['registry_no']
        clean_individual_sport_plays_in_phase = self.cleaned_data['individual_sport_plays_in_phase']
        app_state_mode = AppState.objects.all().first().mode

        conflicts = Student.objects.filter(mode=app_state_mode,
                                           plays_in='Ατομικό Άθλημα',
                                           school=self.request.user,
                                           school_year=clean_school_year,
                                           registry_no=clean_registry_no,
                                           individual_sport_plays_in_phase=clean_individual_sport_plays_in_phase).exclude(
            pk=self.instance.pk)

        if any(conflicts):
            raise ValidationError('Ο μαθητής υπάρχει ήδη !!!', code='invalid')

        # Μπορεί να δηλωθεί ο μαθητής στη Φάση 2 αλλά σε άλλο αγώνισμα
        conflicts: StudentForIndividualSportForm = Student.objects.filter(mode=app_state_mode,
                                                                          plays_in='Ατομικό Άθλημα',
                                                                          school=self.request.user,
                                                                          school_year=clean_school_year,
                                                                          registry_no=clean_registry_no).exclude(
            pk=self.instance.pk).first()

        if conflicts:
            if conflicts.individual_sport_list.individual_sport != self.individual_sport_list.individual_sport:
                raise ValidationError('Ο μαθητής έχει δηλωθεί σε άλλο αγώνισμα στην προηγούμενη φάση !!!',
                                      code='invalid')

        return cleaned_data


class TeamSportMainListUnlockForm(BSModalModelForm):
    class Meta:
        model = TeamSportMainList
        fields = ['team_sport', 'gender', 'pt_teacher']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['team_sport'].disabled = True
        self.fields['gender'].disabled = True
        self.fields['pt_teacher'].disabled = True


class TeamSportPhaseListUnlockForm(BSModalModelForm):
    class Meta:
        model = TeamSportPhaseList
        fields = ['team_sport_main_list', 'phase', 'pt_teacher']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['team_sport_main_list'].disabled = True
        self.fields['phase'].disabled = True
        self.fields['pt_teacher'].disabled = True


class IndividualSportsGroupPhaseUnlockForm(BSModalModelForm):
    class Meta:
        model = IndividualSportsGroupPhase
        fields = ['school']
        widgets = {'school': HiddenInput(), }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['school'].disabled = True
        self.fields['school'].initial = self.request.user


class SchoolRegistrationUnlockForm(BSModalModelForm):
    class Meta:
        model = SchoolRegistration
        fields = ['school']
        widgets = {'school': HiddenInput(), }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['school'].disabled = True
        self.fields['school'].initial = self.request.user


class AppStateModeToggleForm(ModelForm):
    class Meta:
        model = AppState
        fields = ['mode', 'active_sch_year']

    def clean(self):
        cleaned_data = super().clean()
        clean_active_sch_year = cleaned_data.get('active_sch_year')

        if '-' not in clean_active_sch_year:
            raise ValidationError('Το Σχολικό Έτος δεν έχει σωστή μορφή, π.χ. 2024-2025. '
                                  'Λείπει ο χαρακτήρας "-" !!!',
                                  code='invalid')

        y1, y2 = clean_active_sch_year.split('-')

        if int(y1) != int(y2) - 1:
            raise ValidationError('Το Σχολικό Έτος δεν έχει σωστή μορφή, π.χ. 2024-2025. '
                                  'Τα έτη δεν είναι διαδοχικά !!!',
                                  code='invalid')


class AppStateSchoolsEnabledToggleForm(ModelForm):
    class Meta:
        model = AppState
        fields = ['schools_enabled']
