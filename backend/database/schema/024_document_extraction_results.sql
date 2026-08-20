-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 024_document_extraction_results.sql
-- Version     : 1.0
-- Description : Machine-extracted values from employee documents
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Stores extraction results produced from an EmployeeDocument.
--
-- The extraction result preserves:
--
--   - the source employee document
--   - the document definition field
--   - the raw machine-detected value
--   - the normalized value
--   - extraction confidence
--   - extraction source
--
-- These values are NOT automatically treated as approved HR data.
-- Human review / approval will be implemented by a later application slice.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- DOCUMENT EXTRACTION RESULTS
-- =============================================================================

CREATE TABLE document_extraction_results (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Source Document
    ---------------------------------------------------------------------------

    employee_document_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Definition Field
    ---------------------------------------------------------------------------

    document_definition_field_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Extracted Values
    ---------------------------------------------------------------------------

    raw_value TEXT,

    normalized_value TEXT,

    ---------------------------------------------------------------------------
    -- Extraction Metadata
    ---------------------------------------------------------------------------

    confidence NUMERIC(5,4),

    source VARCHAR(50) NOT NULL,

    ---------------------------------------------------------------------------
    -- Lifecycle
    ---------------------------------------------------------------------------

    extracted_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

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

    CONSTRAINT fk_document_extraction_results_document
        FOREIGN KEY (employee_document_id)
        REFERENCES employee_documents(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_document_extraction_results_field
        FOREIGN KEY (document_definition_field_id)
        REFERENCES document_definition_fields(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_document_extraction_results_source
        CHECK (
            LENGTH(TRIM(source)) > 0
        ),

    CONSTRAINT chk_document_extraction_results_confidence
        CHECK (
            confidence IS NULL
            OR (
                confidence >= 0
                AND confidence <= 1
            )
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_document_extraction_results_tenant
    ON document_extraction_results(tenant_id);

CREATE INDEX idx_document_extraction_results_document
    ON document_extraction_results(employee_document_id);

CREATE INDEX idx_document_extraction_results_field
    ON document_extraction_results(document_definition_field_id);

CREATE INDEX idx_document_extraction_results_source
    ON document_extraction_results(source);

CREATE INDEX idx_document_extraction_results_extracted_at
    ON document_extraction_results(extracted_at);

-- =============================================================================
-- ACTIVE-RESULT LOOKUP
-- =============================================================================

CREATE INDEX idx_document_extraction_results_active_field
    ON document_extraction_results(
        employee_document_id,
        document_definition_field_id
    )
    WHERE deleted_at IS NULL;

COMMIT;