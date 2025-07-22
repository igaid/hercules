from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AppState(models.Model):
    MODE_CHOICES = (
        ('Σχολικά Πρωταθλήματα', 'Σχολικά Πρωταθλήματα'),
        ('Αγώνες ΑθλοΠΑΙΔΕΙΑΣ', 'Αγώνες ΑθλοΠΑΙΔΕΙΑΣ')
    )

    SCHOOLS_ENABLED_CHOICES = (
        ('Τα σχολεία είναι ενεργοποιημένα', 'Τα σχολεία είναι ενεργοποιημένα'),
        ('Τα σχολεία είναι απενεργοποιημένα', 'Τα σχολεία είναι απενεργοποιημένα')
    )

    mode = models.CharField(default='Σχολικά Πρωταθλήματα', choices=MODE_CHOICES, max_length=25,
                            verbose_name='Σχολικά Πρωταθλήματα / Αγώνες ΑθλοΠΑΙΔΕΙΑΣ')
    active_sch_year = models.CharField(default='2024-2025', max_length=10, verbose_name='Ενεργό Σχολικό Έτος')
    schools_enabled = models.CharField(default='Τα σχολεία είναι ενεργοποιημένα', choices=SCHOOLS_ENABLED_CHOICES,
                                       max_length=40, verbose_name='Ενεργοποίηση / Απενεργοποίηση Σχολείων')
    home_message = models.CharField(default='Καλώς ορίσατε', max_length=1000, verbose_name='Μήνυμα αρχικής οθόνης')

    def __str__(self):
        return f"{self.mode}"


class TrustedUser(models.Model):
    ROLE_CHOICES = (
        ('ΣΧΟΛΕΙΟ', 'ΣΧΟΛΕΙΟ'),
        ('ΔΔΕ', 'ΔΔΕ')
    )

    SCHOOL_TYPE_CHOICES = (
        ('ΓΥΜΝΑΣΙΟ', 'ΓΥΜΝΑΣΙΟ'),
        ('ΛΥΚΕΙΟ', 'ΛΥΚΕΙΟ'),
        ('ΔΔΕ', 'ΔΔΕ')
    )

    trusted_user = models.CharField(unique=True, max_length=20, verbose_name='Νόμιμος χρήστης')
    name = models.CharField(max_length=100, verbose_name='Όνομα νόμιμου χρήστη')
    user_role = models.CharField(choices=ROLE_CHOICES, max_length=10, verbose_name='ΣΧΟΛΕΙΟ / ΔΔΕ')
    school_type = models.CharField(choices=SCHOOL_TYPE_CHOICES, max_length=10, verbose_name='ΣΧΟΛΕΙΟ / ΔΔΕ')
    headmaster = models.CharField(max_length=100, verbose_name='Διευθυντής σχολείου')
    enabled = models.BooleanField(default=True, verbose_name='Ενεργός χρήστης')

    def __str__(self):
        return f"{self.name} ({self.user_role})"


