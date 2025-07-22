from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import (
    AppState,
    TrustedUser,
    TeamSport,
    TeamSportLimits,
    IndividualSportsGroup,
    IndividualSport
)
from main.common import (
    BASKETBALL_STR,
    VOLLEYBALL_STR,
    FOOTBALL_STR,
    HANDBALL_STR,
    ISG_TRACK_STR,
    ISG_SWIMMING_STR,
    ISG_TENNIS_STR
)
import os

MODE_1_MIN_STUDENTS_MAIN_LIST_BASKETBALL = 5
MODE_1_MIN_STUDENTS_MAIN_LIST_VOLLEYBALL = 6
MODE_1_MIN_STUDENTS_MAIN_LIST_HANDBALL = 7
MODE_1_MIN_STUDENTS_MAIN_LIST_FOOTBALL = 11

MODE_2_MIN_STUDENTS_MAIN_LIST_BASKETBALL = 3
MODE_2_MIN_STUDENTS_MAIN_LIST_VOLLEYBALL = 4
MODE_2_MIN_STUDENTS_MAIN_LIST_FOOTBALL = 5

# TODO: to change value
MODE_2_MIN_STUDENTS_MAIN_LIST_HANDBALL = 7

MIN_STUDENTS_PHASE_LIST_BASKETBALL = 5
MIN_STUDENTS_PHASE_LIST_VOLLEYBALL = 6
MIN_STUDENTS_PHASE_LIST_HANDBALL = 7
MIN_STUDENTS_PHASE_LIST_FOOTBALL = 11

MAX_STUDENTS_MAIN_LIST_BASKETBALL = 18
MAX_STUDENTS_MAIN_LIST_VOLLEYBALL = 20
MAX_STUDENTS_MAIN_LIST_HANDBALL = 22
MAX_STUDENTS_MAIN_LIST_FOOTBALL = 24

MAX_STUDENTS_PHASE_LIST_BASKETBALL = 12
MAX_STUDENTS_PHASE_LIST_VOLLEYBALL = 14
MAX_STUDENTS_PHASE_LIST_HANDBALL = 16
MAX_STUDENTS_PHASE_LIST_FOOTBALL = 18

