#!/usr/bin/env python3
"""
Script to create the complete multi-agent loan approval system folder structure
Run: python create_structure.py
"""

import os
from pathlib import Path

# Define the complete folder structure
STRUCTURE = {
    "presentation": {
        "_init_": True,
        "config.py": "# Streamlit configuration",
        "components": {
            "_init_": True,
            "forms.py": "# Form components",
            "cards.py": "# Card components",
            "charts.py": "# Chart components",
            "status_indicators.py": "# Status indicators",
            "navigation.py": "# Navigation components",
        },
        "pages": {
            "_init_": True,
            "01_dashboard.py": "# Dashboard page",
            "02_loan_application.py": "# Loan application page",
            "03_application_status.py": "# Application status page",
            "04_analytics.py": "# Analytics page",
            "05_settings.py": "# Settings page",
        },
        "utils": {
            "_init_": True,
            "api_client.py": "# API client utility",
            "formatters.py": "# Data formatting utilities",
            "validators.py": "# Input validators",
            "session_state.py": "# Streamlit session state",
        },
        "assets": {
            "images": {},
            "icons": {},
        },
    },
    "microservices": {
        "_init_": True,
        "main.py": "# FastAPI main app",
        "api": {
            "_init_": True,
            "routes.py": "# Main router",
            "loan_routes.py": "# Loan endpoints",
            "status_routes.py": "# Status endpoints",
            "analytics_routes.py": "# Analytics endpoints",
            "health.py": "# Health check",
        },
        "schemas": {
            "_init_": True,
            "loan.py": "# Loan schemas",
            "applicant.py": "# Applicant schemas",
            "decision.py": "# Decision schemas",
            "responses.py": "# Response schemas",
        },
        "models": {
            "_init_": True,
            "loan_application.py": "# LoanApplication ORM model",
            "applicant.py": "# Applicant ORM model",
            "decision.py": "# Decision ORM model",
            "audit_log.py": "# Audit log ORM model",
        },
        "middleware": {
            "_init_": True,
            "auth.py": "# Authentication middleware",
            "logging.py": "# Logging middleware",
            "error_handling.py": "# Error handling middleware",
            "cors.py": "# CORS configuration",
        },
        "dependencies": {
            "_init_": True,
            "database.py": "# Database dependency",
            "auth.py": "# Auth dependency",
            "orchestrator.py": "# Orchestrator dependency",
            "mcp.py": "# MCP dependency",
        },
        "crud": {
            "_init_": True,
            "loan.py": "# Loan CRUD operations",
            "applicant.py": "# Applicant CRUD operations",
            "decision.py": "# Decision CRUD operations",
        },
    },
    "orchestration": {
        "_init_": True,
        "graph.py": "# LangGraph graph builder",
        "state.py": "# Graph state definition",
        "router.py": "# Routing logic",
        "workflows": {
            "_init_": True,
            "loan_approval_workflow.py": "# Main approval workflow",
            "parallel_workflow.py": "# Parallel processing",
            "callback_workflow.py": "# Callback workflow",
        },
        "state_managers": {
            "_init_": True,
            "conversation_state.py": "# Conversation state",
            "workflow_state.py": "# Workflow state",
            "context_manager.py": "# Context manager",
        },
        "validators": {
            "_init_": True,
            "state_validator.py": "# State validators",
            "workflow_validator.py": "# Workflow validators",
        },
    },
    "agents": {
        "_init_": True,
        "base_agent.py": "# Base agent class",
        "loan_processor": {
            "_init_": True,
            "agent.py": "# Loan processor agent",
            "prompts.py": "# Agent prompts",
            "tools.py": "# Agent tools",
            "validators.py": "# Input validators",
        },
        "credit_analyzer": {
            "_init_": True,
            "agent.py": "# Credit analyzer agent",
            "prompts.py": "# Agent prompts",
            "tools.py": "# Agent tools",
            "validators.py": "# Input validators",
        },
        "risk_assessor": {
            "_init_": True,
            "agent.py": "# Risk assessor agent",
            "prompts.py": "# Agent prompts",
            "tools.py": "# Agent tools",
            "validators.py": "# Input validators",
        },
        "decision_maker": {
            "_init_": True,
            "agent.py": "# Decision maker agent",
            "prompts.py": "# Agent prompts",
            "tools.py": "# Agent tools",
            "validators.py": "# Input validators",
        },
        "shared": {
            "_init_": True,
            "common_tools.py": "# Common tools",
            "memory.py": "# Agent memory",
            "response_formatter.py": "# Response formatting",
        },
    },
    "mcp": {
        "_init_": True,
        "server.py": "# MCP server",
        "clients": {
            "_init_": True,
            "mcp_client.py": "# MCP client",
            "tool_client.py": "# Tool client",
        },
        "tools": {
            "_init_": True,
            "database_tools.py": "# Database tools",
            "external_api_tools.py": "# External API tools",
            "calculation_tools.py": "# Calculation tools",
            "document_tools.py": "# Document tools",
        },
        "resources": {
            "_init_": True,
            "credit_rules.py": "# Credit rules",
            "compliance_rules.py": "# Compliance rules",
            "reference_data.py": "# Reference data",
        },
        "handlers": {
            "_init_": True,
            "call_tool_handler.py": "# Tool call handler",
            "read_resource_handler.py": "# Resource handler",
            "list_handler.py": "# List handler",
        },
    },
    "shared": {
        "_init_": True,
        "config.py": "# Global configuration",
        "logger.py": "# Logging setup",
        "constants.py": "# Application constants",
        "enums.py": "# Enumerations",
        "database": {
            "_init_": True,
            "connection.py": "# Database connection",
            "session.py": "# Session management",
            "migrations.py": "# Migrations",
        },
        "exceptions": {
            "_init_": True,
            "loan_exceptions.py": "# Loan exceptions",
            "agent_exceptions.py": "# Agent exceptions",
            "mcp_exceptions.py": "# MCP exceptions",
        },
        "utils": {
            "_init_": True,
            "validators.py": "# Validators",
            "formatters.py": "# Formatters",
            "calculators.py": "# Calculators",
            "helpers.py": "# Helpers",
        },
    },
    "config": {
        "_init_": True,
        "settings.py": "# Environment settings",
        "database.py": "# Database config",
        "logging.py": "# Logging config",
        "mcp.py": "# MCP config",
        "agents.py": "# Agent config",
    },
    "scripts": {
        "_init_": True,
        "setup_db.py": "# Database setup",
        "seed_data.py": "# Seed data",
        "run_migration.py": "# Run migrations",
        "cleanup.py": "# Cleanup",
    },
    "tests": {
        "_init_": True,
        "conftest.py": "# Pytest config",
        "unit": {
            "_init_": True,
            "test_agents.py": "# Agent tests",
            "test_microservices.py": "# Microservice tests",
            "test_orchestration.py": "# Orchestration tests",
        },
        "integration": {
            "_init_": True,
            "test_workflow.py": "# Workflow tests",
            "test_api.py": "# API tests",
            "test_mcp_integration.py": "# MCP integration tests",
        },
        "fixtures": {
            "_init_": True,
            "loan_fixtures.py": "# Loan fixtures",
            "agent_fixtures.py": "# Agent fixtures",
            "mcp_fixtures.py": "# MCP fixtures",
        },
    },
    "docs": {
        "architecture.md": "# Architecture documentation",
        "api.md": "# API documentation",
        "agents.md": "# Agent documentation",
        "workflows.md": "# Workflow documentation",
        "mcp.md": "# MCP integration guide",
        "deployment.md": "# Deployment guide",
    },
}


