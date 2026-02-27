# Getting Started with aumai-dhansetu

> **DISCLAIMER:** aumai-dhansetu is for financial education only. It does NOT provide SEBI-registered investment advice. Verify all figures with official sources before making financial decisions.

---

## Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.11 or higher |
| pip | 22.0 or higher recommended |
| Operating System | Linux, macOS, or Windows |
| Internet connection | Required only for installation; the package runs fully offline |

Check your Python version:

```bash
python --version
# Python 3.11.x or 3.12.x
```

---

## Installation

### Option 1: Install from PyPI (recommended)

```bash
pip install aumai-dhansetu
```

Verify the installation:

```bash
dhansetu --version
# aumai-dhansetu, version 0.1.0
```

### Option 2: Install from source

```bash
git clone https://github.com/aumai-org/aumai-dhansetu.git
cd aumai-dhansetu
pip install -e ".[dev]"
```

The `[dev]` extra installs pytest, ruff, mypy, and hypothesis for running tests.

### Virtual environment (recommended)

Always use a virtual environment to avoid dependency conflicts:

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows

pip install aumai-dhansetu
```

---

## Step-by-Step Tutorial

This tutorial walks you through the five main capabilities of aumai-dhansetu.

### Step 1: Explore financial concepts

Start by looking at what concepts are available at the beginner level:

```bash
dhansetu learn --level beginner
```

You will see concepts like "Savings Account", "UPI", "Term Life Insurance", "Credit Score (CIBIL)", and "Income Tax Basics" — all explained in plain language.

Now try filtering to a specific topic:

```bash
dhansetu learn --topic savings
```

If you want to search for something specific:

```bash
dhansetu learn --search "PPF"
dhansetu learn --search "mutual fund"
```

In Python:

```python
from aumai_dhansetu.core import ConceptLibrary
from aumai_dhansetu.models import FinancialTopic, LiteracyLevel

library = ConceptLibrary()

# All concepts about insurance
for concept in library.get_by_topic(FinancialTopic.INSURANCE):
    print(f"[{concept.level.value}] {concept.title}")
    print(f"  {concept.explanation[:120]}...\n")
```

### Step 2: Build your budget plan

Enter your monthly take-home income (after tax):

```bash
dhansetu budget --income 30000
```

The output shows you exactly how much to allocate to needs, wants, and savings — adjusted for your income level. At Rs 30,000/month you will see a 50/25/25 split with recommendations to start an index fund SIP and build an emergency fund.

Try different income levels to see how the recommendations change:

```bash
dhansetu budget --income 12000   # Low income: conservative plan
dhansetu budget --income 75000   # Mid income: growth focus
dhansetu budget --income 150000  # High income: diversification
```

In Python:

```python
from aumai_dhansetu.core import BudgetPlanner

planner = BudgetPlanner()
plan = planner.plan(30_000)

print(f"Needs:   Rs {plan.allocations['needs']:,.0f}/month")
print(f"Wants:   Rs {plan.allocations['wants']:,.0f}/month")
print(f"Savings: Rs {plan.savings_target:,.0f}/month")
print(f"Build emergency fund of: {plan.emergency_fund_months} months")
print()
for recommendation in plan.recommendations:
    print(f"  * {recommendation}")
```

### Step 3: Find government schemes you qualify for

Provide your age and occupation to get matched to relevant central government schemes:

```bash
# A 30-year-old salaried employee
dhansetu schemes --age 30

# A 45-year-old farmer
dhansetu schemes --age 45 --occupation farmer

# A 65-year-old retiree
dhansetu schemes --age 65
```

Each result shows the scheme name, description, benefits, eligibility, and exact steps to apply. Many people are surprised to find they qualify for PMJJBY (Rs 2 lakh life cover for Rs 436/year) or PMSBY (Rs 2 lakh accident cover for just Rs 20/year).

In Python:

```python
from aumai_dhansetu.core import SchemeAdvisor

advisor = SchemeAdvisor()

