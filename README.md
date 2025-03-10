# virtual-commerce


- Se tomó la decisón de diseño de utilizar tailwind en en frontend con la finalidad de priorizar velocidad de desarrollo por sobre control especifico de detalles css, daod que los requerimientos no tenian especificaciones de diseño especificas.

- asumió que los productos no varian durante el dia, por lo que la base de datos de productos se actualiza solo una vez al día mediante un cron job.

- Dado que las apis de envios daban problemas con su certificado ssl se decidó usar verify = false en los parametros de post hacia ellas 

Se agregó una verificación de stock antes de navegar a la vista de cotizar despacho, esto para evitar llamar a las apis externas de envios cuando ya sabemsos de antemano que no hay stcok del carrito.

se guardan los carritos en base de datos postgres para asegurar persistencia de los datos, el boton vaciar carrito borra el elemento de la base de datos.

cuando se hace la consula a la api de dummy products los resultado se guardan en la base de datos para tener cosnistencia.




test

para ejecutar test 
pip install pytest
pytest tests/test_shipping.py --disable-warnings


# 🚀 Cómo correr los tests

Este proyecto usa **pytest** para ejecutar pruebas unitarias y validar el correcto funcionamiento del servicio de tarificación de envíos.

## 📌 Prerrequisitos
Asegúrate de que **Docker** y **Docker Compose** estén instalados en tu máquina.

## 🛠 1️⃣ Levantar los contenedores
Antes de ejecutar los tests, asegúrate de que los contenedores estén corriendo:

docker-compose up -d

## 🧪 2️⃣ Ejecutar los tests
Para correr los tests dentro del contenedor, usa el siguiente comando:

```docker exec -it fastapi_app pytest tests --disable-warnings```

📌 Reemplaza fastapi_app por el nombre real del servicio en docker-compose.yml si es diferente.

## ✅ 3️⃣ Verificar los resultados
Si los tests pasan correctamente, deberías ver una salida similar a esta:

```======================================================= test session starts =======================================================
platform linux -- Python 3.10.16, pytest-8.3.5, pluggy-1.5.0
rootdir: /app
plugins: anyio-4.8.0
collected 2 items                                                                                                                  

tests/test_shipping.py ..                                                                                                   [100%] 

======================================================== 2 passed in 9.83s ========================================================
```
