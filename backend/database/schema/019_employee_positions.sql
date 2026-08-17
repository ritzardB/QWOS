-- -- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 019_employee_positions.sql
-- Version     : 1.0
-- Description : Employee Organizational Position
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Stores an employee's organizational position/title.
--
-- Reporting relationships belong to:
--
--     employee_reporting_relationships
--
-- Organizational position belongs to:
--
--     employee_positions
--
-- This separation allows an employee to change positions over time without
-- changing the reporting relationship model.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- EMPLOYEE POSITIONS
-- =============================================================================

CREATE TABLE employee_positions (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Employee Ownership
    ---------------------------------------------------------------------------

    employee_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Position
    ---------------------------------------------------------------------------

    job_title VARCHAR(150) NOT NULL,

    organizational_level VARCHAR(50) NOT NULL,

    ---------------------------------------------------------------------------
    -- Effective Dating
    ---------------------------------------------------------------------------

    effective_from DATE NOT NULL,

    effective_to DATE,

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

    CONSTRAINT fk_employee_positions_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_employee_positions_job_title
        CHECK (
            LENGTH(TRIM(job_title)) > 0
        ),

    CONSTRAINT chk_employee_positions_organizational_level
        CHECK (
            LENGTH(TRIM(organizational_level)) > 0
        ),

    CONSTRAINT chk_employee_positions_effective_dates
        CHECK (
            effective_to IS NULL
            OR effective_to >= effective_from
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_employee_positions_tenant
    ON employee_positions(tenant_id);

CREATE INDEX idx_employee_positions_employee
    ON employee_positions(employee_id);

CREATE INDEX idx_employee_positions_level
    ON employee_positions(organizational_level);

CREATE INDEX idx_employee_positions_effective_from
    ON employee_positions(effective_from);

COMMIT;