-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 048_leave_holiday_calendars.sql
-- Version     : 1.0
-- Description : Tenant holiday calendar definitions
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Defines reusable holiday calendars for a tenant.
--
-- Examples:
--     UAE Public Holidays
--     UAE Abu Dhabi Holidays
--     Philippines Public Holidays
--     Company Holidays
--
-- Individual holiday dates are stored in:
--
--     047_leave_holidays.sql
--
-- Relationship:
--
--     Holiday Calendar
--            │
--            ├── Holiday Date
--            ├── Holiday Date
--            └── Holiday Date
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE HOLIDAY CALENDARS
-- =============================================================================

CREATE TABLE leave_holiday_calendars (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Calendar Identification
    ---------------------------------------------------------------------------

    calendar_code VARCHAR(50) NOT NULL,

    calendar_name VARCHAR(150) NOT NULL,

    ---------------------------------------------------------------------------
    -- Calendar Description
    ---------------------------------------------------------------------------

    description TEXT,

    ---------------------------------------------------------------------------
    -- Calendar Scope
    --
    -- public   = government/public holiday calendar
    -- company  = company-defined calendar
    -- custom   = tenant-defined calendar
    ---------------------------------------------------------------------------

    calendar_type identifier_code NOT NULL DEFAULT 'public',

    ---------------------------------------------------------------------------
    -- Location
    --
    -- Optional location associated with the calendar.
    -- Examples:
    --     AE
    --     AE-AUH
    --     PH
    --     PH-CAV
    ---------------------------------------------------------------------------

    location_code VARCHAR(50),

    ---------------------------------------------------------------------------
    -- Calendar Year
    --
    -- NULL allows calendars that span multiple years.
    -- A populated value is useful for annual holiday calendars.
    ---------------------------------------------------------------------------

    calendar_year INTEGER,

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

    CONSTRAINT chk_leave_holiday_calendars_code
        CHECK (
            LENGTH(TRIM(calendar_code)) > 0
        ),

    CONSTRAINT chk_leave_holiday_calendars_name
        CHECK (
            LENGTH(TRIM(calendar_name)) > 0
        ),

    CONSTRAINT chk_leave_holiday_calendars_type
        CHECK (
            calendar_type IN (
                'public',
                'company',
                'custom'
            )
        ),

    CONSTRAINT chk_leave_holiday_calendars_year
        CHECK (
            calendar_year IS NULL
            OR calendar_year BETWEEN 1900 AND 2200
        ),

    CONSTRAINT uq_leave_holiday_calendars_code
        UNIQUE (
            tenant_id,
            calendar_code
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_holiday_calendars_type
    ON leave_holiday_calendars(
        tenant_id,
        calendar_type
    );

CREATE INDEX idx_leave_holiday_calendars_location
    ON leave_holiday_calendars(
        tenant_id,
        location_code
    );

CREATE INDEX idx_leave_holiday_calendars_year
    ON leave_holiday_calendars(
        tenant_id,
        calendar_year
    );

CREATE INDEX idx_leave_holiday_calendars_active
    ON leave_holiday_calendars(
        is_active
    );

COMMIT;