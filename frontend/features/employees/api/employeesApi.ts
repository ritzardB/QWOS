import type {
  Employee,
  EmployeeDocument,
  EmployeeDocumentExtraction,
  EmployeeImmigration,
  EmployeeManager,
  EmployeePosition,
  EmployeeProfile,
} from "../types/employee";

import {
  getAuthenticatedHeaders,
  handleAuthenticationFailure,
} from "../../../api/apiClient";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ??
  "http://localhost:8000/api/v1";

type ListEmployeesResponse = {
  employees: Employee[];
};

type ListEmployeeDocumentsResponse = {
  items: EmployeeDocument[];
};

export async function listEmployees(): Promise<Employee[]> {
  const response = await fetch(
    `${API_BASE_URL}/hr/employees`,
    {
      method: "GET",
      headers: getAuthenticatedHeaders(),
    },
  );

  handleAuthenticationFailure(response);

  if (!response.ok) {
    throw new Error(
      `Unable to load employees (${response.status})`,
    );
  }

  const data =
    (await response.json()) as ListEmployeesResponse;

  return data.employees;
}

export async function getEmployee(
  employeeId: string,
): Promise<Employee> {
  const response = await fetch(
    `${API_BASE_URL}/hr/employees/${employeeId}`,
    {
      method: "GET",
      headers: getAuthenticatedHeaders(),
    },
  );

  handleAuthenticationFailure(response);

  if (response.status === 404) {
    throw new Error("Employee not found.");
  }

  if (!response.ok) {
    throw new Error(
      `Unable to load employee (${response.status})`,
    );
  }

  return (await response.json()) as Employee;
}

export async function getEmployeeProfile(
  employeeId: string,
): Promise<EmployeeProfile> {
  const response = await fetch(
    `${API_BASE_URL}/hr/employees/${employeeId}/profile`,
    {
      method: "GET",
      headers: getAuthenticatedHeaders(),
    },
  );

  handleAuthenticationFailure(response);

  if (response.status === 404) {
    throw new Error("Employee profile not found.");
  }

  if (!response.ok) {
    throw new Error(
      `Unable to load employee profile (${response.status})`,
    );
  }

  return (await response.json()) as EmployeeProfile;
}

export async function getEmployeeManager(
  employeeId: string,
): Promise<EmployeeManager> {
  const response = await fetch(
    `${API_BASE_URL}/hr/employees/${employeeId}/manager`,
    {
      method: "GET",
      headers: getAuthenticatedHeaders(),
    },
  );

  handleAuthenticationFailure(response);

  if (response.status === 404) {
    throw new Error("Employee manager not found.");
  }

  if (!response.ok) {
    throw new Error(
      `Unable to load employee manager (${response.status})`,
    );
  }

  return (await response.json()) as EmployeeManager;
}

export async function getEmployeePosition(
  employeeId: string,
): Promise<EmployeePosition> {
  const response = await fetch(
    `${API_BASE_URL}/hr/employees/${employeeId}/position`,
    {
      method: "GET",
      headers: getAuthenticatedHeaders(),
    },
  );

  handleAuthenticationFailure(response);

  if (response.status === 404) {
    throw new Error("Employee position not found.");
  }

  if (!response.ok) {
    throw new Error(
      `Unable to load employee position (${response.status})`,
    );
  }

  return (await response.json()) as EmployeePosition;
}

export async function getEmployeeImmigration(
  employeeId: string,
  immigrationType: string,
): Promise<EmployeeImmigration> {
  const response = await fetch(
    `${API_BASE_URL}/hr/employees/${employeeId}/immigration?immigration_type=${encodeURIComponent(
      immigrationType,
    )}`,
    {
      method: "GET",
      headers: getAuthenticatedHeaders(),
    },
  );

  handleAuthenticationFailure(response);

  if (response.status === 404) {
    throw new Error(
      "Current immigration record not found.",
    );
  }

  if (!response.ok) {
    throw new Error(
      `Unable to load immigration record (${response.status})`,
    );
  }

  return (await response.json()) as EmployeeImmigration;
}

export async function listEmployeeImmigration(
  employeeId: string,
  immigrationType?: string,
): Promise<EmployeeImmigration[]> {
  const searchParams = new URLSearchParams();

  if (immigrationType) {
    searchParams.set(
      "immigration_type",
      immigrationType,
    );
  }

  const queryString = searchParams.toString();

  const response = await fetch(
    `${API_BASE_URL}/hr/employees/${employeeId}/immigration/history${
      queryString ? `?${queryString}` : ""
    }`,
    {
      method: "GET",
      headers: getAuthenticatedHeaders(),
    },
  );

  handleAuthenticationFailure(response);

  if (!response.ok) {
    throw new Error(
      `Unable to load immigration history (${response.status})`,
    );
  }

  const data = (await response.json()) as {
    items: EmployeeImmigration[];
  };

  return data.items;
}

