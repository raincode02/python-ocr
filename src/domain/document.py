from dataclasses import dataclass

# Document 객체 정의: 통관 문서 필드와 OCR 결과를 담음
@dataclass
class Document:
    hs_code: str | None        # HS 코드 (상품 분류 코드)
    declaration_no: str | None # 신고번호
    importer: str | None       # 수입자 이름
    raw_text: str              # Textract에서 추출한 전체 텍스트
