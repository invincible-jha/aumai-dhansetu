"""Pydantic models for aumai-dhansetu."""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class FinancialTopic(str, Enum):
    """Financial literacy topic categories."""

    SAVINGS = "savings"
    INSURANCE = "insurance"
    INVESTMENT = "investment"
    CREDIT = "credit"
    TAXATION = "taxation"
    DIGITAL_PAYMENTS = "digital_payments"


class LiteracyLevel(str, Enum):
    """Financial literacy level."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class BudgetCategory(str, Enum):
    """Budget allocation categories (50/30/20 rule)."""

    NEEDS = "needs"
    WANTS = "wants"
    SAVINGS = "savings"
    EMI = "emi"


class FinancialConcept(BaseModel):
    """A financial literacy concept."""

    topic: FinancialTopic
    title: str
    explanation: str
    examples: list[str] = Field(default_factory=list)
    level: LiteracyLevel
    key_terms: list[str] = Field(default_factory=list)


class BudgetPlan(BaseModel):
    """A monthly budget plan based on the 50/30/20 rule."""

    income: float = Field(gt=0)
    allocations: dict[str, float] = Field(default_factory=dict)
    recommendations: list[str] = Field(default_factory=list)
    savings_target: float = 0.0
    emergency_fund_months: int = 6


class GovernmentScheme(BaseModel):
    """Indian government financial scheme."""

    name: str
    description: str
    eligibility: str
    benefits: str
    how_to_apply: str
    ministry: str = ""
    min_age: int | None = None
    max_age: int | None = None
    income_limit: float | None = None
    target_group: str = ""


class InvestmentOption(BaseModel):
    """Investment option comparison."""

    name: str
    risk_level: Literal["low", "moderate", "high"]
    expected_return_pct: str
    lock_in_years: float
    tax_benefit: bool
    min_investment: float
    description: str


class UPIGuideEntry(BaseModel):
    """UPI guidance entry."""

    topic: str
    steps: list[str]
    tips: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


__all__ = [
    "FinancialTopic",
    "LiteracyLevel",
    "BudgetCategory",
    "FinancialConcept",
    "BudgetPlan",
    "GovernmentScheme",
    "InvestmentOption",
    "UPIGuideEntry",
]
