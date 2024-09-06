# src/data_structures/pdf_info.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class PDFInfo:
    filename: str
    branch_address: Optional[str] = None
    our_address: Optional[str] = None
    statement_period: Optional[str] = None
    account_summary: Optional[str] = None
    additional_info: Optional[str] = None

    def to_dict(self):
        return {
            "filename": self.filename,
            "branch_address": self.branch_address or "Need more details",
            "our_address": self.our_address or "Need more details",
            "statement_period": self.statement_period or "Need more details",
            "account_summary": self.account_summary or "Need more details",
            "additional_info": self.additional_info or ""
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            filename=data["filename"],
            branch_address=data.get("branch_address"),
            our_address=data.get("our_address"),
            statement_period=data.get("statement_period"),
            account_summary=data.get("account_summary"),
            additional_info=data.get("additional_info")
        )