-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 031_pay_periods.sql
-- Version     : 1.0
-- Description : Generated payroll periods based on pay calendar definitions
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- PAY PERIODS
-- =============================================================================

CREATE TABLE pay_periods (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Pay Calendar
    ---------------------------------------------------------------------------

    pay_calendar_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Period Identity
    ---------------------------------------------------------------------------

    period_number INTEGER NOT NULL,

    ---------------------------------------------------------------------------
    -- Period Dates
    ---------------------------------------------------------------------------

    period_start DATE NOT NULL,

    period_end DATE NOT NULL,

    pay_date DATE,

    ---------------------------------------------------------------------------
    -- Period Status
    --
    -- Examples:
    --
    --     open
    --     processing
    --     closed
    --     paid
    --
    ---------------------------------------------------------------------------

    status identifier_code
        NOT NULL
        DEFAULT 'open',

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

    CONSTRAINT fk_pay_periods_calendar
        FOREIGN KEY (pay_calendar_id)
        REFERENCES pay_calendars(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_pay_periods_number
        CHECK (
            period_number > 0
        ),

    CONSTRAINT chk_pay_periods_dates
        CHECK (
            period_end >= period_start
        ),

    CONSTRAINT chk_pay_periods_pay_date
        CHECK (
            pay_date IS NULL
            OR pay_date >= period_end
        ),

    CONSTRAINT uq_pay_periods_calendar_number
        UNIQUE (
            tenant_id,
            pay_calendar_id,
            period_number
        ),

    CONSTRAINT uq_pay_periods_calendar_dates
        UNIQUE (
            tenant_id,
            pay_calendar_id,
            period_start,
            period_end
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_pay_periods_calendar
    ON pay_periods(pay_calendar_id);

CREATE INDEX idx_pay_periods_dates
    ON pay_periods(period_start, period_end);

CREATE INDEX idx_pay_periods_status
    ON pay_periods(status);

COMMIT;