export async function listEmployeeDocuments(
  employeeId: string,
  documentCategory?: string,
): Promise<EmployeeDocument[]> {
  const searchParams = new URLSearchParams();

  if (documentCategory) {
    searchParams.set(
      "document_category",
      documentCategory,
    );
  }

  const queryString = searchParams.toString();

  const response = await fetch(
    `${API_BASE_URL}/hr/employees/${employeeId}/documents${
      queryString ? `?${queryString}` : ""
    }`,
    {
      method: "GET",
      headers: getAuthenticatedHeaders(),
    },
  );

  handleAuthenticationFailure(response);

  if (response.status === 403) {
    throw new Error(
      "You are not authorized to view employee documents.",
    );
  }

  if (response.status === 404) {
    throw new Error("Employee not found.");
  }

  if (!response.ok) {
    throw new Error(
      `Unable to load employee documents (${response.status})`,
    );
  }

  const data =
    (await response.json()) as ListEmployeeDocumentsResponse;

  return data.items;
}

export type UploadEmployeeDocumentInput = {
  documentName: string;
  documentCategory: string;
  immigrationId?: string;
  file: File;
};

export async function uploadEmployeeDocument(
  employeeId: string,
  input: UploadEmployeeDocumentInput,
): Promise<EmployeeDocument> {
  const formData = new FormData();

  formData.append(
    "document_name",
    input.documentName,
  );

  formData.append(
    "document_category",
    input.documentCategory,
  );

  if (input.immigrationId) {
    formData.append(
      "immigration_id",
      input.immigrationId,
    );
  }

  formData.append("file", input.file);

  const response = await fetch(
    `${API_BASE_URL}/hr/employees/${employeeId}/documents`,
    {
      method: "POST",
      headers: getAuthenticatedHeaders(),
      body: formData,
    },
  );

  handleAuthenticationFailure(response);

  if (response.status === 403) {
    throw new Error(
      "You are not authorized to upload employee documents.",
    );
  }

  if (response.status === 404) {
    throw new Error("Employee not found.");
  }

  if (response.status === 422) {
    throw new Error(
      "Please check the document details and selected file.",
    );
  }

  if (!response.ok) {
    throw new Error(
      `Unable to upload employee document (${response.status})`,
    );
  }

  return (await response.json()) as EmployeeDocument;
}

export function getEmployeeDocumentContentUrl(
  employeeId: string,
  documentId: string,
): string {
  return `${API_BASE_URL}/hr/employees/${employeeId}/documents/${documentId}/content`;
}

export async function downloadEmployeeDocument(
  employeeId: string,
  documentId: string,
  filename: string,
): Promise<void> {
  const response = await fetch(
    getEmployeeDocumentContentUrl(
      employeeId,
      documentId,
    ),
    {
      method: "GET",
      headers: getAuthenticatedHeaders(),
    },
  );

  handleAuthenticationFailure(response);

  if (!response.ok) {
    throw new Error(
      `Unable to download document (${response.status})`,
    );
  }

  const blob = await response.blob();
  const url = URL.createObjectURL(blob);

  try {
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = filename;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
  } finally {
    URL.revokeObjectURL(url);
  }
}

export async function extractEmployeeDocument(
  employeeId: string,
  documentId: string,
): Promise<EmployeeDocumentExtraction> {
  const response = await fetch(
    `${API_BASE_URL}/hr/employees/${employeeId}/documents/${documentId}/extraction`,
    {
      method: "POST",
      headers: getAuthenticatedHeaders(),
    },
  );

  handleAuthenticationFailure(response);

  if (response.status === 403) {
    throw new Error(
      "You are not authorized to analyze employee documents.",
    );
  }

  if (response.status === 404) {
    throw new Error(
      "Employee document or document definition not found.",
    );
  }

  if (response.status === 422) {
    throw new Error(
      "The document could not be processed.",
    );
  }

  if (!response.ok) {
    throw new Error(
      `Unable to analyze employee document (${response.status})`,
    );
  }

  return (await response.json()) as EmployeeDocumentExtraction;
}

export type ApprovedEmployeeDocumentFieldInput = {
  extraction_result_id: string;
  value: string | null;
};

export type ApproveEmployeeDocumentExtractionResponse = {
  document_id: string;
  employee_id: string;
  approved_fields: Array<{
    extraction_result_id: string;
    field_code: string;
    target_entity: string;
    target_field: string;
    value: string | null;
  }>;
};

export async function approveEmployeeDocumentExtraction(
  employeeId: string,
  documentId: string,
  fields: ApprovedEmployeeDocumentFieldInput[],
): Promise<ApproveEmployeeDocumentExtractionResponse> {
  const response = await fetch(
    `${API_BASE_URL}/hr/employees/${employeeId}/documents/${documentId}/extraction/approve`,
    {
      method: "POST",
      headers: {
        ...getAuthenticatedHeaders(),
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        fields,
      }),
    },
  );

  handleAuthenticationFailure(response);

  if (response.status === 403) {
    throw new Error(
      "You are not authorized to approve document extraction.",
    );
  }

  if (response.status === 404) {
    throw new Error(
      "Document or extraction result was not found.",
    );
  }

  if (response.status === 422) {
    throw new Error(
      "One or more approved values are invalid.",
    );
  }

  if (!response.ok) {
    throw new Error(
      `Unable to approve document extraction (${response.status})`,
    );
  }

  return (
    (await response.json()) as
      ApproveEmployeeDocumentExtractionResponse
  );
}

