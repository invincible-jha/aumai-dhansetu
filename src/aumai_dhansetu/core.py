"""Core logic for aumai-dhansetu."""

from __future__ import annotations

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
# Built-in concept library
# ---------------------------------------------------------------------------

_CONCEPTS: list[FinancialConcept] = [
    # Savings - Beginner
    FinancialConcept(
        topic=FinancialTopic.SAVINGS, title="Savings Account",
        explanation="A basic bank account that earns interest on your deposited money. Most banks offer 2.5-4% annual interest. Required for receiving salary, government subsidies, and digital payments.",
        examples=["SBI Savings Account", "Jan Dhan Yojana Account", "Post Office Savings Account"],
        level=LiteracyLevel.BEGINNER, key_terms=["interest rate", "minimum balance", "passbook"],
    ),
    FinancialConcept(
        topic=FinancialTopic.SAVINGS, title="Fixed Deposit (FD)",
        explanation="Lock your money for a fixed period (7 days to 10 years) at a higher interest rate than savings accounts. Typically 6-7.5% annual interest. Early withdrawal incurs a penalty.",
        examples=["1-year FD at 7%", "5-year Tax Saver FD under 80C"],
        level=LiteracyLevel.BEGINNER, key_terms=["maturity", "premature withdrawal", "TDS"],
    ),
    FinancialConcept(
        topic=FinancialTopic.SAVINGS, title="Recurring Deposit (RD)",
        explanation="Save a fixed amount every month for a chosen period. Earns similar interest as FD. Good for building a savings habit with small monthly amounts starting from Rs 100.",
        examples=["Rs 500/month RD for 2 years", "Post Office RD at 6.7%"],
        level=LiteracyLevel.BEGINNER, key_terms=["monthly installment", "maturity amount"],
    ),
    FinancialConcept(
        topic=FinancialTopic.SAVINGS, title="Public Provident Fund (PPF)",
        explanation="Government-backed long-term savings scheme with 15-year lock-in. Currently offers ~7.1% tax-free interest. Maximum Rs 1.5L per year deposit. Triple tax benefit: investment, interest, and maturity all tax-free (EEE).",
        examples=["PPF account in SBI or Post Office"],
        level=LiteracyLevel.INTERMEDIATE, key_terms=["EEE tax benefit", "Section 80C", "15-year lock-in"],
    ),
    # Insurance
    FinancialConcept(
        topic=FinancialTopic.INSURANCE, title="Term Life Insurance",
        explanation="Pure life cover at low cost. Pays the sum assured to your nominee if you die during the policy term. No survival benefit. Most affordable form of life insurance. Rule of thumb: cover should be 10-15x annual income.",
        examples=["Rs 1 Crore cover for Rs 700/month at age 30"],
        level=LiteracyLevel.BEGINNER, key_terms=["sum assured", "premium", "nominee", "term"],
    ),
    FinancialConcept(
        topic=FinancialTopic.INSURANCE, title="Health Insurance",
        explanation="Covers hospitalization expenses. Mediclaim policies reimburse actual hospital bills up to sum insured. Family floater plans cover entire family under one sum insured. Mandatory to avoid financial ruin from medical emergencies.",
        examples=["Rs 5L family floater for Rs 12,000/year"],
        level=LiteracyLevel.BEGINNER, key_terms=["sum insured", "cashless", "copay", "waiting period"],
    ),
    FinancialConcept(
        topic=FinancialTopic.INSURANCE, title="PM Jeevan Jyoti Bima Yojana (PMJJBY)",
        explanation="Government life insurance scheme. Rs 2 lakh life cover for just Rs 436/year premium. Available for anyone aged 18-50 with a bank account. Auto-debited from bank account annually.",
        examples=["Rs 436/year for Rs 2L life cover"],
        level=LiteracyLevel.BEGINNER, key_terms=["annual premium", "auto-debit", "death claim"],
    ),
    # Investment
    FinancialConcept(
        topic=FinancialTopic.INVESTMENT, title="Mutual Funds",
        explanation="Pool money from many investors to invest in stocks, bonds, or both. Managed by professional fund managers. Entry point as low as Rs 500 via SIP. Categories: equity (high risk/return), debt (low risk), hybrid (mixed).",
        examples=["Nifty 50 Index Fund", "Liquid Fund for emergency money"],
        level=LiteracyLevel.INTERMEDIATE, key_terms=["NAV", "SIP", "expense ratio", "CAGR"],
    ),
    FinancialConcept(
        topic=FinancialTopic.INVESTMENT, title="Systematic Investment Plan (SIP)",
        explanation="Invest a fixed amount regularly (monthly/weekly) in mutual funds. Benefits from rupee cost averaging - buy more units when prices are low, fewer when high. Best started early for compounding benefit.",
        examples=["Rs 1000/month SIP in index fund for 20 years"],
        level=LiteracyLevel.BEGINNER, key_terms=["rupee cost averaging", "compounding", "SIP date"],
    ),
    FinancialConcept(
        topic=FinancialTopic.INVESTMENT, title="National Pension System (NPS)",
        explanation="Government pension scheme for retirement savings. Two accounts: Tier I (locked till 60, tax benefits) and Tier II (flexible). Invest in equity, corporate bonds, and government securities. Additional Rs 50,000 deduction under Section 80CCD(1B).",
        examples=["NPS Tier I with 75% equity allocation at age 30"],
        level=LiteracyLevel.INTERMEDIATE, key_terms=["Tier I/II", "PFRDA", "annuity", "80CCD"],
    ),
    # Credit
    FinancialConcept(
        topic=FinancialTopic.CREDIT, title="Credit Score (CIBIL)",
        explanation="A 3-digit number (300-900) reflecting your creditworthiness. Banks check this before giving loans. Score above 750 is considered good. Maintained by CIBIL, Experian, Equifax, CRIF. Check free once a year from each bureau.",
        examples=["Score 780 = easy loan approval at lower interest"],
        level=LiteracyLevel.BEGINNER, key_terms=["CIBIL score", "credit report", "EMI default"],
    ),
    FinancialConcept(
        topic=FinancialTopic.CREDIT, title="Personal Loan vs Credit Card",
        explanation="Personal loans: fixed EMI, 10-18% interest, 1-5 year term. Credit cards: revolving credit, 24-42% annualized interest if not paid in full. Always pay credit card full amount by due date. Never pay only minimum due.",
        examples=["Rs 5L personal loan at 12% for 3 years"],
        level=LiteracyLevel.INTERMEDIATE, key_terms=["EMI", "interest rate", "minimum due", "billing cycle"],
    ),
    # Taxation
    FinancialConcept(
        topic=FinancialTopic.TAXATION, title="Income Tax Basics",
        explanation="Income up to Rs 3L is tax-free (new regime FY 2024-25). Slabs: 3-7L at 5%, 7-10L at 10%, 10-12L at 15%, 12-15L at 20%, above 15L at 30%. Old regime allows deductions under 80C (up to 1.5L), 80D (health insurance), HRA, etc.",
        examples=["Rs 8L income = ~Rs 30,000 tax under new regime"],
        level=LiteracyLevel.BEGINNER, key_terms=["slab", "old vs new regime", "Section 80C", "ITR"],
    ),
    FinancialConcept(
        topic=FinancialTopic.TAXATION, title="Section 80C Deductions",
        explanation="Claim up to Rs 1.5 lakh deduction from taxable income under old regime. Eligible investments: PPF, ELSS mutual funds, 5-year FD, NSC, life insurance premium, EPF, tuition fees for children, home loan principal.",
        examples=["Rs 1.5L in ELSS = save Rs 46,800 tax at 30% slab"],
        level=LiteracyLevel.INTERMEDIATE, key_terms=["deduction", "EEE", "ELSS", "lock-in period"],
    ),
    # Digital Payments
    FinancialConcept(
        topic=FinancialTopic.DIGITAL_PAYMENTS, title="UPI (Unified Payments Interface)",
        explanation="Instant bank-to-bank transfer using mobile phone. Free of charge. Works 24/7. Send/receive money using UPI ID (yourname@bank), phone number, or QR code. Daily limit typically Rs 1 lakh. India's most popular digital payment system.",
        examples=["Pay shopkeeper via PhonePe QR scan", "Send money via Google Pay"],
        level=LiteracyLevel.BEGINNER, key_terms=["UPI ID", "VPA", "QR code", "UPI PIN"],
    ),
    FinancialConcept(
        topic=FinancialTopic.DIGITAL_PAYMENTS, title="Digital Payment Security",
        explanation="Never share UPI PIN, OTP, or CVV with anyone. Banks/UPI apps never call asking for PIN/OTP. Verify receiver details before sending. Check transaction amount carefully. Use app lock. Report fraud immediately to bank and cybercrime.gov.in.",
        examples=["Phishing call claiming to be bank - always hang up"],
        level=LiteracyLevel.BEGINNER, key_terms=["UPI PIN", "OTP", "phishing", "fraud reporting"],
    ),
]

