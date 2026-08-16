-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 016_employees.sql
-- Version     : 1.0
-- Description : HR Employee Records
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Represents the HR workforce record associated with a person.
--
-- Authentication information belongs to:
--
--     users
--
-- Personal profile information belongs to:
--
--     user_profiles
--
-- HR workforce information belongs to:
--
--     employees
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- EMPLOYEES
-- =============================================================================

CREATE TABLE employees (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Authentication / Identity Link
    --
    -- Nullable because an HR administrator may create an employee record
    -- before the employee receives a QWOS authentication account.
    ---------------------------------------------------------------------------

    user_id CHAR(26),

    ---------------------------------------------------------------------------
    -- Workforce Identity
    ---------------------------------------------------------------------------

    employee_number VARCHAR(50) NOT NULL,

    ---------------------------------------------------------------------------
    -- Employment Dates
    ---------------------------------------------------------------------------

    hire_date DATE,

    ---------------------------------------------------------------------------
    -- Employment Classification
    ---------------------------------------------------------------------------

    employment_status identifier_code
        NOT NULL
        DEFAULT 'active',

    employment_type identifier_code
        NOT NULL
        DEFAULT 'full_time',

    ---------------------------------------------------------------------------
    -- Work Contact
    ---------------------------------------------------------------------------

    work_email email_address,

    work_phone VARCHAR(30),

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

    CONSTRAINT uq_employees_employee_number
        UNIQUE (tenant_id, employee_number),

    CONSTRAINT uq_employees_user
        UNIQUE (tenant_id, user_id),

    CONSTRAINT fk_employees_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_employees_work_phone
        CHECK (
            work_phone IS NULL
            OR LENGTH(TRIM(work_phone)) > 0
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_employees_user
    ON employees(user_id);

CREATE INDEX idx_employees_status
    ON employees(employment_status);

CREATE INDEX idx_employees_type
    ON employees(employment_type);

CREATE INDEX idx_employees_hire_date
    ON employees(hire_date);

COMMIT;