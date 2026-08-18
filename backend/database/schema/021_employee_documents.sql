-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 021_employee_documents.sql
-- Version     : 1.0
-- Description : Employee HR Documents
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Stores metadata for employee HR documents.
--
-- Binary file contents are stored outside PostgreSQL. This table stores the
-- document metadata and the reference required to retrieve the file.
--
-- Documents may optionally reference an employee immigration record.
-- This allows general HR documents and immigration-related documents to use
-- the same document-management model.
--
-- QWOS Stored Filename Convention:
--
-- {EMPLOYEE_NUMBER}_{DOCUMENT_CATEGORY}_{ISSUE_DATE}_{EXPIRY_DATE}_{VERSION}.{EXT}
--
-- Examples:
--
-- QW-00002_RESIDENCE-VISA_2026-08-16_2027-08-15_V01.pdf
-- QW-00002_WORK-PERMIT_2026-08-16_2027-08-15_V01.pdf
-- QW-00002_PASSPORT_2024-03-10_2034-03-09_V01.pdf
-- QW-00002_EMPLOYMENT-CONTRACT_2026-02-01_V01.pdf
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- EMPLOYEE DOCUMENTS
-- =============================================================================

CREATE TABLE employee_documents (

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
    -- Optional Immigration Association
    ---------------------------------------------------------------------------

    immigration_id CHAR(26),

    ---------------------------------------------------------------------------
    -- Human-Friendly Document Identity
    ---------------------------------------------------------------------------

    document_name VARCHAR(150) NOT NULL,

    document_category VARCHAR(50) NOT NULL,

    ---------------------------------------------------------------------------
    -- Uploaded File Information
    ---------------------------------------------------------------------------

    original_filename VARCHAR(255) NOT NULL,

    stored_filename VARCHAR(255) NOT NULL,

    mime_type VARCHAR(150),

    file_extension VARCHAR(20),

    file_size_bytes BIGINT NOT NULL,

    ---------------------------------------------------------------------------
    -- Storage Reference
    ---------------------------------------------------------------------------

    storage_provider VARCHAR(50) NOT NULL,

    storage_key TEXT NOT NULL,

    ---------------------------------------------------------------------------
    -- Integrity
    ---------------------------------------------------------------------------

    checksum_sha256 CHAR(64) NOT NULL,

    ---------------------------------------------------------------------------
    -- Document Lifecycle
    ---------------------------------------------------------------------------

    document_version INTEGER
        NOT NULL
        DEFAULT 1,

    uploaded_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    uploaded_by CHAR(26),

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
    -- Relationships
    ---------------------------------------------------------------------------

    CONSTRAINT fk_employee_documents_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_employee_documents_immigration
        FOREIGN KEY (immigration_id)
        REFERENCES employee_immigration(id)
        ON DELETE RESTRICT,

    ---------------------------------------------------------------------------
    -- Validation
    ---------------------------------------------------------------------------

    CONSTRAINT chk_employee_documents_name
        CHECK (
            LENGTH(TRIM(document_name)) > 0
        ),

    CONSTRAINT chk_employee_documents_category
        CHECK (
            LENGTH(TRIM(document_category)) > 0
        ),

    CONSTRAINT chk_employee_documents_original_filename
        CHECK (
            LENGTH(TRIM(original_filename)) > 0
        ),

    CONSTRAINT chk_employee_documents_stored_filename
        CHECK (
            LENGTH(TRIM(stored_filename)) > 0
        ),

    CONSTRAINT chk_employee_documents_file_size
        CHECK (
            file_size_bytes > 0
        ),

    CONSTRAINT chk_employee_documents_storage_provider
        CHECK (
            LENGTH(TRIM(storage_provider)) > 0
        ),

    CONSTRAINT chk_employee_documents_storage_key
        CHECK (
            LENGTH(TRIM(storage_key)) > 0
        ),

    CONSTRAINT chk_employee_documents_checksum
        CHECK (
            checksum_sha256 ~ '^[0-9A-Fa-f]{64}$'
        ),

    CONSTRAINT chk_employee_documents_version
        CHECK (
            document_version > 0
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_employee_documents_tenant
    ON employee_documents(tenant_id);

CREATE INDEX idx_employee_documents_employee
    ON employee_documents(employee_id);

CREATE INDEX idx_employee_documents_immigration
    ON employee_documents(immigration_id);

CREATE INDEX idx_employee_documents_category
    ON employee_documents(document_category);

CREATE INDEX idx_employee_documents_uploaded_at
    ON employee_documents(uploaded_at);

CREATE INDEX idx_employee_documents_checksum
    ON employee_documents(checksum_sha256);

CREATE INDEX idx_employee_documents_storage_key
    ON employee_documents(storage_key);

-- =============================================================================
-- Audit Trigger
-- =============================================================================
--
-- The existing global audit trigger will update updated_at automatically when
-- the table is included in the trigger configuration.
--
-- =============================================================================

COMMIT;