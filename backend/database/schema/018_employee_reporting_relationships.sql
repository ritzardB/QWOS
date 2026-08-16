-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 018_employee_reporting_relationships.sql
-- Version     : 1.0
-- Description : HR Employee Reporting Relationships
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Represents reporting relationships between employees.
--
-- Employees may have multiple reporting relationships over time and may
-- participate in different relationship types such as:
--
--     PRIMARY_MANAGER
--     FUNCTIONAL_MANAGER
--     MATRIX_MANAGER
--
-- The active primary-manager relationship represents the direct reporting
-- hierarchy used by HR workflows.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- EMPLOYEE REPORTING RELATIONSHIPS
-- =============================================================================

CREATE TABLE employee_reporting_relationships (

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
    -- Manager
    ---------------------------------------------------------------------------

    manager_employee_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Relationship
    ---------------------------------------------------------------------------

    relationship_type identifier_code
        NOT NULL
        DEFAULT 'primary_manager',

    ---------------------------------------------------------------------------
    -- Effective Dates
    ---------------------------------------------------------------------------

    effective_from DATE
        NOT NULL,

    effective_to DATE,

    ---------------------------------------------------------------------------
    -- Primary Relationship
    ---------------------------------------------------------------------------

    is_primary BOOLEAN
        NOT NULL
        DEFAULT FALSE,

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

    CONSTRAINT fk_employee_reporting_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_employee_reporting_manager
        FOREIGN KEY (manager_employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_employee_reporting_not_self
        CHECK (
            employee_id <> manager_employee_id
        ),

    CONSTRAINT chk_employee_reporting_dates
        CHECK (
            effective_to IS NULL
            OR effective_to >= effective_from
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_employee_reporting_employee
    ON employee_reporting_relationships(employee_id);

CREATE INDEX idx_employee_reporting_manager
    ON employee_reporting_relationships(manager_employee_id);

CREATE INDEX idx_employee_reporting_type
    ON employee_reporting_relationships(relationship_type);

CREATE INDEX idx_employee_reporting_effective
    ON employee_reporting_relationships(
        employee_id,
        effective_from,
        effective_to
    );

-- =============================================================================
-- ACTIVE PRIMARY MANAGER
-- =============================================================================

CREATE UNIQUE INDEX uq_employee_reporting_active_primary_manager
    ON employee_reporting_relationships(employee_id)
    WHERE
        relationship_type = 'primary_manager'
        AND is_primary = TRUE
        AND deleted_at IS NULL
        AND effective_to IS NULL;

COMMIT;