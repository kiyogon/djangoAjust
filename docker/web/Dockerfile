# Dockerfile
FROM --platform=linux/x86_64 public.ecr.aws/docker/library/python:3.11

# 環境変数の設定
ENV PYTHONUNBUFFERED 1

# 作業ディレクトリの設定
WORKDIR /app/ajust_pj

# コンテナが立ち上がるときにローカルからのファイルがコピーされないのでコンテナにファイルをコピー
COPY ./ajust_pj/ /app/ajust_pj

# コンテナ上でコマンドが実行される（requirements.txtからライブラリをインストールする）
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
