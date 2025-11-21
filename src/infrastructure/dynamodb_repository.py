from interface.repository import DocumentRepository
from domain.document import Document
import boto3
from uuid import uuid4
import os

# DynamoDBDocumentRepository: DocumentRepository 인터페이스 구현
class DynamoDBDocumentRepository(DocumentRepository):
    def __init__(self):
        # 환경변수에서 테이블명 가져오기
        self.table_name = os.getenv("DYNAMODB_TABLE")
        # DynamoDB 테이블 객체 생성
        self.client = boto3.resource('dynamodb').Table(self.table_name)

    def save(self, doc: Document) -> str:
        # 문서 ID 생성
        doc_id = str(uuid4())
        # 저장할 아이템 구성
        item = {
            "doc_id": doc_id,
            "hs_code": doc.hs_code or "",
            "declaration_no": doc.declaration_no or "",
            "importer": doc.importer or "",
            "raw_text": doc.raw_text or ""
        }
        # DynamoDB에 저장
        self.client.put_item(Item=item)
        return doc_id  # 저장된 문서 ID 반환

    def get(self, doc_id: str) -> Document | None:
        # DynamoDB에서 doc_id로 조회
        resp = self.client.get_item(Key={"doc_id": doc_id})
        item = resp.get("Item")
        if not item:
            return None  # 없으면 None 반환
        # 조회된 데이터로 Document 객체 생성
        return Document(
            hs_code=item.get("hs_code"),
            declaration_no=item.get("declaration_no"),
            importer=item.get("importer"),
            raw_text=item.get("raw_text")
        )
