from pydantic import BaseModel

class RetrievedDocument(BaseModel):

    id: str

    chunk: str

    section: str

    subsection: str