def create_structure(base_path: str, structure: dict, level: int = 0) -> None:
    """
    Recursively create the folder structure and files.

    Args:
        base_path: The base path to create structure in
        structure: Dictionary defining the structure
        level: Current nesting level (for display)
    """
    for name, content in structure.items():
        item_path = Path(base_path) / name

        if name == "_init_":
            # Create __init__.py file
            init_file = Path(base_path) / "__init__.py"
            init_file.touch()
            print(f"{'  ' * level}✓ Created {init_file.relative_to(base_path.split(os.sep)[0])}")

        elif isinstance(content, dict):
            # Create directory
            item_path.mkdir(parents=True, exist_ok=True)
            print(f"{'  ' * level}📁 {name}/")

            # Recursively create subdirectories
            create_structure(str(item_path), content, level + 1)

        elif isinstance(content, str):
            # Create file with content
            item_path.write_text(f"{content}\n")
            print(f"{'  ' * level}✓ {name}")


def main():
    """Main function to create the entire structure."""
    # Get the current directory or use specified base path
    base_path = Path.cwd()

    print("=" * 60)
    print("Multi-Agent Loan Approval System - Structure Creator")
    print("=" * 60)
    print(f"\nCreating structure in: {base_path}\n")

    try:
        create_structure(str(base_path), STRUCTURE)

        print("\n" + "=" * 60)
        print("✅ Structure created successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Review PROJECT_STRUCTURE.md for detailed information")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Configure .env file with your API keys")
        print("4. Start implementing agents and services")
        print("\nFor more details, see:")
        print("- docs/architecture.md")
        print("- docs/api.md")
        print("- README.md")

    except Exception as e:
        print(f"\n❌ Error creating structure: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
