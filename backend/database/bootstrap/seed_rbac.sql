-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- Database Bootstrap
--
-- File        : seed_rbac.sql
-- Description : Initial RBAC roles, permissions, and bootstrap assignment.
--
-- Author      : Richard Balabarcon
-- =============================================================================

BEGIN;

-- =============================================================================
-- Bootstrap Context
-- =============================================================================

\set tenant_id '''01KZYRPZANTQJBZYE7KS4DCRGW'''
\set admin_user_id '''01KZYTCWRF8S12V28R9NX6JXS5'''

-- =============================================================================
-- Roles
-- =============================================================================

\set role_system_admin '''01M0ARWRFEMQE2T0D9Y2N45GAX'''
\set role_hr_manager   '''01M0ARWRFEMQE2T0D9Y2N45GAY'''
\set role_hr_officer   '''01M0ARWRFEMQE2T0D9Y2N45GAZ'''
\set role_manager      '''01M0ARWRFEMQE2T0D9Y2N45GB0'''
\set role_employee     '''01M0ARWRFEMQE2T0D9Y2N45GB1'''

-- =============================================================================
-- Permissions
-- =============================================================================

\set perm_employee_view   '''01M0ARWRFEMQE2T0D9Y2N45GB2'''
\set perm_employee_create '''01M0ARWRFEMQE2T0D9Y2N45GB3'''
\set perm_employee_update '''01M0ARWRFEMQE2T0D9Y2N45GB4'''

\set perm_profile_view    '''01M0ARWRFEMQE2T0D9Y2N45GB5'''
\set perm_profile_create  '''01M0ARWRFEMQE2T0D9Y2N45GB6'''
\set perm_profile_update  '''01M0ARWRFEMQE2T0D9Y2N45GB7'''

\set perm_position_view   '''01M0ARWRFEMQE2T0D9Y2N45GB8'''
\set perm_position_create '''01M0ARWRFEMQE2T0D9Y2N45GB9'''
\set perm_position_update '''01M0ARWRFEMQE2T0D9Y2N45GBA'''

\set perm_reporting_view   '''01M0ARWRFEMQE2T0D9Y2N45GBB'''
\set perm_reporting_update '''01M0ARWRFEMQE2T0D9Y2N45GBC'''

\set perm_immigration_view   '''01M0ARWRFEMQE2T0D9Y2N45GBD'''
\set perm_immigration_create '''01M0ARWRFEMQE2T0D9Y2N45GBE'''
\set perm_immigration_update '''01M0ARWRFEMQE2T0D9Y2N45GBF'''

\set perm_document_view   '''01M0ARWRFEMQE2T0D9Y2N45GBG'''
\set perm_document_upload '''01M0ARWRFEMQE2T0D9Y2N45GBH'''
\set perm_document_update '''01M0ARWRFEMQE2T0D9Y2N45GBJ'''
\set perm_document_delete '''01M0ARWRFEMQE2T0D9Y2N45GBK'''

-- =============================================================================
-- User Role Assignment
-- =============================================================================

\set user_role_admin '''01M0ARWRFEMQE2T0D9Y2N45GBM'''

-- =============================================================================
-- Role Permission Assignment IDs
-- =============================================================================

\set rp001 '''01M0AS075A6E3YEACZC720B2P6'''
\set rp002 '''01M0AS075A6E3YEACZC720B2P7'''
\set rp003 '''01M0AS075A6E3YEACZC720B2P8'''
\set rp004 '''01M0AS075A6E3YEACZC720B2P9'''
\set rp005 '''01M0AS075A6E3YEACZC720B2PA'''
\set rp006 '''01M0AS075A6E3YEACZC720B2PB'''
\set rp007 '''01M0AS075A6E3YEACZC720B2PC'''
\set rp008 '''01M0AS075A6E3YEACZC720B2PD'''
\set rp009 '''01M0AS075A6E3YEACZC720B2PE'''
\set rp010 '''01M0AS075A6E3YEACZC720B2PF'''
\set rp011 '''01M0AS075A6E3YEACZC720B2PG'''
\set rp012 '''01M0AS075A6E3YEACZC720B2PH'''
\set rp013 '''01M0AS075A6E3YEACZC720B2PJ'''
\set rp014 '''01M0AS075A6E3YEACZC720B2PK'''
\set rp015 '''01M0AS075A6E3YEACZC720B2PM'''
\set rp016 '''01M0AS075A6E3YEACZC720B2PN'''
\set rp017 '''01M0AS075A6E3YEACZC720B2PP'''
\set rp018 '''01M0AS075A6E3YEACZC720B2PQ'''

