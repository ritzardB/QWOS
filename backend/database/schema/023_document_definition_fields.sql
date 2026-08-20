-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 023_document_definition_fields.sql
-- Version     : 1.0
-- Description : Fields supported by QWOS document definitions
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Defines the structured fields that can be extracted from a document
-- definition.
--
-- Example:
--
--   national_id
--       document_number
--       full_name
--       date_of_birth
--       nationality
--       issue_date
--       expiry_date
--
--   passport
--       document_number
--       surname
--       given_names
--       date_of_birth
--       nationality
--       sex
--       issuing_country
--       issue_date
--       expiry_date
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- DOCUMENT DEFINITION FIELDS
-- =============================================================================

CREATE TABLE document_definition_fields (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Definition Ownership
    ---------------------------------------------------------------------------

    document_definition_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Field Identity
    ---------------------------------------------------------------------------

    field_code VARCHAR(100) NOT NULL,

    field_label VARCHAR(150) NOT NULL,

    ---------------------------------------------------------------------------
    -- Data Definition
    ---------------------------------------------------------------------------

    data_type VARCHAR(30) NOT NULL,

    ---------------------------------------------------------------------------
    -- Behavior
    ---------------------------------------------------------------------------

    is_required BOOLEAN
        NOT NULL
        DEFAULT FALSE,

    is_extractable BOOLEAN
        NOT NULL
        DEFAULT TRUE,

    sort_order INTEGER
        NOT NULL
        DEFAULT 0,

    ---------------------------------------------------------------------------
    -- Optional Validation
    ---------------------------------------------------------------------------

    validation_pattern TEXT,

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

    CONSTRAINT fk_document_definition_fields_definition
        FOREIGN KEY (document_definition_id)
        REFERENCES document_definitions(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_document_definition_fields_code
        CHECK (
            LENGTH(TRIM(field_code)) > 0
        ),

    CONSTRAINT chk_document_definition_fields_label
        CHECK (
            LENGTH(TRIM(field_label)) > 0
        ),

    CONSTRAINT chk_document_definition_fields_data_type
        CHECK (
            LENGTH(TRIM(data_type)) > 0
        ),

    CONSTRAINT chk_document_definition_fields_sort_order
        CHECK (
            sort_order >= 0
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_document_definition_fields_definition
    ON document_definition_fields(document_definition_id);

CREATE INDEX idx_document_definition_fields_code
    ON document_definition_fields(field_code);

CREATE INDEX idx_document_definition_fields_active
    ON document_definition_fields(is_active);

CREATE INDEX idx_document_definition_fields_order
    ON document_definition_fields(
        document_definition_id,
        sort_order
    );

-- =============================================================================
-- UNIQUENESS
-- =============================================================================

CREATE UNIQUE INDEX uq_document_definition_fields_code
    ON document_definition_fields(
        document_definition_id,
        field_code
    )
    WHERE deleted_at IS NULL;

COMMIT;