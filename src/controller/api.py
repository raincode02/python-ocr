from fastapi import FastAPI, UploadFile
from infrastructure.textract_service import TextractOCRService
from infrastructure.dynamodb_repository import DynamoDBDocumentRepository
from usecase.document_processor import DocumentProcessor
import boto3
import tempfile
import logging
import os  # 환경변수 사용

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# 환경변수에서 AWS 설정 불러오기
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE")

# AWS 클라이언트 생성
s3_client = boto3.client("s3", region_name=AWS_REGION)

# 의존성 주입
ocr_service = TextractOCRService()
repo = DynamoDBDocumentRepository(table_name=DYNAMODB_TABLE)  # 테이블 이름 env 기반
processor = DocumentProcessor(ocr_service, repo)

@app.post("/upload")
async def upload(file: UploadFile):
    # 업로드 받은 파일을 임시 파일로 저장
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(await file.read())  # 파일 읽기
        tmp.flush()
        key = file.filename
        # S3 업로드
        s3_client.upload_file(tmp.name, S3_BUCKET, key)
        s3_path = f"s3://{S3_BUCKET}/{key}"
        # DocumentProcessor로 OCR + 필드 추출 + 저장
        doc_id = processor.process_pdf(s3_path)
        logger.info(f"Uploaded and processed file: {key}")
        return {"doc_id": doc_id}

@app.get("/document/{doc_id}")
def get_document(doc_id: str):
    # doc_id로 DynamoDB 조회
    doc = repo.get(doc_id)
    if not doc:
        logger.warning(f"Document {doc_id} not found")
        return {"error": "Document not found"}
    return doc