-- =============================================================================
-- Roles
-- =============================================================================

INSERT INTO roles (
    id,
    tenant_id,
    code,
    name,
    description,
    is_system,
    is_active
)
VALUES
(
    :role_system_admin,
    :tenant_id,
    'SYSTEM_ADMIN',
    'System Administrator',
    'Platform and system administration.',
    TRUE,
    TRUE
),
(
    :role_hr_manager,
    :tenant_id,
    'HR_MANAGER',
    'HR Manager',
    'HR management and controlled HR operations.',
    TRUE,
    TRUE
),
(
    :role_hr_officer,
    :tenant_id,
    'HR_OFFICER',
    'HR Officer',
    'Operational HR administration.',
    TRUE,
    TRUE
),
(
    :role_manager,
    :tenant_id,
    'MANAGER',
    'Manager',
    'Managerial workforce access.',
    TRUE,
    TRUE
),
(
    :role_employee,
    :tenant_id,
    'EMPLOYEE',
    'Employee',
    'Employee self-service access.',
    TRUE,
    TRUE
)
ON CONFLICT (tenant_id, code)
DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    is_system = EXCLUDED.is_system,
    is_active = EXCLUDED.is_active,
    updated_at = NOW();

-- =============================================================================
-- Permissions
-- =============================================================================

INSERT INTO permissions (
    id,
    code,
    name,
    description,
    module,
    is_system,
    is_active
)
VALUES
(
    :perm_employee_view,
    'HR_EMPLOYEE_VIEW',
    'View Employees',
    'View employee records.',
    'hr',
    TRUE,
    TRUE
),
(
    :perm_employee_create,
    'HR_EMPLOYEE_CREATE',
    'Create Employees',
    'Create employee records.',
    'hr',
    TRUE,
    TRUE
),
(
    :perm_employee_update,
    'HR_EMPLOYEE_UPDATE',
    'Update Employees',
    'Update employee records.',
    'hr',
    TRUE,
    TRUE
),
(
    :perm_profile_view,
    'HR_PROFILE_VIEW',
    'View Employee Profiles',
    'View employee HR profiles.',
    'hr',
    TRUE,
    TRUE
),
(
    :perm_profile_create,
    'HR_PROFILE_CREATE',
    'Create Employee Profiles',
    'Create employee HR profiles.',
    'hr',
    TRUE,
    TRUE
),
(
    :perm_profile_update,
    'HR_PROFILE_UPDATE',
    'Update Employee Profiles',
    'Update employee HR profiles.',
    'hr',
    TRUE,
    TRUE
),
(
    :perm_position_view,
    'HR_POSITION_VIEW',
    'View Employee Positions',
    'View employee positions.',
    'hr',
    TRUE,
    TRUE
),
(
    :perm_position_create,
    'HR_POSITION_CREATE',
    'Create Employee Positions',
    'Create employee positions.',
    'hr',
    TRUE,
    TRUE
),
(
    :perm_position_update,
    'HR_POSITION_UPDATE',
    'Update Employee Positions',
    'Update employee positions.',
    'hr',
    TRUE,
    TRUE
),
(
    :perm_reporting_view,
    'HR_REPORTING_VIEW',
    'View Reporting Relationships',
    'View employee reporting relationships.',
    'hr',
    TRUE,
    TRUE
),
(
    :perm_reporting_update,
    'HR_REPORTING_UPDATE',
    'Update Reporting Relationships',
    'Update employee reporting relationships.',
    'hr',
    TRUE,
    TRUE
),
(
    :perm_immigration_view,
    'HR_IMMIGRATION_VIEW',
    'View Immigration',
    'View employee immigration records.',
    'hr',
    TRUE,
    TRUE
),
(
    :perm_immigration_create,
    'HR_IMMIGRATION_CREATE',
    'Create Immigration Records',
    'Create employee immigration records.',
    'hr',
    TRUE,
    TRUE
),
(
    :perm_immigration_update,
    'HR_IMMIGRATION_UPDATE',
    'Update Immigration',
    'Update employee immigration records.',
    'hr',
    TRUE,
    TRUE
),
(
    :perm_document_view,
    'HR_DOCUMENT_VIEW',
    'View HR Documents',
    'View employee HR documents.',
    'hr',
    TRUE,
    TRUE
),
(
    :perm_document_upload,
    'HR_DOCUMENT_UPLOAD',
    'Upload HR Documents',
    'Upload employee HR documents.',
    'hr',
    TRUE,
    TRUE
),
(
    :perm_document_update,
    'HR_DOCUMENT_UPDATE',
    'Update HR Documents',
    'Update employee HR documents.',
    'hr',
    TRUE,
    TRUE
),
(
    :perm_document_delete,
    'HR_DOCUMENT_DELETE',
    'Delete HR Documents',
    'Delete employee HR documents.',
    'hr',
    TRUE,
    TRUE
)
ON CONFLICT (code)
DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    module = EXCLUDED.module,
    is_system = EXCLUDED.is_system,
    is_active = EXCLUDED.is_active,
    updated_at = NOW();

