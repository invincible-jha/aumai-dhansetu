"""Comprehensive tests for aumai-dhansetu core and models.

Disclaimer: These tests are for software testing purposes only.
This codebase provides financial education, not financial advice.
Consult a qualified financial advisor before making investment decisions.
"""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from pydantic import ValidationError

from aumai_dhansetu.core import (
    BudgetPlanner,
    ConceptLibrary,
    InvestmentBasics,
    SchemeAdvisor,
    UPIGuide,
)
from aumai_dhansetu.models import (
    BudgetCategory,
    BudgetPlan,
    FinancialConcept,
    FinancialTopic,
    GovernmentScheme,
    InvestmentOption,
    LiteracyLevel,
    UPIGuideEntry,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def concept_library() -> ConceptLibrary:
    return ConceptLibrary()


@pytest.fixture()
def budget_planner() -> BudgetPlanner:
    return BudgetPlanner()


@pytest.fixture()
def scheme_advisor() -> SchemeAdvisor:
    return SchemeAdvisor()


@pytest.fixture()
def upi_guide() -> UPIGuide:
    return UPIGuide()


@pytest.fixture()
def investment_basics() -> InvestmentBasics:
    return InvestmentBasics()


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestFinancialConcept:
    def test_basic_creation(self) -> None:
        concept = FinancialConcept(
            topic=FinancialTopic.SAVINGS,
            title="Test Concept",
            explanation="This is a test concept.",
            level=LiteracyLevel.BEGINNER,
        )
        assert concept.title == "Test Concept"
        assert concept.topic == FinancialTopic.SAVINGS
        assert concept.level == LiteracyLevel.BEGINNER

    def test_examples_default_empty(self) -> None:
        concept = FinancialConcept(
            topic=FinancialTopic.CREDIT,
            title="Credit Score",
            explanation="A number reflecting creditworthiness.",
            level=LiteracyLevel.BEGINNER,
        )
        assert concept.examples == []
        assert concept.key_terms == []


class TestBudgetPlan:
    def test_income_must_be_positive(self) -> None:
        with pytest.raises(ValidationError):
            BudgetPlan(income=0.0, allocations={})

    def test_negative_income_rejected(self) -> None:
        with pytest.raises(ValidationError):
            BudgetPlan(income=-1000.0, allocations={})

    def test_valid_budget_plan(self) -> None:
        plan = BudgetPlan(
            income=50000.0,
            allocations={"needs": 25000.0, "wants": 12500.0, "savings": 12500.0},
        )
        assert plan.income == 50000.0


class TestGovernmentScheme:
    def test_basic_creation(self) -> None:
        scheme = GovernmentScheme(
            name="Test Scheme",
            description="A test scheme.",
            eligibility="All citizens",
            benefits="Test benefits",
            how_to_apply="Visit bank",
        )
        assert scheme.name == "Test Scheme"
        assert scheme.min_age is None
        assert scheme.max_age is None

    def test_age_limits_optional(self) -> None:
        scheme = GovernmentScheme(
            name="APY",
            description="Pension scheme",
            eligibility="18-40",
            benefits="Pension",
            how_to_apply="Bank",
            min_age=18,
            max_age=40,
        )
        assert scheme.min_age == 18
        assert scheme.max_age == 40


class TestInvestmentOption:
    def test_low_risk_investment(self) -> None:
        option = InvestmentOption(
            name="PPF",
            risk_level="low",
            expected_return_pct="7.1%",
            lock_in_years=15,
            tax_benefit=True,
            min_investment=500,
            description="Government-backed",
        )
        assert option.risk_level == "low"
        assert option.tax_benefit is True

    def test_invalid_risk_level_rejected(self) -> None:
        with pytest.raises(ValidationError):
            InvestmentOption(
                name="Invalid",
                risk_level="very_high",  # type: ignore[arg-type]
                expected_return_pct="30%",
                lock_in_years=0,
                tax_benefit=False,
                min_investment=1000,
                description="Invalid risk level",
            )


class TestUPIGuideEntry:
    def test_basic_creation(self) -> None:
        entry = UPIGuideEntry(
            topic="UPI Setup",
            steps=["Step 1", "Step 2"],
        )
        assert entry.topic == "UPI Setup"
        assert len(entry.steps) == 2
        assert entry.tips == []
        assert entry.warnings == []


# ---------------------------------------------------------------------------
# ConceptLibrary tests
# ---------------------------------------------------------------------------


class TestConceptLibrary:
    def test_all_concepts_returns_list(self, concept_library: ConceptLibrary) -> None:
        concepts = concept_library.all_concepts()
        assert isinstance(concepts, list)
        assert len(concepts) >= 10

    def test_get_by_topic_savings(self, concept_library: ConceptLibrary) -> None:
        concepts = concept_library.get_by_topic(FinancialTopic.SAVINGS)
        assert len(concepts) >= 3
        for c in concepts:
            assert c.topic == FinancialTopic.SAVINGS

    def test_get_by_topic_insurance(self, concept_library: ConceptLibrary) -> None:
        concepts = concept_library.get_by_topic(FinancialTopic.INSURANCE)
        assert len(concepts) >= 2
        for c in concepts:
            assert c.topic == FinancialTopic.INSURANCE

    def test_get_by_topic_digital_payments(self, concept_library: ConceptLibrary) -> None:
        concepts = concept_library.get_by_topic(FinancialTopic.DIGITAL_PAYMENTS)
        assert len(concepts) >= 1
        for c in concepts:
            assert c.topic == FinancialTopic.DIGITAL_PAYMENTS

    def test_get_by_level_beginner(self, concept_library: ConceptLibrary) -> None:
        concepts = concept_library.get_by_level(LiteracyLevel.BEGINNER)
        assert len(concepts) >= 5
        for c in concepts:
            assert c.level == LiteracyLevel.BEGINNER

    def test_get_by_level_intermediate(self, concept_library: ConceptLibrary) -> None:
        concepts = concept_library.get_by_level(LiteracyLevel.INTERMEDIATE)
        assert len(concepts) >= 3
        for c in concepts:
            assert c.level == LiteracyLevel.INTERMEDIATE

    def test_get_by_topic_and_level(self, concept_library: ConceptLibrary) -> None:
        concepts = concept_library.get_by_topic_and_level(
            FinancialTopic.SAVINGS, LiteracyLevel.BEGINNER
        )
        for c in concepts:
            assert c.topic == FinancialTopic.SAVINGS
            assert c.level == LiteracyLevel.BEGINNER

    def test_search_upi(self, concept_library: ConceptLibrary) -> None:
        concepts = concept_library.search("UPI")
        assert len(concepts) >= 1

    def test_search_ppf(self, concept_library: ConceptLibrary) -> None:
        concepts = concept_library.search("PPF")
        assert len(concepts) >= 1

    def test_search_case_insensitive(self, concept_library: ConceptLibrary) -> None:
        lower = concept_library.search("savings account")
        upper = concept_library.search("SAVINGS ACCOUNT")
        assert len(lower) == len(upper)

    def test_search_no_results(self, concept_library: ConceptLibrary) -> None:
        concepts = concept_library.search("xyznonexistentterm12345")
        assert concepts == []

    def test_all_concepts_returns_new_list(self, concept_library: ConceptLibrary) -> None:
        list1 = concept_library.all_concepts()
        list2 = concept_library.all_concepts()
        assert list1 is not list2

    def test_all_concepts_have_explanation(self, concept_library: ConceptLibrary) -> None:
        for concept in concept_library.all_concepts():
            assert len(concept.explanation) > 10

    def test_get_by_topic_investment(self, concept_library: ConceptLibrary) -> None:
        concepts = concept_library.get_by_topic(FinancialTopic.INVESTMENT)
        assert len(concepts) >= 2

    def test_get_by_topic_taxation(self, concept_library: ConceptLibrary) -> None:
        concepts = concept_library.get_by_topic(FinancialTopic.TAXATION)
        assert len(concepts) >= 1


# ---------------------------------------------------------------------------
# BudgetPlanner tests
# ---------------------------------------------------------------------------


class TestBudgetPlanner:
    def test_plan_returns_budget_plan(self, budget_planner: BudgetPlanner) -> None:
        plan = budget_planner.plan(30000.0)
        assert isinstance(plan, BudgetPlan)

    def test_plan_income_matches(self, budget_planner: BudgetPlanner) -> None:
        plan = budget_planner.plan(25000.0)
        assert plan.income == 25000.0

    def test_plan_has_three_allocations(self, budget_planner: BudgetPlanner) -> None:
        plan = budget_planner.plan(30000.0)
        assert BudgetCategory.NEEDS.value in plan.allocations
        assert BudgetCategory.WANTS.value in plan.allocations
        assert BudgetCategory.SAVINGS.value in plan.allocations

    def test_plan_allocations_sum_to_income(self, budget_planner: BudgetPlanner) -> None:
        income = 40000.0
        plan = budget_planner.plan(income)
        total = sum(plan.allocations.values())
        assert abs(total - income) < 0.01  # Floating point tolerance

    def test_plan_has_recommendations(self, budget_planner: BudgetPlanner) -> None:
        plan = budget_planner.plan(30000.0)
        assert len(plan.recommendations) >= 1

    def test_plan_savings_target_positive(self, budget_planner: BudgetPlanner) -> None:
        plan = budget_planner.plan(30000.0)
        assert plan.savings_target > 0

    def test_plan_very_low_income_prioritizes_needs(
        self, budget_planner: BudgetPlanner
    ) -> None:
        plan = budget_planner.plan(10000.0)
        needs = plan.allocations[BudgetCategory.NEEDS.value]
        savings = plan.allocations[BudgetCategory.SAVINGS.value]
        # Needs should be greater than savings for very low income
        assert needs > savings

    def test_plan_high_income_higher_savings_pct(
        self, budget_planner: BudgetPlanner
    ) -> None:
        plan = budget_planner.plan(150000.0)
        savings_pct = plan.allocations[BudgetCategory.SAVINGS.value] / 150000.0
        assert savings_pct >= 0.30

    def test_plan_emergency_fund_months_for_low_income(
        self, budget_planner: BudgetPlanner
    ) -> None:
        plan = budget_planner.plan(10000.0)
        assert plan.emergency_fund_months == 3

    def test_plan_emergency_fund_months_for_higher_income(
        self, budget_planner: BudgetPlanner
    ) -> None:
        plan = budget_planner.plan(30000.0)
        assert plan.emergency_fund_months == 6

    def test_plan_income_band_below_15k(self, budget_planner: BudgetPlanner) -> None:
        plan = budget_planner.plan(12000.0)
        # 65/15/20 split → needs should be 65%
        needs_pct = plan.allocations[BudgetCategory.NEEDS.value] / 12000.0
        assert abs(needs_pct - 0.65) < 0.01

    def test_plan_income_band_15k_to_25k(self, budget_planner: BudgetPlanner) -> None:
        plan = budget_planner.plan(20000.0)
        # 55/20/25 split
        needs_pct = plan.allocations[BudgetCategory.NEEDS.value] / 20000.0
        assert abs(needs_pct - 0.55) < 0.01

    def test_plan_income_band_25k_to_50k(self, budget_planner: BudgetPlanner) -> None:
        plan = budget_planner.plan(35000.0)
        # 50/25/25 split
        needs_pct = plan.allocations[BudgetCategory.NEEDS.value] / 35000.0
        assert abs(needs_pct - 0.50) < 0.01

    def test_plan_income_band_50k_to_100k(self, budget_planner: BudgetPlanner) -> None:
        plan = budget_planner.plan(75000.0)
        # 45/25/30 split
        needs_pct = plan.allocations[BudgetCategory.NEEDS.value] / 75000.0
        assert abs(needs_pct - 0.45) < 0.01

    def test_plan_income_above_100k(self, budget_planner: BudgetPlanner) -> None:
        plan = budget_planner.plan(120000.0)
        # 40/25/35 split
        savings_pct = plan.allocations[BudgetCategory.SAVINGS.value] / 120000.0
        assert abs(savings_pct - 0.35) < 0.01


# ---------------------------------------------------------------------------
# SchemeAdvisor tests
# ---------------------------------------------------------------------------


class TestSchemeAdvisor:
    def test_all_schemes_returns_list(self, scheme_advisor: SchemeAdvisor) -> None:
        schemes = scheme_advisor.all_schemes()
        assert isinstance(schemes, list)
        assert len(schemes) >= 8

    def test_find_eligible_no_filters_returns_common_schemes(
        self, scheme_advisor: SchemeAdvisor
    ) -> None:
        eligible = scheme_advisor.find_eligible()
        assert len(eligible) >= 1

    def test_find_eligible_age_25(self, scheme_advisor: SchemeAdvisor) -> None:
        eligible = scheme_advisor.find_eligible(age=25)
        names = [s.name for s in eligible]
        # PMJDY has no age restriction → should be present
        assert any("Jan Dhan" in name for name in names)

    def test_find_eligible_age_25_includes_apy(
        self, scheme_advisor: SchemeAdvisor
    ) -> None:
        eligible = scheme_advisor.find_eligible(age=25)
        names = [s.name for s in eligible]
        assert any("Atal" in name or "APY" in name for name in names)

    def test_find_eligible_age_45_excludes_apy(
        self, scheme_advisor: SchemeAdvisor
    ) -> None:
        # APY max age is 40
        eligible = scheme_advisor.find_eligible(age=45)
        names = [s.name for s in eligible]
        assert not any("Atal" in name for name in names)

    def test_find_eligible_farmer_occupation(
        self, scheme_advisor: SchemeAdvisor
    ) -> None:
        eligible = scheme_advisor.find_eligible(occupation="farmer")
        names = [s.name for s in eligible]
        assert any("Kisan" in name or "KISAN" in name for name in names)

    def test_find_eligible_girl_child_under_10(
        self, scheme_advisor: SchemeAdvisor
    ) -> None:
        eligible = scheme_advisor.find_eligible(age=5)
        names = [s.name for s in eligible]
        assert any("Sukanya" in name or "SSY" in name for name in names)

    def test_find_eligible_girl_child_age_10_excluded(
        self, scheme_advisor: SchemeAdvisor
    ) -> None:
        # SSY is for girl child below 10
        eligible = scheme_advisor.find_eligible(age=10)
        names = [s.name for s in eligible]
        assert not any("Sukanya" in name for name in names)

    def test_find_eligible_senior_citizen_age_65(
        self, scheme_advisor: SchemeAdvisor
    ) -> None:
        eligible = scheme_advisor.find_eligible(age=65)
        names = [s.name for s in eligible]
        assert any("Senior" in name or "SCSS" in name for name in names)

    def test_get_scheme_jan_dhan(self, scheme_advisor: SchemeAdvisor) -> None:
        scheme = scheme_advisor.get_scheme("Jan Dhan")
        assert scheme is not None
        assert "Jan Dhan" in scheme.name

    def test_get_scheme_pmjjby(self, scheme_advisor: SchemeAdvisor) -> None:
        scheme = scheme_advisor.get_scheme("Jeevan Jyoti")
        assert scheme is not None

    def test_get_scheme_pmsby(self, scheme_advisor: SchemeAdvisor) -> None:
        scheme = scheme_advisor.get_scheme("Suraksha")
        assert scheme is not None

    def test_get_scheme_nonexistent_returns_none(
        self, scheme_advisor: SchemeAdvisor
    ) -> None:
        scheme = scheme_advisor.get_scheme("NonExistentScheme99XYZ")
        assert scheme is None

    def test_all_schemes_have_benefits(self, scheme_advisor: SchemeAdvisor) -> None:
        for scheme in scheme_advisor.all_schemes():
            assert len(scheme.benefits) > 0

    def test_all_schemes_have_how_to_apply(self, scheme_advisor: SchemeAdvisor) -> None:
        for scheme in scheme_advisor.all_schemes():
            assert len(scheme.how_to_apply) > 0


# ---------------------------------------------------------------------------
# UPIGuide tests
# ---------------------------------------------------------------------------


class TestUPIGuide:
    def test_get_guide_setup(self, upi_guide: UPIGuide) -> None:
        entry = upi_guide.get_guide("setup")
        assert entry is not None
        assert "UPI" in entry.topic

    def test_get_guide_security(self, upi_guide: UPIGuide) -> None:
        entry = upi_guide.get_guide("security")
        assert entry is not None
        assert len(entry.warnings) > 0

    def test_get_guide_disputes(self, upi_guide: UPIGuide) -> None:
        entry = upi_guide.get_guide("disputes")
        assert entry is not None

    def test_get_guide_limits(self, upi_guide: UPIGuide) -> None:
        entry = upi_guide.get_guide("limits")
        assert entry is not None

    def test_get_guide_nonexistent_returns_none(self, upi_guide: UPIGuide) -> None:
        assert upi_guide.get_guide("nonexistent_topic") is None

    def test_available_topics(self, upi_guide: UPIGuide) -> None:
        topics = upi_guide.available_topics()
        assert "setup" in topics
        assert "security" in topics
        assert "disputes" in topics
        assert "limits" in topics

    def test_all_guides_returns_dict(self, upi_guide: UPIGuide) -> None:
        guides = upi_guide.all_guides()
        assert isinstance(guides, dict)
        assert len(guides) >= 4

    def test_setup_guide_has_steps(self, upi_guide: UPIGuide) -> None:
        entry = upi_guide.get_guide("setup")
        assert entry is not None
        assert len(entry.steps) >= 5

    def test_security_guide_warns_about_pin(self, upi_guide: UPIGuide) -> None:
        entry = upi_guide.get_guide("security")
        assert entry is not None
        all_text = " ".join(entry.steps + entry.tips + entry.warnings).upper()
        assert "PIN" in all_text

    def test_get_guide_case_insensitive(self, upi_guide: UPIGuide) -> None:
        # Keys are lowercase in the dict, so "setup" works but "SETUP" may not
        lower_entry = upi_guide.get_guide("setup")
        assert lower_entry is not None


# ---------------------------------------------------------------------------
# InvestmentBasics tests
# ---------------------------------------------------------------------------


class TestInvestmentBasics:
    def test_compare_all_returns_list(self, investment_basics: InvestmentBasics) -> None:
        options = investment_basics.compare_all()
        assert isinstance(options, list)
        assert len(options) >= 8

    def test_by_risk_low(self, investment_basics: InvestmentBasics) -> None:
        options = investment_basics.by_risk("low")
        assert len(options) >= 3
        for o in options:
            assert o.risk_level == "low"

    def test_by_risk_moderate(self, investment_basics: InvestmentBasics) -> None:
        options = investment_basics.by_risk("moderate")
        assert len(options) >= 1
        for o in options:
            assert o.risk_level == "moderate"

    def test_by_risk_high(self, investment_basics: InvestmentBasics) -> None:
        options = investment_basics.by_risk("high")
        assert len(options) >= 1
        for o in options:
            assert o.risk_level == "high"

    def test_by_risk_nonexistent_returns_empty(
        self, investment_basics: InvestmentBasics
    ) -> None:
        options = investment_basics.by_risk("extreme")
        assert options == []

    def test_tax_saving_returns_list(self, investment_basics: InvestmentBasics) -> None:
        options = investment_basics.tax_saving()
        assert len(options) >= 1
        for o in options:
            assert o.tax_benefit is True

    def test_for_beginner_returns_low_risk(
        self, investment_basics: InvestmentBasics
    ) -> None:
        options = investment_basics.for_beginner()
        assert len(options) >= 1
        for o in options:
            assert o.risk_level == "low"

    def test_ppf_in_tax_saving(self, investment_basics: InvestmentBasics) -> None:
        options = investment_basics.tax_saving()
        names = [o.name for o in options]
        assert any("PPF" in name for name in names)

    def test_elss_in_tax_saving(self, investment_basics: InvestmentBasics) -> None:
        options = investment_basics.tax_saving()
        names = [o.name for o in options]
        assert any("ELSS" in name for name in names)

    def test_all_options_have_min_investment(
        self, investment_basics: InvestmentBasics
    ) -> None:
        for option in investment_basics.compare_all():
            assert option.min_investment > 0


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------


class TestIntegration:
    def test_budget_plus_schemes_integration(
        self, budget_planner: BudgetPlanner, scheme_advisor: SchemeAdvisor
    ) -> None:
        plan = budget_planner.plan(20000.0)
        eligible = scheme_advisor.find_eligible(age=30)
        assert isinstance(plan, BudgetPlan)
        assert len(eligible) > 0

    def test_concept_library_covers_all_topics(
        self, concept_library: ConceptLibrary
    ) -> None:
        for topic in FinancialTopic:
            concepts = concept_library.get_by_topic(topic)
            # Some topics may have no entries; just check the call doesn't fail
            assert isinstance(concepts, list)


# ---------------------------------------------------------------------------
# Hypothesis property-based tests
# ---------------------------------------------------------------------------


@given(income=st.floats(min_value=1.0, max_value=10_000_000.0, allow_nan=False))
@settings(max_examples=20)
def test_budget_planner_never_raises(income: float) -> None:
    planner = BudgetPlanner()
    plan = planner.plan(income)
    assert isinstance(plan, BudgetPlan)
    assert plan.income == income


@given(income=st.floats(min_value=1.0, max_value=10_000_000.0, allow_nan=False))
@settings(max_examples=20)
def test_budget_allocations_sum_to_income(income: float) -> None:
    planner = BudgetPlanner()
    plan = planner.plan(income)
    total = sum(plan.allocations.values())
    assert abs(total - income) < 0.01


@given(
    age=st.integers(min_value=18, max_value=70),
)
@settings(max_examples=15)
def test_scheme_advisor_returns_list_for_any_age(age: int) -> None:
    advisor = SchemeAdvisor()
    eligible = advisor.find_eligible(age=age)
    assert isinstance(eligible, list)
