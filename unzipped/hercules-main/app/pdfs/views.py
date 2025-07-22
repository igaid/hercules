from main.models import (
    AppState,
    TeamSportMainList,
    TeamSportPhaseList,
    IndividualSportList,
    IndividualSportsGroup,
    IndividualSportsGroupPhase,
    IndividualSport,
    TrustedUser,
    SchoolRegistration
)
from weasyprint import HTML
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import redirect
import tempfile
import os
from django.contrib.auth.models import User
from main.common import (
    get_school_year,
    FOOTBALL_STR,
    BASKETBALL_STR,
    VOLLEYBALL_STR,
    HANDBALL_STR
)
from slugify import slugify
import logging
from django.utils import timezone

logging.getLogger('fontTools').setLevel(logging.ERROR)
logging.getLogger('weasyprint').setLevel(logging.ERROR)


def pdf_school_registrations(request, *args, **kwargs):
    trusted_users = TrustedUser.objects.filter(trusted_user=request.user, enabled=True)

    user_role = 'N/A'

    if trusted_users:
        user_role = trusted_users[0].user_role

    if user_role != 'ΔΔΕ':
        return redirect('main:home')

    school_year = AppState.objects.first().active_sch_year
    school_registrations = SchoolRegistration.objects.filter(school_year=school_year,
                                                             locked=True)

    title = 'Δηλώσεις Συμμετοχής Ομάδων και Ατομικών Αθλημάτων'
    data = school_registrations
    app_state_mode = AppState.objects.all().first().mode

    # context passed in the template
    context = {
        'app_state_mode': app_state_mode,
        'title': title,
        'data': data,
        'school_year': school_year
    }
    template = 'pdfs/pdf_school_registrations.html'

    # render
    html_string = render_to_string(template, context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # http response
    response = HttpResponse(content_type='application/pdf;')
    filename = f'{slugify(title)}.pdf'
    response['Content-Disposition'] = f'inline; filename={filename}'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=False) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    if output is not None:
        output.close()
        os.unlink(output.name)

    return response


def pdf_school_registration(request, *args, **kwargs):
    school_registation = SchoolRegistration.objects.get(pk=kwargs.get('pk'))
    user = request.user
    trusted_users = TrustedUser.objects.filter(trusted_user=user, enabled=True)

    user_role = 'N/A'

    if trusted_users:
        user_role = trusted_users[0].user_role

    if not (school_registation.school == user or user_role == 'ΔΔΕ'):
        return redirect('main:home')

    if not school_registation.locked:
        return redirect('main:home')

    data = school_registation

    submit_date = str(school_registation.submit_date_time).split(" ")[0].split("-")
    submit_date_str = f'{submit_date[2]}-{submit_date[1]}-{submit_date[0]}'

    # context passed in the template
    school_year = AppState.objects.first().active_sch_year
    school = school_registation.school.last_name
    title = f'{school} - Δήλωση Συμμετοχής Ομάδων και Ατομικών Αθλημάτων'
    app_state_mode = AppState.objects.all().first().mode

    context = {
        'app_state_mode': app_state_mode,
        'title': title,
        'data': data,
        'school_year': school_year,
        'submit_date': submit_date_str
    }

    # render
    html_string = render_to_string('pdfs/pdf_school_registration.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # http response
    response = HttpResponse(content_type='application/pdf;')
    filename = f'{slugify(title)}.pdf'
    response['Content-Disposition'] = f'inline; filename={filename}'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=False) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    if output is not None:
        output.close()
        os.unlink(output.name)

    return response


