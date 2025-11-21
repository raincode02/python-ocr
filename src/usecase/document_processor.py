from domain.document import Document
from interface.ocr_service import OCRService
from interface.repository import DocumentRepository
import re
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# DocumentProcessor: PDF 처리, OCR 호출, 필드 추출, Repository 저장
class DocumentProcessor:
    def __init__(self, ocr_service: OCRService, repository: DocumentRepository):
        self.ocr_service = ocr_service  # TextractOCRService 주입
        self.repository = repository    # DynamoDBDocumentRepository 주입

    def process_pdf(self, file_s3_path: str) -> str:
        # Textract 호출로 텍스트 추출
        raw_text = self.ocr_service.extract_text(file_s3_path)
        logger.info("OCR text extracted")

        # 필드 추출 helper
        def _find(pattern):
            m = re.search(pattern, raw_text)
            return m.group(1).strip() if m else None

        # Document 객체 생성
        doc = Document(
            hs_code=_find(r"HS\s*Code[:\s]*([\d]+)"),          # HS 코드 추출
            declaration_no=_find(r"신고번호[:\s]*([\w-]+)"),  # 신고번호 추출
            importer=_find(r"수입자[:\s]*([가-힣A-Za-z\s]+)"), # 수입자 추출
            raw_text=raw_text
        )

        # DynamoDB에 저장 후 doc_id 반환
        doc_id = self.repository.save(doc)
        logger.info(f"Document saved with ID: {doc_id}")
        return doc_id
