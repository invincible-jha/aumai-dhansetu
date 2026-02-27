# API Reference — aumai-dhansetu

> **DISCLAIMER:** All financial figures, scheme details, and interest rates in this package are indicative and subject to change. This package does not provide SEBI-registered investment advice. Verify all information with official sources before making financial decisions.

---

## Module Overview

```
aumai_dhansetu/
├── __init__.py         — version string only
├── core.py             — ConceptLibrary, BudgetPlanner, SchemeAdvisor, UPIGuide, InvestmentBasics
├── models.py           — Pydantic v2 models and enums
└── cli.py              — Click CLI (entry point: dhansetu)
```

---

## aumai_dhansetu.models

### Enumerations

---

#### `FinancialTopic`

```python
class FinancialTopic(str, Enum):
```

Topic categories for financial literacy concepts.

| Member | Value |
|---|---|
| `SAVINGS` | `"savings"` |
| `INSURANCE` | `"insurance"` |
| `INVESTMENT` | `"investment"` |
| `CREDIT` | `"credit"` |
| `TAXATION` | `"taxation"` |
| `DIGITAL_PAYMENTS` | `"digital_payments"` |

---

#### `LiteracyLevel`

```python
class LiteracyLevel(str, Enum):
```

Difficulty/complexity level for financial concepts.

| Member | Value | Intended audience |
|---|---|---|
| `BEGINNER` | `"beginner"` | No prior financial knowledge |
| `INTERMEDIATE` | `"intermediate"` | Basic banking familiarity |
| `ADVANCED` | `"advanced"` | Comfortable with markets and tax |

---

#### `BudgetCategory`

```python
class BudgetCategory(str, Enum):
```

Budget allocation categories (50/30/20 rule).

| Member | Value |
|---|---|
| `NEEDS` | `"needs"` |
| `WANTS` | `"wants"` |
| `SAVINGS` | `"savings"` |
| `EMI` | `"emi"` |

---

### Pydantic Models

---

#### `FinancialConcept`

```python
class FinancialConcept(BaseModel):
    topic: FinancialTopic
    title: str
    explanation: str
    examples: list[str]          # default: []
    level: LiteracyLevel
    key_terms: list[str]         # default: []
```

A single financial literacy concept with explanation and examples.

**Fields:**

| Field | Type | Description |
|---|---|---|
| `topic` | `FinancialTopic` | Topic category this concept belongs to |
| `title` | `str` | Short display name (e.g., "Public Provident Fund (PPF)") |
| `explanation` | `str` | Plain-language explanation with real-world context |
| `examples` | `list[str]` | Concrete Indian examples (e.g., "1-year FD at 7%") |
| `level` | `LiteracyLevel` | Target literacy level |
| `key_terms` | `list[str]` | Glossary terms introduced in this concept |

**Example:**

```python
from aumai_dhansetu.models import FinancialConcept, FinancialTopic, LiteracyLevel

concept = FinancialConcept(
    topic=FinancialTopic.SAVINGS,
    title="Kisan Vikas Patra",
    explanation="Post Office savings certificate that doubles your money in a fixed period.",
    examples=["Rs 10,000 certificate doubles in 115 months"],
    level=LiteracyLevel.BEGINNER,
    key_terms=["doubling period", "post office", "certificate"],
)
print(concept.model_dump_json(indent=2))
```

---

#### `BudgetPlan`

```python
class BudgetPlan(BaseModel):
    income: float                       # gt=0
    allocations: dict[str, float]       # default: {}
    recommendations: list[str]          # default: []
    savings_target: float               # default: 0.0
    emergency_fund_months: int          # default: 6
```

A monthly budget plan output from `BudgetPlanner.plan()`.

**Fields:**

| Field | Type | Description |
|---|---|---|
| `income` | `float` | Monthly income in INR (must be > 0) |
| `allocations` | `dict[str, float]` | Keys are `BudgetCategory` values; values are INR amounts |
| `recommendations` | `list[str]` | 3 personalised financial recommendations |
| `savings_target` | `float` | Monthly savings amount in INR |
| `emergency_fund_months` | `int` | Recommended emergency fund depth in months (3 or 6) |

