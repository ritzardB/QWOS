-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 027_employee_work_arrangements.sql
-- Version     : 1.0
-- Description : Effective-dated employee work arrangements
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- EMPLOYEE WORK ARRANGEMENTS
-- =============================================================================

CREATE TABLE employee_work_arrangements (

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
    -- Work Arrangement
    --
    -- Supported values:
    --
    --     office
    --     hybrid
    --     remote
    --
    ---------------------------------------------------------------------------

    work_arrangement identifier_code
        NOT NULL
        DEFAULT 'office',

    ---------------------------------------------------------------------------
    -- Effective Dates
    ---------------------------------------------------------------------------

    effective_from DATE NOT NULL,

    effective_until DATE,

    ---------------------------------------------------------------------------
    -- Status
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

    CONSTRAINT fk_employee_work_arrangements_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_employee_work_arrangements_type
        CHECK (
            work_arrangement IN (
                'office',
                'hybrid',
                'remote'
            )
        ),

    CONSTRAINT chk_employee_work_arrangements_dates
        CHECK (
            effective_until IS NULL
            OR effective_until >= effective_from
        ),

    CONSTRAINT uq_employee_work_arrangements_start
        UNIQUE (
            tenant_id,
            employee_id,
            effective_from
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_employee_work_arrangements_employee
    ON employee_work_arrangements(employee_id);

CREATE INDEX idx_employee_work_arrangements_active
    ON employee_work_arrangements(is_active);

CREATE INDEX idx_employee_work_arrangements_effective
    ON employee_work_arrangements(
        employee_id,
        effective_from,
        effective_until
    );

COMMIT;