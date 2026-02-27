"""aumai-dhansetu quickstart examples.

Run this file directly to verify your installation and explore the API:

    python examples/quickstart.py

Each demo function is independent and can be run or imported separately.

DISCLAIMER: This file is for educational and demonstration purposes only.
Interest rates and scheme details are indicative. This does not constitute
financial advice. Verify all information with official sources.
"""

from __future__ import annotations

from aumai_dhansetu.core import (
    BudgetPlanner,
    ConceptLibrary,
    InvestmentBasics,
    SchemeAdvisor,
    UPIGuide,
)
from aumai_dhansetu.models import FinancialTopic, LiteracyLevel


def demo_concept_library() -> None:
    """Demonstrate the financial concept library.

    Shows how to browse, filter, and search the built-in financial
    literacy content across topics and difficulty levels.
    """
    print("=" * 60)
    print("DEMO 1: Financial Concept Library")
    print("=" * 60)

    library = ConceptLibrary()

    # Count and display total concepts
    all_concepts = library.all_concepts()
    print(f"\nTotal concepts in library: {len(all_concepts)}")

    # Display all topic + level combinations
    print("\nConcepts by topic and level:")
    for topic in FinancialTopic:
        for level in LiteracyLevel:
            concepts = library.get_by_topic_and_level(topic, level)
            if concepts:
                names = ", ".join(c.title for c in concepts)
                print(f"  [{topic.value} / {level.value}]: {names}")

    # Keyword search
    print("\nSearch results for 'SIP':")
    for concept in library.search("SIP"):
        print(f"  - {concept.title} [{concept.level.value}]")
        print(f"    {concept.explanation[:100]}...")

    # Display a complete concept
    print("\nFull concept detail: 'PM Jeevan Jyoti Bima Yojana'")
    results = library.search("PMJJBY")
    if results:
        c = results[0]
        print(f"  Title: {c.title}")
        print(f"  Topic: {c.topic.value} | Level: {c.level.value}")
        print(f"  {c.explanation}")
        print(f"  Examples: {', '.join(c.examples)}")
        print(f"  Key terms: {', '.join(c.key_terms)}")


def demo_budget_planner() -> None:
    """Demonstrate the budget planner across different income levels.

    Shows how the 50/30/20 rule adapts to different income bands
    and generates personalised recommendations.
    """
    print("\n" + "=" * 60)
    print("DEMO 2: Budget Planner")
    print("=" * 60)

    planner = BudgetPlanner()

    # Show how allocations change across income bands
    income_examples = [
        (12_000, "Low income (informal worker)"),
        (22_000, "Entry-level salaried"),
        (40_000, "Mid-level salaried"),
        (75_000, "Senior professional"),
        (1_50_000, "High income"),
    ]

    print(f"\n{'Income':>12}  {'Needs%':>7}  {'Wants%':>7}  {'Savings%':>9}")
    print("-" * 45)
    for income, label in income_examples:
        plan = planner.plan(income)
        needs_pct = (plan.allocations["needs"] / income) * 100
        wants_pct = (plan.allocations["wants"] / income) * 100
        savings_pct = (plan.savings_target / income) * 100
        print(f"Rs {income:>8,}  {needs_pct:>6.0f}%  {wants_pct:>6.0f}%  {savings_pct:>8.0f}%  # {label}")

    # Detailed plan for Rs 35,000/month
    print("\nDetailed budget plan for Rs 35,000/month:")
    plan = planner.plan(35_000)
    print(f"  Needs   : Rs {plan.allocations['needs']:>8,.0f}/month")
    print(f"  Wants   : Rs {plan.allocations['wants']:>8,.0f}/month")
    print(f"  Savings : Rs {plan.savings_target:>8,.0f}/month")
    print(f"  Emergency fund goal: {plan.emergency_fund_months} months = Rs {plan.allocations['needs'] * plan.emergency_fund_months:,.0f}")
    print("\n  Personalised recommendations:")
    for i, rec in enumerate(plan.recommendations, 1):
        print(f"  {i}. {rec}")


