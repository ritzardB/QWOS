-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 029_employee_work_agreements.sql
-- Version     : 1.0
-- Description : Effective-dated employee work agreements and compensation
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- EMPLOYEE WORK AGREEMENTS
-- =============================================================================

CREATE TABLE employee_work_agreements (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Employee
    ---------------------------------------------------------------------------

    employee_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Agreement Identity
    ---------------------------------------------------------------------------

    agreement_type identifier_code
        NOT NULL
        DEFAULT 'standard',

    ---------------------------------------------------------------------------
    -- Effective Dates
    ---------------------------------------------------------------------------

    effective_from DATE NOT NULL,

    effective_until DATE,

    ---------------------------------------------------------------------------
    -- Compensation Basis
    --
    -- Examples:
    --
    --     monthly
    --     daily
    --     hourly
    --     task_based
    --     commission
    --     mixed
    --
    ---------------------------------------------------------------------------

    compensation_basis identifier_code
        NOT NULL
        DEFAULT 'monthly',

    ---------------------------------------------------------------------------
    -- Base Compensation
    ---------------------------------------------------------------------------

    base_salary NUMERIC(18, 2),

    salary_currency CHAR(3),

    ---------------------------------------------------------------------------
    -- Pay Frequency
    --
    -- Examples:
    --
    --     monthly
    --     semi_monthly
    --     biweekly
    --     weekly
    --     daily
    --
    ---------------------------------------------------------------------------

    pay_frequency identifier_code
        NOT NULL
        DEFAULT 'monthly',

    ---------------------------------------------------------------------------
    -- Lifecycle
    ---------------------------------------------------------------------------

    is_active BOOLEAN
        NOT NULL
        DEFAULT TRUE,

    ---------------------------------------------------------------------------
    -- Audit
    ---------------------------------------------------------------------------

    created_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    created_by CHAR(26),

    updated_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    updated_by CHAR(26),

    deleted_at TIMESTAMPTZ,

    deleted_by CHAR(26),

    ---------------------------------------------------------------------------
    -- Concurrency
    ---------------------------------------------------------------------------

    version INTEGER
        NOT NULL
        DEFAULT 1,

    ---------------------------------------------------------------------------
    -- Constraints
    ---------------------------------------------------------------------------

    CONSTRAINT fk_employee_work_agreements_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_employee_work_agreements_dates
        CHECK (
            effective_until IS NULL
            OR effective_until >= effective_from
        ),

    CONSTRAINT chk_employee_work_agreements_salary
        CHECK (
            base_salary IS NULL
            OR base_salary >= 0
        ),

    CONSTRAINT chk_employee_work_agreements_currency
        CHECK (
            base_salary IS NULL
            OR salary_currency IS NOT NULL
        ),

    CONSTRAINT chk_employee_work_agreements_currency_format
        CHECK (
            salary_currency IS NULL
            OR salary_currency ~ '^[A-Z]{3}$'
        ),

    CONSTRAINT uq_employee_work_agreements_start
        UNIQUE (
            tenant_id,
            employee_id,
            effective_from
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_employee_work_agreements_employee
    ON employee_work_agreements(employee_id);

CREATE INDEX idx_employee_work_agreements_active
    ON employee_work_agreements(is_active);

CREATE INDEX idx_employee_work_agreements_compensation
    ON employee_work_agreements(compensation_basis);

CREATE INDEX idx_employee_work_agreements_pay_frequency
    ON employee_work_agreements(pay_frequency);

CREATE INDEX idx_employee_work_agreements_effective
    ON employee_work_agreements(
        employee_id,
        effective_from,
        effective_until
    );

COMMIT;