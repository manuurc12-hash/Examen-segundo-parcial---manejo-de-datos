FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instalar Java, Python 3, OpenSSH y herramientas del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    python3 \
    python3-pip \
    curl \
    tar \
    procps \
    openssh-server \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Definir variables de entorno (Requisito A1)
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Descargar e instalar Hadoop 3.3.6 Standalone
RUN curl -sSL https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz \
    | tar -xz -C /opt/ \
    && mv /opt/hadoop-${HADOOP_VERSION} ${HADOOP_HOME}

WORKDIR /app

CMD ["tail", "-f", "/dev/null"]
