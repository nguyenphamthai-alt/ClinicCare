from app.repositories.patient_repository import PatientRepository


class PatientService:
    def __init__(self, patient_repository: PatientRepository | None = None):
        self.patient_repository = patient_repository or PatientRepository()

    def search(self, db, search_term: str, limit: int):
        return [dict(r) for r in self.patient_repository.search(db, search_term, limit)]


    def create(self, db, body):
        patient_id = self.patient_repository.create(
            db,
            body.full_name,
            body.date_of_birth,
            body.sex,
            body.phone,
            body.email,
        )
        return self.patient_repository.find_by_id(db, patient_id)
