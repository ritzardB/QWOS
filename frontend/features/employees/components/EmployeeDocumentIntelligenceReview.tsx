import {
  useEffect,
  useState,
} from "react";

import type {
  DocumentExtractionField,
  EmployeeDocument,
  EmployeeDocumentExtraction,
} from "../types/employee";

type EmployeeDocumentIntelligenceReviewProps = {
  employee: EmployeeDocument;
  extraction: EmployeeDocumentExtraction | null;
  loading: boolean;
  error: string | null;
  approving: boolean;
  onAnalyze: () => void;
  onClose: () => void;
  onApprove: (
    fields: DocumentExtractionField[],
  ) => void;
};

type ReviewField = DocumentExtractionField & {
  editedValue: string;
};

function formatFieldLabel(
  fieldCode: string,
): string {
  return fieldCode
    .replaceAll("_", " ")
    .replaceAll("-", " ")
    .replace(/\b\w/g, (character) =>
      character.toUpperCase(),
    );
}

function formatConfidence(
  confidence: number | null,
): string {
  if (confidence === null) {
    return "—";
  }

  return `${(confidence * 100).toFixed(1)}%`;
}

function getConfidenceClass(
  confidence: number | null,
): string {
  if (confidence === null) {
    return "employee-document-intelligence-confidence-neutral";
  }

  if (confidence >= 0.9) {
    return "employee-document-intelligence-confidence-high";
  }

  if (confidence >= 0.75) {
    return "employee-document-intelligence-confidence-medium";
  }

  return "employee-document-intelligence-confidence-low";
}

function formatSource(
  source: string,
): string {
  return source
    .replaceAll("_", " ")
    .replaceAll("-", " ")
    .replace(/\b\w/g, (character) =>
      character.toUpperCase(),
    );
}

