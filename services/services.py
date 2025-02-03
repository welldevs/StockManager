from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from models.document import DocumentModel
from typing import List

def fetch_invoices(db: Session, query) -> List[dict]:
    results = db.execute(query).fetchall()
    
    data = []
    for row in results:
        row_dict = {column: value for column, value in zip(DocumentModel.__annotations__.keys(), row)}
        # Convertendo datetime para string ISO 8601
        if isinstance(row_dict.get("DTAFATURAMENTO"), datetime):
            row_dict["DTAFATURAMENTO"] = row_dict["DTAFATURAMENTO"].isoformat()
        if isinstance(row_dict.get("DTAINCLUSAO"), datetime):
            row_dict["DTAINCLUSAO"] = row_dict["DTAINCLUSAO"].isoformat()
        data.append(row_dict)
    
    return data
