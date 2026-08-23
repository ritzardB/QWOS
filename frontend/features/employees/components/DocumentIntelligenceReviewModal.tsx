import {
  useEffect,
  useMemo,
  useState,
} from "react";

import type {
  DocumentExtractionField,
  EmployeeDocument,
  EmployeeDocumentExtraction,
} from "../types/employee";

type DocumentIntelligenceReviewModalProps = {
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
  displayLabel: string;
};

type FieldConfig = {
  fieldCode: string;
  label: string;
};

const DOCUMENT_FIELD_CONFIG: Record<
  string,
  FieldConfig[]
> = {
  "national id": [
    {
      fieldCode: "document_number",
      label: "National ID Number",
    },
    {
      fieldCode: "full_name",
      label: "Full Name",
    },
    {
      fieldCode: "date_of_birth",
      label: "Date of Birth",
    },
    {
      fieldCode: "nationality",
      label: "Nationality",
    },
    {
      fieldCode: "issue_date",
      label: "Issue Date",
    },
    {
      fieldCode: "expiry_date",
      label: "Expiry Date",
    },
  ],

  passport: [
    {
      fieldCode: "document_number",
      label: "Passport Number",
    },
    {
      fieldCode: "surname",
      label: "Surname",
    },
    {
      fieldCode: "given_names",
      label: "Given Names",
    },
    {
      fieldCode: "date_of_birth",
      label: "Date of Birth",
    },
    {
      fieldCode: "nationality",
      label: "Nationality",
    },
    {
      fieldCode: "expiry_date",
      label: "Expiry Date",
    },
  ],
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

export function DocumentIntelligenceReviewModal({
  employee,
  extraction,
  loading,
  error,
  approving,
  onAnalyze,
  onClose,
  onApprove,
}: DocumentIntelligenceReviewModalProps) {
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
        displayLabel: formatFieldLabel(
          field.field_code,
        ),
      })),
    );
  }, [extraction]);

  const configuredFields = useMemo(() => {
    if (!extraction) {
      return [];
    }

    return (
      DOCUMENT_FIELD_CONFIG[
        extraction.document_family
          .trim()
          .toLowerCase()
      ] ?? []
    );
  }, [extraction]);

  const reviewFields = useMemo<ReviewField[]>(() => {
    if (!extraction) {
      return [];
    }

    const configuredByCode = new Map(
      configuredFields.map((config) => [
        config.fieldCode,
        config,
      ]),
    );

    return fields
      .filter((field) =>
        configuredByCode.has(
          field.field_code,
        ),
      )
      .map((field) => {
        const config =
          configuredByCode.get(
            field.field_code,
          );

        return {
          ...field,
          displayLabel:
            config?.label ??
            formatFieldLabel(
              field.field_code,
            ),
        };
      })
      .filter((field) => {
        /*
         * Do not display an empty expiry date.
         */
        if (
          field.field_code ===
          "expiry_date"
        ) {
          return (
            field.editedValue.trim()
              .length > 0
          );
        }

        return true;
      });
  }, [
    configuredFields,
    extraction,
    fields,
  ]);

  const approvedFields =
    reviewFields
      .filter(
        (field) =>
          field.is_hr_updateable,
      )
      .map(
        (field): DocumentExtractionField => ({
          extraction_result_id:
            field.extraction_result_id,
          field_code:
            field.field_code,
          raw_value:
            field.raw_value,
          normalized_value:
            field.editedValue,
          confidence:
            field.confidence,
          source:
            field.source,
          is_hr_updateable:
            field.is_hr_updateable,
          target_entity:
            field.target_entity,
          target_field:
            field.target_field,
        }),
      );

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

  const documentFamilyLabel =
    extraction
      ? formatFieldLabel(
          extraction.document_family,
        )
      : formatFieldLabel(
          employee.document_category,
        );

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
              Please review the important document
              information before updating HR
              records.
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
                identify important information,
                and prepare it for your review.
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

                <h3>
                  Analyzing Document
                </h3>

                <p>
                  QWOS is reading and analyzing
                  the document. Please wait...
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
                  Document Type: 
                </span>

                <strong>
                  {documentFamilyLabel}
                </strong>
              </div>

              <div>
                <span>
                  Country of Issuance: 
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
                  {reviewFields.length}
                </strong>
              </div>
            </div>

            <div className="employee-document-intelligence-review">
              <div className="employee-document-intelligence-review-header">
                <div>
                  <h3>
                    Extraction Results
                  </h3>

                  <p>
                    Confirm the important values
                    before approving HR updates.
                  </p>
                </div>
              </div>

              {reviewFields.length === 0 ? (
                <div className="employee-inline-empty">
                  <strong>
                    No important fields detected
                  </strong>

                  <span>
                    The document was recognized,
                    but no configured review
                    fields were found.
                  </span>
                </div>
              ) : (
                <div className="employee-document-intelligence-fields">
                  {reviewFields.map((field) => (
                    <div
                      key={
                        field.extraction_result_id
                      }
                      className="employee-document-intelligence-field"
                    >
                      <div className="employee-document-intelligence-field-label">
                        <strong>
                          {field.displayLabel}
                        </strong>
                      </div>

                      <div className="employee-document-intelligence-field-value">
                        {field.is_hr_updateable ? (
                          <input
                            type="text"
                            value={
                              field.editedValue
                            }
                            onChange={(
                              event,
                            ) =>
                              updateField(
                                field.extraction_result_id,
                                event.target
                                  .value,
                              )
                            }
                            disabled={approving}
                            aria-label={
                              field.displayLabel
                            }
                          />
                        ) : (
                          <div className="employee-document-intelligence-readonly-value">
                            {field.editedValue ||
                              "—"}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="employee-document-intelligence-footer">
              <div className="employee-document-intelligence-footer-summary">
                <strong>
                  {approvedFields.length} HR{" "}
                  {approvedFields.length === 1
                    ? "field"
                    : "fields"}{" "}
                  ready to update
                </strong>
              </div>

              <div className="employee-document-intelligence-footer-actions">
                <button
                  type="button"
                  className="employee-document-secondary-button"
                  onClick={onAnalyze}
                  disabled={
                    approving ||
                    loading
                  }
                >
                  Re-analyze
                </button>

                <button
                  type="button"
                  className="employee-document-cancel-button"
                  onClick={onClose}
                  disabled={approving}
                >
                  Close
                </button>

                <button
                  type="button"
                  className="employee-document-submit-button"
                  onClick={() =>
                    onApprove(
                      approvedFields,
                    )
                  }
                  disabled={
                    approving ||
                    approvedFields.length === 0
                  }
                >
                  {approving
                    ? "Updating HR..."
                    : "Approve & Update"}
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}