class SchoolRegistration(models.Model):
    SCHOOL_CHOICES = (
        ('---', '---'),
        ('10ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', '10ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('10ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', '10ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('11ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', '11ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('11ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', '11ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('12ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', '12ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('13ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', '13ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('13ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', '13ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('1ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', '1ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('1ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', '1ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('1ο ΕΠΑ.Λ. ΑΡΚΑΛΟΧΩΡΙΟΥ', '1ο ΕΠΑ.Λ. ΑΡΚΑΛΟΧΩΡΙΟΥ'),
        ('1ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ', '1ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ'),
        ('1ο ΕΠΑ.Λ. ΜΟΙΡΩΝ', '1ο ΕΠΑ.Λ. ΜΟΙΡΩΝ'),
        ('2ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', '2ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('2ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', '2ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('2ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ', '2ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ'),
        ('3ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', '3ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('3ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', '3ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('3ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ', '3ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ'),
        ('4ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', '4ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('4ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', '4ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('4ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ (ΕΣΠΕΡΙΝΟ)', '4ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ (ΕΣΠΕΡΙΝΟ)'),
        ('5ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', '5ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('5ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', '5ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('5ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ', '5ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ'),
        ('6ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', '6ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('6ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', '6ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('6ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ', '6ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ'),
        ('7ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', '7ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('7ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', '7ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('8ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', '8ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('8ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', '8ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('9ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', '9ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΓΙΑΣ ΒΑΡΒΑΡΑΣ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΓΙΑΣ ΒΑΡΒΑΡΑΣ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΓΙΟΥ ΜΥΡΩΝΑ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΓΙΟΥ ΜΥΡΩΝΑ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΓΙΩΝ ΔΕΚΑ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΓΙΩΝ ΔΕΚΑ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΡΚΑΛΟΧΩΡΙΟΥ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΡΚΑΛΟΧΩΡΙΟΥ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΡΧΑΝΩΝ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΡΧΑΝΩΝ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΣΗΜΙΟΥ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΣΗΜΙΟΥ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΒΙΑΝΝΟΥ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΒΙΑΝΝΟΥ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΓΑΖΙΟΥ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΓΑΖΙΟΥ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΓΟΥΒΩΝ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΓΟΥΒΩΝ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΕΠΙΣΚΟΠΗΣ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΕΠΙΣΚΟΠΗΣ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΚΑΣΤΕΛΛΙΟΥ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΚΑΣΤΕΛΛΙΟΥ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΚΡΟΥΣΩΝΑ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΚΡΟΥΣΩΝΑ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ Λ. ΧΕΡΣΟΝΗΣΟΥ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ Λ. ΧΕΡΣΟΝΗΣΟΥ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΜΑΛΙΩΝ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΜΑΛΙΩΝ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΜΕΛΕΣΩΝ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΜΕΛΕΣΩΝ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΜΟΙΡΩΝ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΜΟΙΡΩΝ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΜΟΧΟΥ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΜΟΧΟΥ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ Ν. ΑΛΙΚΑΡΝΑΣΣΟΥ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ Ν. ΑΛΙΚΑΡΝΑΣΣΟΥ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΠΟΜΠΙΑΣ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΠΟΜΠΙΑΣ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΤΥΜΠΑΚΙΟΥ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΤΥΜΠΑΚΙΟΥ'),
        ('ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΧΑΡΑΚΑ', 'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΧΑΡΑΚΑ'),
        ('ΓΥΜΝΑΣΙΟ ΑΓΙΑΣ ΒΑΡΒΑΡΑΣ', 'ΓΥΜΝΑΣΙΟ ΑΓΙΑΣ ΒΑΡΒΑΡΑΣ'),
        ('ΓΥΜΝΑΣΙΟ ΑΓΙΟΥ ΜΥΡΩΝΑ', 'ΓΥΜΝΑΣΙΟ ΑΓΙΟΥ ΜΥΡΩΝΑ'),
        ('ΓΥΜΝΑΣΙΟ ΑΓΙΩΝ ΔΕΚΑ', 'ΓΥΜΝΑΣΙΟ ΑΓΙΩΝ ΔΕΚΑ'),
        ('ΓΥΜΝΑΣΙΟ ΑΡΚΑΛΟΧΩΡΙΟΥ', 'ΓΥΜΝΑΣΙΟ ΑΡΚΑΛΟΧΩΡΙΟΥ'),
        ('ΓΥΜΝΑΣΙΟ ΑΡΧΑΝΩΝ', 'ΓΥΜΝΑΣΙΟ ΑΡΧΑΝΩΝ'),
        ('ΓΥΜΝΑΣΙΟ ΑΣΗΜΙΟΥ', 'ΓΥΜΝΑΣΙΟ ΑΣΗΜΙΟΥ'),
        ('ΓΥΜΝΑΣΙΟ ΒΑΓΙΟΝΙΑΣ', 'ΓΥΜΝΑΣΙΟ ΒΑΓΙΟΝΙΑΣ'),
        ('ΓΥΜΝΑΣΙΟ ΒΕΝΕΡΑΤΟΥ', 'ΓΥΜΝΑΣΙΟ ΒΕΝΕΡΑΤΟΥ'),
        ('ΓΥΜΝΑΣΙΟ ΒΙΑΝΝΟΥ', 'ΓΥΜΝΑΣΙΟ ΒΙΑΝΝΟΥ'),
        ('ΓΥΜΝΑΣΙΟ ΓΑΖΙΟΥ', 'ΓΥΜΝΑΣΙΟ ΓΑΖΙΟΥ'),
        ('ΓΥΜΝΑΣΙΟ ΓΕΡΓΕΡΗΣ', 'ΓΥΜΝΑΣΙΟ ΓΕΡΓΕΡΗΣ'),
        ('ΓΥΜΝΑΣΙΟ ΓΟΥΒΩΝ', 'ΓΥΜΝΑΣΙΟ ΓΟΥΒΩΝ'),
        ('ΓΥΜΝΑΣΙΟ ΕΠΙΣΚΟΠΗΣ', 'ΓΥΜΝΑΣΙΟ ΕΠΙΣΚΟΠΗΣ'),
        ('ΓΥΜΝΑΣΙΟ ΖΑΡΟΥ', 'ΓΥΜΝΑΣΙΟ ΖΑΡΟΥ'),
        ('ΓΥΜΝΑΣΙΟ ΘΡΑΨΑΝΟΥ', 'ΓΥΜΝΑΣΙΟ ΘΡΑΨΑΝΟΥ'),
        ('ΓΥΜΝΑΣΙΟ ΚΑΣΤΕΛΛΙΟΥ', 'ΓΥΜΝΑΣΙΟ ΚΑΣΤΕΛΛΙΟΥ'),
        ('ΓΥΜΝΑΣΙΟ ΚΡΟΥΣΩΝΑ', 'ΓΥΜΝΑΣΙΟ ΚΡΟΥΣΩΝΑ'),
        ('ΓΥΜΝΑΣΙΟ Λ. ΧΕΡΣΟΝΗΣΟΥ', 'ΓΥΜΝΑΣΙΟ Λ. ΧΕΡΣΟΝΗΣΟΥ'),
        ('ΓΥΜΝΑΣΙΟ ΜΑΛΙΩΝ', 'ΓΥΜΝΑΣΙΟ ΜΑΛΙΩΝ'),
        ('ΓΥΜΝΑΣΙΟ ΜΕΛΕΣΩΝ', 'ΓΥΜΝΑΣΙΟ ΜΕΛΕΣΩΝ'),
        ('ΓΥΜΝΑΣΙΟ ΜΟΙΡΩΝ', 'ΓΥΜΝΑΣΙΟ ΜΟΙΡΩΝ'),
        ('ΓΥΜΝΑΣΙΟ ΜΟΧΟΥ', 'ΓΥΜΝΑΣΙΟ ΜΟΧΟΥ'),
        ('ΓΥΜΝΑΣΙΟ Ν. ΑΛΙΚΑΡΝΑΣΣΟΥ', 'ΓΥΜΝΑΣΙΟ Ν. ΑΛΙΚΑΡΝΑΣΣΟΥ'),
        ('ΓΥΜΝΑΣΙΟ ΠΟΜΠΙΑΣ', 'ΓΥΜΝΑΣΙΟ ΠΟΜΠΙΑΣ'),
        ('ΓΥΜΝΑΣΙΟ ΠΡΟΦΗΤΗ ΗΛΙΑ', 'ΓΥΜΝΑΣΙΟ ΠΡΟΦΗΤΗ ΗΛΙΑ'),
        ('ΓΥΜΝΑΣΙΟ ΠΥΡΓΟΥ', 'ΓΥΜΝΑΣΙΟ ΠΥΡΓΟΥ'),
        ('ΓΥΜΝΑΣΙΟ ΤΕΦΕΛΙΟΥ', 'ΓΥΜΝΑΣΙΟ ΤΕΦΕΛΙΟΥ'),
        ('ΓΥΜΝΑΣΙΟ ΤΥΛΙΣΟΥ', 'ΓΥΜΝΑΣΙΟ ΤΥΛΙΣΟΥ'),
        ('ΓΥΜΝΑΣΙΟ ΤΥΜΠΑΚΙΟΥ', 'ΓΥΜΝΑΣΙΟ ΤΥΜΠΑΚΙΟΥ'),
        ('ΓΥΜΝΑΣΙΟ ΧΑΡΑΚΑ', 'ΓΥΜΝΑΣΙΟ ΧΑΡΑΚΑ'),
        ('ΕΕΕΕΚ ΗΡΑΚΛΕΙΟΥ', 'ΕΕΕΕΚ ΗΡΑΚΛΕΙΟΥ'),
        ('ΕΕΕΕΚ ΤΥΜΠΑΚΙΟΥ', 'ΕΕΕΕΚ ΤΥΜΠΑΚΙΟΥ'),
        ('ΕΙΔΙΚΟ ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', 'ΕΙΔΙΚΟ ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('ΕΠΑΛ ΕΙΔΙΚΗΣ ΑΓΩΓΗΣ', 'ΕΠΑΛ ΕΙΔΙΚΗΣ ΑΓΩΓΗΣ'),
        ('ΕΣΠΕΡΙΝΟ ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', 'ΕΣΠΕΡΙΝΟ ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('ΕΣΠΕΡΙΝΟ ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', 'ΕΣΠΕΡΙΝΟ ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('ΕΣΠΕΡΙΝΟ ΓΥΜΝΑΣΙΟ ΤΥΜΠΑΚΙΟΥ', 'ΕΣΠΕΡΙΝΟ ΓΥΜΝΑΣΙΟ ΤΥΜΠΑΚΙΟΥ'),
        ('ΚΑΛΛΙΤΕΧΝΙΚΟ ΓΥΜΝΑΣΙΟ', 'ΚΑΛΛΙΤΕΧΝΙΚΟ ΓΥΜΝΑΣΙΟ'),
        ('ΜΟΥΣΙΚΟ ΣΧΟΛΕΙΟ - ΓΥΜΝΑΣΙΟ', 'ΜΟΥΣΙΚΟ ΣΧΟΛΕΙΟ - ΓΥΜΝΑΣΙΟ'),
        ('ΠΡΟΤΥΠΟ ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ', 'ΠΡΟΤΥΠΟ ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ'),
        ('ΠΡΟΤΥΠΟ ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ', 'ΠΡΟΤΥΠΟ ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ')
    )
    school = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Σχολείο')
    school_year = models.CharField(max_length=10, verbose_name='Σχολικό έτος')
    locked = models.BooleanField(default=False, verbose_name='Κλειδωμένο')

    football_boys = models.PositiveIntegerField(default=0, verbose_name='Πλήθος Ομάδων Αγοριών για Ποδόσφαιρο')
    football_girls = models.PositiveIntegerField(default=0, verbose_name='Πλήθος Ομάδων Κοριτσιών για Ποδόσφαιρο')
    football_mix_1 = models.PositiveIntegerField(default=0,
                                                 verbose_name='Πλήθος Μικτών Ομάδων (Αγόρια + Κορίτσια) για Ποδόσφαιρο')
    football_mix_2 = models.PositiveIntegerField(default=0,
                                                 verbose_name='Πλήθος Μικτών Ομάδων (ΣΜΕΑ + ΓΕΝΙΚΗ ΕΚΠ/ΣΗ) για Ποδόσφαιρο')
    football_mix_school = models.CharField(max_length=100, default='---', choices=SCHOOL_CHOICES,
                                           verbose_name='Όνομα Σχολείου που συμμετέχει στη Μικτή Ομάδα για Ποδόσφαιρο')

    handball_boys = models.PositiveIntegerField(default=0, verbose_name='Πλήθος Ομάδων Αγοριών για Χειροσφαίριση')
    handball_girls = models.PositiveIntegerField(default=0, verbose_name='Πλήθος Ομάδων Κοριτσιών για Χειροσφαίριση')
    handball_mix_1 = models.PositiveIntegerField(default=0,
                                                 verbose_name='Πλήθος Μικτών Ομάδων (Αγόρια + Κορίτσια) για Χειροσφαίριση')
    handball_mix_2 = models.PositiveIntegerField(default=0,
                                                 verbose_name='Πλήθος Μικτών Ομάδων (ΣΜΕΑ + ΓΕΝΙΚΗ ΕΚΠ/ΣΗ) για Χειροσφαίριση')
    handball_mix_school = models.CharField(max_length=100, default='---', choices=SCHOOL_CHOICES,
                                           verbose_name='Όνομα Σχολείου που συμμετέχει στη Μικτή Ομάδα για Χειροσφαίριση')

    basketball_boys = models.PositiveIntegerField(default=0, verbose_name='Πλήθος Ομάδων Αγοριών για Καλαθοσφαίριση')
    basketball_girls = models.PositiveIntegerField(default=0, verbose_name='Πλήθος Ομάδων Κοριτσιών για Καλαθοσφαίριση')
    basketball_mix_1 = models.PositiveIntegerField(default=0,
                                                   verbose_name='Πλήθος Μικτών Ομάδων (Αγόρια + Κορίτσια) για Καλαθοσφαίριση')
    basketball_mix_2 = models.PositiveIntegerField(default=0,
                                                   verbose_name='Πλήθος Μικτών Ομάδων (ΣΜΕΑ + ΓΕΝΙΚΗ ΕΚΠ/ΣΗ) για Καλαθοσφαίριση')
    basketball_mix_school = models.CharField(max_length=100, default='---', choices=SCHOOL_CHOICES,
                                             verbose_name='Όνομα Σχολείου που συμμετέχει στη Μικτή Ομάδα για Καλαθοσφαίριση')

    beach_volleyball_boys = models.PositiveIntegerField(default=0,
                                                        verbose_name='Πλήθος Ομάδων Αγοριών για Beach Volley')
    beach_volleyball_girls = models.PositiveIntegerField(default=0,
                                                         verbose_name='Πλήθος Ομάδων Κοριτσιών για Beach Volley')
    beach_volleyball_mix_1 = models.PositiveIntegerField(default=0,
                                                         verbose_name='Πλήθος Μικτών Ομάδων (Αγόρια + Κορίτσια) για Beach Volley')
    beach_volleyball_mix_2 = models.PositiveIntegerField(default=0,
                                                         verbose_name='Πλήθος Μικτών Ομάδων (ΣΜΕΑ + ΓΕΝΙΚΗ ΕΚΠ/ΣΗ) για Beach Volley')
    beach_volleyball_mix_school = models.CharField(max_length=100, default='---', choices=SCHOOL_CHOICES,
                                                   verbose_name='Όνομα Σχολείου που συμμετέχει στη Μικτή Ομάδα για Beach Volley')

    volleyball_boys = models.PositiveIntegerField(default=0, verbose_name='Πλήθος Ομάδων Αγοριών για Πετοσφαίριση')
    volleyball_girls = models.PositiveIntegerField(default=0, verbose_name='Πλήθος Ομάδων Κοριτσιών για Πετοσφαίριση')
    volleyball_mix_1 = models.PositiveIntegerField(default=0,
                                                   verbose_name='Πλήθος Μικτών Ομάδων (Αγόρια + Κορίτσια) για Πετοσφαίριση')
    volleyball_mix_2 = models.PositiveIntegerField(default=0,
                                                   verbose_name='Πλήθος Μικτών Ομάδων (ΣΜΕΑ + ΓΕΝΙΚΗ ΕΚΠ/ΣΗ) για Πετοσφαίριση')
    volleyball_mix_school = models.CharField(max_length=100, default='---', choices=SCHOOL_CHOICES,
                                             verbose_name='Όνομα Σχολείου που συμμετέχει στη Μικτή Ομάδα για Πετοσφαίριση')

    swimming_boys = models.BooleanField(default=False, verbose_name='Κολύμβηση Αγοριών')
    swimming_girls = models.BooleanField(default=False, verbose_name='Κολύμβηση Κοριτσιών')
    track_boys = models.BooleanField(default=False, verbose_name='Κλασσικός Αθλητισμός Αγοριών')
    track_girls = models.BooleanField(default=False, verbose_name='Κλασσικός Αθλητισμός Κοριτσιών')
    fencing_boys = models.BooleanField(default=False, verbose_name='Ξιφασκία Αγοριών')
    fencing_girls = models.BooleanField(default=False, verbose_name='Ξιφασκία Κοριτσιών')
    tennis_boys = models.BooleanField(default=False, verbose_name='Αντισφαίριση Αγοριών')
    tennis_girls = models.BooleanField(default=False, verbose_name='Αντισφαίριση Κοριτσιών')

    submit_date_time = models.DateTimeField(null=True, verbose_name='Χρονική σήμανση')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['school', 'school_year'],
                                    name='unique_school_registration')
        ]


class TeamSport(models.Model):
    MODE_CHOICES = (
        ('Σχολικά Πρωταθλήματα', 'Σχολικά Πρωταθλήματα'),
        ('Αγώνες ΑθλοΠΑΙΔΕΙΑΣ', 'Αγώνες ΑθλοΠΑΙΔΕΙΑΣ')
    )

    mode = models.CharField(default='Σχολικά Πρωταθλήματα', choices=MODE_CHOICES, max_length=25,
                            verbose_name='Σχολικά Πρωταθλήματα / Αγώνες ΑθλοΠΑΙΔΕΙΑΣ')
    team_sport = models.CharField(max_length=100, verbose_name='Ομαδικό άθλημα')
    enabled = models.BooleanField(default=True, verbose_name='Ενεργό ομαδικό άθλημα')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['mode', 'team_sport'],
                                    name='unique_team_sport')
        ]

    def __str__(self):
        return f"{self.team_sport}"


class TeamSportLimits(models.Model):
    MODE_CHOICES = (
        ('Σχολικά Πρωταθλήματα', 'Σχολικά Πρωταθλήματα'),
        ('Αγώνες ΑθλοΠΑΙΔΕΙΑΣ', 'Αγώνες ΑθλοΠΑΙΔΕΙΑΣ')
    )

    mode = models.CharField(default='Σχολικά Πρωταθλήματα', choices=MODE_CHOICES, max_length=25,
                            verbose_name='Σχολικά Πρωταθλήματα / Αγώνες ΑθλοΠΑΙΔΕΙΑΣ')
    team_sport = models.OneToOneField(TeamSport, on_delete=models.CASCADE, verbose_name='Ομαδικό άθλημα')
    min_students_main_list = models.IntegerField(default=1, verbose_name='Ελάχιστο πλήθος μαθητών στη Λίστα')
    max_students_main_list = models.IntegerField(default=24, verbose_name='Μέγιστο πλήθος μαθητών στη Λίστα')
    min_students_phase_list = models.IntegerField(default=1,
                                                  verbose_name='Ελάχιστο πλήθος μαθητών στην Κατάσταση Συμμετοχής')
    max_students_phase_list = models.IntegerField(default=18,
                                                  verbose_name='Μέγιστο πλήθος μαθητών στην Κατάσταση Συμμετοχής')

    def __str__(self):
        return f"{str(self.team_sport)} {self.min_students_main_list}/{self.max_students_main_list}/{self.min_students_phase_list}/{self.max_students_phase_list}"


class TeamSportMainList(models.Model):
    MODE_CHOICES = (
        ('Σχολικά Πρωταθλήματα', 'Σχολικά Πρωταθλήματα'),
        ('Αγώνες ΑθλοΠΑΙΔΕΙΑΣ', 'Αγώνες ΑθλοΠΑΙΔΕΙΑΣ')
    )

    GENDER_CHOICES = (
        ('Αγόρια', 'Αγόρια'),
        ('Κορίτσια', 'Κορίτσια')
    )

    mode = models.CharField(choices=MODE_CHOICES, max_length=25,
                            verbose_name='Σχολικά Πρωταθλήματα / Αγώνες ΑθλοΠΑΙΔΕΙΑΣ')
    school = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Σχολείο')
    school_year = models.CharField(max_length=10, verbose_name='Σχολικό έτος')
    team_sport = models.ForeignKey(TeamSport, on_delete=models.CASCADE, verbose_name='Ομαδικό άθλημα')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, verbose_name='Φύλο')
    pt_teacher = models.CharField(max_length=100, verbose_name='Εκπαιδευτικός')
    locked = models.BooleanField(default=False, verbose_name='Κλειδωμένο')
    # students_count = models.IntegerField(default=0, verbose_name='Πλήθος μαθητών')
    submit_date_time = models.DateTimeField(null=True, verbose_name='Χρονική σήμανση')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['mode', 'school', 'school_year', 'team_sport', 'gender'],
                                    name='unique_team_sport_ml')
        ]

    def __str__(self):
        return f"{self.team_sport}-{self.gender}"


class TeamSportPhaseList(models.Model):
    MODE_CHOICES = (
        ('Σχολικά Πρωταθλήματα', 'Σχολικά Πρωταθλήματα'),
        ('Αγώνες ΑθλοΠΑΙΔΕΙΑΣ', 'Αγώνες ΑθλοΠΑΙΔΕΙΑΣ')
    )

    PHASE_CHOICES = (
        ('1η', '1η'),
        ('2η', '2η'),
        ('3η', '3η')
    )

    mode = models.CharField(choices=MODE_CHOICES, max_length=25,
                            verbose_name='Σχολικά Πρωταθλήματα / Αγώνες ΑθλοΠΑΙΔΕΙΑΣ')
    school = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Σχολείο')
    school_year = models.CharField(max_length=10, verbose_name='Σχολικό έτος')
    team_sport_main_list = models.ForeignKey(TeamSportMainList, on_delete=models.CASCADE,
                                             related_name='team_sport_phases', verbose_name='Λίστα ομάδας')
    phase = models.CharField(choices=PHASE_CHOICES, max_length=2, verbose_name='Φάση')
    pt_teacher = models.CharField(max_length=100, verbose_name='Εκπαιδευτικός')
    locked = models.BooleanField(default=False, verbose_name='Κλειδωμένο')
    students_count = models.IntegerField(default=0, verbose_name='Πλήθος μαθητών')
    submit_date_time = models.DateTimeField(null=True, verbose_name='Χρονική σήμανση')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['mode', 'school', 'school_year', 'team_sport_main_list', 'phase'],
                                    name='unique_team_sport_pl')
        ]

    def __str__(self):
        return f"{self.team_sport_main_list}-{self.phase} Φάση"


class IndividualSportsGroup(models.Model):
    MODE_CHOICES = (
        ('Σχολικά Πρωταθλήματα', 'Σχολικά Πρωταθλήματα'),
        ('Αγώνες ΑθλοΠΑΙΔΕΙΑΣ', 'Αγώνες ΑθλοΠΑΙΔΕΙΑΣ')
    )

    mode = models.CharField(default='Σχολικά Πρωταθλήματα', choices=MODE_CHOICES, max_length=25,
                            verbose_name='Σχολικά Πρωταθλήματα / Αγώνες ΑθλοΠΑΙΔΕΙΑΣ')
    individual_sports_group = models.CharField(max_length=100, verbose_name='Ατομικό άθλημα')
    enabled = models.BooleanField(default=True, verbose_name='Ενεργό ατομικό άθλημα')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['mode', 'individual_sports_group'],
                                    name='unique_individual_sports_group')
        ]

    def __str__(self):
        return f"{self.individual_sports_group}"


class IndividualSport(models.Model):
    MODE_CHOICES = (
        ('Σχολικά Πρωταθλήματα', 'Σχολικά Πρωταθλήματα'),
        ('Αγώνες ΑθλοΠΑΙΔΕΙΑΣ', 'Αγώνες ΑθλοΠΑΙΔΕΙΑΣ')
    )

    EXPORT_CODE_CHOICES = (
        ('a', 'a'),
        ('b', 'b'),
        ('c', 'c'),
        ('d', 'd'),
        ('x1', 'x1'),
        ('x2', 'x2'),
    )

    mode = models.CharField(default='Σχολικά Πρωταθλήματα', choices=MODE_CHOICES, max_length=25,
                            verbose_name='Σχολικά Πρωταθλήματα / Αγώνες ΑθλοΠΑΙΔΕΙΑΣ')
    individual_sport = models.CharField(max_length=100, verbose_name='Αγώνισμα')
    individual_sports_group = models.ForeignKey(IndividualSportsGroup, on_delete=models.CASCADE,
                                                related_name='individual_sports', verbose_name='Ατομικό άθλημα')
    export_code = models.CharField(default='a', choices=EXPORT_CODE_CHOICES, max_length=2,
                                   verbose_name='Κωδικός Πινακίου')
    enabled = models.BooleanField(default=True, verbose_name='Ενεργό αγώνισμα')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['mode', 'individual_sport'],
                                    name='unique_individual_sport')
        ]

    def __str__(self):
        return f"{self.individual_sport}"


class IndividualSportsGroupPhase(models.Model):
    MODE_CHOICES = (
        ('Σχολικά Πρωταθλήματα', 'Σχολικά Πρωταθλήματα'),
        ('Αγώνες ΑθλοΠΑΙΔΕΙΑΣ', 'Αγώνες ΑθλοΠΑΙΔΕΙΑΣ')
    )

    PHASE_CHOICES = (
        ('1η', '1η'),
        ('2η', '2η'),
        ('3η', '3η')
    )

    mode = models.CharField(choices=MODE_CHOICES, max_length=25,
                            verbose_name='Σχολικά Πρωταθλήματα / Αγώνες ΑθλοΠΑΙΔΕΙΑΣ')
    school = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Σχολείο')
    school_year = models.CharField(max_length=10, verbose_name='Σχολικό έτος')
    individual_sports_group = models.ForeignKey(IndividualSportsGroup, on_delete=models.CASCADE,
                                                related_name='individual_sports_group_phases',
                                                verbose_name='Ατομικό άθλημα')
    phase = models.CharField(choices=PHASE_CHOICES, max_length=2, verbose_name='Φάση')
    pt_teacher = models.CharField(max_length=100, verbose_name='Εκπαιδευτικός')
    locked = models.BooleanField(default=False, verbose_name='Κλειδωμένο')
    students_count = models.IntegerField(default=0, verbose_name='Πλήθος μαθητών')
    submit_date_time = models.DateTimeField(null=True, verbose_name='Χρονική σήμανση')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['mode', 'school', 'school_year', 'individual_sports_group', 'phase'],
                                    name='unique_individual_sports_group_phase')
        ]

    def __str__(self):
        return f"{self.individual_sports_group}"


