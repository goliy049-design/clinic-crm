from apps.patients.models import PatientProfile


class PublicPatientService:
    """
    Handles patient lookup and creation from public channels.

    Used by:
    - Website
    - Telegram bot
    """


    def __init__(
        self,
        clinic,
        phone_number,
        first_name,
        last_name,
    ):
        self.clinic = clinic
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name


    def get_or_create(self):
        """
        Find existing patient by phone inside the clinic.
        Otherwise create a new patient.
        """

        patient = PatientProfile.objects.filter(
            clinic=self.clinic,
            phone_number=self.phone_number,
        ).first()


        if patient:
            return patient


        patient = PatientProfile.objects.create(
            clinic=self.clinic,
            phone_number=self.phone_number,
            first_name=self.first_name,
            last_name=self.last_name,
        )


        return patient