**Validation:** `income` has `gt=0` constraint. A `ValidationError` is raised for zero or negative income.

**Example:**

```python
from aumai_dhansetu.core import BudgetPlanner

plan = BudgetPlanner().plan(40_000)
print(plan.income)           # 40000.0
print(plan.allocations)      # {'needs': 20000.0, 'wants': 10000.0, 'savings': 10000.0}
print(plan.savings_target)   # 10000.0
print(plan.emergency_fund_months)  # 6
```

---

#### `GovernmentScheme`

```python
class GovernmentScheme(BaseModel):
    name: str
    description: str
    eligibility: str
    benefits: str
    how_to_apply: str
    ministry: str               # default: ""
    min_age: int | None         # default: None
    max_age: int | None         # default: None
    income_limit: float | None  # default: None
    target_group: str           # default: ""
```

A central government financial scheme with eligibility and application details.

**Fields:**

| Field | Type | Description |
|---|---|---|
| `name` | `str` | Official scheme name (e.g., "Pradhan Mantri Jan Dhan Yojana (PMJDY)") |
| `description` | `str` | One-line scheme description |
| `eligibility` | `str` | Plain-language eligibility criteria |
| `benefits` | `str` | Concrete benefit amounts and terms |
| `how_to_apply` | `str` | Step-by-step application instructions |
| `ministry` | `str` | Administering ministry |
| `min_age` | `int \| None` | Minimum age in years; `None` = no minimum |
| `max_age` | `int \| None` | Maximum age in years; `None` = no maximum |
| `income_limit` | `float \| None` | Annual income ceiling in INR; `None` = no limit |
| `target_group` | `str` | Target group key used for eligibility matching |

**Target group values used in built-in data:**

| Value | Description |
|---|---|
| `"all"` | No group restriction |
| `"all_rural"` | Rural households |
| `"unbanked"` | People without a bank account |
| `"farmers"` | Agricultural workers |
| `"girl_child"` | Girl children (age < 10) |
| `"senior_citizens"` | Age 55+ |
| `"sc_st_women"` | SC/ST or women entrepreneurs |
| `"entrepreneurs"` | Small business owners |
| `"salaried_all"` | All earning individuals |
| `"unorganized_workers"` | Informal sector workers |

---

#### `InvestmentOption`

```python
class InvestmentOption(BaseModel):
    name: str
    risk_level: Literal["low", "moderate", "high"]
    expected_return_pct: str
    lock_in_years: float
    tax_benefit: bool
    min_investment: float
    description: str
```

A retail investment instrument comparison entry.

**Fields:**

| Field | Type | Description |
|---|---|---|
| `name` | `str` | Instrument name |
| `risk_level` | `Literal["low", "moderate", "high"]` | Risk category |
| `expected_return_pct` | `str` | Indicative return range (e.g., `"7.1%"`, `"10-12%"`) |
| `lock_in_years` | `float` | Lock-in period in years; `0` = no lock-in |
| `tax_benefit` | `bool` | `True` if eligible under Section 80C |
| `min_investment` | `float` | Minimum investment in INR |
| `description` | `str` | Brief description of the instrument |

**Note:** `expected_return_pct` is a string (not float) because many instruments have ranges (e.g., "6.5-7.5%"). Returns are indicative and subject to change.

---

#### `UPIGuideEntry`

```python
class UPIGuideEntry(BaseModel):
    topic: str
    steps: list[str]
    tips: list[str]      # default: []
    warnings: list[str]  # default: []
```

A structured UPI guide for a specific topic area.

**Fields:**

| Field | Type | Description |
|---|---|---|
| `topic` | `str` | Human-readable topic title |
| `steps` | `list[str]` | Ordered, numbered action steps |
| `tips` | `list[str]` | Best-practice tips (not ordered) |
| `warnings` | `list[str]` | Fraud warnings and critical cautions |

---

## aumai_dhansetu.core

### `ConceptLibrary`

```python
class ConceptLibrary:
    def __init__(self) -> None: ...
```

Built-in library of 16 financial literacy concepts. Initialises with all pre-loaded concepts. Thread-safe for read operations; modifications to `_concepts` are not thread-safe.

---