def pdf_team_sport_main_list_students(request, *args, **kwargs):
    team_sport_ml = TeamSportMainList.objects.get(pk=kwargs.get('pk'))
    user = request.user
    trusted_users = TrustedUser.objects.filter(trusted_user=user, enabled=True)

    user_role = 'N/A'

    if trusted_users:
        user_role = trusted_users[0].user_role

    if not (team_sport_ml.school == user or user_role == 'ΔΔΕ'):
        return redirect('main:home')

    if not team_sport_ml.locked:
        return redirect('main:home')

    data = team_sport_ml.team_sport_students.all()

    # context passed in the template
    school_year = AppState.objects.first().active_sch_year
    school = team_sport_ml.school.last_name
    sport = str(team_sport_ml.team_sport)
    title = f'{school} - {str(team_sport_ml)}'

    if sport == BASKETBALL_STR:
        sport_t1 = 'ΚΑΛΑΘΟΣΦΑΙΡΙΣΗΣ'
        sport_t2 = 'ΣΤΗΝ ΚΑΛΑΘΟΣΦΑΙΡΙΣΗ'
        code = '1α'
    elif sport == FOOTBALL_STR:
        sport_t1 = 'ΠΟΔΟΣΦΑΙΡΟΥ'
        sport_t2 = 'ΣΤΟ ΠΟΔΟΣΦΑΙΡΟ'
        code = '1β'
    elif sport == VOLLEYBALL_STR:
        sport_t1 = 'ΠΕΤΟΣΦΑΙΡΙΣΗΣ'
        sport_t2 = 'ΣΤΗΝ ΠΕΤΟΣΦΑΙΡΙΣΗ'
        code = '1γ'
    elif sport == HANDBALL_STR:
        sport_t1 = 'ΧΕΙΡΟΣΦΑΙΡΙΣΗΣ'
        sport_t2 = 'ΣΤΗ ΧΕΙΡΟΣΦΑΙΡΙΣΗ'
        code = '1δ'
    else:
        sport_t1 = sport
        sport_t2 = sport
        code = '1'

    if team_sport_ml.gender == 'Αγόρια':
        students_gender = 'ΜΑΘΗΤΩΝ'
    else:
        students_gender = 'ΜΑΘΗΤΡΙΩΝ'

    submit_date = str(team_sport_ml.submit_date_time).split(" ")[0].split("-")
    submit_date_str = f'{submit_date[2]}-{submit_date[1]}-{submit_date[0]}'
    pt_teacher = team_sport_ml.pt_teacher

    app_state_mode = AppState.objects.all().first().mode

    context = {'title': title,
               'data': data,
               'school_year': school_year,
               'school': school,
               'sport_t1': sport_t1,
               'sport_t2': sport_t2,
               'code': code,
               'students_gender': students_gender,
               'submit_date': submit_date_str,
               'pt_teacher': pt_teacher,
               'app_state_mode': app_state_mode
               }

    # render
    html_string = render_to_string('pdfs/pdf_team_sport_main_list_students.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # http response
    response = HttpResponse(content_type='application/pdf;')
    filename = f'{slugify(title)}.pdf'
    response['Content-Disposition'] = f'inline; filename={filename}'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=False) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    if output is not None:
        output.close()
        os.unlink(output.name)

    return response