class IndividualSportList(models.Model):
    MODE_CHOICES = (
        ('Σχολικά Πρωταθλήματα', 'Σχολικά Πρωταθλήματα'),
        ('Αγώνες ΑθλοΠΑΙΔΕΙΑΣ', 'Αγώνες ΑθλοΠΑΙΔΕΙΑΣ')
    )

    mode = models.CharField(choices=MODE_CHOICES, max_length=25,
                            verbose_name='Σχολικά Πρωταθλήματα / Αγώνες ΑθλοΠΑΙΔΕΙΑΣ')
    school = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Σχολείο')
    school_year = models.CharField(max_length=10, verbose_name='Σχολικό έτος')
    individual_sport = models.ForeignKey(IndividualSport, on_delete=models.CASCADE, verbose_name='Αγώνισμα')
    individual_sports_group_phase = models.ForeignKey(IndividualSportsGroupPhase, on_delete=models.CASCADE,
                                                      related_name='individual_sport_lists',
                                                      verbose_name='Ατομικό άθλημα')
    pt_teacher = models.CharField(max_length=100, verbose_name='Εκπαιδευτικός')
    locked = models.BooleanField(default=False, verbose_name='Κλειδωμένο')
    # students_count = models.IntegerField(default=0, verbose_name='Πλήθος μαθητών')
    submit_date_time = models.DateTimeField(null=True, verbose_name='Χρονική σήμανση')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['mode', 'school', 'school_year', 'individual_sport', 'individual_sports_group_phase'],
                name='unique_individual_sport_l')
        ]

    def __str__(self):
        return f"{self.individual_sport}"