-- =============================================================================
-- HR Manager Permissions
-- =============================================================================

INSERT INTO role_permissions (
    id,
    tenant_id,
    role_id,
    permission_id,
    is_enabled,
    assignment_reason
)
VALUES
(
    :rp001,
    :tenant_id,
    :role_hr_manager,
    :perm_employee_view,
    TRUE,
    'Bootstrap HR Manager role.'
),
(
    :rp002,
    :tenant_id,
    :role_hr_manager,
    :perm_employee_create,
    TRUE,
    'Bootstrap HR Manager role.'
),
(
    :rp003,
    :tenant_id,
    :role_hr_manager,
    :perm_employee_update,
    TRUE,
    'Bootstrap HR Manager role.'
),
(
    :rp004,
    :tenant_id,
    :role_hr_manager,
    :perm_profile_view,
    TRUE,
    'Bootstrap HR Manager role.'
),
(
    :rp005,
    :tenant_id,
    :role_hr_manager,
    :perm_profile_create,
    TRUE,
    'Bootstrap HR Manager role.'
),
(
    :rp006,
    :tenant_id,
    :role_hr_manager,
    :perm_profile_update,
    TRUE,
    'Bootstrap HR Manager role.'
),
(
    :rp007,
    :tenant_id,
    :role_hr_manager,
    :perm_position_view,
    TRUE,
    'Bootstrap HR Manager role.'
),
(
    :rp008,
    :tenant_id,
    :role_hr_manager,
    :perm_position_create,
    TRUE,
    'Bootstrap HR Manager role.'
),
(
    :rp009,
    :tenant_id,
    :role_hr_manager,
    :perm_position_update,
    TRUE,
    'Bootstrap HR Manager role.'
),
(
    :rp010,
    :tenant_id,
    :role_hr_manager,
    :perm_reporting_view,
    TRUE,
    'Bootstrap HR Manager role.'
),
(
    :rp011,
    :tenant_id,
    :role_hr_manager,
    :perm_reporting_update,
    TRUE,
    'Bootstrap HR Manager role.'
),
(
    :rp012,
    :tenant_id,
    :role_hr_manager,
    :perm_immigration_view,
    TRUE,
    'Bootstrap HR Manager role.'
),
(
    :rp013,
    :tenant_id,
    :role_hr_manager,
    :perm_immigration_create,
    TRUE,
    'Bootstrap HR Manager role.'
),
(
    :rp014,
    :tenant_id,
    :role_hr_manager,
    :perm_immigration_update,
    TRUE,
    'Bootstrap HR Manager role.'
),
(
    :rp015,
    :tenant_id,
    :role_hr_manager,
    :perm_document_view,
    TRUE,
    'Bootstrap HR Manager role.'
),
(
    :rp016,
    :tenant_id,
    :role_hr_manager,
    :perm_document_upload,
    TRUE,
    'Bootstrap HR Manager role.'
),
(
    :rp017,
    :tenant_id,
    :role_hr_manager,
    :perm_document_update,
    TRUE,
    'Bootstrap HR Manager role.'
),
(
    :rp018,
    :tenant_id,
    :role_hr_manager,
    :perm_document_delete,
    TRUE,
    'Bootstrap HR Manager role.'
)
ON CONFLICT (
    tenant_id,
    role_id,
    permission_id
)
DO UPDATE SET
    is_enabled = EXCLUDED.is_enabled,
    assignment_reason = EXCLUDED.assignment_reason,
    updated_at = NOW();

-- =============================================================================
-- Initial System Administrator Assignment
-- =============================================================================

INSERT INTO user_roles (
    id,
    tenant_id,
    user_id,
    role_id,
    is_primary,
    is_enabled,
    assignment_reason
)
VALUES (
    :user_role_admin,
    :tenant_id,
    :admin_user_id,
    :role_system_admin,
    TRUE,
    TRUE,
    'Initial QWOS development administrator bootstrap assignment.'
)
ON CONFLICT (
    tenant_id,
    user_id,
    role_id
)
DO UPDATE SET
    is_primary = EXCLUDED.is_primary,
    is_enabled = EXCLUDED.is_enabled,
    assignment_reason = EXCLUDED.assignment_reason,
    updated_at = NOW();

COMMIT;