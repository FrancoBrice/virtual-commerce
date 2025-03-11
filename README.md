# Virtual Commerce

## 🚀 Despliegue local con Docker

La aplicación está completamente dockerizada y puede ejecutarse en local con el siguiente comando:

```sh
docker-compose up --build -d 
```

Esto desplegará el frontend en 🔗 **[http://localhost:3000/](http://localhost:3000/)**.

## 🌍 Deploy en AWS

La aplicación está desplegada en una instancia **EC2** de AWS, asociada al dominio:

🔗 **[https://virtualcommerce.work.gd/](https://virtualcommerce.work.gd/)**

Para esto, se configuró:
- Una instancia **t2.micro**
- Una dirección **IP elástica**

## 🔧 Configuración de entorno

Antes de ejecutar la aplicación, asegúrate de crear un archivo `.env` en la carpeta base con el siguiente formato:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=virtualcommerce
DATABASE_URL=postgresql://postgres:password@db:5432/virtualcommerce

# API Keys couriers
TRAELOYA_API_KEY= Api Key proporcionada
TRAELOYA_API_URL="https://recruitment.weflapp.com/tarifier/traelo_ya"

UDER_API_KEY= Api Key proporcionada
UDER_API_URL="https://recruitment.weflapp.com/tarifier/uder"
```


En la carpeta `frontend`, también debes crear un archivo `.env` con la siguiente configuración:

```env
REACT_APP_API_URL=http://localhost:8000/api
```

## 🧪 Cómo ejecutar los tests

Este proyecto usa **pytest** para ejecutar pruebas unitarias y validar el correcto funcionamiento del servicio de tarificación de envíos.

### 📌 Prerrequisitos

Asegúrate de que **Docker** y **Docker Compose** estén instalados en tu máquina.

### 🛠 1️⃣ Levantar los contenedores

Antes de ejecutar los tests, asegúrate de que los contenedores estén corriendo:

```sh
docker-compose up -d
```

### 🧪 2️⃣ Ejecutar los tests

Para correr los tests dentro del contenedor, usa el siguiente comando:

```sh
docker exec -it fastapi_app pytest tests --disable-warnings
```

📌 *Reemplaza `fastapi_app` por el nombre real del servicio en `docker-compose.yml` si es diferente.*

### ✅ 3️⃣ Verificar los resultados

Si los tests pasan correctamente, deberías ver una salida similar a esta:

```sh
======================================================= test session starts =======================================================
platform linux -- Python 3.10.16, pytest-8.3.5, pluggy-1.5.0
rootdir: /app
plugins: anyio-4.8.0
collected 2 items                                                                                                                  

tests/test_shipping.py ..                                                                                                   [100%] 

======================================================== 2 passed in 9.83s ========================================================
```

---


## 📱 Responsividad
La aplicación es completamente responsive, adaptándose tanto a dispositivos móviles como a navegadores web.

## 📌 Notas 


- Dado que las APIs de envíos daban problemas con su certificado SSL, se decidió usar verify = false en los parámetros de POST hacia ellas.

- Se agregó una verificación de stock antes de navegar a la vista de cotizar despacho, esto para evitar llamar a las APIs externas de envíos cuando ya sabemos de antemano que no hay stock en el carrito.

- Se guardan los carritos en una base de datos PostgreSQL para asegurar la persistencia de los datos. El botón "Vaciar carrito" borra el elemento de la base de datos.

- Cuando se hace la consulta a la API de dummy products, los resultados se guardan en la base de datos para mantener la consistencia.

- Las respuestas de api/cart/random y api/cart tienen una pequeña latencia, ya que recuperan todos los productos a través de la API dummyjson, tal como se indica en las instrucciones.