#### `ConceptLibrary.get_by_topic`

```python
def get_by_topic(self, topic: FinancialTopic) -> list[FinancialConcept]:
```

Returns all concepts for a given topic category.

**Parameters:**

| Name | Type | Description |
|---|---|---|
| `topic` | `FinancialTopic` | The topic category to filter by |

**Returns:** `list[FinancialConcept]` — may be empty if no concepts match.

**Example:**

```python
library = ConceptLibrary()
savings_concepts = library.get_by_topic(FinancialTopic.SAVINGS)
# Returns: [FinancialConcept(title="Savings Account"), FinancialConcept(title="Fixed Deposit"), ...]
```

---

#### `ConceptLibrary.get_by_level`

```python
def get_by_level(self, level: LiteracyLevel) -> list[FinancialConcept]:
```

Returns all concepts at a specific literacy level.

**Parameters:**

| Name | Type | Description |
|---|---|---|
| `level` | `LiteracyLevel` | The literacy level to filter by |

**Returns:** `list[FinancialConcept]`

---

#### `ConceptLibrary.get_by_topic_and_level`

```python
def get_by_topic_and_level(
    self, topic: FinancialTopic, level: LiteracyLevel
) -> list[FinancialConcept]:
```

Returns concepts matching both a topic and a literacy level.

**Parameters:**

| Name | Type | Description |
|---|---|---|
| `topic` | `FinancialTopic` | Topic category |
| `level` | `LiteracyLevel` | Literacy level |

**Returns:** `list[FinancialConcept]`

**Example:**

```python
beginner_investment = library.get_by_topic_and_level(
    FinancialTopic.INVESTMENT, LiteracyLevel.BEGINNER
)
# Returns only beginner-level investment concepts (SIP in this case)
```

---

#### `ConceptLibrary.search`

```python
def search(self, query: str) -> list[FinancialConcept]:
```

Case-insensitive keyword search across concept `title` and `explanation` fields.

**Parameters:**

| Name | Type | Description |
|---|---|---|
| `query` | `str` | Search term (case-insensitive substring match) |

**Returns:** `list[FinancialConcept]` — all concepts where `query` appears in title or explanation.

**Raises:** Nothing. Returns empty list if no matches.

**Example:**

```python
results = library.search("tax")
# Returns concepts mentioning "tax" in title or explanation
# Includes: Income Tax Basics, Section 80C Deductions, PPF, etc.

results = library.search("SIP")
# Returns: Systematic Investment Plan (SIP), Mutual Funds (mentions SIP)
```

---

#### `ConceptLibrary.all_concepts`

```python
def all_concepts(self) -> list[FinancialConcept]:
```

Returns all 16 built-in concepts as a new list (modifications do not affect the library).

**Returns:** `list[FinancialConcept]`

---

### `BudgetPlanner`

```python
class BudgetPlanner:
```

Generates monthly budget plans using an income-adaptive 50/30/20 variant. Stateless — no constructor arguments.

---

#### `BudgetPlanner.plan`

```python
def plan(self, monthly_income: float) -> BudgetPlan:
```

Generate a budget plan for a given monthly income.

**Parameters:**

| Name | Type | Description |
|---|---|---|
| `monthly_income` | `float` | Monthly take-home income in INR |

**Returns:** `BudgetPlan`

**Raises:** `pydantic.ValidationError` if `monthly_income <= 0` (the returned `BudgetPlan` has `gt=0` on `income`).

**Income band behaviour:**

| Band | Needs | Wants | Savings | Emergency fund |
|---|---|---|---|---|
| < 15,000 | 65% | 15% | 20% | 3 months |
| 15,000–24,999 | 55% | 20% | 25% | 6 months |
| 25,000–49,999 | 50% | 25% | 25% | 6 months |
| 50,000–99,999 | 45% | 25% | 30% | 6 months |
| 100,000+ | 40% | 25% | 35% | 6 months |

**Example:**

```python
planner = BudgetPlanner()
plan = planner.plan(45_000)

assert "needs" in plan.allocations
assert "wants" in plan.allocations
assert "savings" in plan.allocations
assert plan.savings_target == plan.allocations["savings"]
assert len(plan.recommendations) == 3
```

