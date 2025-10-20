# Dockerfile para el microservicio de reseñas en Java
FROM openjdk:17-jdk-slim

# Información del mantenedor
LABEL maintainer="UnxChange Team"
LABEL description="Microservicio de Reseñas - UnxChange"
LABEL version="1.0.1"

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de Maven
COPY pom.xml .
COPY mvnw .
COPY .mvn .mvn

# Descargar dependencias (para aprovechar cache de Docker)
RUN ./mvnw dependency:go-offline -B

# Copiar código fuente
COPY src ./src

# Compilar la aplicación
RUN ./mvnw clean package -DskipTests

# Exponer puerto
EXPOSE 8003

# Variables de entorno por defecto
ENV MONGO_URI=mongodb://localhost:27017
ENV DATABASE_NAME=unxchange_reviews
ENV SECRET_KEY=your-super-secret-key-change-this-in-production-unxchange-2025
ENV CORS_ORIGINS=http://localhost,http://localhost:80,http://localhost:3000

# Comando para ejecutar la aplicación
CMD ["java", "-jar", "target/reviews-service-1.0.1.jar"]

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8003/reviews/health/check || exit 1