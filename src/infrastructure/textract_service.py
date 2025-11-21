from interface.ocr_service import OCRService
import boto3
import time
import logging

# 로깅 설정
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# TextractOCRService: OCRService 인터페이스 구현
class TextractOCRService(OCRService):
    def __init__(self):
        # Textract API 클라이언트 생성
        self.client = boto3.client('textract')

    def extract_text(self, file_s3_path: str) -> str:
        # S3 경로 파싱
        bucket, key = self._parse_s3_path(file_s3_path)
        logger.info(f"Starting Textract job for {file_s3_path}")

        # Textract 비동기 텍스트 추출 시작
        try:
            response = self.client.start_document_text_detection(
                DocumentLocation={'S3Object': {'Bucket': bucket, 'Name': key}}
            )
        except Exception as e:
            logger.error(f"Textract start job failed: {e}")
            raise

        job_id = response['JobId']  # Textract Job ID 반환

        # Textract 완료 대기 (폴링)
        while True:
            try:
                result = self.client.get_document_text_detection(JobId=job_id)
            except Exception as e:
                logger.error(f"Textract get result failed: {e}")
                raise

            status = result['JobStatus']  # SUCCEEDED, FAILED, IN_PROGRESS
            if status in ['SUCCEEDED', 'FAILED']:
                break  # 완료되면 루프 종료
            logger.info("Waiting for Textract job completion...")
            time.sleep(2)  # 2초 대기 후 재조회

        if status == 'FAILED':
            logger.error("Textract job failed")
            raise Exception("Textract job failed")  # 실패 처리

        # 결과 블록에서 LINE 타입 텍스트만 추출
        lines = [b['Text'] for b in result['Blocks'] if b['BlockType'] == 'LINE']
        logger.info(f"Textract job completed with {len(lines)} lines")
        return "\n".join(lines)  # 모든 줄 합쳐서 반환

    def _parse_s3_path(self, s3_path: str):
        # s3://bucket/key.pdf 형식에서 버킷과 키 분리
        path = s3_path.replace("s3://", "")
        bucket, key = path.split("/", 1)
        return bucket, key