def pdf_team_sport_phase_list_students(request, *args, **kwargs):
    team_sport_pl = TeamSportPhaseList.objects.get(pk=kwargs.get('pk'))
    user = request.user
    trusted_users = TrustedUser.objects.filter(trusted_user=user, enabled=True)

    user_role = 'N/A'

    if trusted_users:
        user_role = trusted_users[0].user_role

    if not (team_sport_pl.school == user or user_role == 'ΔΔΕ'):
        return redirect('main:home')

    if not team_sport_pl.locked:
        return redirect('main:home')

    team_sport_ml = team_sport_pl.team_sport_main_list
    team_sport_students = team_sport_ml.team_sport_students.all()

    if team_sport_pl.phase == '1η':
        data = team_sport_students.filter(plays_in_phase_1=True)
    elif team_sport_pl.phase == '2η':
        data = team_sport_students.filter(plays_in_phase_2=True)
    else:
        data = team_sport_students.filter(plays_in_phase_3=True)

    phase = team_sport_pl.phase

    # context passed in the template
    school_year = team_sport_pl.school_year
    school = team_sport_ml.school.last_name
    sport = str(team_sport_ml.team_sport)
    title = f'{school} - {str(team_sport_ml)} - {phase} Φάση'

    if sport == BASKETBALL_STR:
        sport_t1 = 'ΚΑΛΑΘΟΣΦΑΙΡΙΣΗΣ'
        sport_t2 = 'ΣΤΗΝ ΚΑΛΑΘΟΣΦΑΙΡΙΣΗ'
        code = '3α'
    elif sport == FOOTBALL_STR:
        sport_t1 = 'ΠΟΔΟΣΦΑΙΡΟΥ'
        sport_t2 = 'ΣΤΟ ΠΟΔΟΣΦΑΙΡΟ'
        code = '3β'
    elif sport == VOLLEYBALL_STR:
        sport_t1 = 'ΠΕΤΟΣΦΑΙΡΙΣΗΣ'
        sport_t2 = 'ΣΤΗΝ ΠΕΤΟΣΦΑΙΡΙΣΗ'
        code = '3γ'
    elif sport == HANDBALL_STR:
        sport_t1 = 'ΧΕΙΡΟΣΦΑΙΡΙΣΗΣ'
        sport_t2 = 'ΣΤΗ ΧΕΙΡΟΣΦΑΙΡΙΣΗ'
        code = '3δ'
    else:
        sport_t1 = sport
        sport_t2 = sport
        code = '3'

    if team_sport_ml.gender == 'Αγόρια':
        students_gender = 'ΜΑΘΗΤΩΝ'
    else:
        students_gender = 'ΜΑΘΗΤΡΙΩΝ'

    submit_date = str(team_sport_ml.submit_date_time).split(" ")[0].split("-")
    submit_date_str = f'{submit_date[2]}-{submit_date[1]}-{submit_date[0]}'
    pt_teacher = team_sport_ml.pt_teacher

    app_state_mode = AppState.objects.all().first().mode

    context = {'title': title,
               'data': data,
               'school_year': school_year,
               'school': school,
               'sport_t1': sport_t1,
               'sport_t2': sport_t2,
               'code': code,
               'phase': phase,
               'students_gender': students_gender,
               'submit_date': submit_date_str,
               'pt_teacher': pt_teacher,
               'app_state_mode': app_state_mode
               }

    # render
    html_string = render_to_string('pdfs/pdf_team_sport_phase_list_students.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # http response
    response = HttpResponse(content_type='application/pdf;')
    filename = f'{slugify(title)}.pdf'
    response['Content-Disposition'] = f'inline; filename={filename}'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=False) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    if output is not None:
        output.close()
        os.unlink(output.name)

    return response


def pdf_dde_individual_sport_list_students(request, *args, **kwargs):
    user = request.user
    trusted_users = TrustedUser.objects.filter(trusted_user=user, enabled=True)

    user_role = 'N/A'

    if trusted_users:
        user_role = trusted_users[0].user_role

    if user_role != 'ΔΔΕ':
        return redirect('main:home')

    individual_sport = IndividualSport.objects.get(pk=kwargs.get('pk'))
    phase = kwargs.get('phase')

    school_year = AppState.objects.first().active_sch_year
    app_state_mode = AppState.objects.all().first().mode

    data_boys = list()
    data_girls = list()

    isls = IndividualSportList.objects.filter(mode=app_state_mode,
                                              individual_sport=individual_sport,
                                              school_year=school_year,
                                              individual_sports_group_phase__phase=phase,
                                              locked=True).order_by('school')

    for item in isls:
        data_boys += item.individual_sport_students.filter(gender='Αγόρι')
        data_girls += item.individual_sport_students.filter(gender='Κορίτσι')

    # context passed in the template
    school_year = AppState.objects.first().active_sch_year
    sport = str(individual_sport)

    app_state_mode = AppState.objects.all().first().mode

    title = f'{sport} - Φάση {phase} - {school_year}'
    context = {'title': title,
               'data_boys': data_boys,
               'data_girls': data_girls,
               'user_role': user_role,
               'school_year': school_year,
               'sport': f'{sport} - Φάση {phase}',
               'app_state_mode': app_state_mode}

    # render
    template = f'pdfs/pdf_dde_individual_sport_list_students-{individual_sport.export_code}.html'
    html_string = render_to_string(template, context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf()

    # http response
    response = HttpResponse(content_type='application/pdf;')
    filename = f'{slugify(title)}.pdf'
    response['Content-Disposition'] = f'inline; filename={filename}'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=False) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    if output is not None:
        output.close()
        os.unlink(output.name)

    return response


