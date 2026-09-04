-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 046_leave_request_comments.sql
-- Version     : 1.0
-- Description : Comments and discussion history for employee leave requests
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Stores comments associated with a leave request.
--
-- Leave Request
--     = WHAT the employee is requesting
--
-- Leave Request Approval
--     = WHO reviews the request and WHAT decision is made
--
-- Leave Request Comment
--     = CONVERSATION and supporting discussion surrounding the request
--
-- Comments are independent of approval decisions and do not directly change
-- the status of a leave request.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE REQUEST COMMENTS
-- =============================================================================

CREATE TABLE leave_request_comments (

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
    -- Comment Author
    ---------------------------------------------------------------------------

    author_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Comment
    ---------------------------------------------------------------------------

    comment TEXT NOT NULL,

    ---------------------------------------------------------------------------
    -- Parent Comment
    --
    -- Allows threaded replies without requiring a separate conversation table.
    ---------------------------------------------------------------------------

    parent_comment_id CHAR(26),

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

    CONSTRAINT fk_leave_request_comments_request
        FOREIGN KEY (leave_request_id)
        REFERENCES leave_requests(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_request_comments_author
        FOREIGN KEY (author_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_request_comments_parent
        FOREIGN KEY (parent_comment_id)
        REFERENCES leave_request_comments(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_leave_request_comments_content
        CHECK (
            LENGTH(TRIM(comment)) > 0
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_request_comments_request
    ON leave_request_comments(
        leave_request_id,
        created_at
    );

CREATE INDEX idx_leave_request_comments_author
    ON leave_request_comments(
        author_id
    );

CREATE INDEX idx_leave_request_comments_parent
    ON leave_request_comments(
        parent_comment_id
    );

CREATE INDEX idx_leave_request_comments_active
    ON leave_request_comments(
        is_active
    );

COMMIT;