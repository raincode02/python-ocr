from abc import ABC, abstractmethod

# OCRService 인터페이스: OCR 구현체가 반드시 구현해야 하는 메서드 정의
class OCRService(ABC):
    @abstractmethod
    def extract_text(self, file_s3_path: str) -> str:
        # S3 경로로 전달된 PDF/이미지에서 텍스트 추출
        pass
