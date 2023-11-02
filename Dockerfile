FROM python:3.11-slim

WORKDIR /app

ADD requirements.txt /app

ARG DEBIAN_MIRROR_HOST=mirrors.tuna.tsinghua.edu.cn
ARG PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

RUN rm /etc/apt/sources.list.d/debian.sources && \
    echo "deb http://${DEBIAN_MIRROR_HOST}/debian/ bookworm main contrib non-free non-free-firmware" > /etc/apt/sources.list && \
    echo "deb http://${DEBIAN_MIRROR_HOST}/debian/ bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb http://${DEBIAN_MIRROR_HOST}/debian/ bookworm-backports main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb http://${DEBIAN_MIRROR_HOST}/debian-security bookworm-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends openssl ca-certificates default-mysql-client && \
    pip install -r requirements.txt -i ${PIP_INDEX_URL} && \
    apt-get clean && \
    pip cache purge

CMD [ "python", "main.py" ]