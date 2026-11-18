from app.repositories.patient_repository import PatientRepository


class PatientService:
    def __init__(self, patient_repository: PatientRepository | None = None):
        self.patient_repository = patient_repository or PatientRepository()

    def search(self, db, search_term: str, limit: int):
        return [dict(r) for r in self.patient_repository.search(db, search_term, limit)]