export function EmployeeDocumentIntelligenceReview({
  employee,
  extraction,
  loading,
  error,
  approving,
  onAnalyze,
  onClose,
  onApprove,
}: EmployeeDocumentIntelligenceReviewProps) {
  const [fields, setFields] = useState<
    ReviewField[]
  >([]);

  useEffect(() => {
    if (!extraction) {
      setFields([]);
      return;
    }

    setFields(
      extraction.fields.map((field) => ({
        ...field,
        editedValue:
          field.normalized_value ??
          field.raw_value ??
          "",
      })),
    );
  }, [extraction]);

  function updateField(
    extractionResultId: string,
    value: string,
  ): void {
    setFields((current) =>
      current.map((field) =>
        field.extraction_result_id ===
        extractionResultId
          ? {
              ...field,
              editedValue: value,
            }
          : field,
      ),
    );
  }

  const approvedFields = fields
  .filter(
    (field) => field.is_hr_updateable,
  )
  .map((field) => ({
    ...field,
    normalized_value:
      field.editedValue,
  }));

  return (
    <div
      className="employee-document-intelligence-overlay"
      role="dialog"
      aria-modal="true"
      aria-labelledby="employee-document-intelligence-title"
    >
      <div className="employee-document-intelligence-window">
        <div className="employee-document-intelligence-header">
          <div>
            <span className="employee-document-intelligence-eyebrow">
              Document Intelligence
            </span>

            <h2 id="employee-document-intelligence-title">
              {employee.document_name}
            </h2>

            <p>
              Review extracted information before
              updating the employee record.
            </p>
          </div>

          <button
            type="button"
            className="employee-document-close-button"
            onClick={onClose}
            disabled={approving}
            aria-label="Close document intelligence review"
          >
            ×
          </button>
        </div>

        {!extraction &&
          !loading &&
          !error && (
            <div className="employee-document-intelligence-start">
              <div className="employee-document-intelligence-start-icon">
                AI
              </div>

              <h3>
                Analyze this document
              </h3>

              <p>
                QWOS will read the document,
                identify structured fields, and
                prepare them for your review.
              </p>

              <button
                type="button"
                className="employee-document-submit-button"
                onClick={onAnalyze}
              >
                Analyze Document
              </button>
            </div>
          )}

                {loading && (
          <div
            className="employee-document-intelligence-processing-overlay"
            role="status"
            aria-live="polite"
            aria-label="Analyzing document"
          >
            <div className="employee-document-intelligence-processing-modal">
              <div
                className="employee-document-intelligence-spinner"
                aria-hidden="true"
              />

              <div className="employee-document-intelligence-processing-content">
                <span className="employee-document-intelligence-processing-eyebrow">
                  Document Intelligence
                </span>

                <h3>Analyzing Document</h3>

                <p>
                  QWOS is reading and analyzing the document.
                  Please wait...
                </p>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div
            className="employee-document-upload-error"
            role="alert"
          >
            {error}
          </div>
        )}

        {extraction && !loading && (
          <>
            <div className="employee-document-intelligence-summary">
              <div>
                <span>
                  Document Family
                </span>

                <strong>
                  {formatFieldLabel(
                    extraction.document_family,
                  )}
                </strong>
              </div>

              <div>
                <span>
                  Country
                </span>

                <strong>
                  {extraction.country_code ??
                    "—"}
                </strong>
              </div>

              <div>
                <span>
                  Fields Detected
                </span>

                <strong>
                  {fields.length}
                </strong>
              </div>
            </div>

            <div className="employee-document-intelligence-review">
              <div className="employee-document-intelligence-review-header">
                <div>
                  <h3>
                    Extracted Information
                  </h3>

                  <p>
                    Review each value before
                    approving the HR update.
                  </p>
                </div>

                <span className="employee-document-intelligence-review-badge">
                  Human Confirmation Required
                </span>
              </div>

              {fields.length === 0 ? (
                <div className="employee-inline-empty">
                  <strong>
                    No extractable fields
                  </strong>

                  <span>
                    The document was recognized, but
                    no configured extraction fields
                    were found.
                  </span>
                </div>
              ) : (
                <div className="employee-document-intelligence-fields">
                  {fields.map((field) => (
                    <div
                      key={
                        field.extraction_result_id
                      }
                      className="employee-document-intelligence-field"
                    >
                      <div className="employee-document-intelligence-field-label">
                      <strong>
                        {formatFieldLabel(
                          field.field_code,
                        )}
                      </strong>

                      <span>
                        {formatSource(
                          field.source,
                        )}
                      </span>

                      {field.is_hr_updateable ? (
                        <span className="employee-document-intelligence-hr-badge">
                          HR Update
                        </span>
                      ) : (
                        <span className="employee-document-intelligence-evidence-badge">
                          Evidence Only
                        </span>
                      )}
                    </div>

                      <div className="employee-document-intelligence-field-value">
                        <input
                          type="text"
                          value={field.editedValue}
                          onChange={(event) =>
                            updateField(
                              field.extraction_result_id,
                              event.target.value,
                            )
                          }
                          disabled={approving}
                        />

                        <span
                          className={`employee-document-intelligence-confidence ${getConfidenceClass(
                            field.confidence,
                          )}`}
                        >
                          {formatConfidence(
                            field.confidence,
                          )}
                        </span>
                      </div>

                      {field.raw_value !==
                        field.normalized_value && (
                        <small>
                          Raw OCR:{" "}
                          {field.raw_value ??
                            "—"}
                        </small>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="employee-document-intelligence-warning">
              <strong>
                Review before approval
              </strong>

              <span>
                Approving will allow these values
                to be used to update the employee's
                HR records.
              </span>
            </div>
          </>
        )}

        <div className="employee-document-intelligence-actions">
          <button
            type="button"
            className="employee-document-cancel-button"
            onClick={onClose}
            disabled={approving}
          >
            Close
          </button>

          {extraction && (
            <>
              <button
                type="button"
                className="employee-document-action-button"
                onClick={onAnalyze}
                disabled={
                  loading || approving
                }
              >
                Re-analyze
              </button>

              <button
                type="button"
                className="employee-document-submit-button"
                onClick={() =>
                  onApprove(approvedFields)
                }
                disabled={
                  approving ||
                  fields.length === 0
                }
              >
                {approving
                  ? "Updating HR..."
                  : "Approve & Update HR"}
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}