# ---------------------------------------------------------------------------
# Government schemes database
# ---------------------------------------------------------------------------

_SCHEMES: list[GovernmentScheme] = [
    GovernmentScheme(
        name="Pradhan Mantri Jan Dhan Yojana (PMJDY)",
        description="Zero-balance bank account with RuPay debit card, Rs 2 lakh accident insurance, and Rs 30,000 life cover.",
        eligibility="Any Indian citizen without a bank account",
        benefits="Zero balance account, RuPay card, Rs 2L accident cover, Rs 30K life cover, overdraft up to Rs 10,000",
        how_to_apply="Visit any bank branch with Aadhaar card and passport photo",
        ministry="Ministry of Finance", target_group="unbanked",
    ),
    GovernmentScheme(
        name="Atal Pension Yojana (APY)",
        description="Guaranteed pension of Rs 1,000-5,000/month after age 60, based on contribution amount and joining age.",
        eligibility="Indian citizens aged 18-40, with a bank account",
        benefits="Guaranteed monthly pension of Rs 1000-5000 after 60. Government co-contributes 50% for 5 years for non-taxpayers.",
        how_to_apply="Apply through your bank branch or net banking. Auto-debit from savings account.",
        ministry="Ministry of Finance", min_age=18, max_age=40, target_group="unorganized_workers",
    ),
    GovernmentScheme(
        name="PM Jeevan Jyoti Bima Yojana (PMJJBY)",
        description="Life insurance cover of Rs 2 lakh at just Rs 436/year premium.",
        eligibility="Bank account holders aged 18-50",
        benefits="Rs 2 lakh life cover. Premium auto-debited annually.",
        how_to_apply="Enroll through bank (form available at branch or net banking). One-time consent for auto-debit.",
        ministry="Ministry of Finance", min_age=18, max_age=50, target_group="all",
    ),
    GovernmentScheme(
        name="PM Suraksha Bima Yojana (PMSBY)",
        description="Accident insurance of Rs 2 lakh at just Rs 20/year premium.",
        eligibility="Bank account holders aged 18-70",
        benefits="Rs 2L for accidental death, Rs 2L for total permanent disability, Rs 1L for partial permanent disability.",
        how_to_apply="Enroll through bank branch or net banking. Rs 20 auto-debited annually.",
        ministry="Ministry of Finance", min_age=18, max_age=70, target_group="all",
    ),
    GovernmentScheme(
        name="PM Kisan Samman Nidhi (PM-KISAN)",
        description="Rs 6,000/year direct income support to farmer families in 3 installments of Rs 2,000 each.",
        eligibility="All landholding farmer families (subject to exclusion criteria)",
        benefits="Rs 6,000 per year in 3 installments directly to bank account via DBT.",
        how_to_apply="Register at pmkisan.gov.in or through Common Service Centre (CSC) with Aadhaar and land records.",
        ministry="Ministry of Agriculture", target_group="farmers",
    ),
    GovernmentScheme(
        name="Sukanya Samriddhi Yojana (SSY)",
        description="Savings scheme for girl child with high interest rate (~8%) and full tax exemption (EEE).",
        eligibility="Parents/guardians of girl child below 10 years of age",
        benefits="High interest (~8.2%), tax-free under 80C. Partial withdrawal at 18 for education. Matures at 21.",
        how_to_apply="Open account at Post Office or designated bank with birth certificate of girl child.",
        ministry="Ministry of Finance", target_group="girl_child",
    ),
    GovernmentScheme(
        name="Senior Citizens Saving Scheme (SCSS)",
        description="High-interest savings for senior citizens with quarterly interest payout.",
        eligibility="Indian citizens aged 60+ (55+ for retired defence/government employees)",
        benefits="~8.2% interest paid quarterly. Max deposit Rs 30 lakh. Tax deduction under 80C.",
        how_to_apply="Apply at Post Office or designated banks with age proof and retirement documents.",
        ministry="Ministry of Finance", min_age=60, target_group="senior_citizens",
    ),
    GovernmentScheme(
        name="National Pension System (NPS)",
        description="Voluntary pension scheme for retirement planning with tax benefits.",
        eligibility="Indian citizens aged 18-70",
        benefits="Market-linked returns. Extra Rs 50,000 deduction under 80CCD(1B). Partial withdrawal after 3 years.",
        how_to_apply="Register at enps.nsdl.com with Aadhaar and PAN. Minimum Rs 500/month contribution.",
        ministry="Ministry of Finance", min_age=18, max_age=70, target_group="salaried_all",
    ),
    GovernmentScheme(
        name="PM Mudra Yojana (PMMY)",
        description="Loans up to Rs 10 lakh for non-corporate, non-farm small/micro enterprises.",
        eligibility="Any Indian citizen with a business plan for non-farm income generating activity",
        benefits="Shishu (up to 50K), Kishore (50K-5L), Tarun (5L-10L). No collateral required.",
        how_to_apply="Apply at any bank, NBFC, or MFI with business plan and KYC documents.",
        ministry="Ministry of Finance", target_group="entrepreneurs",
    ),
    GovernmentScheme(
        name="Stand Up India",
        description="Bank loans between Rs 10 lakh and Rs 1 crore for SC/ST and women entrepreneurs.",
        eligibility="SC/ST or women entrepreneurs for greenfield enterprises in manufacturing/services/trading",
        benefits="Composite loan of Rs 10L to Rs 1Cr. Covers 75% of project cost. Repayment up to 7 years.",
        how_to_apply="Apply at standupmitra.in or visit bank branch with project report.",
        ministry="Ministry of Finance", target_group="sc_st_women",
    ),
]

