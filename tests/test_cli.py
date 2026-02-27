"""Tests for the aumai-dhansetu CLI.

Disclaimer: These tests are for software testing only.
Consult a qualified financial advisor before making investment decisions.
"""

from __future__ import annotations

import json

import pytest
from click.testing import CliRunner

from aumai_dhansetu.cli import main


@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()


def test_cli_version(runner: CliRunner) -> None:
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_cli_help(runner: CliRunner) -> None:
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "DhanSetu" in result.output or "financial" in result.output.lower()


def test_learn_command_no_args(runner: CliRunner) -> None:
    result = runner.invoke(main, ["learn"])
    assert result.exit_code == 0
    assert "Found" in result.output


def test_learn_command_by_topic_savings(runner: CliRunner) -> None:
    result = runner.invoke(main, ["learn", "--topic", "savings"])
    assert result.exit_code == 0
    assert "savings" in result.output.lower() or "Savings" in result.output


def test_learn_command_by_topic_insurance(runner: CliRunner) -> None:
    result = runner.invoke(main, ["learn", "--topic", "insurance"])
    assert result.exit_code == 0


def test_learn_command_by_level_beginner(runner: CliRunner) -> None:
    result = runner.invoke(main, ["learn", "--level", "beginner"])
    assert result.exit_code == 0
    assert "beginner" in result.output.lower() or "Found" in result.output


def test_learn_command_topic_and_level(runner: CliRunner) -> None:
    result = runner.invoke(main, ["learn", "--topic", "savings", "--level", "beginner"])
    assert result.exit_code == 0


def test_learn_command_search(runner: CliRunner) -> None:
    result = runner.invoke(main, ["learn", "--search", "UPI"])
    assert result.exit_code == 0


def test_learn_command_json_output(runner: CliRunner) -> None:
    result = runner.invoke(main, ["learn", "--topic", "savings", "--json-output"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert isinstance(data, list)
    assert len(data) >= 1


def test_learn_command_shows_disclaimer(runner: CliRunner) -> None:
    result = runner.invoke(main, ["learn", "--topic", "savings"])
    assert "financial" in result.output.lower() and (
        "advisor" in result.output.lower() or "advice" in result.output.lower()
    )


def test_budget_command_income_30000(runner: CliRunner) -> None:
    result = runner.invoke(main, ["budget", "--income", "30000"])
    assert result.exit_code == 0
    assert "30,000" in result.output or "Budget Plan" in result.output


def test_budget_command_shows_all_categories(runner: CliRunner) -> None:
    result = runner.invoke(main, ["budget", "--income", "50000"])
    assert result.exit_code == 0
    output_upper = result.output.upper()
    assert "NEEDS" in output_upper
    assert "WANTS" in output_upper
    assert "SAVINGS" in output_upper


def test_budget_command_shows_recommendations(runner: CliRunner) -> None:
    result = runner.invoke(main, ["budget", "--income", "25000"])
    assert result.exit_code == 0
    assert "Recommendation" in result.output or "recommendation" in result.output.lower()


def test_budget_command_json_output(runner: CliRunner) -> None:
    result = runner.invoke(main, ["budget", "--income", "40000", "--json-output"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert "income" in data
    assert data["income"] == 40000.0


def test_budget_command_shows_disclaimer(runner: CliRunner) -> None:
    result = runner.invoke(main, ["budget", "--income", "30000"])
    assert "financial" in result.output.lower()


def test_schemes_command_no_args(runner: CliRunner) -> None:
    result = runner.invoke(main, ["schemes"])
    assert result.exit_code == 0
    assert "scheme" in result.output.lower() or "Found" in result.output


def test_schemes_command_with_age(runner: CliRunner) -> None:
    result = runner.invoke(main, ["schemes", "--age", "30"])
    assert result.exit_code == 0


def test_schemes_command_with_farmer_occupation(runner: CliRunner) -> None:
    result = runner.invoke(main, ["schemes", "--occupation", "farmer"])
    assert result.exit_code == 0
    assert "Kisan" in result.output or "farmer" in result.output.lower()


def test_schemes_command_json_output(runner: CliRunner) -> None:
    result = runner.invoke(main, ["schemes", "--age", "25", "--json-output"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert isinstance(data, list)


def test_schemes_command_shows_disclaimer(runner: CliRunner) -> None:
    result = runner.invoke(main, ["schemes", "--age", "30"])
    assert "financial" in result.output.lower() or "advisor" in result.output.lower()


def test_upi_command_setup(runner: CliRunner) -> None:
    result = runner.invoke(main, ["upi", "--topic", "setup"])
    assert result.exit_code == 0
    assert "UPI" in result.output


def test_upi_command_security(runner: CliRunner) -> None:
    result = runner.invoke(main, ["upi", "--topic", "security"])
    assert result.exit_code == 0
    assert "PIN" in result.output or "security" in result.output.lower()


def test_upi_command_disputes(runner: CliRunner) -> None:
    result = runner.invoke(main, ["upi", "--topic", "disputes"])
    assert result.exit_code == 0


def test_upi_command_limits(runner: CliRunner) -> None:
    result = runner.invoke(main, ["upi", "--topic", "limits"])
    assert result.exit_code == 0
    assert "1,00,000" in result.output or "lakh" in result.output.lower() or "limit" in result.output.lower()


def test_upi_command_security_shows_warnings(runner: CliRunner) -> None:
    result = runner.invoke(main, ["upi", "--topic", "security"])
    assert result.exit_code == 0
    assert "Warning" in result.output or "warning" in result.output.lower()


def test_invest_command_all_options(runner: CliRunner) -> None:
    result = runner.invoke(main, ["invest"])
    assert result.exit_code == 0
    assert "PPF" in result.output or "Investment" in result.output


def test_invest_command_low_risk(runner: CliRunner) -> None:
    result = runner.invoke(main, ["invest", "--risk", "low"])
    assert result.exit_code == 0
    assert "low" in result.output


def test_invest_command_tax_saving(runner: CliRunner) -> None:
    result = runner.invoke(main, ["invest", "--tax-saving"])
    assert result.exit_code == 0
    assert "PPF" in result.output or "ELSS" in result.output


def test_invest_command_json_output(runner: CliRunner) -> None:
    result = runner.invoke(main, ["invest", "--json-output"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert isinstance(data, list)
    assert len(data) >= 1


def test_invest_command_shows_disclaimer(runner: CliRunner) -> None:
    result = runner.invoke(main, ["invest"])
    assert "financial" in result.output.lower()
