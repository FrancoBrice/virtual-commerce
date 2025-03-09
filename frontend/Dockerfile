# Stage 1: construir la aplicación React
FROM node:16-alpine as build
WORKDIR /app
# Copia package.json y package-lock.json para instalar dependencias
COPY package.json package-lock.json ./
RUN npm install
# Copia el resto del código y crea la build de producción
COPY . ./
RUN npm run build

# Stage 2: servir la build con Nginx
FROM nginx:stable-alpine
# Copia la build a la carpeta donde Nginx sirve los archivos estáticos
COPY --from=build /app/build /usr/share/nginx/html
# Expone el puerto 80
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