# ---------------------------------------------------------------------------
# Investment options
# ---------------------------------------------------------------------------

_INVESTMENTS: list[InvestmentOption] = [
    InvestmentOption(name="Public Provident Fund (PPF)", risk_level="low", expected_return_pct="7.1%", lock_in_years=15, tax_benefit=True, min_investment=500, description="Government-backed, EEE tax status, 15-year lock-in"),
    InvestmentOption(name="Fixed Deposit (FD)", risk_level="low", expected_return_pct="6.5-7.5%", lock_in_years=0.25, tax_benefit=False, min_investment=1000, description="Bank deposit with guaranteed returns, premature withdrawal with penalty"),
    InvestmentOption(name="Recurring Deposit (RD)", risk_level="low", expected_return_pct="6.5-7%", lock_in_years=0.5, tax_benefit=False, min_investment=100, description="Monthly fixed deposit, good for building savings habit"),
    InvestmentOption(name="ELSS Mutual Fund", risk_level="high", expected_return_pct="12-15%", lock_in_years=3, tax_benefit=True, min_investment=500, description="Equity fund with 3-year lock-in and 80C tax benefit"),
    InvestmentOption(name="Index Fund (Nifty 50)", risk_level="moderate", expected_return_pct="10-12%", lock_in_years=0, tax_benefit=False, min_investment=500, description="Passive fund tracking Nifty 50, low expense ratio"),
    InvestmentOption(name="Debt Mutual Fund", risk_level="low", expected_return_pct="6-8%", lock_in_years=0, tax_benefit=False, min_investment=500, description="Invests in bonds and government securities, lower risk than equity"),
    InvestmentOption(name="National Pension System (NPS)", risk_level="moderate", expected_return_pct="8-10%", lock_in_years=0, tax_benefit=True, min_investment=500, description="Retirement-focused, extra 80CCD(1B) deduction of Rs 50K"),
    InvestmentOption(name="Sukanya Samriddhi (SSY)", risk_level="low", expected_return_pct="8.2%", lock_in_years=21, tax_benefit=True, min_investment=250, description="For girl child, highest small savings rate, EEE status"),
    InvestmentOption(name="Gold (Sovereign Gold Bond)", risk_level="moderate", expected_return_pct="8-10%", lock_in_years=8, tax_benefit=True, description="Government gold bonds, 2.5% annual interest + gold appreciation, tax-free on maturity", min_investment=4500),
]

