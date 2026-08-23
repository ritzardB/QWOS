import {
  useEffect,
  useMemo,
  useState,
} from "react";
import type {
  ChangeEvent,
  FormEvent,
} from "react";

import {
  approveEmployeeDocumentExtraction,
  extractEmployeeDocument,
  downloadEmployeeDocument,
  getEmployeeDocumentContentUrl,
  listEmployeeDocuments,
  uploadEmployeeDocument,
} from "../api/employeesApi";

import type {
  DocumentExtractionField,
  EmployeeDocument,
  EmployeeDocumentExtraction,
  EmployeeImmigration,
} from "../types/employee";

import {
  DocumentIntelligenceReviewModal,
} from "./DocumentIntelligenceReviewModal";

import {
  getAuthenticatedHeaders,
  handleAuthenticationFailure,
} from "../../../api/apiClient";

type EmployeeDocumentsProps = {
  employeeId: string;
  immigration: EmployeeImmigration[];
};

type DocumentTypeOption = {
  value: string;
  label: string;
  requiresImmigration: boolean;
};

type DocumentGroup = {
  key: string;
  category: string;
  immigrationId: string | null;
  versions: EmployeeDocument[];
  current: EmployeeDocument;
};

const DOCUMENT_TYPES: DocumentTypeOption[] = [
  {
    value: "residence visa",
    label: "Residence Visa",
    requiresImmigration: true,
  },
  {
    value: "work permit",
    label: "Work Permit",
    requiresImmigration: true,
  },
  {
    value: "passport",
    label: "Passport",
    requiresImmigration: false,
  },
  {
    value: "national id",
    label: "Emirates ID",
    requiresImmigration: false,
  },
  {
    value: "employment contract",
    label: "Employment Contract",
    requiresImmigration: false,
  },
  {
    value: "other",
    label: "Other",
    requiresImmigration: false,
  },
];

