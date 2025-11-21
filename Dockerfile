# Dockerfile
FROM python:3.12-slim
WORKDIR /app

# 종속성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 복사
COPY . .

# AWS 환경변수는 Docker 실행 시 주입
# FastAPI 앱 실행
CMD ["uvicorn", "controller.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
