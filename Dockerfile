# 使用官方 Python 3.10 镜像作为基础镜像
FROM python:3.10.9-slim

# 安装构建工具和 MySQL 客户端开发包
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    build-essential

# 设置工作目录
WORKDIR /app

# 创建并激活虚拟环境
RUN python -m venv /venv
ENV PATH="/venv/bin:${PATH}"

# 安装 pip 的最新版本
RUN pip install --upgrade pip

# 将 requirements.txt 复制到容器中
COPY requirements.txt .

# 将项目文件复制到容器中
COPY . .

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 确保 uvicorn 可以被找到
RUN pip show uvicorn

# 暴露端口
EXPOSE 8000

# 运行 FastAPI 项目
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
