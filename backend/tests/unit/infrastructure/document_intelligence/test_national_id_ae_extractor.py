from qwos.application.common.ports.document_ocr import OCRTextResult
from qwos.infrastructure.document_intelligence.national_id.national_id_ae_extractor import (
    NationalIdAEExtractor,
)

OCR_TEXT = """UNITEDARABEMIRATES
FEDERALAUTHORITYFORIDENTITY&
CITIZENSHIP CUSTOMS & PORT SECURITY
Resident Identity Card
ID Number/
784-1971-4792765-7
Name: Richard Santisas Balabarcon
Date of Birth :
06/04/1971
Nationality: Philippines
Issuing Date /
12/11/2024
Expiry Date/
06/04
Sex:M
Signature/
11/11/2026
UNTEDARABEMIRATES
CardNmber/
140875397
ILARE1408753976784197147927657
7104066M2611114PHL<<<<<<<<<<<8
BALABARCON<<RICHARD<SANTISAS<<
"""


def test_extracts_uae_national_id_fields() -> None:
    extractor = NationalIdAEExtractor()

    result = extractor.extract(
        ocr_result=OCRTextResult(
            text=OCR_TEXT,
            source="paddleocr",
            confidence=0.9450957477092743,
        ),
    )

    fields = {
        field.field_code: field
        for field in result.fields
    }

    assert fields["document_number"].normalized_value == (
        "784-1971-4792765-7"
    )

    assert fields["full_name"].normalized_value == (
        "Richard Santisas Balabarcon"
    )

    assert fields["date_of_birth"].normalized_value == (
        "1971-04-06"
    )

    assert fields["nationality"].normalized_value == (
        "Philippines"
    )

    assert fields["issue_date"].normalized_value == (
        "2024-11-12"
    )

    assert "expiry_date" not in fields