# ---------------------------------------------------------------------------
# UPI guidance
# ---------------------------------------------------------------------------

_UPI_GUIDES: dict[str, UPIGuideEntry] = {
    "setup": UPIGuideEntry(
        topic="Setting Up UPI",
        steps=[
            "1. Download a UPI app (PhonePe, Google Pay, Paytm, BHIM, or your bank's app)",
            "2. Register with your mobile number (must be linked to your bank account)",
            "3. Verify via SMS OTP sent to your registered mobile",
            "4. Select your bank and link your bank account",
            "5. Set a 6-digit UPI PIN (you need your debit card number and expiry date for this)",
            "6. Your UPI ID is created (e.g., yourphone@ybl for PhonePe, yourphone@okaxis for GPay)",
            "7. You can now send and receive money instantly",
        ],
        tips=["Keep your registered mobile number active", "Remember your UPI PIN securely"],
    ),
    "security": UPIGuideEntry(
        topic="UPI Security Best Practices",
        steps=[
            "1. NEVER share your UPI PIN with anyone - not even bank officials",
            "2. NEVER share OTP received on your phone with any caller",
            "3. Do NOT scan QR codes sent by strangers claiming to 'send' you money",
            "4. Verify the receiver's name before confirming any payment",
            "5. Enable app lock (fingerprint/PIN) on your UPI app",
            "6. Check transaction amount carefully before entering PIN",
            "7. Regularly check your transaction history for unauthorized transactions",
        ],
        tips=[
            "Banks NEVER call asking for UPI PIN or OTP",
            "To RECEIVE money, you never need to scan a QR code or enter PIN",
            "Report suspicious activity immediately",
        ],
        warnings=[
            "Collect requests from unknown numbers are often scams",
            "No UPI app charges fees - callers claiming 'UPI fees' are fraudsters",
        ],
    ),
    "disputes": UPIGuideEntry(
        topic="UPI Dispute Resolution",
        steps=[
            "1. Check your bank account balance to confirm if money was actually debited",
            "2. Wait 30 minutes - sometimes transactions reverse automatically",
            "3. If not resolved, raise a complaint in your UPI app (usually under Help/Support)",
            "4. Note down the UPI Transaction Reference Number (UTR/RRN)",
            "5. If unresolved after 48 hours, contact your bank's customer care",
            "6. File complaint on NPCI portal: npci.org.in/what-we-do/upi/dispute-redressal",
            "7. If still unresolved after 30 days, file on RBI's CMS portal: cms.rbi.org.in",
        ],
        tips=["Always save transaction screenshots", "Keep UTR/RRN numbers for reference"],
    ),
    "limits": UPIGuideEntry(
        topic="UPI Transaction Limits",
        steps=[
            "1. Per-transaction limit: Rs 1,00,000 (Rs 1 lakh) for most transactions",
            "2. Capital market/IPO payments: up to Rs 5,00,000",
            "3. Tax payments: up to Rs 5,00,000",
            "4. Hospital/education: up to Rs 5,00,000",
            "5. UPI Lite: Rs 500 per transaction, Rs 2,000 wallet limit (offline capable)",
            "6. No charges on UPI transactions for individuals",
            "7. Works 24/7 including weekends and holidays",
        ],
        tips=["Daily and monthly limits may vary by bank", "UPI Lite works without internet for small payments"],
    ),
}


