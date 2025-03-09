# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos e instálalo
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia todo el código de la aplicación
COPY . /app

# Expone el puerto en el que corre la aplicación (8000)
EXPOSE 8000

# Comando para iniciar la aplicación en modo desarrollo con recarga automática
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
