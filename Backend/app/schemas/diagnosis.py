from pydantic import BaseModel


class DiagnosisOut(BaseModel):
    code: str
    description: str