---

### `SchemeAdvisor`

```python
class SchemeAdvisor:
    def __init__(self) -> None: ...
```

Matches users to eligible central government financial schemes. Initialises with all 10 built-in schemes.

---

#### `SchemeAdvisor.find_eligible`

```python
def find_eligible(
    self,
    age: int | None = None,
    income: float | None = None,
    occupation: str | None = None,
) -> list[GovernmentScheme]:
```

Returns schemes the user is eligible for based on profile.

**Parameters:**

| Name | Type | Default | Description |
|---|---|---|---|
| `age` | `int \| None` | `None` | Age in years; `None` skips age filtering |
| `income` | `float \| None` | `None` | Annual income in INR; currently not used in filtering logic (reserved) |
| `occupation` | `str \| None` | `None` | Occupation string; used for target group matching |

**Returns:** `list[GovernmentScheme]` — schemes where the user meets all applicable criteria.

**Matching logic:**
- If `age` is provided: schemes with `min_age > age` or `max_age < age` are excluded
- If `occupation` is provided: schemes with restrictive `target_group` are matched by substring (e.g., `"farmer"` matches target groups containing `"farm"` or `"agri"`)
- Permissive: missing profile data never excludes a scheme

**Example:**

```python
advisor = SchemeAdvisor()

# No filters: returns all 10 schemes
all_schemes = advisor.find_eligible()

# Age-filtered
over_60 = advisor.find_eligible(age=62)
# SCSS (min_age=60) is included; APY (max_age=40) is excluded

# Farmer-specific
farmer_schemes = advisor.find_eligible(age=40, occupation="farmer")
# PM-KISAN (target_group="farmers") is included
```

---

#### `SchemeAdvisor.get_scheme`

```python
def get_scheme(self, name: str) -> GovernmentScheme | None:
```

Look up a scheme by partial name match (case-insensitive).

**Parameters:**

| Name | Type | Description |
|---|---|---|
| `name` | `str` | Partial or full scheme name |

**Returns:** `GovernmentScheme | None` — first match, or `None` if not found.

**Example:**

```python
scheme = advisor.get_scheme("Jan Dhan")
assert scheme is not None
assert "PMJDY" in scheme.name

scheme = advisor.get_scheme("PMJJBY")
assert scheme is not None
```

---

#### `SchemeAdvisor.all_schemes`

```python
def all_schemes(self) -> list[GovernmentScheme]:
```

Returns all 10 built-in schemes as a new list.

---

### `UPIGuide`

```python
class UPIGuide:
```

Step-by-step UPI guidance. Stateless.

---

#### `UPIGuide.get_guide`

```python
def get_guide(self, topic: str) -> UPIGuideEntry | None:
```

Get the guide for a topic. Topic lookup is case-insensitive.

**Parameters:**

| Name | Type | Description |
|---|---|---|
| `topic` | `str` | One of: `"setup"`, `"security"`, `"disputes"`, `"limits"` |

**Returns:** `UPIGuideEntry | None` — `None` if topic is not recognised.

**Example:**

```python
guide = UPIGuide()
entry = guide.get_guide("security")
assert entry is not None
assert len(entry.warnings) > 0  # Security guide has explicit fraud warnings
```

---

#### `UPIGuide.available_topics`

```python
def available_topics(self) -> list[str]:
```

Returns list of topic keys: `["setup", "security", "disputes", "limits"]`.

---

#### `UPIGuide.all_guides`

```python
def all_guides(self) -> dict[str, UPIGuideEntry]:
```

Returns all guides as a dictionary keyed by topic name.

---

### `InvestmentBasics`

```python
class InvestmentBasics:
    def __init__(self) -> None: ...
```

Catalogue of 9 retail investment instruments for comparison. Initialised with all built-in options.

---

#### `InvestmentBasics.compare_all`

```python
def compare_all(self) -> list[InvestmentOption]:
```

Returns all 9 investment options.

---

#### `InvestmentBasics.by_risk`

```python
def by_risk(self, risk_level: str) -> list[InvestmentOption]:
```

Filter options by risk level.

**Parameters:**

