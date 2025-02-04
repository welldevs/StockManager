# Usa a imagem base com Oracle Instant Client
FROM ghcr.io/oracle/oraclelinux8-instantclient:21

# Define o diretório de trabalho no container
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY . /app

# Atualiza os repositórios e instala Python 3.9 corretamente
RUN yum install -y python39 python39-pip python39-setuptools && \
    alternatives --set python3 /usr/bin/python3.9 && \
    python3 -m ensurepip && \
    python3 -m pip install --upgrade pip && \
    yum clean all

# Instala dependências do projeto
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Define as variáveis de ambiente do Oracle Instant Client
ENV LD_LIBRARY_PATH=/usr/lib/oracle/21/client64/lib
ENV TNS_ADMIN=/app/config

# Define a pasta app no PYTHONPATH para evitar problemas de importação
ENV PYTHONPATH=/app

# Expõe a porta do FastAPI
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
