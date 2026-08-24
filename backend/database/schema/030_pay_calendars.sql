-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 030_pay_calendars.sql
-- Version     : 1.0
-- Description : Generic employer payroll calendar definitions
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- PAY CALENDARS
-- =============================================================================

CREATE TABLE pay_calendars (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Calendar Identity
    ---------------------------------------------------------------------------

    calendar_code VARCHAR(50) NOT NULL,

    calendar_name VARCHAR(150) NOT NULL,

    ---------------------------------------------------------------------------
    -- Payroll Frequency
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
    -- Period Rule
    --
    -- Examples:
    --
    --     calendar_month
    --     fixed_days
    --     rolling_days
    --
    ---------------------------------------------------------------------------

    period_rule identifier_code
        NOT NULL
        DEFAULT 'calendar_month',

    ---------------------------------------------------------------------------
    -- Period Configuration
    --
    -- Used when the selected period rule requires an anchor or boundary.
    --
    ---------------------------------------------------------------------------

    period_anchor_day INTEGER,

    period_length_days INTEGER,

    ---------------------------------------------------------------------------
    -- Country / Currency Context
    --
    -- Optional because the same tenant may operate across jurisdictions.
    --
    ---------------------------------------------------------------------------

    country_code CHAR(2),

    currency_code CHAR(3),

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

    CONSTRAINT uq_pay_calendars_code
        UNIQUE (
            tenant_id,
            calendar_code
        ),

    CONSTRAINT chk_pay_calendars_code
        CHECK (
            LENGTH(TRIM(calendar_code)) > 0
        ),

    CONSTRAINT chk_pay_calendars_name
        CHECK (
            LENGTH(TRIM(calendar_name)) > 0
        ),

    CONSTRAINT chk_pay_calendars_anchor_day
        CHECK (
            period_anchor_day IS NULL
            OR period_anchor_day BETWEEN 1 AND 31
        ),

    CONSTRAINT chk_pay_calendars_period_length
        CHECK (
            period_length_days IS NULL
            OR period_length_days > 0
        ),

    CONSTRAINT chk_pay_calendars_country
        CHECK (
            country_code IS NULL
            OR country_code ~ '^[A-Z]{2}$'
        ),

    CONSTRAINT chk_pay_calendars_currency
        CHECK (
            currency_code IS NULL
            OR currency_code ~ '^[A-Z]{3}$'
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_pay_calendars_active
    ON pay_calendars(is_active);

CREATE INDEX idx_pay_calendars_frequency
    ON pay_calendars(pay_frequency);

CREATE INDEX idx_pay_calendars_rule
    ON pay_calendars(period_rule);

CREATE INDEX idx_pay_calendars_country
    ON pay_calendars(country_code);

COMMIT;