class Student(models.Model):
    MODE_CHOICES = (
        ('Σχολικά Πρωταθλήματα', 'Σχολικά Πρωταθλήματα'),
        ('Αγώνες ΑθλοΠΑΙΔΕΙΑΣ', 'Αγώνες ΑθλοΠΑΙΔΕΙΑΣ')
    )

    PLAYS_IN_CHOICES = (
        ('Ομαδικό Άθλημα', 'Ομαδικό Άθλημα'),
        ('Ατομικό Άθλημα', 'Ατομικό Άθλημα')
    )

    GENDER_CHOICES = (
        ('Αγόρι', 'Αγόρι'),
        ('Κορίτσι', 'Κορίτσι')
    )

    SCHOOL_CLASS_CHOICES = (
        ('Α', 'Α'),
        ('B', 'B'),
        ('Γ', 'Γ')
    )

    PHASE_CHOICES = (
        ('1η', '1η'),
        ('2η', '2η'),
        ('3η', '3η')
    )

    mode = models.CharField(choices=MODE_CHOICES, max_length=25,
                            verbose_name='Σχολικά Πρωταθλήματα / Αγώνες ΑθλοΠΑΙΔΕΙΑΣ')
    plays_in = models.CharField(choices=PLAYS_IN_CHOICES, max_length=20, verbose_name='Παίζει σε')
    school = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Σχολείο')
    school_year = models.CharField(max_length=10, verbose_name='Σχολικό έτος')
    last_name = models.CharField(max_length=100, verbose_name='Επώνυμο μαθητή')
    first_name = models.CharField(max_length=100, verbose_name='Όνομα μαθητή')
    father_name = models.CharField(max_length=100, verbose_name='Όνομα πατέρα')
    mother_name = models.CharField(max_length=100, verbose_name='Όνομα μητέρας')
    year_of_birth = models.CharField(max_length=4, verbose_name='Έτος γέννησης')
    registry_no = models.CharField(max_length=10, verbose_name='Αρ. Μητρώου')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, verbose_name='Φύλο')
    school_class = models.CharField(choices=SCHOOL_CLASS_CHOICES, max_length=2, verbose_name='Τάξη')
    team_sport_main_list = models.ForeignKey(TeamSportMainList, on_delete=models.CASCADE, null=True, blank=True,
                                             related_name='team_sport_students')
    individual_sport_list = models.ForeignKey(IndividualSportList, on_delete=models.CASCADE, null=True, blank=True,
                                              related_name='individual_sport_students')
    plays_in_phase_1 = models.BooleanField(default=False, verbose_name='1η Φάση')
    plays_in_phase_2 = models.BooleanField(default=False, verbose_name='2η Φάση')
    plays_in_phase_3 = models.BooleanField(default=False, verbose_name='3η Φάση')
    individual_sport_plays_in_phase = models.CharField(default='1η', choices=PHASE_CHOICES, max_length=2,
                                                       verbose_name='Φάση ατομικού αθλήματος')

    def __str__(self):
        return f"[{self.school}] (AM: {self.registry_no}) {self.last_name} {self.first_name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['mode', 'plays_in', 'school', 'school_year', 'registry_no',
                                            'individual_sport_plays_in_phase'],
                                    name='unique_student')
        ]


class UnlockEntry(models.Model):
    dde_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Χρήστης ΔΔΕ')
    list_to_unlock = models.CharField(max_length=255, verbose_name='Λίστα για ξεκλείδωμα')
    unlock_date_time = models.DateTimeField(null=True, verbose_name='Χρονική σήμανση')

    def __str__(self):
        return f"[{self.dde_user}] {self.list_to_unlock} ({self.unlock_date_time})"