USER_PASSWORD = os.getenv('USER_PASSWORD', '1234')


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin'):
            User.objects.create_superuser(username='admin', password=USER_PASSWORD)

        if not TrustedUser.objects.filter(trusted_user='admin'):
            TrustedUser.objects.create(trusted_user='admin', name='admin', user_role='ΔΔΕ', school_type='ΔΔΕ',
                                       enabled=True)

        trusted_users = [
            ['1727010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ Ν. ΑΛΙΚΑΡΝΑΣΣΟΥ', 'mail@gym-n-alikarn.ira.sch.gr', 'ΣΦΥΡΑΚΗΣ ΜΙΧΑΗΛ'],
            ['1751042', 'ΛΥΚΕΙΟ', '6ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@6lyk-irakl.ira.sch.gr', 'ΣΤΑΜΑΤΑΚΗ ΕΡΩΦΙΛΗ'],
            ['1725030', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΠΥΡΓΟΥ', 'mail@gym-pyrgou.ira.sch.gr', 'ΚΡΟΥΣΤΑΛΑΚΗΣ ΓΕΩΡΓΙΟΣ'],
            ['1701041', 'ΓΥΜΝΑΣΙΟ', '5ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@5gym-irakl.ira.sch.gr', 'ΠΕΔΙΑΔΙΤΟΥ ΧΑΡΙΚΛΕΙΑ'],
            ['1777010', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ Ν. ΑΛΙΚΑΡΝΑΣΣΟΥ', 'mail@lyk-n-alikarn.ira.sch.gr',
             'ΜΗΛΑΚΗΣ ΕΜΜΑΝΟΥΗΛ'],
            ['1701030', 'ΓΥΜΝΑΣΙΟ', '3ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@3gym-irakl.ira.sch.gr', 'ΠΕΡΙΣΤΕΡΗ ΜΕΛΠΟΜΕΝΗ'],
            ['1714010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΖΑΡΟΥ', 'mail@gym-zarou.ira.sch.gr', 'ΔΕΝΔΡΑΛΙΔΗΣ ΕΜΜΑΝΟΥΗΛ'],
            ['1751020', 'ΛΥΚΕΙΟ', '2ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@2lyk-irakl.ira.sch.gr',
             'ΚΩΝΣΤΑΝΤΙΝΟΥ ΚΩΝΣΤΑΝΤΙΝΟΣ'],
            ['1741002', 'ΓΥΜΝΑΣΙΟ', 'ΚΑΛΛΙΤΕΧΝΙΚΟ ΓΥΜΝΑΣΙΟ', 'mail@gym-kallitech.ira.sch.gr', 'ΚΑΛΟΥΔΙΩΤΗ ΜΑΡΙΑ'],
            ['1720010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΒΑΓΙΟΝΙΑΣ', 'mail@gym-vagion.ira.sch.gr', 'ΡΟΥΣΣΑΚΗΣ ΕΜΜΑΝΟΥΗΛ'],
            ['1764010', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΓΟΥΒΩΝ', 'mail@lyk-gouvon.ira.sch.gr', 'ΦΟΥΚΑΔΑΚΗΣ ΓΕΩΡΓΙΟΣ'],
            ['1751030', 'ΛΥΚΕΙΟ', '3ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@3lyk-irakl.ira.sch.gr', 'ΑΛΕΞΑΚΗΣ ΕΜΜΑΝΟΥΗΛ'],
            ['1701050', 'ΓΥΜΝΑΣΙΟ', '6ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@6gym-irakl.ira.sch.gr', 'ΠΕΡΒΟΛΑΡΑΚΗ ΑΙΚΑΤΕΡΙΝΗ'],
            ['1790210', 'ΛΥΚΕΙΟ', '13ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@13lyk-irakl.ira.sch.gr', 'ΜΙΚΡΑΚΗ ΑΙΚΑΤΕΡΙΝΗ'],
            ['1752010', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΡΚΑΛΟΧΩΡΙΟΥ', 'mail@lyk-arkal.ira.sch.gr', 'ΜΑΝΤΑΡΑΣ ΑΘΑΝΑΣΙΟΣ'],
            ['1790200', 'ΛΥΚΕΙΟ', 'ΕΣΠΕΡΙΝΟ ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@lyk-esp-irakl.ira.sch.gr',
             'ΜΠΕΖΙΡΤΖΟΓΛΟΥ ΕΛΕΝΗ'],
            ['1751001', 'ΛΥΚΕΙΟ', 'ΠΡΟΤΥΠΟ ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@lyk-peir-irakl.ira.sch.gr',
             'ΠΑΤΡΑΜΑΝΗ ΜΑΡΙΑ'],
            ['1751010', 'ΛΥΚΕΙΟ', '1ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@1lyk-irakl.ira.sch.gr', 'ΧΑΤΖΑΚΗ ΑΙΚΑΤΕΡΙΝΗ'],
            ['1760010', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΚΡΟΥΣΩΝΑ', 'mail@lyk-krous.ira.sch.gr', 'ΖΑΧΑΡΙΟΥΔΑΚΗΣ ΑΝΤΩΝΙΟΣ'],
            ['1701053', 'ΓΥΜΝΑΣΙΟ', '9ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@9gym-irakl.ira.sch.gr', 'ΚΟΥΡΤΗ ΜΑΡΙΑ'],
            ['1751070', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΕΠΙΣΚΟΠΗΣ', 'mail@lyk-episk.ira.sch.gr', 'ΜΑΓΚΑΦΟΥΡΑΚΗΣ ΔΗΜΗΤΡΙΟΣ'],
            ['1701060', 'ΓΥΜΝΑΣΙΟ', 'ΕΣΠΕΡΙΝΟ ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@gym-esp-irakl.ira.sch.gr',
             'ΑΠΟΣΤΟΛΑΚΗ ΕΥΑΓΓΕΛΙΑ'],
            ['1706010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΜΟΙΡΩΝ', 'mail@gym-moiron.ira.sch.gr', 'ΕΠΤΑΜΗΝΙΤΑΚΗΣ ΓΕΩΡΓΙΟΣ'],
            ['1726010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΤΥΛΙΣΟΥ', 'mail@gym-tylis.ira.sch.gr', 'ΒΑΣΙΛΑΚΗ ΜΑΡΙΑ'],
            ['1701054', 'ΓΥΜΝΑΣΙΟ', '10ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@10gym-irakl.ira.sch.gr', 'ΦΟΥΣΤΑΝΑΚΗΣ ΓΕΩΡΓΙΟΣ'],
            ['1717011', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ Λ. ΧΕΡΣΟΝΗΣΟΥ', 'mail@gym-chers.ira.sch.gr', 'ΚΟΙΛΑΔΗ ΑΙΚΑΤΕΡΙΝΗ'],
            ['1701010', 'ΓΥΜΝΑΣΙΟ', '1ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@1gym-irakl.ira.sch.gr', 'ΣΜΑΡΔΑΣ ΑΝΤΩΝΙΟΣ'],
            ['1714012', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΓΟΥΒΩΝ', 'mail@gym-gouvon.ira.sch.gr', 'ΒΟΥΛΚΟΣ ΣΤΑΥΡΟΣ'],
            ['1756010', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΜΟΙΡΩΝ', 'mail@1lyk-moiron.ira.sch.gr', 'ΧΟΥΣΤΟΥΛΑΚΗΣ ΕΥΑΓΓΕΛΟΣ'],
            ['1701051', 'ΓΥΜΝΑΣΙΟ', '7ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@7gym-irakl.ira.sch.gr', 'ΤΟΥΤΟΥΔΑΚΗΣ ΝΙΚΟΛΑΟΣ'],
            ['1757010', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΠΟΜΠΙΑΣ', 'mail@lyk-pompias.ira.sch.gr', 'ΤΟΥΜΑΝΙΔΗΣ ΝΙΚΟΛΑΟΣ'],
            ['1759010', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΓΙΑΣ ΒΑΡΒΑΡΑΣ', 'mail@lyk-ag-varvar.ira.sch.gr',
             'ΚΟΥΤΕΝΤΑΚΗ ΧΑΡΟΥΛΑ'],
            ['1740070', 'ΛΥΚΕΙΟ', '1ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ', 'mail@1epal-irakl.ira.sch.gr', 'ΤΑΚΑ ΜΑΡΙΑ'],
            ['1701015', 'ΓΥΜΝΑΣΙΟ', 'ΜΟΥΣΙΚΟ ΣΧΟΛΕΙΟ - ΓΥΜΝΑΣΙΟ', 'mail@gym-mous-irakl.ira.sch.gr',
             'ΒΑΡΒΕΡΑΚΗΣ ΚΩΝΣΤΑΝΤΙΝΟΣ'],
            ['1778010', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΓΑΖΙΟΥ', 'mail@lyk-gaziou.ira.sch.gr', 'ΚΩΣΤΑΚΗΣ ΙΩΑΝΝΗΣ'],
            ['1716010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΒΕΝΕΡΑΤΟΥ', 'mail@gym-vener.ira.sch.gr', 'ΔΕΛΛΑΤΟΛΑΣ ΣΤΥΛΙΑΝΟΣ'],
            ['1751052', 'ΛΥΚΕΙΟ', '8ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@8lyk-irakl.ira.sch.gr', 'ΠΑΠΑΔΑΚΗΣ ΙΩΑΝΝΗΣ'],
            ['1701055', 'ΓΥΜΝΑΣΙΟ', '11ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@11gym-irakl.ira.sch.gr', 'ΚΟΚΟΤΣΑΚΗ ΑΝΤΩΝΙΑ'],
            ['1701080', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΑΓΙΟΥ ΜΥΡΩΝΑ', 'mail@gym-ag-myron.ira.sch.gr', 'ΛΕΛΕΚΑ ΔΕΣΠΟΙΝΑ'],
            ['1725010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΤΕΦΕΛΙΟΥ', 'mail@gym-tefel.ira.sch.gr', 'ΜΑΡΚΟΔΗΜΗΤΡΑΚΗ ΠΑΡΑΣΚΕΥΗ'],
            ['1712010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΜΟΧΟΥ', 'mail@gym-mochou.ira.sch.gr', 'ΦΡΟΥΔΑΡΑΚΗ ΑΙΚΑΤΕΡΙΝΗ'],
            ['1740310', 'ΛΥΚΕΙΟ', '1ο ΕΠΑ.Λ. ΑΡΚΑΛΟΧΩΡΙΟΥ', 'mail@1epal-arkal.ira.sch.gr', 'ΚΑΓΙΑΜΠΑΚΗΣ ΕΜΜΑΝΟΥΗΛ'],
            ['1740200', 'ΛΥΚΕΙΟ', '4ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ (ΕΣΠΕΡΙΝΟ)', 'mail@4epal-esp-irakl.ira.sch.gr',
             'ΑΝΑΓΝΩΣΤΑΚΗΣ ΜΑΡΚΟΣ'],
            ['1751051', 'ΛΥΚΕΙΟ', '7ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@7lyk-irakl.ira.sch.gr', 'ΣΑΚΕΛΛΑΡΗΣ ΔΗΜΗΤΡΙΟΣ'],
            ['1753010', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΡΧΑΝΩΝ', 'mail@lyk-archan.ira.sch.gr', 'ΔΡΑΚΩΝΑΚΗ ΜΑΡΙΑ'],
            ['1768010', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΜΑΛΙΩΝ', 'mail@lyk-malion.ira.sch.gr', 'ΚΡΑΣΑΝΑΚΗΣ ΙΩΑΝΝΗΣ'],
            ['1701040', 'ΓΥΜΝΑΣΙΟ', '4ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@4gym-irakl.ira.sch.gr', 'ΓΙΑΧΝΑΚΗΣ ΑΔΑΜ'],
            ['1708010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΧΑΡΑΚΑ', 'mail@gym-charak.ira.sch.gr', 'ΦΡΑΓΚΟΥΛΙΔΑΚΗΣ ΕΥΑΓΓΕΛΟΣ'],
            ['1721010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΑΓΙΩΝ ΔΕΚΑ', 'mail@gym-ag-deka.ira.sch.gr', 'ΜΕΣΣΑΡΙΤΑΚΗ ΑΝΝΑ'],
            ['1754010', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΒΙΑΝΝΟΥ', 'mail@lyk-viann.ira.sch.gr', 'ΣΟΥΚΟΥΛΗ ΓΕΩΡΓΙΑ'],
            ['1701057', 'ΓΥΜΝΑΣΙΟ', '13ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@13gym-irakl.ira.sch.gr', 'ΚΛΕΙΝΑΚΗ ΑΝΝΑ'],
            ['1701002', 'ΓΥΜΝΑΣΙΟ', 'ΕΙΔΙΚΟ ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@gym-eid-irakl.ira.sch.gr', 'ΜΑΝΙΚΑΣ ΣΩΤΗΡΙΟΣ'],
            ['1740080', 'ΛΥΚΕΙΟ', '3ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ', 'mail@3epal-irakl.ira.sch.gr', 'ΣΤΟΓΙΑΝΝΟΠΟΥΛΟΣ ΔΙΟΝΥΣΙΟΣ'],
            ['1701056', 'ΓΥΜΝΑΣΙΟ', '12ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@12gym-irakl.ira.sch.gr', 'ΠΑΥΛΙΔΗΣ ΓΕΩΡΓΙΟΣ'],
            ['1740100', 'ΛΥΚΕΙΟ', '2ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ', 'mail@2epal-irakl.ira.sch.gr', 'ΤΣΑΓΚΑΡΑΚΗ ΕΥΑΓΓΕΛΙΑ'],
            ['1790100', 'ΛΥΚΕΙΟ', '11ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@11lyk-irakl.ira.sch.gr', 'ΣΗΦΑΚΗΣ ΕΥΑΓΓΕΛΟΣ'],
            ['1703010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΑΡΧΑΝΩΝ', 'mail@gym-archan.ira.sch.gr', 'ΜΠΡΟΥΧΟΥΤΑ ΑΡΓΥΡΩ'],
            ['1751041', 'ΛΥΚΕΙΟ', '5ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@5lyk-irakl.ira.sch.gr', 'ΠΑΠΑΔΑΚΗΣ ΣΤΑΜΑΤΙΟΣ'],
            ['1751040', 'ΛΥΚΕΙΟ', '4ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@4lyk-irakl.ira.sch.gr', 'ΚΑΤΣΙΔΗΣ ΧΑΡΑΛΑΜΠΟΣ'],
            ['1702010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΑΡΚΑΛΟΧΩΡΙΟΥ', 'mail@gym-arkal.ira.sch.gr', 'ΣΤΕΙΑΚΑΚΗΣ ΚΩΝΣΤΑΝΤΙΝΟΣ'],
            ['1701001', 'ΓΥΜΝΑΣΙΟ', 'ΠΡΟΤΥΠΟ ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@gym-peir-irakl.ira.sch.gr',
             'ΠΟΛΥΧΡΟΝΑΚΗ ΜΑΡΙΑ'],
            ['1740210', 'ΛΥΚΕΙΟ', '5ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ', 'mail@5epal-irakl.ira.sch.gr', 'ΠΑΠΑΔΟΓΙΩΡΓΑΚΗΣ ΚΩΝΣΤΑΝΤΙΝΟΣ'],
            ['1765010', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΣΗΜΙΟΥ', 'mail@lyk-asim.ira.sch.gr', 'ΣΑΠΙΟΣ ΠΑΝΑΓΙΩΤΗΣ'],
            ['1750080', 'ΛΥΚΕΙΟ', '6ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ', 'mail@6epal-irakl.ira.sch.gr', 'ΛΙΒΑ ΑΝΝΑ'],
            ['1761010', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΜΕΛΕΣΩΝ', 'mail@lyk-meles.ira.sch.gr', 'ΤΖΟΥΡΜΠΑΚΗΣ ΣΤΑΥΡΟΣ'],
            ['1707010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΠΟΜΠΙΑΣ', 'mail@gym-pompias.ira.sch.gr', 'ΠΑΤΣΙΑΝΩΤΑΚΗ ΙΩΑΝΝΑ'],
            ['1740300', 'ΛΥΚΕΙΟ', '1ο ΕΠΑ.Λ. ΜΟΙΡΩΝ', 'mail@1epal-moiron.ira.sch.gr', 'ΚΑΔΙΑΝΑΚΗΣ ΛΑΜΠΡΟΣ'],
            ['1710010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΚΡΟΥΣΩΝΑ', 'mail@gym-krous.ira.sch.gr', 'ΜΑΣΤΡΟΓΙΩΡΓΑΚΗΣ ΧΑΡΑΛΑΜΠΟΣ'],
            ['1728010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΓΑΖΙΟΥ', 'mail@gym-gaziou.ira.sch.gr', 'ΜΑΚΡΟΓΙΑΝΝΑΚΗΣ ΕΜΜΑΝΟΥΗΛ'],
            ['1701070', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΕΠΙΣΚΟΠΗΣ', 'mail@gym-episk.ira.sch.gr', 'ΒΑΒΟΥΡΑΝΑΚΗ ΒΙΛΜΑ'],
            ['1718010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΜΑΛΙΩΝ', 'mail@gym-malion.ira.sch.gr', 'ΧΟΥΡΔΑΚΗΣ ΔΗΜΗΤΡΙΟΣ'],
            ['1715010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΑΣΗΜΙΟΥ', 'mail@gym-asimiou.ira.sch.gr', 'ΜΑΡΟΥΛΑΚΗ ΠΕΛΑΓΙΑ'],
            ['1705010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΚΑΣΤΕΛΛΙΟΥ', 'mail@gym-kastell.ira.sch.gr', 'ΣΟΥΝΔΟΥΛΟΥΝΑΚΗΣ ΝΙΚΟΛΑΟΣ'],
            ['1711010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΜΕΛΕΣΩΝ', 'mail@gym-meles.ira.sch.gr', 'ΠΑΠΑΖΗ ΧΑΙΔΗ'],
            ['1701052', 'ΓΥΜΝΑΣΙΟ', '8ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@8gym-irakl.ira.sch.gr', 'ΣΦΑΚΙΑΝΑΚΗΣ ΓΕΩΡΓΙΟΣ'],
            ['1713015', 'ΓΥΜΝΑΣΙΟ', 'ΕΣΠΕΡΙΝΟ ΓΥΜΝΑΣΙΟ ΤΥΜΠΑΚΙΟΥ', 'mail@gym-esp-tympak.ira.sch.gr',
             'ΣΟΥΛΑΔΑΚΗΣ ΜΑΡΙΝΟΣ'],
            ['1701020', 'ΓΥΜΝΑΣΙΟ', '2ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@2gym-irakl.ira.sch.gr', 'ΧΟΥΡΣΑΝΙΔΗΣ ΕΜΜΑΝΟΥΗΛ'],
            ['1790070', 'ΛΥΚΕΙΟ', '10ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', 'mail@10lyk-irakl.ira.sch.gr', 'ΜΑΝΟΥΣΕΛΗΣ ΕΥΑΓΓΕΛΟΣ'],
            ['1755010', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΚΑΣΤΕΛΛΙΟΥ', 'mail@lyk-kastell.ira.sch.gr',
             'ΘΕΟΔΩΡΟΜΑΝΩΛΑΚΗΣ ΕΜΜΑΝΟΥΗΛ'],
            ['1704010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΒΙΑΝΝΟΥ', 'mail@gym-viannou.ira.sch.gr', 'ΚΥΡΙΑΚΟΥ ΓΕΩΡΓΙΑ'],
            ['1722010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΓΕΡΓΕΡΗΣ', 'mail@gym-gerger.ira.sch.gr', 'ΝΙΘΑΥΡΙΑΝΑΚΗΣ ΚΩΝΣΤΑΝΤΙΝΟΣ'],
            ['1751080', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΓΙΟΥ ΜΥΡΩΝΑ', 'mail@lyk-ag-myron.ira.sch.gr', 'ΜΑΡΚΟΥ ΛΑΖΑΡΟΣ'],
            ['1762010', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΜΟΧΟΥ', 'mail@lyk-mochou.ira.sch.gr', 'ΚΡΗΤΣΩΤΑΚΗ ΦΩΤΕΙΝΗ'],
            ['1713010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΤΥΜΠΑΚΙΟΥ', 'mail@gym-tympak.ira.sch.gr', 'ΚΑΜΠΑΝΑΡΑΚΗΣ ΑΛΕΞΑΝΔΡΟΣ'],
            ['1763010', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΤΥΜΠΑΚΙΟΥ', 'mail@lyk-tympak.ira.sch.gr', 'ΛΕΝΑΚΑΚΗ ΝΙΚΗ'],
            ['1771010', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΓΙΩΝ ΔΕΚΑ', 'mail@lyk-ag-deka.ira.sch.gr', 'ΒΛΑΧΑΚΗΣ ΜΙΧΑΗΛ'],
            ['1709010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΑΓΙΑΣ ΒΑΡΒΑΡΑΣ', 'mail@gym-ag-varvar.ira.sch.gr', 'ΠΑΠΑΔΑΚΗ ΕΙΡΗΝΗ'],
            ['1758010', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΧΑΡΑΚΑ', 'mail@lyk-charak.ira.sch.gr', 'ΓΕΡΓΕΡΙΤΑΚΗΣ ΕΜΜΑΝΟΥΗΛ'],
            ['1767011', 'ΛΥΚΕΙΟ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ Λ. ΧΕΡΣΟΝΗΣΟΥ', 'mail@lyk-limen.ira.sch.gr', 'ΜΠΑΤΣΟΣ ΧΡΙΣΤΟΦΟΡΟΣ'],
            ['1701090', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΠΡΟΦΗΤΗ ΗΛΙΑ', 'mail@gym-prof-ilia.ira.sch.gr', 'ΠΑΞΙΜΑΔΑΚΗΣ ΕΜΜΑΝΟΥΗΛ'],
            ['1740060', 'ΓΥΜΝΑΣΙΟ', 'ΕΠΑΛ ΕΙΔΙΚΗΣ ΑΓΩΓΗΣ', 'mail@epal-eid-agogis-irak.ira.sch.gr', 'ΣΑΚΕΛΛΑΡΗ ΕΛΕΝΗ'],
            ['1724010', 'ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ ΘΡΑΨΑΝΟΥ', 'mail@gym-thraps.ira.sch.gr', 'ΑΛΕΞΑΚΗ ΣΟΦΙΑ']
        ]

        for tu in trusted_users:
            if not User.objects.filter(username=tu[0]):
                User.objects.create_user(username=tu[0], password=USER_PASSWORD, email=tu[3], last_name=tu[2])

            if not TrustedUser.objects.filter(trusted_user=tu[0]):
                if tu[1] == 'ΛΥΚΕΙΟ':
                    TrustedUser.objects.create(trusted_user=tu[0], name=tu[2], user_role='ΣΧΟΛΕΙΟ',
                                               school_type=tu[1], enabled=True)
                else:
                    TrustedUser.objects.create(trusted_user=tu[0], name=tu[2], user_role='ΣΧΟΛΕΙΟ',
                                               school_type=tu[1], enabled=False)

        if not AppState.objects.all():
            AppState.objects.create(mode='Σχολικά Πρωταθλήματα')

        mode_1_team_sports = ['Καλαθοσφαίριση', 'Πετοσφαίριση', 'Χειροσφαίριση', 'Ποδόσφαιρο']

        for team_sport in mode_1_team_sports:
            ts = TeamSport.objects.filter(mode='Σχολικά Πρωταθλήματα', team_sport=team_sport).first()
            if not ts:
                ts = TeamSport.objects.create(mode='Σχολικά Πρωταθλήματα', team_sport=team_sport, enabled=True)

            tsl = TeamSportLimits.objects.filter(team_sport=ts)
            if not tsl:
                if str(ts.team_sport) == BASKETBALL_STR:
                    min_students_main_list = MODE_1_MIN_STUDENTS_MAIN_LIST_BASKETBALL
                    max_students_main_list = MAX_STUDENTS_MAIN_LIST_BASKETBALL
                    min_students_phase_list = MIN_STUDENTS_PHASE_LIST_BASKETBALL
                    max_students_phase_list = MAX_STUDENTS_PHASE_LIST_BASKETBALL
                elif str(ts.team_sport) == VOLLEYBALL_STR:
                    min_students_main_list = MODE_1_MIN_STUDENTS_MAIN_LIST_VOLLEYBALL
                    max_students_main_list = MAX_STUDENTS_MAIN_LIST_VOLLEYBALL
                    min_students_phase_list = MIN_STUDENTS_PHASE_LIST_VOLLEYBALL
                    max_students_phase_list = MAX_STUDENTS_PHASE_LIST_VOLLEYBALL
                elif str(ts.team_sport) == HANDBALL_STR:
                    min_students_main_list = MODE_1_MIN_STUDENTS_MAIN_LIST_HANDBALL
                    max_students_main_list = MAX_STUDENTS_MAIN_LIST_HANDBALL
                    min_students_phase_list = MIN_STUDENTS_PHASE_LIST_HANDBALL
                    max_students_phase_list = MAX_STUDENTS_PHASE_LIST_HANDBALL
                elif str(ts.team_sport) == FOOTBALL_STR:
                    min_students_main_list = MODE_1_MIN_STUDENTS_MAIN_LIST_FOOTBALL
                    max_students_main_list = MAX_STUDENTS_MAIN_LIST_FOOTBALL
                    min_students_phase_list = MIN_STUDENTS_PHASE_LIST_FOOTBALL
                    max_students_phase_list = MAX_STUDENTS_PHASE_LIST_FOOTBALL

                TeamSportLimits.objects.create(mode='Σχολικά Πρωταθλήματα',
                                               team_sport=ts,
                                               min_students_main_list=min_students_main_list,
                                               max_students_main_list=max_students_main_list,
                                               min_students_phase_list=min_students_phase_list,
                                               max_students_phase_list=max_students_phase_list)

        mode_2_team_sports = ['Καλαθοσφαίριση', 'Πετοσφαίριση', 'Χειροσφαίριση', 'Ποδόσφαιρο']

        for team_sport in mode_2_team_sports:
            ts = TeamSport.objects.filter(mode='Αγώνες ΑθλοΠΑΙΔΕΙΑΣ', team_sport=team_sport).first()
            if not ts:
                ts = TeamSport.objects.create(mode='Αγώνες ΑθλοΠΑΙΔΕΙΑΣ', team_sport=team_sport, enabled=True)

            tsl = TeamSportLimits.objects.filter(team_sport=ts)
            if not tsl:
                if str(ts.team_sport) == BASKETBALL_STR:
                    min_students_main_list = MODE_2_MIN_STUDENTS_MAIN_LIST_BASKETBALL
                    max_students_main_list = 100
                    min_students_phase_list = MODE_2_MIN_STUDENTS_MAIN_LIST_BASKETBALL
                    max_students_phase_list = 100
                elif str(ts.team_sport) == VOLLEYBALL_STR:
                    min_students_main_list = MODE_2_MIN_STUDENTS_MAIN_LIST_VOLLEYBALL
                    max_students_main_list = 100
                    min_students_phase_list = MODE_2_MIN_STUDENTS_MAIN_LIST_VOLLEYBALL
                    max_students_phase_list = 100
                elif str(ts.team_sport) == HANDBALL_STR:
                    min_students_main_list = MODE_2_MIN_STUDENTS_MAIN_LIST_HANDBALL
                    max_students_main_list = 100
                    min_students_phase_list = MODE_2_MIN_STUDENTS_MAIN_LIST_HANDBALL
                    max_students_phase_list = 100
                elif str(ts.team_sport) == FOOTBALL_STR:
                    min_students_main_list = MODE_2_MIN_STUDENTS_MAIN_LIST_FOOTBALL
                    max_students_main_list = 100
                    min_students_phase_list = MODE_2_MIN_STUDENTS_MAIN_LIST_FOOTBALL
                    max_students_phase_list = 100

                TeamSportLimits.objects.create(mode='Αγώνες ΑθλοΠΑΙΔΕΙΑΣ',
                                               team_sport=ts,
                                               min_students_main_list=min_students_main_list,
                                               max_students_main_list=max_students_main_list,
                                               min_students_phase_list=min_students_phase_list,
                                               max_students_phase_list=max_students_phase_list)

        mode_1_track_individual_sports_a = ['Στίβος - 100μ',
                                            'Στίβος - 200μ',
                                            'Στίβος - 400μ',
                                            'Στίβος - 800μ',
                                            'Στίβος - 1500μ',
                                            'Στίβος - 3000μ',
                                            'Στίβος - 100μ εμπόδια',
                                            'Στίβος - 110μ εμπόδια',
                                            'Στίβος - 400μ εμπόδια',
                                            'Στίβος - 2000μ φυσ. εμπόδια',
                                            'Στίβος - 5000μ βάδην',
                                            'Στίβος - 10.000μ βάδην']

        mode_1_track_individual_sports_b = ['Στίβος - Μήκος',
                                            'Στίβος - Τριπλούν',
                                            'Στίβος - Σφαίρα',
                                            'Στίβος - Δίσκος',
                                            'Στίβος - Σφύρα',
                                            'Στίβος - Ακόντιο']
        mode_1_track_individual_sports_c = ['Στίβος - Ύψος',
                                            'Στίβος - Επί κοντώ']
        mode_1_track_individual_sports_x = ['Στίβος - Έπταθλο',
                                            'Στίβος - Δέκαθλο']

        track = IndividualSportsGroup.objects.filter(mode='Σχολικά Πρωταθλήματα',
                                                     individual_sports_group=ISG_TRACK_STR).first()

        if not track:
            track = IndividualSportsGroup.objects.create(mode='Σχολικά Πρωταθλήματα',
                                                         individual_sports_group=ISG_TRACK_STR,
                                                         enabled=True)

        for individual_sport in mode_1_track_individual_sports_a:
            if not IndividualSport.objects.filter(mode='Σχολικά Πρωταθλήματα', individual_sport=individual_sport):
                IndividualSport.objects.create(mode='Σχολικά Πρωταθλήματα',
                                               individual_sport=individual_sport,
                                               individual_sports_group=track,
                                               export_code='a',
                                               enabled=True)

        for individual_sport in mode_1_track_individual_sports_b:
            if not IndividualSport.objects.filter(mode='Σχολικά Πρωταθλήματα', individual_sport=individual_sport):
                IndividualSport.objects.create(mode='Σχολικά Πρωταθλήματα',
                                               individual_sport=individual_sport,
                                               individual_sports_group=track,
                                               export_code='b',
                                               enabled=True)

        for individual_sport in mode_1_track_individual_sports_c:
            if not IndividualSport.objects.filter(mode='Σχολικά Πρωταθλήματα', individual_sport=individual_sport):
                IndividualSport.objects.create(mode='Σχολικά Πρωταθλήματα',
                                               individual_sport=individual_sport,
                                               individual_sports_group=track,
                                               export_code='c',
                                               enabled=True)

        for i, individual_sport in enumerate(mode_1_track_individual_sports_x):
            if not IndividualSport.objects.filter(mode='Σχολικά Πρωταθλήματα', individual_sport=individual_sport):
                IndividualSport.objects.create(mode='Σχολικά Πρωταθλήματα',
                                               individual_sport=individual_sport,
                                               individual_sports_group=track,
                                               export_code=f'x{i + 1}',
                                               enabled=True)

        mode_2_track_individual_sports_a = ['Στίβος - 80μ',
                                            'Στίβος - 150μ',
                                            'Στίβος - 300μ',
                                            'Στίβος - 80μ εμπόδια (Μόνο Κορίτσια)',
                                            'Στίβος - 100μ εμπόδια (Μόνο Αγόρια)',
                                            'Στίβος - 200μ εμπόδια',
                                            'Στίβος - Δρόμος 600μ (Μόνο Κορίτσια)',
                                            'Στίβος - Δρόμος 1000μ (Μόνο Αγόρια)']

        mode_2_track_individual_sports_b = ['Στίβος - Μήκος',
                                            'Στίβος - ΤΕΤΡΑΠΛΟΥΝ',
                                            'Στίβος - Σφαίρα',
                                            'Στίβος - Σφύρα',
                                            'Στίβος - Δίσκος',
                                            'Στίβος - Ακόντιο']

        mode_2_track_individual_sports_c = ['Στίβος - Ύψος',
                                            'Στίβος - Επί κοντώ']

        track = IndividualSportsGroup.objects.filter(mode='Αγώνες ΑθλοΠΑΙΔΕΙΑΣ',
                                                     individual_sports_group=ISG_TRACK_STR).first()

        if not track:
            track = IndividualSportsGroup.objects.create(mode='Αγώνες ΑθλοΠΑΙΔΕΙΑΣ',
                                                         individual_sports_group=ISG_TRACK_STR,
                                                         enabled=True)

        for individual_sport in mode_2_track_individual_sports_a:
            if not IndividualSport.objects.filter(mode='Αγώνες ΑθλοΠΑΙΔΕΙΑΣ', individual_sport=individual_sport):
                IndividualSport.objects.create(mode='Αγώνες ΑθλοΠΑΙΔΕΙΑΣ',
                                               individual_sport=individual_sport,
                                               individual_sports_group=track,
                                               export_code='a',
                                               enabled=False)

        for individual_sport in mode_2_track_individual_sports_b:
            if not IndividualSport.objects.filter(mode='Αγώνες ΑθλοΠΑΙΔΕΙΑΣ', individual_sport=individual_sport):
                IndividualSport.objects.create(mode='Αγώνες ΑθλοΠΑΙΔΕΙΑΣ',
                                               individual_sport=individual_sport,
                                               individual_sports_group=track,
                                               export_code='b',
                                               enabled=False)

        for individual_sport in mode_2_track_individual_sports_c:
            if not IndividualSport.objects.filter(mode='Αγώνες ΑθλοΠΑΙΔΕΙΑΣ', individual_sport=individual_sport):
                IndividualSport.objects.create(mode='Αγώνες ΑθλοΠΑΙΔΕΙΑΣ',
                                               individual_sport=individual_sport,
                                               individual_sports_group=track,
                                               export_code='c',
                                               enabled=False)

        swimming_individual_sports = ['Κολύμβηση - 50μ Ελεύθερο',
                                      'Κολύμβηση - 100μ Ελεύθερο',
                                      'Κολύμβηση - 100μ Πρόσθιο',
                                      'Κολύμβηση - 100μ Ύπτιο',
                                      'Κολύμβηση - 100μ Πεταλούδα',
                                      'Κολύμβηση - 200μ Ελεύθερο',
                                      'Κολύμβηση - 200μ Πρόσθιο',
                                      'Κολύμβηση - 200μ Ύπτιο',
                                      'Κολύμβηση - 200μ Μικτή Ατομική',
                                      'Κολύμβηση - 400μ Ελεύθερο',
                                      'Κολύμβηση - 800μ Ελεύθερο',
                                      'Κολύμβηση - Σκυταλοδρομία 4x50 Ελεύθερο'
                                      ]

        swimming = IndividualSportsGroup.objects.filter(mode='Αγώνες ΑθλοΠΑΙΔΕΙΑΣ',
                                                        individual_sports_group=ISG_SWIMMING_STR).first()

        if not swimming:
            swimming = IndividualSportsGroup.objects.create(mode='Αγώνες ΑθλοΠΑΙΔΕΙΑΣ',
                                                            individual_sports_group=ISG_SWIMMING_STR,
                                                            enabled=True)
        for individual_sport in swimming_individual_sports:
            if not IndividualSport.objects.filter(mode='Αγώνες ΑθλοΠΑΙΔΕΙΑΣ', individual_sport=individual_sport):
                IndividualSport.objects.create(mode='Αγώνες ΑθλοΠΑΙΔΕΙΑΣ',
                                               individual_sport=individual_sport,
                                               individual_sports_group=swimming,
                                               export_code='d',
                                               enabled=False)

        tennis_individual_sports = ['Αντισφαίριση', ]

        tennis = IndividualSportsGroup.objects.filter(mode='Αγώνες ΑθλοΠΑΙΔΕΙΑΣ',
                                                      individual_sports_group=ISG_TENNIS_STR).first()

        if not tennis:
            tennis = IndividualSportsGroup.objects.create(mode='Αγώνες ΑθλοΠΑΙΔΕΙΑΣ',
                                                          individual_sports_group=ISG_TENNIS_STR,
                                                          enabled=True)
        for individual_sport in tennis_individual_sports:
            if not IndividualSport.objects.filter(mode='Αγώνες ΑθλοΠΑΙΔΕΙΑΣ', individual_sport=individual_sport):
                IndividualSport.objects.create(mode='Αγώνες ΑθλοΠΑΙΔΕΙΑΣ',
                                               individual_sport=individual_sport,
                                               individual_sports_group=tennis,
                                               export_code='d',
                                               enabled=False)
