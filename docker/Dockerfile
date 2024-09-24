# 使用官方的 Python 3.9 作為基礎映像
FROM python:3.9

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝依賴
COPY src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 複製應用代碼
COPY src .

# 暴露 FastAPI 默認端口
EXPOSE 8000

# 使用 uvicorn 運行 FastAPI 應用
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]