class ConceptLibrary:
    """Built-in library of financial literacy concepts."""

    def __init__(self) -> None:
        self._concepts: list[FinancialConcept] = list(_CONCEPTS)

    def get_by_topic(self, topic: FinancialTopic) -> list[FinancialConcept]:
        """Get concepts for a specific topic."""
        return [c for c in self._concepts if c.topic == topic]

    def get_by_level(self, level: LiteracyLevel) -> list[FinancialConcept]:
        """Get concepts for a specific literacy level."""
        return [c for c in self._concepts if c.level == level]

    def get_by_topic_and_level(
        self, topic: FinancialTopic, level: LiteracyLevel
    ) -> list[FinancialConcept]:
        """Get concepts filtered by both topic and level."""
        return [c for c in self._concepts if c.topic == topic and c.level == level]

    def search(self, query: str) -> list[FinancialConcept]:
        """Search concepts by keyword in title and explanation."""
        q = query.lower()
        return [
            c for c in self._concepts
            if q in c.title.lower() or q in c.explanation.lower()
        ]

    def all_concepts(self) -> list[FinancialConcept]:
        """Return all concepts."""
        return list(self._concepts)


class BudgetPlanner:
    """Generate budget plans based on the 50/30/20 rule."""

    def plan(self, monthly_income: float) -> BudgetPlan:
        """Generate a budget plan adjusted for income level."""
        recommendations: list[str] = []

        if monthly_income < 15000:
            # Very low income: prioritize needs
            needs_pct, wants_pct, savings_pct = 0.65, 0.15, 0.20
            recommendations.append("At this income, prioritize essential needs and build a small emergency buffer.")
            recommendations.append("Open a Jan Dhan account if you don't have a bank account.")
            recommendations.append("Enroll in PM Suraksha Bima (Rs 20/year) for accident cover.")
        elif monthly_income < 25000:
            needs_pct, wants_pct, savings_pct = 0.55, 0.20, 0.25
            recommendations.append("Start a small RD of Rs 500-1000/month to build savings habit.")
            recommendations.append("Get health insurance (at least Rs 3L family floater).")
            recommendations.append("Consider Atal Pension Yojana for retirement security.")
        elif monthly_income < 50000:
            needs_pct, wants_pct, savings_pct = 0.50, 0.25, 0.25
            recommendations.append("Start a SIP of Rs 2000-5000/month in an index fund.")
            recommendations.append("Build emergency fund of 3-6 months expenses in liquid fund or FD.")
            recommendations.append("Maximize Section 80C deduction with PPF + ELSS.")
        elif monthly_income < 100000:
            needs_pct, wants_pct, savings_pct = 0.45, 0.25, 0.30
            recommendations.append("Increase SIP to 20-30% of income across equity and debt funds.")
            recommendations.append("Consider NPS for additional Rs 50K tax deduction under 80CCD(1B).")
            recommendations.append("Get term life insurance of Rs 1 Crore if you have dependents.")
        else:
            needs_pct, wants_pct, savings_pct = 0.40, 0.25, 0.35
            recommendations.append("Diversify investments: equity mutual funds, NPS, PPF, gold bonds.")
            recommendations.append("Consider hiring a SEBI-registered financial advisor.")
            recommendations.append("Review and optimize tax strategy between old and new regime.")

        allocations = {
            BudgetCategory.NEEDS.value: round(monthly_income * needs_pct, 2),
            BudgetCategory.WANTS.value: round(monthly_income * wants_pct, 2),
            BudgetCategory.SAVINGS.value: round(monthly_income * savings_pct, 2),
        }

        return BudgetPlan(
            income=monthly_income,
            allocations=allocations,
            recommendations=recommendations,
            savings_target=round(monthly_income * savings_pct, 2),
            emergency_fund_months=6 if monthly_income >= 25000 else 3,
        )


