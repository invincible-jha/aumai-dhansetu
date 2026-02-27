"""CLI entry point for aumai-dhansetu."""

from __future__ import annotations

import json

import click

from aumai_dhansetu.core import (
    BudgetPlanner,
    ConceptLibrary,
    InvestmentBasics,
    SchemeAdvisor,
    UPIGuide,
)
from aumai_dhansetu.models import FinancialTopic, LiteracyLevel

_DISCLAIMER = (
    "\nIMPORTANT: Interest rates and returns mentioned are indicative and subject to change. "
    "Past performance does not guarantee future results. "
    "This tool does not provide SEBI-registered investment advisory. "
    "Verify all financial information with official sources before making decisions.\n"
)


@click.group()
@click.version_option()
def cli() -> None:
    """AumAI DhanSetu - Financial literacy AI for India."""


@cli.command()
@click.option("--topic", type=click.Choice([t.value for t in FinancialTopic]), help="Financial topic")
@click.option("--level", type=click.Choice([l.value for l in LiteracyLevel]), help="Literacy level")
@click.option("--search", "query", default=None, help="Search by keyword")
@click.option("--json-output", is_flag=True, help="Output as JSON")
def learn(topic: str | None, level: str | None, query: str | None, json_output: bool) -> None:
    """Learn financial concepts by topic and level."""
    library = ConceptLibrary()

    if query:
        concepts = library.search(query)
    elif topic and level:
        concepts = library.get_by_topic_and_level(FinancialTopic(topic), LiteracyLevel(level))
    elif topic:
        concepts = library.get_by_topic(FinancialTopic(topic))
    elif level:
        concepts = library.get_by_level(LiteracyLevel(level))
    else:
        concepts = library.all_concepts()

    if json_output:
        click.echo(json.dumps([c.model_dump() for c in concepts], indent=2, ensure_ascii=False))
        return

    for concept in concepts:
        click.echo(f"\n{'='*60}")
        click.echo(f"  {concept.title}")
        click.echo(f"  Topic: {concept.topic.value} | Level: {concept.level.value}")
        click.echo(f"{'='*60}")
        click.echo(f"\n{concept.explanation}\n")
        if concept.examples:
            click.echo("Examples:")
            for ex in concept.examples:
                click.echo(f"  - {ex}")
        if concept.key_terms:
            click.echo(f"\nKey terms: {', '.join(concept.key_terms)}")

    click.echo(f"\nFound {len(concepts)} concept(s).")
    click.echo(_DISCLAIMER)


@cli.command()
@click.option("--income", required=True, type=float, help="Monthly income in INR")
@click.option("--json-output", is_flag=True, help="Output as JSON")
def budget(income: float, json_output: bool) -> None:
    """Generate a budget plan based on your monthly income."""
    planner = BudgetPlanner()
    plan = planner.plan(income)

    if json_output:
        click.echo(plan.model_dump_json(indent=2))
        return

    click.echo(f"\n{'='*50}")
    click.echo(f"  Budget Plan for Rs {income:,.0f}/month")
    click.echo(f"{'='*50}\n")

    for category, amount in plan.allocations.items():
        pct = (amount / income) * 100
        click.echo(f"  {category.upper():12s}: Rs {amount:>10,.0f}  ({pct:.0f}%)")

    click.echo(f"\n  Savings target: Rs {plan.savings_target:,.0f}/month")
    click.echo(f"  Emergency fund goal: {plan.emergency_fund_months} months of expenses")

    click.echo("\nRecommendations:")
    for i, rec in enumerate(plan.recommendations, 1):
        click.echo(f"  {i}. {rec}")

    click.echo(_DISCLAIMER)


@cli.command()
@click.option("--age", type=int, help="Your age")
@click.option("--income", type=float, help="Annual income in INR")
@click.option("--occupation", type=str, help="Occupation (e.g., farmer, salaried, self-employed)")
@click.option("--json-output", is_flag=True, help="Output as JSON")
def schemes(age: int | None, income: float | None, occupation: str | None, json_output: bool) -> None:
    """Find eligible government financial schemes."""
    advisor = SchemeAdvisor()
    eligible = advisor.find_eligible(age=age, income=income, occupation=occupation)

    if json_output:
        click.echo(json.dumps([s.model_dump() for s in eligible], indent=2, ensure_ascii=False))
        return

    click.echo(f"\nFound {len(eligible)} eligible scheme(s):\n")
    for scheme in eligible:
        click.echo(f"  {'='*55}")
        click.echo(f"  {scheme.name}")
        click.echo(f"  {'='*55}")
        click.echo(f"  {scheme.description}\n")
        click.echo(f"  Eligibility: {scheme.eligibility}")
        click.echo(f"  Benefits: {scheme.benefits}")
        click.echo(f"  How to apply: {scheme.how_to_apply}\n")

    click.echo(_DISCLAIMER)


@cli.command()
@click.option("--topic", type=click.Choice(["setup", "security", "disputes", "limits"]), required=True, help="UPI topic")
def upi(topic: str) -> None:
    """Get UPI guidance on setup, security, disputes, or limits."""
    guide = UPIGuide()
    entry = guide.get_guide(topic)

    if entry is None:
        click.echo(f"Unknown topic: {topic}. Available: {', '.join(guide.available_topics())}")
        return

    click.echo(f"\n{'='*50}")
    click.echo(f"  {entry.topic}")
    click.echo(f"{'='*50}\n")

    for step in entry.steps:
        click.echo(f"  {step}")

    if entry.tips:
        click.echo("\nTips:")
        for tip in entry.tips:
            click.echo(f"  * {tip}")

    if entry.warnings:
        click.echo("\nWarnings:")
        for warn in entry.warnings:
            click.echo(f"  ! {warn}")

    click.echo(_DISCLAIMER)


@cli.command()
@click.option("--risk", type=click.Choice(["low", "moderate", "high"]), help="Filter by risk level")
@click.option("--tax-saving", is_flag=True, help="Show only tax-saving options")
@click.option("--json-output", is_flag=True, help="Output as JSON")
def invest(risk: str | None, tax_saving: bool, json_output: bool) -> None:
    """Compare investment options."""
    basics = InvestmentBasics()

    if tax_saving:
        options = basics.tax_saving()
    elif risk:
        options = basics.by_risk(risk)
    else:
        options = basics.compare_all()

    if json_output:
        click.echo(json.dumps([o.model_dump() for o in options], indent=2, ensure_ascii=False))
        return

    click.echo(f"\n{'Investment':<30s} {'Risk':<10s} {'Return':<10s} {'Lock-in':<10s} {'Tax Benefit':<12s} {'Min Invest'}")
    click.echo("-" * 95)
    for opt in options:
        lock = f"{opt.lock_in_years}yr" if opt.lock_in_years > 0 else "None"
        tax = "Yes (80C)" if opt.tax_benefit else "No"
        click.echo(f"{opt.name:<30s} {opt.risk_level:<10s} {opt.expected_return_pct:<10s} {lock:<10s} {tax:<12s} Rs {opt.min_investment:,.0f}")

    click.echo(_DISCLAIMER)


main = cli

if __name__ == "__main__":
    cli()
