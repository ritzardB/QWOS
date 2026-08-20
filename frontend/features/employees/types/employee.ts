export type Employee = {
  id: string;
  employee_number: string;
  user_id: string | null;
  hire_date: string | null;
  employment_status: string;
  employment_type: string;
  work_email: string | null;
  work_phone: string | null;
  created_at: string;
};

export type EmployeeProfile = {
  id: string;
  employee_id: string;
  date_of_birth: string | null;
  gender: string | null;
  nationality: string | null;
  marital_status: string | null;
  personal_email: string | null;
  personal_phone: string | null;
  address_line_1: string | null;
  address_line_2: string | null;
  city: string | null;
  state_province: string | null;
  postal_code: string | null;
  country_code: string | null;
  emergency_contact_name: string | null;
  emergency_contact_relationship: string | null;
  emergency_contact_phone: string | null;
  created_at: string;
};

export type EmployeeManager = {
  employee_id: string;
  manager_employee_id: string;
  manager_employee_number: string;
  relationship_type: string;
  effective_from: string;
};

export type EmployeePosition = {
  id: string;
  employee_id: string;
  job_title: string;
  organizational_level: string;
  effective_from: string;
  effective_to: string | null;
};

export type EmployeeImmigration = {
  id: string;
  employee_id: string;
  immigration_type: string;
  status: string;
  document_number: string | null;
  sponsor_name: string | null;
  issuing_authority: string | null;
  issue_date: string | null;
  expiry_date: string | null;
  notes: string | null;
};

export type EmployeeDocument = {
  id: string;
  employee_id: string;
  immigration_id: string | null;
  document_name: string;
  document_category: string;
  original_filename: string;
  stored_filename: string;
  mime_type: string | null;
  file_extension: string | null;
  file_size_bytes: number;
  storage_provider: string;
  storage_key: string;
  checksum_sha256: string;
  document_version: number;
};

