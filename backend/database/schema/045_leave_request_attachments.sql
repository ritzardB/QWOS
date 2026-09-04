-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 045_leave_request_attachments.sql
-- Version     : 1.0
-- Description : Supporting document metadata for employee leave requests
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Stores metadata and storage references for documents attached to a leave
-- request.
--
-- The actual file contents MUST NOT be stored in this table.
--
-- Examples:
--     - Medical certificate
--     - Supporting documentation
--     - Travel documentation
--     - Other company-required evidence
--
-- Leave Request
--     = WHAT the employee is requesting
--
-- Leave Request Attachment
--     = SUPPORTING DOCUMENTATION for the request
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE REQUEST ATTACHMENTS
-- =============================================================================

CREATE TABLE leave_request_attachments (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Leave Request
    ---------------------------------------------------------------------------

    leave_request_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Employee
    ---------------------------------------------------------------------------

    employee_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- File Metadata
    ---------------------------------------------------------------------------

    file_name VARCHAR(255) NOT NULL,

    original_file_name VARCHAR(255) NOT NULL,

    mime_type VARCHAR(150) NOT NULL,

    file_extension VARCHAR(20),

    file_size_bytes BIGINT NOT NULL,

    ---------------------------------------------------------------------------
    -- Storage Reference
    --
    -- Identifies where the physical file is stored.
    --
    -- Examples:
    --     object-storage key
    --     document-storage identifier
    --     encrypted file reference
    ---------------------------------------------------------------------------

    storage_provider VARCHAR(50) NOT NULL,

    storage_key VARCHAR(500) NOT NULL,

    ---------------------------------------------------------------------------
    -- File Integrity
    --
    -- SHA-256 or equivalent content hash.
    ---------------------------------------------------------------------------

    file_hash VARCHAR(128),

    ---------------------------------------------------------------------------
    -- Document Classification
    ---------------------------------------------------------------------------

    attachment_type identifier_code
        NOT NULL
        DEFAULT 'supporting_document',

    ---------------------------------------------------------------------------
    -- Upload Information
    ---------------------------------------------------------------------------

    uploaded_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    uploaded_by CHAR(26) NOT NULL,

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

    CONSTRAINT fk_leave_request_attachments_request
        FOREIGN KEY (leave_request_id)
        REFERENCES leave_requests(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_request_attachments_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_leave_request_attachments_file_size
        CHECK (
            file_size_bytes > 0
        ),

    CONSTRAINT chk_leave_request_attachments_storage_provider
        CHECK (
            LENGTH(TRIM(storage_provider)) > 0
        ),

    CONSTRAINT chk_leave_request_attachments_storage_key
        CHECK (
            LENGTH(TRIM(storage_key)) > 0
        ),

    CONSTRAINT chk_leave_request_attachments_file_name
        CHECK (
            LENGTH(TRIM(file_name)) > 0
        ),

    CONSTRAINT chk_leave_request_attachments_original_name
        CHECK (
            LENGTH(TRIM(original_file_name)) > 0
        ),

    CONSTRAINT chk_leave_request_attachments_mime_type
        CHECK (
            LENGTH(TRIM(mime_type)) > 0
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_request_attachments_request
    ON leave_request_attachments(
        leave_request_id
    );

CREATE INDEX idx_leave_request_attachments_employee
    ON leave_request_attachments(
        employee_id
    );

CREATE INDEX idx_leave_request_attachments_type
    ON leave_request_attachments(
        attachment_type
    );

CREATE INDEX idx_leave_request_attachments_active
    ON leave_request_attachments(
        is_active
    );

CREATE INDEX idx_leave_request_attachments_uploaded
    ON leave_request_attachments(
        uploaded_at
    );

CREATE INDEX idx_leave_request_attachments_storage
    ON leave_request_attachments(
        storage_provider,
        storage_key
    );

COMMIT;