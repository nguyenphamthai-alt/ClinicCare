from app.repositories.diagnosis_repository import DiagnosisRepository


class DiagnosisService:
    def __init__(self, diagnosis_repository: DiagnosisRepository | None = None):
        self.diagnosis_repository = diagnosis_repository or DiagnosisRepository()

    def search(self, db, search_term: str, limit: int, offset: int):
        rows = self.diagnosis_repository.search(db, search_term, limit, offset)
        return [dict(r) for r in rows]
