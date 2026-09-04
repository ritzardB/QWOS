-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 047_leave_holidays.sql
-- Version     : 1.0
-- Description : Tenant holiday calendar and holiday definitions
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Stores holidays applicable to a tenant.
--
-- A holiday may represent:
--     - Public holiday
--     - Company holiday
--     - Observed holiday
--     - Other organization-defined non-working day
--
-- Holiday records are maintained independently from leave requests so that
-- multiple employees and leave calculations can reference the same calendar.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE HOLIDAYS
-- =============================================================================

CREATE TABLE leave_holidays (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Holiday
    ---------------------------------------------------------------------------

    holiday_date DATE NOT NULL,

    holiday_name VARCHAR(150) NOT NULL,

    ---------------------------------------------------------------------------
    -- Holiday Type
    --
    -- public   = government/public holiday
    -- company  = organization-defined holiday
    -- observed = observed replacement holiday
    -- other    = other approved non-working day
    ---------------------------------------------------------------------------

    holiday_type identifier_code NOT NULL DEFAULT 'public',

    ---------------------------------------------------------------------------
    -- Optional Description
    ---------------------------------------------------------------------------

    description TEXT,

    ---------------------------------------------------------------------------
    -- Optional Location
    --
    -- Allows a tenant to distinguish holidays applicable to a particular
    -- country, region, city, or office.
    ---------------------------------------------------------------------------

    location_code VARCHAR(50),

    ---------------------------------------------------------------------------
    -- Working-Day Override
    --
    -- TRUE  = date remains a working day
    -- FALSE = date is treated as a non-working holiday
    --
    -- This provides flexibility for organizations that observe a holiday
    -- differently from the official calendar.
    ---------------------------------------------------------------------------

    is_working_day BOOLEAN
        NOT NULL
        DEFAULT FALSE,

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

    CONSTRAINT chk_leave_holidays_name
        CHECK (
            LENGTH(TRIM(holiday_name)) > 0
        ),

    CONSTRAINT chk_leave_holidays_type
        CHECK (
            holiday_type IN (
                'public',
                'company',
                'observed',
                'other'
            )
        ),

    CONSTRAINT uq_leave_holidays_date
        UNIQUE (
            tenant_id,
            holiday_date,
            location_code
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_holidays_date
    ON leave_holidays(
        tenant_id,
        holiday_date
    );

CREATE INDEX idx_leave_holidays_type
    ON leave_holidays(
        holiday_type
    );

CREATE INDEX idx_leave_holidays_location
    ON leave_holidays(
        tenant_id,
        location_code
    );

CREATE INDEX idx_leave_holidays_active
    ON leave_holidays(
        is_active
    );

COMMIT;