# Check eligibility
schemes = advisor.find_eligible(age=30, occupation="farmer")
print(f"You qualify for {len(schemes)} schemes:\n")
for scheme in schemes:
    print(f"  {scheme.name}")
    print(f"    Benefits: {scheme.benefits}")
    print(f"    Apply at: {scheme.how_to_apply}\n")

# Look up a specific scheme by name
pmjjby = advisor.get_scheme("PMJJBY")
if pmjjby:
    print(f"Annual premium: see benefits field")
    print(f"Benefits: {pmjjby.benefits}")
```

### Step 4: Use UPI safely

If you are new to UPI or want to guide someone who is, start with the setup guide:

```bash
dhansetu upi --topic setup
```

Follow the 7-step guide to create a UPI ID from scratch. Then read the security guide — this is the most important one:

```bash
dhansetu upi --topic security
```

Key warnings that the security guide highlights:
- Banks **never** call asking for your UPI PIN or OTP
- You **never** need to enter your PIN or scan a QR code to **receive** money
- Collect requests from unknown numbers are almost always scams

If a payment fails or goes wrong:

```bash
dhansetu upi --topic disputes
```

In Python:

```python
from aumai_dhansetu.core import UPIGuide

guide = UPIGuide()

# All available topics
print("Available guides:", guide.available_topics())

# Get and display the security guide
security = guide.get_guide("security")
print(f"\n{security.topic}")
print("Steps:")
for step in security.steps:
    print(f"  {step}")
print("Warnings (critical):")
for warning in security.warnings:
    print(f"  !! {warning}")
```

### Step 5: Compare investment options

View all options and compare:

```bash
dhansetu invest
```

For a first-time investor, start with low-risk options:

```bash
dhansetu invest --risk low
```

If you pay income tax and want to reduce your tax bill:

```bash
dhansetu invest --tax-saving
```

This shows all options eligible under Section 80C (PPF, ELSS, SSY, NPS), helping you choose how to use your Rs 1.5 lakh annual deduction limit.

In Python:

```python
from aumai_dhansetu.core import InvestmentBasics

basics = InvestmentBasics()

# Best starting point for new investors
print("Beginner-safe options (low risk):")
for opt in basics.for_beginner():
    lock = f"{opt.lock_in_years}yr" if opt.lock_in_years > 0 else "No lock-in"
    print(f"  {opt.name}: {opt.expected_return_pct} | {lock} | Rs {opt.min_investment:,.0f} min")

# Tax-saving breakdown
print("\nSection 80C eligible options:")
for opt in basics.tax_saving():
    print(f"  {opt.name}: {opt.expected_return_pct} returns, {opt.lock_in_years}yr lock-in")
```

---

## Common Patterns and Recipes

### Recipe 1: Financial health check for a household

Run a complete financial health assessment in one script:

```python
from aumai_dhansetu.core import BudgetPlanner, SchemeAdvisor, InvestmentBasics

monthly_income = 28_000
age = 32
occupation = "salaried"

# Step 1: Budget
planner = BudgetPlanner()
plan = planner.plan(monthly_income)
print(f"Monthly savings capacity: Rs {plan.savings_target:,.0f}")

# Step 2: Schemes they might be missing
advisor = SchemeAdvisor()
schemes = advisor.find_eligible(age=age, occupation=occupation)
high_value = [s for s in schemes if "2 lakh" in s.benefits or "6,000" in s.benefits]
print(f"\nHigh-value schemes to enroll in: {len(high_value)}")
for s in high_value:
    print(f"  {s.name}")

# Step 3: Where to put the savings
basics = InvestmentBasics()
safe_options = basics.for_beginner()
print(f"\nSafe places for savings: {len(safe_options)}")
for opt in safe_options[:3]:
    print(f"  {opt.name}: {opt.expected_return_pct}")
```

### Recipe 2: Export full concept library as JSON

For building a chatbot, training data, or feeding into a knowledge base:

```python
import json
from aumai_dhansetu.core import ConceptLibrary

library = ConceptLibrary()
concepts = library.all_concepts()

