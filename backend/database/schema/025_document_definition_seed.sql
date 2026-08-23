-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 025_document_definition_seed.sql
-- Version     : 1.0
-- Description : Initial global document-definition catalog
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- DOCUMENT DEFINITIONS
-- =============================================================================

INSERT INTO document_definitions (
    id,
    tenant_id,
    country_code,
    document_family,
    display_name,
    is_active
)
VALUES (
    '01M0DEF0000000000000000001',
    NULL,
    NULL,
    'passport',
    'Passport',
    TRUE
)
ON CONFLICT DO NOTHING;

INSERT INTO document_definitions (
    id,
    tenant_id,
    country_code,
    document_family,
    display_name,
    is_active
)
VALUES (
    '01M0DEF0000000000000000002',
    NULL,
    'AE',
    'national id',
    'Emirates ID',
    TRUE
)
ON CONFLICT DO NOTHING;


-- =============================================================================
-- PASSPORT FIELDS
-- =============================================================================

INSERT INTO document_definition_fields (
    id,
    document_definition_id,
    field_code,
    field_label,
    data_type,
    is_required,
    is_extractable,
    sort_order,
    is_hr_updateable,
    target_entity,
    target_field,
    validation_pattern,
    is_active
)
VALUES
(
    '01M0FLD0000000000000000001',
    '01M0DEF0000000000000000001',
    'document_number',
    'Document Number',
    'identifier',
    TRUE,
    TRUE,
    10,
    FALSE,
    NULL,
    NULL,
    '^[A-Z0-9<]{5,20}$',
    TRUE
),
(
    '01M0FLD0000000000000000002',
    '01M0DEF0000000000000000001',
    'surname',
    'Surname',
    'string',
    TRUE,
    TRUE,
    20,
    FALSE,
    NULL,
    NULL,
    NULL,
    TRUE
),
(
    '01M0FLD0000000000000000003',
    '01M0DEF0000000000000000001',
    'given_names',
    'Given Names',
    'string',
    TRUE,
    TRUE,
    30,
    FALSE,
    NULL,
    NULL,
    NULL,
    TRUE
),
(
    '01M0FLD0000000000000000004',
    '01M0DEF0000000000000000001',
    'date_of_birth',
    'Date of Birth',
    'date',
    TRUE,
    TRUE,
    40,
    TRUE,
    'employee_profile',
    'date_of_birth',
    '^[0-9]{4}-[0-9]{2}-[0-9]{2}$',
    TRUE
),
(
    '01M0FLD0000000000000000005',
    '01M0DEF0000000000000000001',
    'nationality',
    'Nationality',
    'string',
    TRUE,
    TRUE,
    50,
    TRUE,
    'employee_profile',
    'nationality',
    '^[A-Z]{3}$',
    TRUE
),
(
    '01M0FLD0000000000000000006',
    '01M0DEF0000000000000000001',
    'sex',
    'Sex',
    'string',
    TRUE,
    TRUE,
    60,
    TRUE,
    'employee_profile',
    'gender',
    '^(male|female|other)$',
    TRUE
),
(
    '01M0FLD0000000000000000007',
    '01M0DEF0000000000000000001',
    'issuing_country',
    'Issuing Country',
    'string',
    TRUE,
    TRUE,
    70,
    FALSE,
    NULL,
    NULL,
    '^[A-Z]{3}$',
    TRUE
),
(
    '01M0FLD0000000000000000008',
    '01M0DEF0000000000000000001',
    'expiry_date',
    'Expiry Date',
    'date',
    TRUE,
    TRUE,
    80,
    FALSE,
    NULL,
    NULL,
    '^[0-9]{4}-[0-9]{2}-[0-9]{2}$',
    TRUE
)
ON CONFLICT DO NOTHING;


-- =============================================================================
-- EMIRATES ID FIELDS
-- =============================================================================

INSERT INTO document_definition_fields (
    id,
    document_definition_id,
    field_code,
    field_label,
    data_type,
    is_required,
    is_extractable,
    sort_order,
    is_hr_updateable,
    target_entity,
    target_field,
    validation_pattern,
    is_active
)
VALUES
(
    '01M0FLD0000000000000000009',
    '01M0DEF0000000000000000002',
    'document_number',
    'Document Number',
    'identifier',
    TRUE,
    TRUE,
    10,
    FALSE,
    NULL,
    NULL,
    '^[0-9-]{5,30}$',
    TRUE
),
(
    '01M0FLD0000000000000000010',
    '01M0DEF0000000000000000002',
    'full_name',
    'Full Name',
    'string',
    TRUE,
    TRUE,
    20,
    FALSE,
    NULL,
    NULL,
    NULL,
    TRUE
),
(
    '01M0FLD0000000000000000011',
    '01M0DEF0000000000000000002',
    'date_of_birth',
    'Date of Birth',
    'date',
    TRUE,
    TRUE,
    30,
    TRUE,
    'employee_profile',
    'date_of_birth',
    '^[0-9]{4}-[0-9]{2}-[0-9]{2}$',
    TRUE
),
(
    '01M0FLD0000000000000000012',
    '01M0DEF0000000000000000002',
    'nationality',
    'Nationality',
    'string',
    TRUE,
    TRUE,
    40,
    TRUE,
    'employee_profile',
    'nationality',
    '^[A-Z]{2,3}$',
    TRUE
),
(
    '01M0FLD0000000000000000013',
    '01M0DEF0000000000000000002',
    'issue_date',
    'Issue Date',
    'date',
    FALSE,
    TRUE,
    50,
    FALSE,
    NULL,
    NULL,
    '^[0-9]{4}-[0-9]{2}-[0-9]{2}$',
    TRUE
),
(
    '01M0FLD0000000000000000014',
    '01M0DEF0000000000000000002',
    'expiry_date',
    'Expiry Date',
    'date',
    FALSE,
    TRUE,
    60,
    FALSE,
    NULL,
    NULL,
    '^[0-9]{4}-[0-9]{2}-[0-9]{2}$',
    TRUE
)
ON CONFLICT DO NOTHING;

COMMIT;