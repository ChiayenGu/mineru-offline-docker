# Use the official Ubuntu base image
FROM ubuntu:22.04

# Set environment variables to non-interactive to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install necessary packages
RUN apt-get update && \
    apt-get install -y \
        software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y \
        python3.10 \
        python3.10-venv \
        python3.10-distutils \
        python3-pip \
        wget \
        git \
        libgl1 \
        libglib2.0-0 \
        && rm -rf /var/lib/apt/lists/*

# Set Python 3.10 as the default python3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Create a virtual environment for MinerU
RUN python3 -m venv /opt/mineru_venv
COPY ./web_demo /opt/webdemo
WORKDIR /opt/webdemo

# Activate the virtual environment and install necessary Python packages
RUN /bin/bash -c "source /opt/mineru_venv/bin/activate && \
    pip3 install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple && \
    pip3 install -r /opt/webdemo/requirements.txt --extra-index-url https://wheels.myhloli.com -i https://mirrors.aliyun.com/pypi/simple"
RUN /bin/bash -c "source /opt/mineru_venv/bin/activate &&     pip3 install paddlepaddle-gpu==3.0.0rc1 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/"

# Copy the configuration file template and install magic-pdf latest
RUN /bin/bash -c "wget https://gcore.jsdelivr.net/gh/opendatalab/MinerU@master/magic-pdf.template.json && \
    cp magic-pdf.template.json /root/magic-pdf.json && \
    source /opt/mineru_venv/bin/activate && \
    pip3 install -U magic-pdf -i https://mirrors.aliyun.com/pypi/simple"

# Download models and update the configuration file
RUN /bin/bash -c "pip3 install modelscope && \
    wget https://gcore.jsdelivr.net/gh/opendatalab/MinerU@master/scripts/download_models.py -O download_models.py && \
    python3 download_models.py && \
    sed -i 's|cpu|cuda|g' /root/magic-pdf.json"

# 创建必要的目录 下载paddleocr模型
RUN mkdir -p /root/.paddleocr/whl/det/ch/ch_PP-OCRv4_det_infer \
    && mkdir -p /root/.paddleocr/whl/rec/ch/ch_PP-OCRv4_rec_infer \
    && mkdir -p /root/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer \
    && wget -O /root/.paddleocr/whl/det/ch/ch_PP-OCRv4_det_infer/ch_PP-OCRv4_det_infer.tar https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_det_infer.tar \
    && wget -O /root/.paddleocr/whl/rec/ch/ch_PP-OCRv4_rec_infer/ch_PP-OCRv4_rec_infer.tar https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_rec_infer.tar \
    && wget -O /root/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer/ch_ppocr_mobile_v2.0_cls_infer.tar https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar

EXPOSE 5559

# 保持虚拟环境激活状态执行应用
CMD ["/opt/mineru_venv/bin/python", "app.py"]
