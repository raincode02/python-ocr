# test_ocr_pipeline.py
from infrastructure.textract_service import TextractOCRService
from domain.document import Document

# MockOCRService: 실제 Textract 호출 없이 테스트 가능
class MockOCRService(TextractOCRService):
    def __init__(self):
        # 부모 __init__ 호출하지 않음 → AWS 호출 없음
        pass

    def extract_text(self, file_path: str) -> str:
        # 테스트용 고정 텍스트 반환
        return """
        HS Code: 123456
        신고번호: AB-12345
        수입자: 홍길동
        """

    def extract_fields(self, raw_text: str) -> Document:
        # 기존 TextractOCRService 필드 추출 로직 그대로 사용
        import re

        def _find(pattern):
            m = re.search(pattern, raw_text)
            return m.group(1).strip() if m else None

        return Document(
            hs_code=_find(r"HS Code[:\s]*([\d]+)"),
            declaration_no=_find(r"신고번호[:\s]*([\w-]+)"),
            importer=_find(r"수입자[:\s]*([가-힣A-Za-z\s]+)"),
            raw_text=raw_text
        )

# 테스트용 Mock Repository
class MockRepository:
    def save(self, doc):
        print("Mock save:", doc)
        return "mock-id"

# 테스트 함수
def test_pipeline():
    ocr_service = MockOCRService()
    repository = MockRepository()  # 실제 DynamoDB 호출 없음

    raw_text = ocr_service.extract_text("dummy.pdf")
    doc: Document = ocr_service.extract_fields(raw_text)

    doc_id = repository.save(doc)

    # 출력 확인
    print("Doc ID:", doc_id)
    print("HS Code:", doc.hs_code)
    print("신고번호:", doc.declaration_no)
    print("수입자:", doc.importer)
    print("Raw Text:", doc.raw_text[:50], "...")  # 일부만 표시

# 실행
if __name__ == "__main__":
    test_pipeline()
