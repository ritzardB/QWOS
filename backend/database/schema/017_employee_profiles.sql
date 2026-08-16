-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 017_employee_profiles.sql
-- Version     : 1.0
-- Description : Core HR Employee Profile
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Stores core personal and contact information for an employee.
--
-- Authentication information belongs to:
--
--     users
--
-- Personal identity belongs to:
--
--     user_profiles
--
-- Workforce identity belongs to:
--
--     employees
--
-- Extended HR modules such as Immigration, Government IDs, Compensation,
-- Benefits, and Documents belong in their respective tables.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- EMPLOYEE PROFILES
-- =============================================================================

CREATE TABLE employee_profiles (

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
    -- Personal Information
    ---------------------------------------------------------------------------

    date_of_birth DATE,

    gender identifier_code,

    nationality identifier_code,

    marital_status identifier_code,

    ---------------------------------------------------------------------------
    -- Personal Contact
    ---------------------------------------------------------------------------

    personal_email email_address,

    personal_phone VARCHAR(30),

    ---------------------------------------------------------------------------
    -- Address
    ---------------------------------------------------------------------------

    address_line_1 TEXT,

    address_line_2 TEXT,

    city VARCHAR(150),

    state_province VARCHAR(150),

    postal_code VARCHAR(30),

    country_code VARCHAR(2),

    ---------------------------------------------------------------------------
    -- Emergency Contact
    ---------------------------------------------------------------------------

    emergency_contact_name person_name,

    emergency_contact_relationship identifier_code,

    emergency_contact_phone VARCHAR(30),

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

    CONSTRAINT uq_employee_profiles_employee
        UNIQUE (employee_id),

    CONSTRAINT fk_employee_profiles_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_employee_profiles_country_code
        CHECK (
            country_code IS NULL
            OR LENGTH(country_code) = 2
        ),

    CONSTRAINT chk_employee_profiles_personal_phone
        CHECK (
            personal_phone IS NULL
            OR LENGTH(TRIM(personal_phone)) > 0
        ),

    CONSTRAINT chk_employee_profiles_emergency_phone
        CHECK (
            emergency_contact_phone IS NULL
            OR LENGTH(TRIM(emergency_contact_phone)) > 0
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_employee_profiles_tenant
    ON employee_profiles(tenant_id);

CREATE INDEX idx_employee_profiles_gender
    ON employee_profiles(gender);

CREATE INDEX idx_employee_profiles_nationality
    ON employee_profiles(nationality);

CREATE INDEX idx_employee_profiles_marital_status
    ON employee_profiles(marital_status);

CREATE INDEX idx_employee_profiles_country
    ON employee_profiles(country_code);

COMMIT;