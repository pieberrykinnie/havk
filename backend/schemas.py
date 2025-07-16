"""Central pydantic reusable types and constraints."""
from typing import Literal

from pydantic import Field, constr

# E.164 phone number (7–15 digits, optional leading +)
PhoneStr = constr(regex=r"^\+?[0-9]{7,15}$")  # type: ignore[var-annotated]

# Farmer feedback rating literal
RatingStr = Literal["ok", "dry", "wet"]

__all__ = ["PhoneStr", "RatingStr"]