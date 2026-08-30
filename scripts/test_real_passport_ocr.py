from pathlib import Path

from qwos.infrastructure.document_intelligence.passport.passport_mrz_detector import (
    PassportMRZDetector,
)
from qwos.infrastructure.document_intelligence.passport.passport_mrz_parser import (
    PassportMRZParser,
)
from qwos.infrastructure.ocr.paddle_document_ocr import (
    PaddleDocumentOCR,
)


IMAGE_PATH = Path(
    "test-data/passport/real_passport.jpg",
)


def main() -> None:
    content = IMAGE_PATH.read_bytes()

    ocr = PaddleDocumentOCR()
    detector = PassportMRZDetector()
    parser = PassportMRZParser()

    print("=" * 70)
    print("QWOS REAL PASSPORT OCR TEST")
    print("=" * 70)

    ocr_result = ocr.extract_text(
        content=content,
        filename=IMAGE_PATH.name,
        mime_type="image/jpeg",
    )

    print("\nOCR SOURCE:")
    print(ocr_result.source)

    print("\nOCR CONFIDENCE:")
    print(ocr_result.confidence)

    print("\nOCR TEXT:")
    print(ocr_result.text)

    mrz = detector.detect(
        ocr_result.text,
    )

    print("\nDETECTED MRZ:")
    print(mrz)

    extraction = parser.parse(
        mrz,
    )

    print("\nCLASSIFICATION:")
    print(
        "Document family:",
        extraction.classification.document_family,
    )
    print(
        "Country:",
        extraction.classification.country_code,
    )
    print(
        "Confidence:",
        extraction.classification.confidence,
    )

    print("\nEXTRACTED FIELDS:")

    for field in extraction.fields:
        print(
            f"{field.field_code:20} "
            f"{field.normalized_value!s:25} "
            f"confidence={field.confidence} "
            f"source={field.source}"
        )

    print("\nRESULT: OCR → MRZ DETECTOR → PARSER SUCCESS")
    print("=" * 70)


if __name__ == "__main__":
    main()