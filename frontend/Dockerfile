# Usamos una imagen de Node.js para construir la app de React
FROM node:18-alpine AS builder

WORKDIR /app

# Copiar package.json e instalar dependencias
COPY package.json package-lock.json ./
RUN npm install --silent

# Copiar el resto de los archivos del frontend
COPY . .

# Construir la aplicación
RUN npm run build

# Usamos Nginx para servir la app en producción
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html

# Configurar Nginx con el archivo de configuración personalizado
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponer el puerto donde correrá el frontend
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
