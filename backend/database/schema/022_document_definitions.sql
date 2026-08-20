-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 022_document_definitions.sql
-- Version     : 1.0
-- Description : Generic document definitions and country/tenant terminology
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Defines generic QWOS document families independently from country-specific
-- terminology.
--
-- Examples:
--
--   document_family = 'national_id'
--   country_code    = 'AE'
--   display_name    = 'Emirates ID'
--
--   document_family = 'national_id'
--   country_code    = 'PH'
--   display_name    = 'PhilSys National ID'
--
-- Core QWOS terminology remains generic while tenant/country terminology
-- remains configurable.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- DOCUMENT DEFINITIONS
-- =============================================================================

CREATE TABLE document_definitions (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26),

    ---------------------------------------------------------------------------
    -- Country
    ---------------------------------------------------------------------------

    country_code CHAR(2),

    ---------------------------------------------------------------------------
    -- Generic QWOS Document Family
    ---------------------------------------------------------------------------

    document_family VARCHAR(50) NOT NULL,

    ---------------------------------------------------------------------------
    -- Display Name
    ---------------------------------------------------------------------------

    display_name VARCHAR(150) NOT NULL,

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

    CONSTRAINT chk_document_definition_family
        CHECK (
            LENGTH(TRIM(document_family)) > 0
        ),

    CONSTRAINT chk_document_definition_display_name
        CHECK (
            LENGTH(TRIM(display_name)) > 0
        ),

    CONSTRAINT chk_document_definition_country
        CHECK (
            country_code IS NULL
            OR country_code ~ '^[A-Z]{2}$'
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_document_definitions_tenant
    ON document_definitions(tenant_id);

CREATE INDEX idx_document_definitions_country
    ON document_definitions(country_code);

CREATE INDEX idx_document_definitions_family
    ON document_definitions(document_family);

CREATE INDEX idx_document_definitions_active
    ON document_definitions(is_active);

CREATE UNIQUE INDEX uq_document_definitions_global_family_country
    ON document_definitions(
        COALESCE(tenant_id, '00000000000000000000000000'),
        COALESCE(country_code, '__'),
        document_family
    )
    WHERE deleted_at IS NULL;

COMMIT;