def pdf_team_sport_main_lists(request, order_by_list, title, template):
    user = request.user
    trusted_users = TrustedUser.objects.filter(trusted_user=user, enabled=True)

    user_role = 'N/A'

    if trusted_users:
        user_role = trusted_users[0].user_role

    if user_role != 'ΔΔΕ':
        return redirect('main:home')

    school_year = AppState.objects.first().active_sch_year
    app_state_mode = AppState.objects.all().first().mode
    team_sport_mls = TeamSportMainList.objects.filter(mode=app_state_mode,
                                                      school_year=school_year,
                                                      locked=True).order_by(*order_by_list)

    data = team_sport_mls

    # context passed in the template
    context = {'title': title, 'data': data}

    # render
    html_string = render_to_string(template, context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # http response
    response = HttpResponse(content_type='application/pdf;')
    filename = f'{slugify(title)}.pdf'
    response['Content-Disposition'] = f'inline; filename={filename}'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=False) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    if output is not None:
        output.close()
        os.unlink(output.name)

    return response


def pdf_team_sport_main_lists_school(request):
    order_by_list = ['school', 'team_sport', 'gender']
    template = 'pdfs/pdf_team_sport_main_lists_school.html'

    app_state_mode = AppState.objects.all().first().mode

    if app_state_mode == 'Σχολικά Πρωταθλήματα':
        title = 'Λίστες Ομάδων ανά Σχολείο'
    else:
        title = 'Καταστάσεις Συμμετοχής Ομάδων ανά Σχολείο'

    return pdf_team_sport_main_lists(request, order_by_list=order_by_list, title=title, template=template)


def pdf_team_sport_main_lists_sport(request):
    order_by_list = ['team_sport', 'gender', 'school']
    template = 'pdfs/pdf_team_sport_main_lists_sport.html'

    app_state_mode = AppState.objects.all().first().mode

    if app_state_mode == 'Σχολικά Πρωταθλήματα':
        title = 'Λίστες Ομάδων ανά Άθλημα'
    else:
        title = 'Καταστάσεις Συμμετοχής Ομάδων ανά Άθλημα'

    return pdf_team_sport_main_lists(request, order_by_list=order_by_list, title=title, template=template)


def pdf_team_sport_phase_lists(request, order_by_list, title, template):
    user = request.user
    trusted_users = TrustedUser.objects.filter(trusted_user=user, enabled=True)

    user_role = 'N/A'

    if trusted_users:
        user_role = trusted_users[0].user_role

    if user_role != 'ΔΔΕ':
        return redirect('main:home')

    school_year = AppState.objects.first().active_sch_year
    app_state_mode = AppState.objects.all().first().mode
    team_sport_pls = TeamSportPhaseList.objects.filter(mode=app_state_mode,
                                                       school_year=school_year,
                                                       locked=True).order_by(*order_by_list)

    for item in team_sport_pls:
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

    data = team_sport_pls

    # context passed in the template
    context = {'title': title, 'data': data}

    # render
    html_string = render_to_string(template, context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # http response
    response = HttpResponse(content_type='application/pdf;')
    filename = f'{slugify(title)}.pdf'
    response['Content-Disposition'] = f'inline; filename={filename}'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=False) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    if output is not None:
        output.close()
        os.unlink(output.name)

    return response


def pdf_team_sport_phase_lists_school(request):
    order_by_list = ['school', 'team_sport_main_list__team_sport', 'team_sport_main_list__gender', 'phase']
    title = 'Καταστάσεις Συμμετοχής Ομάδων ανά Σχολείο'
    template = 'pdfs/pdf_team_sport_phase_lists_school.html'

    return pdf_team_sport_phase_lists(request, order_by_list=order_by_list, title=title, template=template)


