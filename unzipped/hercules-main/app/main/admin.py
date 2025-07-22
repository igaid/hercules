from django.contrib import admin
from .models import (
    AppState,
    TrustedUser,
    SchoolRegistration,
    TeamSport,
    TeamSportLimits,
    TeamSportMainList,
    TeamSportPhaseList,
    IndividualSportsGroup,
    IndividualSportsGroupPhase,
    IndividualSport,
    IndividualSportList,
    Student,
    UnlockEntry
)


@admin.register(AppState)
class AppStateAdmin(admin.ModelAdmin):
    list_display = ('id', 'mode', 'active_sch_year', 'schools_enabled')


@admin.register(TrustedUser)
class TrustedUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'trusted_user', 'name', 'user_role', 'school_type', 'enabled')
    ordering = ['id']


@admin.register(SchoolRegistration)
class SchoolRegistration(admin.ModelAdmin):
    list_display = ('id', 'school', 'school_year', 'locked')
    ordering = ['id']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'mode', 'school', 'school_year', 'registry_no', 'last_name', 'first_name', 'father_name',
                    'plays_in', 'plays_in_phase_1', 'plays_in_phase_2', 'plays_in_phase_3', 'individual_sport_plays_in_phase')
    ordering = ['id']


@admin.register(TeamSport)
class TeamSportAdmin(admin.ModelAdmin):
    list_display = ('id', 'mode', 'team_sport', 'enabled')
    ordering = ['id']


@admin.register(TeamSportLimits)
class TeamSportLimitsAdmin(admin.ModelAdmin):
    list_display = ('id', 'mode', 'team_sport', 'min_students_main_list', 'max_students_main_list',
                    'min_students_phase_list', 'max_students_phase_list')
    ordering = ['id']


@admin.register(IndividualSportsGroup)
class IndividualSportsGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'mode', 'individual_sports_group', 'enabled')
    ordering = ['id']


@admin.register(IndividualSport)
class IndividualSportAdmin(admin.ModelAdmin):
    list_display = ('id', 'mode', 'individual_sports_group', 'individual_sport', 'export_code', 'enabled')
    ordering = ['id']


@admin.register(IndividualSportsGroupPhase)
class IndividualSportsGroupPhaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'mode', 'school', 'school_year', 'individual_sports_group', 'phase', 'pt_teacher', 'locked',
                    'submit_date_time')
    ordering = ['id']


@admin.register(TeamSportMainList)
class TeamSportMainListAdmin(admin.ModelAdmin):
    list_display = ('id', 'mode', 'school', 'school_year', 'team_sport', 'gender', 'pt_teacher', 'locked',
                    'submit_date_time')
    ordering = ['id']


@admin.register(TeamSportPhaseList)
class TeamSportPhaseListAdmin(admin.ModelAdmin):
    list_display = ('id', 'mode', 'school', 'team_sport_main_list', 'phase', 'pt_teacher', 'locked', 'submit_date_time')
    ordering = ['id']


@admin.register(IndividualSportList)
class IndividualSportListAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'mode', 'school', 'school_year', 'individual_sport', 'pt_teacher', 'locked', 'submit_date_time')
    ordering = ['id']


@admin.register(UnlockEntry)
class UnlockEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'dde_user', 'list_to_unlock', 'unlock_date_time')
    ordering = ['id']
