-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 020_employee_immigration.sql
-- Version     : 1.0
-- Description : Employee Immigration Records
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Stores employee immigration and work-authorization records.
--
-- Multiple records of the same type are permitted so immigration history
-- can be preserved across renewals and replacements.
--
-- Supporting files and scanned documents belong to the document-management
-- layer and should reference this record rather than being stored here.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- EMPLOYEE IMMIGRATION
-- =============================================================================

CREATE TABLE employee_immigration (

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
    -- Immigration Record
    ---------------------------------------------------------------------------

    immigration_type VARCHAR(50) NOT NULL,

    status VARCHAR(30) NOT NULL,

    ---------------------------------------------------------------------------
    -- Identification
    ---------------------------------------------------------------------------

    document_number VARCHAR(100),

    ---------------------------------------------------------------------------
    -- Sponsorship / Authority
    ---------------------------------------------------------------------------

    sponsor_name VARCHAR(150),

    issuing_authority VARCHAR(150),

    ---------------------------------------------------------------------------
    -- Dates
    ---------------------------------------------------------------------------

    issue_date DATE,

    expiry_date DATE,

    ---------------------------------------------------------------------------
    -- Additional Information
    ---------------------------------------------------------------------------

    notes TEXT,

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

    CONSTRAINT fk_employee_immigration_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_employee_immigration_type
        CHECK (
            LENGTH(TRIM(immigration_type)) > 0
        ),

    CONSTRAINT chk_employee_immigration_status
        CHECK (
            LENGTH(TRIM(status)) > 0
        ),

    CONSTRAINT chk_employee_immigration_dates
        CHECK (
            expiry_date IS NULL
            OR issue_date IS NULL
            OR expiry_date >= issue_date
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_employee_immigration_tenant
    ON employee_immigration(tenant_id);

CREATE INDEX idx_employee_immigration_employee
    ON employee_immigration(employee_id);

CREATE INDEX idx_employee_immigration_type
    ON employee_immigration(immigration_type);

CREATE INDEX idx_employee_immigration_status
    ON employee_immigration(status);

CREATE INDEX idx_employee_immigration_expiry
    ON employee_immigration(expiry_date);

COMMIT;