def pdf_team_sport_phase_lists_sport(request):
    order_by_list = ['team_sport_main_list__team_sport', 'team_sport_main_list__gender', 'phase', 'school']
    title = 'Καταστάσεις Συμμετοχής Ομάδων ανά Άθλημα'
    template = 'pdfs/pdf_team_sport_phase_lists_sport.html'

    return pdf_team_sport_phase_lists(request, order_by_list=order_by_list, title=title, template=template)


def pdf_individual_sport_lists(request, order_by_list, title, template):
    user = request.user
    trusted_users = TrustedUser.objects.filter(trusted_user=user, enabled=True)

    user_role = 'N/A'

    if trusted_users:
        user_role = trusted_users[0].user_role

    if user_role != 'ΔΔΕ':
        return redirect('main:home')

    school_year = AppState.objects.first().active_sch_year
    app_state_mode = AppState.objects.all().first().mode
    individual_sport_lists = IndividualSportList.objects.filter(mode=app_state_mode,
                                                                school_year=school_year,
                                                                locked=True).order_by(*order_by_list)

    data = individual_sport_lists

    # context passed in the template
    context = {'title': title, 'data': data}

    # render
    html_string = render_to_string(template, context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # http response
    response = HttpResponse(content_type='application/pdf;')
    filename = f'{slugify(title)}.pdf'
    response['Content-Disposition'] = f'inline; filename={filename}'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=False) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    if output is not None:
        output.close()
        os.unlink(output.name)

    return response


def pdf_individual_sport_lists_school(request):
    order_by_list = ['individual_sports_group_phase__phase', 'school', 'individual_sport']
    title = 'Αγωνίσματα ανά Σχολείο'
    template = 'pdfs/pdf_individual_sport_lists_school.html'

    return pdf_individual_sport_lists(request, order_by_list=order_by_list, title=title, template=template)


def pdf_individual_sport_lists_sport(request):
    order_by_list = ['individual_sports_group_phase__phase', 'individual_sport', 'school']
    title = 'Αγωνίσματα ανά Αγώνισμα'
    template = 'pdfs/pdf_individual_sport_lists_sport.html'

    return pdf_individual_sport_lists(request, order_by_list=order_by_list, title=title, template=template)


def pdf_individual_sports_group_phase(request, *args, **kwargs):
    individual_sports_group_phase = IndividualSportsGroupPhase.objects.get(id=kwargs.get('pk'))
    user = individual_sports_group_phase.school
    school = user
    trusted_users = TrustedUser.objects.filter(trusted_user=request.user, enabled=True)
    app_state_mode = AppState.objects.all().first().mode

    user_role = 'N/A'

    if trusted_users:
        user_role = trusted_users[0].user_role

    if not (request.user == user or user_role == 'ΔΔΕ'):
        return redirect('main:home')

    individual_sport_lists = individual_sports_group_phase.individual_sport_lists.all()

    data_boys = list()
    data_girls = list()
    for item in individual_sport_lists:
        data_boys += item.individual_sport_students.filter(gender='Αγόρι').order_by('last_name', 'first_name',
                                                                                    'father_name')
        data_girls += item.individual_sport_students.filter(gender='Κορίτσι').order_by('last_name', 'first_name',
                                                                                       'father_name')

    pt_teacher = individual_sports_group_phase.pt_teacher
    submit_date = str(individual_sports_group_phase.submit_date_time).split(" ")[0].split("-")
    submit_date_str = f'{submit_date[2]}-{submit_date[1]}-{submit_date[0]}'

    isgroup_dict = {
        'sport': f'{individual_sports_group_phase} - Φάση {individual_sports_group_phase.phase}',
        'data_boys': data_boys,
        'data_girls': data_girls,
        'school_year': individual_sports_group_phase.school_year,
        'pt_teacher': pt_teacher,
        'submit_date': submit_date_str
    }

    context = {
        'school': individual_sports_group_phase.school.last_name,
        'school_year': individual_sports_group_phase.school_year,
        'app_state_mode': app_state_mode,
        'isgroup_dicts_list': [isgroup_dict, ]
    }

    template = 'pdfs/pdf_individual_sport_lists_students.html'
    # render
    html_string = render_to_string(template, context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # http response
    response = HttpResponse(content_type='application/pdf;')
    filename = f'{school.last_name} - {individual_sports_group_phase} - {individual_sports_group_phase.school_year}'
    filename = f'{slugify(filename)}.pdf'
    response['Content-Disposition'] = f'inline; filename={filename}'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=False) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    if output is not None:
        output.close()
        os.unlink(output.name)

    return response