function formatFileSize(bytes: number): string {
  if (bytes < 1024) {
    return `${bytes} B`;
  }

  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`;
  }

  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function formatDocumentCategory(
  value: string,
): string {
  return value
    .replaceAll("_", " ")
    .replaceAll("-", " ")
    .replace(/\b\w/g, (character) =>
      character.toUpperCase(),
    );
}

function formatDate(
  value: string | null,
): string {
  if (!value) {
    return "—";
  }

  return new Intl.DateTimeFormat("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  }).format(new Date(`${value}T00:00:00`));
}

function getDocumentType(
  value: string,
): DocumentTypeOption {
  return (
    DOCUMENT_TYPES.find(
      (documentType) =>
        documentType.value === value,
    ) ??
    DOCUMENT_TYPES[
      DOCUMENT_TYPES.length - 1
    ]
  );
}

function getDocumentGroupKey(
  document: EmployeeDocument,
): string {
  return [
    document.document_category
      .trim()
      .toLowerCase(),
    document.immigration_id ?? "none",
  ].join("::");
}

function groupDocuments(
  documents: EmployeeDocument[],
): DocumentGroup[] {
  const groups = new Map<
    string,
    EmployeeDocument[]
  >();

  for (const document of documents) {
    const key = getDocumentGroupKey(
      document,
    );

    const existing = groups.get(key);

    if (existing) {
      existing.push(document);
    } else {
      groups.set(key, [document]);
    }
  }

  return Array.from(groups.entries())
    .map(([key, versions]) => {
      const sortedVersions = [
        ...versions,
      ].sort(
        (left, right) =>
          right.document_version -
          left.document_version,
      );

      return {
        key,
        category:
          sortedVersions[0]
            .document_category,
        immigrationId:
          sortedVersions[0]
            .immigration_id,
        versions: sortedVersions,
        current: sortedVersions[0],
      };
    })
    .sort((left, right) =>
      left.category.localeCompare(
        right.category,
      ),
    );
}

export function EmployeeDocuments({
  employeeId,
  immigration,
}: EmployeeDocumentsProps) {
  const [documents, setDocuments] =
    useState<EmployeeDocument[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  const [showUploadForm, setShowUploadForm] =
    useState(false);

  const [
    editingDocument,
    setEditingDocument,
  ] = useState<EmployeeDocument | null>(
    null,
  );

  const [expandedHistory, setExpandedHistory] =
    useState<Set<string>>(
      () => new Set(),
    );

  const [documentName, setDocumentName] =
    useState("");

  const [documentCategory, setDocumentCategory] =
    useState("residence visa");

  const [immigrationId, setImmigrationId] =
    useState("");

  const [selectedFile, setSelectedFile] =
    useState<File | null>(null);

  const [uploading, setUploading] =
    useState(false);

  const [uploadError, setUploadError] =
    useState<string | null>(null);

  const [
    documentActionError,
    setDocumentActionError,
  ] = useState<string | null>(null);

  const [
    previewingDocumentId,
    setPreviewingDocumentId,
  ] = useState<string | null>(null);

  const [
    downloadingDocumentId,
    setDownloadingDocumentId,
  ] = useState<string | null>(null);

  const selectedDocumentType =
    getDocumentType(documentCategory);

  const documentGroups = useMemo(
    () => groupDocuments(documents),
    [documents],
  );

  const [
    intelligenceDocument,
    setIntelligenceDocument,
  ] = useState<EmployeeDocument | null>(
    null,
  );

  const [
    intelligenceExtraction,
    setIntelligenceExtraction,
  ] =
    useState<EmployeeDocumentExtraction | null>(
      null,
    );

  const [
    intelligenceLoading,
    setIntelligenceLoading,
  ] = useState(false);

  const [
    intelligenceError,
    setIntelligenceError,
  ] = useState<string | null>(null);

  const [
    intelligenceApproving,
    setIntelligenceApproving,
  ] = useState(false);

  async function handleAnalyzeDocument(
  document: EmployeeDocument,
): Promise<void> {
  setIntelligenceDocument(document);
  setIntelligenceExtraction(null);
  setIntelligenceError(null);
  setIntelligenceLoading(true);

  try {
    const result =
      await extractEmployeeDocument(
        employeeId,
        document.id,
      );

    setIntelligenceExtraction(result);
  } catch (error) {
    setIntelligenceError(
      error instanceof Error
        ? error.message
        : "Unable to analyze document.",
    );
  } finally {
    setIntelligenceLoading(false);
  }
}

  async function handleApproveExtraction(
    fields: DocumentExtractionField[],
  ): Promise<void> {
    if (!intelligenceDocument) {
      return;
    }

    setIntelligenceApproving(true);
    setIntelligenceError(null);

    try {
      await approveEmployeeDocumentExtraction(
        employeeId,
        intelligenceDocument.id,
        fields.map((field) => ({
          extraction_result_id:
            field.extraction_result_id,
          value:
            field.normalized_value ??
            field.raw_value ??
            null,
        })),
      );

      await loadDocuments();

      setIntelligenceDocument(null);
      setIntelligenceExtraction(null);
      setIntelligenceError(null);
    } catch (error) {
      setIntelligenceError(
        error instanceof Error
          ? error.message
          : "Unable to update HR records.",
      );
    } finally {
      setIntelligenceApproving(false);
    }
  }

  async function loadDocuments(): Promise<void> {
    try {
      setLoading(true);
      setError(null);

      const data =
        await listEmployeeDocuments(
          employeeId,
        );

      setDocuments(data);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Unable to load employee documents.",
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    let cancelled = false;

    async function load(): Promise<void> {
      try {
        setLoading(true);
        setError(null);

        const data =
          await listEmployeeDocuments(
            employeeId,
          );

        if (!cancelled) {
          setDocuments(data);
        }
      } catch (error) {
        if (!cancelled) {
          setError(
            error instanceof Error
              ? error.message
              : "Unable to load employee documents.",
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void load();

    return () => {
      cancelled = true;
    };
  }, [employeeId]);

  function resetUploadForm(): void {
    setDocumentName("");
    setDocumentCategory(
      "residence visa",
    );
    setImmigrationId("");
    setSelectedFile(null);
    setUploadError(null);
    setEditingDocument(null);
  }

  function closeUploadForm(): void {
    if (uploading) {
      return;
    }

    setShowUploadForm(false);
    resetUploadForm();
  }

  function openNewDocumentForm(): void {
    setDocumentActionError(null);
    resetUploadForm();
    setShowUploadForm(true);
  }

  function openReplaceForm(
    document: EmployeeDocument,
  ): void {
    setDocumentActionError(null);
    setEditingDocument(document);
    setDocumentName(
      document.document_name,
    );
    setDocumentCategory(
      document.document_category,
    );
    setImmigrationId(
      document.immigration_id ?? "",
    );
    setSelectedFile(null);
    setUploadError(null);
    setShowUploadForm(true);
  }

  function toggleHistory(
    groupKey: string,
  ): void {
    setExpandedHistory((current) => {
      const next = new Set(current);

      if (next.has(groupKey)) {
        next.delete(groupKey);
      } else {
        next.add(groupKey);
      }

      return next;
    });
  }

  function handleDocumentCategoryChange(
    value: string,
  ): void {
    setDocumentCategory(value);

    const option =
      getDocumentType(value);

    if (!option.requiresImmigration) {
      setImmigrationId("");
    }
  }

  function handleFileChange(
    event: ChangeEvent<HTMLInputElement>,
  ): void {
    const file =
      event.target.files?.[0] ?? null;

    setSelectedFile(file);
    setUploadError(null);
  }

  async function handleUpload(
    event: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault();

    setUploadError(null);

    const trimmedName =
      documentName.trim();

    if (!trimmedName) {
      setUploadError(
        "Please enter a document name.",
      );
      return;
    }

    if (!selectedFile) {
      setUploadError(
        "Please select a file to upload.",
      );
      return;
    }

    if (
      selectedDocumentType.requiresImmigration &&
      !immigrationId
    ) {
      setUploadError(
        "Please select the related immigration record.",
      );
      return;
    }

    setUploading(true);

    try {
      await uploadEmployeeDocument(
        employeeId,
        {
          documentName: trimmedName,
          documentCategory,
          immigrationId:
            immigrationId || undefined,
          file: selectedFile,
        },
      );

      await loadDocuments();

      setShowUploadForm(false);
      resetUploadForm();
    } catch (error) {
      setUploadError(
        error instanceof Error
          ? error.message
          : "Unable to upload employee document.",
      );
    } finally {
      setUploading(false);
    }
  }

  async function handlePreview(
    document: EmployeeDocument,
  ): Promise<void> {
    setDocumentActionError(null);
    setPreviewingDocumentId(document.id);

    /*
     * Open a blank tab immediately from the click event.
     * This avoids popup blockers while the authenticated
     * request is being completed.
     */
    const previewWindow = window.open(
      "",
      "_blank",
    );

    if (!previewWindow) {
      setDocumentActionError(
        "Unable to open document preview. Please allow pop-ups for QWOS.",
      );
      setPreviewingDocumentId(null);
      return;
    }

    try {
      const response = await fetch(
        getEmployeeDocumentContentUrl(
          employeeId,
          document.id,
        ),
        {
          method: "GET",
          headers: getAuthenticatedHeaders(),
        },
      );

      handleAuthenticationFailure(response);

      if (!response.ok) {
        throw new Error(
          `Unable to preview document (${response.status})`,
        );
      }

      const blob = await response.blob();
      const url =
        URL.createObjectURL(blob);

      previewWindow.location.href =
        url;

      window.setTimeout(() => {
        URL.revokeObjectURL(url);
      }, 60_000);
    } catch (error) {
      previewWindow.close();

      setDocumentActionError(
        error instanceof Error
          ? error.message
          : "Unable to preview document.",
      );
    } finally {
      setPreviewingDocumentId(null);
    }
  }

  async function handleDownload(
    document: EmployeeDocument,
  ): Promise<void> {
    setDocumentActionError(null);
    setDownloadingDocumentId(document.id);

    try {
      await downloadEmployeeDocument(
        employeeId,
        document.id,
        document.original_filename,
      );
    } catch (error) {
      setDocumentActionError(
        error instanceof Error
          ? error.message
          : "Unable to download document.",
      );
    } finally {
      setDownloadingDocumentId(null);
    }
  }

  return (
    <article className="employee-detail-panel employee-documents-panel">
      <div className="employee-panel-heading">
        <div>
          <h2>Documents</h2>

          <p className="employee-panel-description">
            Employee documents and supporting records.
          </p>
        </div>

        <div className="employee-documents-heading-actions">
          <span className="employee-record-count">
            {loading
              ? "—"
              : documents.length}
          </span>

          <button
            type="button"
            className="employee-document-upload-button"
            onClick={
              openNewDocumentForm
            }
          >
            + Upload Document
          </button>
        </div>
      </div>

      {showUploadForm && (
        <div className="employee-document-upload-form">
          <div className="employee-document-upload-form-header">
            <div>
              <h3>
                {editingDocument
                  ? `Replace ${formatDocumentCategory(
                      editingDocument.document_category,
                    )}`
                  : "Upload Document"}
              </h3>

              <p>
                {editingDocument
                  ? `Upload a new version. Current version is V${String(
                      editingDocument.document_version,
                    ).padStart(2, "0")}.`
                  : "Add a supporting document for this employee."}
              </p>
            </div>

            <button
              type="button"
              className="employee-document-close-button"
              onClick={
                closeUploadForm
              }
              disabled={uploading}
              aria-label="Close upload form"
            >
              ×
            </button>
          </div>

          <form onSubmit={handleUpload}>
            <div className="employee-document-form-grid">
              <label>
                <span>
                  Document Name
                </span>

                <input
                  type="text"
                  value={documentName}
                  onChange={(event) =>
                    setDocumentName(
                      event.target.value,
                    )
                  }
                  placeholder="Residence Visa"
                  disabled={
                    uploading ||
                    Boolean(editingDocument)
                  }
                />
              </label>

              <label>
                <span>
                  Document Type
                </span>

                <select
                  value={documentCategory}
                  onChange={(event) =>
                    handleDocumentCategoryChange(
                      event.target.value,
                    )
                  }
                  disabled={
                    uploading ||
                    Boolean(editingDocument)
                  }
                >
                  {DOCUMENT_TYPES.map(
                    (documentType) => (
                      <option
                        key={
                          documentType.value
                        }
                        value={
                          documentType.value
                        }
                      >
                        {
                          documentType.label
                        }
                      </option>
                    ),
                  )}
                </select>
              </label>

              {selectedDocumentType.requiresImmigration && (
                <label>
                  <span>
                    Immigration Record
                  </span>

                  <select
                    value={immigrationId}
                    onChange={(event) =>
                      setImmigrationId(
                        event.target.value,
                      )
                    }
                    disabled={
                      uploading ||
                      Boolean(editingDocument)
                    }
                  >
                    <option value="">
                      Select immigration record
                    </option>

                    {immigration.map(
                      (record) => (
                        <option
                          key={record.id}
                          value={record.id}
                        >
                          {formatDocumentCategory(
                            record.immigration_type,
                          )}{" "}
                          ·{" "}
                          {formatDate(
                            record.issue_date,
                          )}{" "}
                          —{" "}
                          {formatDate(
                            record.expiry_date,
                          )}
                        </option>
                      ),
                    )}
                  </select>
                </label>
              )}

              <label className="employee-document-file-field">
                <span>
                  File
                </span>

                <input
                  type="file"
                  onChange={
                    handleFileChange
                  }
                  disabled={uploading}
                />

                {selectedFile && (
                  <small>
                    Selected:{" "}
                    {selectedFile.name}
                  </small>
                )}
              </label>
            </div>

            {uploadError && (
              <div className="employee-document-upload-error">
                {uploadError}
              </div>
            )}

            <div className="employee-document-form-actions">
              <button
                type="button"
                className="employee-document-cancel-button"
                onClick={
                  closeUploadForm
                }
                disabled={uploading}
              >
                Cancel
              </button>

              <button
                type="submit"
                className="employee-document-submit-button"
                disabled={uploading}
              >
                {uploading
                  ? "Uploading..."
                  : editingDocument
                    ? "Upload New Version"
                    : "Upload Document"}
              </button>
            </div>
          </form>
        </div>
      )}

      {documentActionError && (
        <div
          className="employee-document-upload-error"
          role="alert"
        >
          {documentActionError}
        </div>
      )}

      {loading && (
        <div className="employee-inline-loading">
          Loading documents...
        </div>
      )}

      {error && (
        <div className="employee-inline-error">
          {error}
        </div>
      )}

      {!loading &&
        !error &&
        documents.length === 0 &&
        !showUploadForm && (
          <div className="employee-inline-empty">
            <strong>
              No documents
            </strong>

            <span>
              No documents have been uploaded
              for this employee.
            </span>
          </div>
        )}

      {!loading &&
        !error &&
        documentGroups.length > 0 && (
          <div className="employee-documents-list">
            {documentGroups.map(
              (group) => {
                const isHistoryExpanded =
                  expandedHistory.has(
                    group.key,
                  );

                const history =
                  group.versions.filter(
                    (version) =>
                      version.id !==
                      group.current.id,
                  );

                return (
                  <div
                    key={group.key}
                    className="employee-document-group"
                  >
                    <div className="employee-document-item">
                      <div className="employee-document-main">
                        <div className="employee-document-icon">
                          {group.current.file_extension
                            ?.toUpperCase() ??
                            "FILE"}
                        </div>

                        <div>
                          <div className="employee-document-title-row">
                            <h3>
                              {
                                group.current
                                  .document_name
                              }
                            </h3>

                            <span className="employee-document-current-badge">
                              Current
                            </span>
                          </div>

                          <p>
                            {formatDocumentCategory(
                              group.current
                                .document_category,
                            )}
                          </p>

                          <span>
                            {
                              group.current
                                .original_filename
                            }
                          </span>

                          <small>
                            Stored as:{" "}
                            {
                              group.current
                                .stored_filename
                            }
                          </small>
                        </div>
                      </div>

                      <div className="employee-document-actions">
                        <div className="employee-document-meta">
                          <strong>
                            V
                            {String(
                              group.current
                                .document_version,
                            ).padStart(
                              2,
                              "0",
                            )}
                          </strong>

                          <span>
                            {formatFileSize(
                              group.current
                                .file_size_bytes,
                            )}
                          </span>

                          <span>
                            {group.current
                              .file_extension
                              ?.toUpperCase() ??
                              "—"}
                          </span>
                        </div>

                        <div className="employee-document-buttons">
                          <button
                            type="button"
                            className="employee-document-action-button"
                            onClick={() =>
                              void handleAnalyzeDocument(
                                group.current,
                              )
                            }
                            disabled={
                              uploading ||
                              intelligenceLoading ||
                              previewingDocumentId ===
                                group.current.id ||
                              downloadingDocumentId ===
                                group.current.id
                            }
                          >
                            {intelligenceLoading &&
                            intelligenceDocument?.id ===
                              group.current.id
                              ? "Analyzing..."
                              : "Analyze"}
                          </button>

                          <button
                            type="button"
                            className="employee-document-action-button"
                            onClick={() =>
                              void handlePreview(
                                group.current,
                              )
                            }
                            disabled={
                              previewingDocumentId ===
                                group.current.id ||
                              downloadingDocumentId ===
                                group.current.id
                            }
                          >
                            {previewingDocumentId ===
                            group.current.id
                              ? "Opening..."
                              : "Preview"}
                          </button>

                          <button
                            type="button"
                            className="employee-document-action-button"
                            onClick={() =>
                              void handleDownload(
                                group.current,
                              )
                            }
                            disabled={
                              downloadingDocumentId ===
                                group.current.id ||
                              previewingDocumentId ===
                                group.current.id
                            }
                          >
                            {downloadingDocumentId ===
                            group.current.id
                              ? "Downloading..."
                              : "Download"}
                          </button>

                          <button
                            type="button"
                            className="employee-document-action-button"
                            onClick={() =>
                              openReplaceForm(
                                group.current,
                              )
                            }
                            disabled={
                              uploading ||
                              previewingDocumentId ===
                                group.current.id ||
                              downloadingDocumentId ===
                                group.current.id
                            }
                          >
                            Replace
                          </button>

                          {history.length >
                            0 && (
                            <button
                              type="button"
                              className="employee-document-action-button"
                              onClick={() =>
                                toggleHistory(
                                  group.key,
                                )
                              }
                            >
                              {isHistoryExpanded
                                ? "Hide History"
                                : `History (${history.length})`}
                            </button>
                          )}
                        </div>
                      </div>
                    </div>

                    {isHistoryExpanded &&
                      history.length >
                        0 && (
                        <div className="employee-document-history">
                          {history.map(
                            (version) => (
                              <div
                                key={
                                  version.id
                                }
                                className="employee-document-history-item"
                              >
                                <div>
                                  <strong>
                                    V
                                    {String(
                                      version.document_version,
                                    ).padStart(
                                      2,
                                      "0",
                                    )}
                                  </strong>

                                  <span>
                                    {
                                      version.original_filename
                                    }
                                  </span>

                                  <small>
                                    {
                                      version.stored_filename
                                    }
                                  </small>
                                </div>

                                <div className="employee-document-meta">
                                  <span>
                                    {formatFileSize(
                                      version.file_size_bytes,
                                    )}
                                  </span>

                                  <span>
                                    {version.file_extension
                                      ?.toUpperCase() ??
                                      "—"}
                                  </span>
                                </div>
                              </div>
                            ),
                          )}
                        </div>
                      )}
                  </div>
                );
              },
            )}
          </div>
        )}
        {intelligenceDocument && (
        <DocumentIntelligenceReviewModal
          employee={intelligenceDocument}
          extraction={intelligenceExtraction}
          loading={intelligenceLoading}
          error={intelligenceError}
          approving={intelligenceApproving}
          onAnalyze={() =>
            void handleAnalyzeDocument(
              intelligenceDocument,
            )
          }
          onClose={() => {
            if (!intelligenceApproving) {
              setIntelligenceDocument(null);
              setIntelligenceExtraction(null);
              setIntelligenceError(null);
            }
          }}
          onApprove={(fields) =>
            void handleApproveExtraction(fields)
          }
        />
      )}
    </article>
  );
}