class SchemeAdvisor:
    """Match users to eligible government schemes."""

    def __init__(self) -> None:
        self._schemes: list[GovernmentScheme] = list(_SCHEMES)

    def find_eligible(
        self,
        age: int | None = None,
        income: float | None = None,
        occupation: str | None = None,
    ) -> list[GovernmentScheme]:
        """Find schemes the user is eligible for based on their profile."""
        eligible: list[GovernmentScheme] = []
        for scheme in self._schemes:
            if scheme.min_age is not None and age is not None and age < scheme.min_age:
                continue
            if scheme.max_age is not None and age is not None and age > scheme.max_age:
                continue

            # Target group matching
            tg = scheme.target_group
            occ = (occupation or "").lower()
            if tg == "farmers" and occ and "farm" not in occ and "agri" not in occ:
                continue
            if tg == "girl_child" and (age is not None and age >= 10):
                continue
            if tg == "senior_citizens" and (age is not None and age < 55):
                continue
            if tg == "sc_st_women" and occ and "sc" not in occ and "st" not in occ and "women" not in occ:
                continue

            eligible.append(scheme)
        return eligible

    def get_scheme(self, name: str) -> GovernmentScheme | None:
        """Look up a scheme by name (partial match)."""
        name_lower = name.lower()
        for scheme in self._schemes:
            if name_lower in scheme.name.lower():
                return scheme
        return None

    def all_schemes(self) -> list[GovernmentScheme]:
        """Return all schemes."""
        return list(self._schemes)


class UPIGuide:
    """Step-by-step UPI guidance."""

    def get_guide(self, topic: str) -> UPIGuideEntry | None:
        """Get UPI guide for a topic."""
        return _UPI_GUIDES.get(topic.lower())

    def available_topics(self) -> list[str]:
        """List available UPI guide topics."""
        return list(_UPI_GUIDES.keys())

    def all_guides(self) -> dict[str, UPIGuideEntry]:
        """Return all UPI guides."""
        return dict(_UPI_GUIDES)


class InvestmentBasics:
    """Compare and explain basic investment options."""

    def __init__(self) -> None:
        self._options: list[InvestmentOption] = list(_INVESTMENTS)

    def compare_all(self) -> list[InvestmentOption]:
        """Return all investment options for comparison."""
        return list(self._options)

    def by_risk(self, risk_level: str) -> list[InvestmentOption]:
        """Filter by risk level."""
        return [o for o in self._options if o.risk_level == risk_level]

    def tax_saving(self) -> list[InvestmentOption]:
        """Return only tax-saving investment options."""
        return [o for o in self._options if o.tax_benefit]

    def for_beginner(self) -> list[InvestmentOption]:
        """Return low-risk options suitable for beginners."""
        return [o for o in self._options if o.risk_level == "low"]