| Name | Type | Description |
|---|---|---|
| `risk_level` | `str` | One of: `"low"`, `"moderate"`, `"high"` |

**Returns:** `list[InvestmentOption]`

**Built-in options by risk level:**

| Risk | Options |
|---|---|
| `low` | PPF, FD, RD, Debt Mutual Fund, Sukanya Samriddhi |
| `moderate` | Index Fund (Nifty 50), NPS, Sovereign Gold Bond |
| `high` | ELSS Mutual Fund |

---

#### `InvestmentBasics.tax_saving`

```python
def tax_saving(self) -> list[InvestmentOption]:
```

Returns options eligible under Section 80C (where `tax_benefit=True`).

**Returns:** `list[InvestmentOption]`

**Built-in tax-saving options:** PPF, ELSS Mutual Fund, NPS, Sukanya Samriddhi, Sovereign Gold Bond.

---

#### `InvestmentBasics.for_beginner`

```python
def for_beginner(self) -> list[InvestmentOption]:
```

Returns low-risk options suitable for investors with no prior market experience.

**Returns:** `list[InvestmentOption]` — same result as `by_risk("low")`.

**Example:**

```python
basics = InvestmentBasics()

# Beginner portfolio building
options = basics.for_beginner()
# PPF (7.1%, 15yr, Rs 500 min)
# FD (6.5-7.5%, Rs 1,000 min)
# RD (6.5-7%, Rs 100 min)
# Debt Mutual Fund (6-8%, Rs 500 min)
# Sukanya Samriddhi (8.2%, 21yr, Rs 250 min — for girl child)

# Tax planning
tax_options = basics.tax_saving()
total_80c_limit = 150_000
for opt in tax_options:
    print(f"{opt.name}: min Rs {opt.min_investment:,}, lock-in {opt.lock_in_years}yr")
```

---

## CLI Reference

The CLI entry point is `dhansetu` (installed via `pyproject.toml` `[project.scripts]`).

### Global options

```
dhansetu [--version] [--help] COMMAND
```

| Option | Description |
|---|---|
| `--version` | Print package version and exit |
| `--help` | Show help |

### Commands

| Command | Description |
|---|---|
| `learn` | Browse and search financial concepts |
| `budget` | Generate a monthly budget plan |
| `schemes` | Find eligible government schemes |
| `upi` | Get UPI guidance by topic |
| `invest` | Compare investment options |

All commands support `--help`. The `learn`, `budget`, `schemes`, and `invest` commands support `--json-output` for machine-readable output.

**JSON output format:** Pydantic `.model_dump()` serialisation with `indent=2`. All `Enum` members serialise as their `.value` string.

---

## Built-in Data Summary

| Component | Count |
|---|---|
| Financial concepts | 16 |
| Government schemes | 10 |
| Investment options | 9 |
| UPI guide topics | 4 |

**Financial concepts by topic:**

| Topic | Count |
|---|---|
| Savings | 4 (Savings Account, FD, RD, PPF) |
| Insurance | 3 (Term Life, Health Insurance, PMJJBY) |
| Investment | 3 (Mutual Funds, SIP, NPS) |
| Credit | 2 (CIBIL score, Personal Loan vs Credit Card) |
| Taxation | 2 (Income Tax Basics, Section 80C) |
| Digital Payments | 2 (UPI, Digital Payment Security) |

**Government schemes:**

| Scheme | Ministry | Key benefit |
|---|---|---|
| PMJDY | Finance | Zero-balance account + Rs 2L accident cover |
| APY | Finance | Rs 1,000–5,000/month pension at 60 |
| PMJJBY | Finance | Rs 2L life cover @ Rs 436/year |
| PMSBY | Finance | Rs 2L accident cover @ Rs 20/year |
| PM-KISAN | Agriculture | Rs 6,000/year for farmers |
| SSY | Finance | ~8.2% tax-free savings for girl child |
| SCSS | Finance | ~8.2% quarterly interest for seniors |
| NPS | Finance | Retirement pension + extra 80CCD(1B) |
| PMMY (Mudra) | Finance | Loans to Rs 10L without collateral |
| Stand Up India | Finance | Rs 10L–1Cr loans for SC/ST/women |
