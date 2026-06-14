# Spreetail Shared Expenses — Scope Document

This document outlines the design, features, and capabilities of the Spreetail Shared Expenses web application.

## 1. System Overview

Spreetail Shared Expenses is a complete, monolithic, server-rendered web application designed to track, split, and audit shared expenses within social or residential groups.

- **Stack**: FastAPI + PostgreSQL + SQLAlchemy 2.0 (asyncpg) + Alembic + Jinja2 + HTMX + Vanilla CSS
- **Design Philosophy**: High performance, strict data integrity, zero placeholders, rich monochrome financial aesthetics, and interactive responsiveness without SPA complexities.

---

## 2. Key Features & Capabilities

### 2.1 User Authentication & Session Management
- Secure registration with minimum 8-character password constraint and email uniqueness check.
- Cookie-based authentication using cryptographically signed tokens (`itsdangerous`).
- Middleware-driven authorization guard and cookie-based flash notifications.

### 2.2 Group Management
- Dynamic creation of expense-sharing groups (e.g., "Flat Expenses").
- Membership controls allowing users to join or leave. Removal of members does not delete historical records; instead, it is date-gated.
- Temporal member gating ensures users are only liable for expenses incurred during their active membership periods.

### 2.3 Multi-Currency Expense Logging
- Support for dual currencies: **INR** (Indian Rupee) and **USD** (US Dollar).
- Automatic daily exchange rate conversion to a base currency (INR) for balance calculations.
- Soft-deletion support for audit trails.

### 2.4 Expense Split Strategies
- **Equal**: Divides total amount equally among all selected group members.
- **Exact**: Specifies exact amounts for each member (validated to ensure the sum matches the total).
- **Percentage**: Divides cost based on user-allocated percentages (validated to ensure sum is exactly 100%).
- **Shares**: Allocates portions relative to specified share values.
- Remainder absorption automatically adds fractions of cents/paise to the largest share to guarantee mathematical consistency (no lost pennies).

### 2.5 Real-time Balance Calculation & Debt Minimization
- Continuous processing of group expenses and payments.
- Greedy-algorithm transaction minimizer to simplify debts (minimizes the number of payment transfers required to settle the group).
- Individual member breakdown views showing total spent, owed, and net positions.

### 2.6 CSV Importer & Audit Engine
- Transactional upload of structured CSV spreadsheets containing expense data.
- **13 Anomaly Detection Rules** flag duplicates, ambiguous names, invalid rates, negative amounts, out-of-bounds membership dates, and format variations.
- Dynamic review board (HTMX powered) allows bulk audit approvals or exclusions.