data = [concept.model_dump() for concept in concepts]
with open("dhansetu_concepts.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Exported {len(data)} concepts to dhansetu_concepts.json")
```

### Recipe 3: Budget planner as a web API response

```python
import json
from aumai_dhansetu.core import BudgetPlanner

def budget_api_response(monthly_income: float) -> str:
    """Generate a JSON response suitable for a REST API."""
    planner = BudgetPlanner()
    plan = planner.plan(monthly_income)
    return plan.model_dump_json(indent=2)

# FastAPI example
# @app.get("/budget")
# def get_budget(income: float) -> dict:
#     planner = BudgetPlanner()
#     return planner.plan(income).model_dump()
```

### Recipe 4: Scheme eligibility CSV export

```python
import csv
from aumai_dhansetu.core import SchemeAdvisor

advisor = SchemeAdvisor()
all_schemes = advisor.all_schemes()

with open("schemes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["name", "ministry", "eligibility", "benefits", "how_to_apply"],
    )
    writer.writeheader()
    for scheme in all_schemes:
        writer.writerow({
            "name": scheme.name,
            "ministry": scheme.ministry,
            "eligibility": scheme.eligibility,
            "benefits": scheme.benefits,
            "how_to_apply": scheme.how_to_apply,
        })
print(f"Exported {len(all_schemes)} schemes to schemes.csv")
```

### Recipe 5: UPI fraud awareness training data

Extract all UPI warnings and tips for awareness campaigns:

```python
from aumai_dhansetu.core import UPIGuide

guide = UPIGuide()
all_guides = guide.all_guides()

print("=== UPI FRAUD AWARENESS CONTENT ===\n")
for topic_key, entry in all_guides.items():
    if entry.warnings:
        print(f"Topic: {entry.topic}")
        for warning in entry.warnings:
            print(f"  DANGER: {warning}")
    if entry.tips:
        for tip in entry.tips:
            print(f"  TIP: {tip}")
    print()
```

---

## Troubleshooting FAQ

**Q: `dhansetu: command not found` after installation**

Make sure your Python scripts directory is on your PATH. On Linux/macOS:
```bash
export PATH="$HOME/.local/bin:$PATH"
```
Or use `python -m aumai_dhansetu.cli` as an alternative.

**Q: `ModuleNotFoundError: No module named 'aumai_dhansetu'`**

You may have multiple Python environments. Install into the active environment:
```bash
which python          # Confirm the Python being used
pip install aumai-dhansetu
```

**Q: The interest rates shown seem out of date**

The rates are indicative and embedded in the package source. They reflect rates at the time of the last package release. For current rates, always check:
- PPF rate: rbi.org.in
- FD rates: your specific bank's website
- SSY/SCSS rates: indiapost.gov.in
- Tax slabs: incometax.gov.in

**Q: A government scheme I know about is not listed**

The built-in database covers 10 major central government schemes. State schemes and newer schemes may not be included. You can add schemes at runtime (see Configuration section in README.md). To propose additions to the package, open an issue on GitHub with the official scheme URL.

**Q: Can I use dhansetu in a multilingual (Hindi/Tamil/Bengali) app?**

The package content is in English. All Pydantic models support UTF-8 strings, so you can create custom `FinancialConcept` objects with content in any language. The JSON output (`--json-output`) is UTF-8 with `ensure_ascii=False`, so regional script characters are preserved.

**Q: Is there a rate limit or quota on usage?**

No. aumai-dhansetu is fully offline and runs entirely in-process. There are no external API calls, no rate limits, and no usage quotas.

**Q: The `schemes` command shows schemes I am not actually eligible for**

The eligibility filter is intentionally permissive. It is better to show a scheme you might not qualify for than to silently exclude a benefit you are entitled to. Read the eligibility field carefully and verify with the scheme's official portal.

**Q: How do I run the tests?**

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

**Q: mypy is reporting errors in my code that uses dhansetu**

aumai-dhansetu ships with full type annotations and `py.typed` marker. Ensure you are using mypy 1.0+ and that your `mypy.ini` or `pyproject.toml` has `strict = true`. All public APIs are fully typed.