def demo_scheme_advisor() -> None:
    """Demonstrate government scheme eligibility matching.

    Shows how to discover central government schemes based on
    age and occupation profile.
    """
    print("\n" + "=" * 60)
    print("DEMO 3: Government Scheme Advisor")
    print("=" * 60)

    advisor = SchemeAdvisor()

    # Total scheme count
    all_schemes = advisor.all_schemes()
    print(f"\nSchemes in database: {len(all_schemes)}")

    # Profile-based matching
    profiles = [
        {"label": "25-year-old unbanked person", "age": 25, "occupation": "unbanked"},
        {"label": "40-year-old farmer", "age": 40, "occupation": "farmer"},
        {"label": "30-year-old salaried employee", "age": 30, "occupation": "salaried"},
        {"label": "62-year-old retiree", "age": 62, "occupation": ""},
        {"label": "8-year-old girl child", "age": 8, "occupation": ""},
    ]

    for profile in profiles:
        eligible = advisor.find_eligible(
            age=profile["age"],
            occupation=profile.get("occupation"),
        )
        print(f"\n{profile['label']}: {len(eligible)} eligible scheme(s)")
        for scheme in eligible:
            print(f"  - {scheme.name}")

    # Deep-dive on one scheme
    print("\nFull details: PM Suraksha Bima Yojana")
    scheme = advisor.get_scheme("Suraksha Bima")
    if scheme:
        print(f"  Description: {scheme.description}")
        print(f"  Eligibility: {scheme.eligibility}")
        print(f"  Benefits:    {scheme.benefits}")
        print(f"  Apply via:   {scheme.how_to_apply}")
        print(f"  Ministry:    {scheme.ministry}")


def demo_upi_guide() -> None:
    """Demonstrate the UPI guidance system.

    Shows setup steps, security warnings, and dispute resolution
    steps — the most commonly needed UPI guidance.
    """
    print("\n" + "=" * 60)
    print("DEMO 4: UPI Guide")
    print("=" * 60)

    guide = UPIGuide()

    print(f"\nAvailable UPI guide topics: {guide.available_topics()}")

    # Display security guide (most important for fraud prevention)
    print("\n--- UPI SECURITY GUIDE ---")
    security = guide.get_guide("security")
    if security:
        print(f"Topic: {security.topic}")
        print("\nSteps:")
        for step in security.steps:
            print(f"  {step}")
        print("\nFraud warnings:")
        for warning in security.warnings:
            print(f"  !! {warning}")
        print("\nSafety tips:")
        for tip in security.tips:
            print(f"  * {tip}")

    # UPI limits summary
    print("\n--- UPI TRANSACTION LIMITS ---")
    limits = guide.get_guide("limits")
    if limits:
        for step in limits.steps[:4]:  # First 4 are the main limits
            print(f"  {step}")


def demo_investment_basics() -> None:
    """Demonstrate investment option comparison.

    Shows how to compare instruments by risk level and identify
    tax-saving options for Section 80C planning.
    """
    print("\n" + "=" * 60)
    print("DEMO 5: Investment Basics")
    print("=" * 60)

    basics = InvestmentBasics()

    # Complete comparison table
    all_options = basics.compare_all()
    print(f"\nTotal instruments in catalogue: {len(all_options)}")
    print()
    print(f"{'Instrument':<32} {'Risk':<10} {'Return':<12} {'Lock-in':<10} {'80C'}")
    print("-" * 75)
    for opt in sorted(all_options, key=lambda o: (o.risk_level, o.name)):
        lock = f"{opt.lock_in_years}yr" if opt.lock_in_years > 0 else "None"
        tax = "Yes" if opt.tax_benefit else "No"
        print(f"{opt.name:<32} {opt.risk_level:<10} {opt.expected_return_pct:<12} {lock:<10} {tax}")

    # Beginner-safe options
    print("\nRecommended for first-time investors (low risk only):")
    for opt in basics.for_beginner():
        print(f"  {opt.name}: minimum Rs {opt.min_investment:,.0f}")
        print(f"    {opt.description}")

    # Tax-saving summary
    tax_options = basics.tax_saving()
    print(f"\nSection 80C eligible options ({len(tax_options)} total):")
    print("  (Up to Rs 1,50,000 deductible per financial year under old regime)")
    for opt in tax_options:
        lock = f"{opt.lock_in_years}yr lock-in" if opt.lock_in_years > 0 else "No lock-in"
        print(f"  {opt.name}: {opt.expected_return_pct} expected, {lock}")


def main() -> None:
    """Run all five demos in sequence."""
    print("\naumai-dhansetu Quickstart Demo")
    print("Financial Literacy AI for India")
    print()
    print("DISCLAIMER: For educational purposes only. Not financial advice.")
    print("Verify all figures with official sources before making decisions.")

    demo_concept_library()
    demo_budget_planner()
    demo_scheme_advisor()
    demo_upi_guide()
    demo_investment_basics()

    print("\n" + "=" * 60)
    print("All demos completed successfully.")
    print("See docs/getting-started.md for detailed tutorials.")
    print("=" * 60)


if __name__ == "__main__":
    main()