def pdf_individual_sports_group_phase_preview(request, *args, **kwargs):
    individual_sports_group_phase = IndividualSportsGroupPhase.objects.get(id=kwargs.get('pk'))
    user = individual_sports_group_phase.school
    school = user
    trusted_users = TrustedUser.objects.filter(trusted_user=request.user, enabled=True)
    app_state_mode = AppState.objects.all().first().mode

    user_role = 'N/A'

    if trusted_users:
        user_role = trusted_users[0].user_role

    if not (request.user == user or user_role == 'ΔΔΕ'):
        return redirect('main:home')

    individual_sport_lists = individual_sports_group_phase.individual_sport_lists.all()

    data_boys = list()
    data_girls = list()
    for item in individual_sport_lists:
        data_boys += item.individual_sport_students.filter(gender='Αγόρι').order_by('last_name', 'first_name',
                                                                                    'father_name')
        data_girls += item.individual_sport_students.filter(gender='Κορίτσι').order_by('last_name', 'first_name',
                                                                                       'father_name')

    pt_teacher = individual_sports_group_phase.pt_teacher

    isgroup_dict = {
        'sport': f'{individual_sports_group_phase} - Φάση {individual_sports_group_phase.phase}',
        'data_boys': data_boys,
        'data_girls': data_girls,
        'school_year': individual_sports_group_phase.school_year,
        'pt_teacher': pt_teacher,
    }

    context = {
        'school': individual_sports_group_phase.school.last_name,
        'school_year': individual_sports_group_phase.school_year,
        'app_state_mode': app_state_mode,
        'isgroup_dicts_list': [isgroup_dict, ],
        'preview': 'True'
    }

    template = 'pdfs/pdf_individual_sport_lists_students.html'
    # render
    html_string = render_to_string(template, context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # http response
    response = HttpResponse(content_type='application/pdf;')
    filename = f'{school.last_name} - {individual_sports_group_phase} - {individual_sports_group_phase.school_year}'
    filename = f'{slugify(filename)}.pdf'
    response['Content-Disposition'] = f'inline; filename={filename}'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=False) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    if output is not None:
        output.close()
        os.unlink(output.name)

    return response


def pdf_individual_sports_groups_phases(request, *args, **kwargs):
    user = request.user
    trusted_users = TrustedUser.objects.filter(trusted_user=user, enabled=True)

    user_role = 'N/A'

    if trusted_users:
        user_role = trusted_users[0].user_role

    if user_role != 'ΔΔΕ':
        return redirect('main:home')

    school_year = AppState.objects.first().active_sch_year
    app_state_mode = AppState.objects.all().first().mode
    individual_sports_groups_phases = IndividualSportsGroupPhase.objects.filter(mode=app_state_mode,
                                                                                school_year=school_year,
                                                                                locked=True).order_by('phase', 'school',
                                                                                                      'individual_sports_group')

    for individual_sports_group_phase in individual_sports_groups_phases:
        individual_sports_lists = individual_sports_group_phase.individual_sport_lists.all()

        students_count = 0
        for individual_sports_list in individual_sports_lists:
            students_count += individual_sports_list.individual_sport_students.all().count()

        individual_sports_group_phase.students_count = students_count
        individual_sports_group_phase.save()

    data = individual_sports_groups_phases
    title = f'Καταστάσεις Συμμετοχής Ατομικών Αθλημάτων - {school_year}'

    # context passed in the template
    context = {'title': title, 'data': data}

    template = 'pdfs/pdf_individual_sports_groups_phases.html'
    # render
    html_string = render_to_string(template, context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # http response
    response = HttpResponse(content_type='application/pdf;')
    filename = f'{slugify(title)}.pdf'
    response['Content-Disposition'] = f'inline; filename={filename}'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=False) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    if output is not None:
        output.close()
        os.unlink(output.name)

    return response
