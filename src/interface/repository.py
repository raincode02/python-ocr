from abc import ABC, abstractmethod
from domain.document import Document

# DocumentRepository 인터페이스: 저장소 구현체가 반드시 구현해야 하는 메서드 정의
class DocumentRepository(ABC):
    @abstractmethod
    def save(self, doc: Document) -> str:
        # Document 객체를 저장하고 고유 ID 반환
        pass

    @abstractmethod
    def get(self, doc_id: str) -> Document | None:
        # 고유 ID로 Document 조회
        pass
