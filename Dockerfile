# Dockerfile para el microservicio de reseñas en Java
FROM maven:3.9-amazoncorretto-17 AS builder

# Información del mantenedor
LABEL maintainer="UnxChange Team"
LABEL description="Microservicio de Reseñas - UnxChange"
LABEL version="1.0.2"

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de Maven
COPY pom.xml .

# Descargar dependencias (para aprovechar cache de Docker)
RUN mvn dependency:go-offline -B

# Copiar código fuente
COPY src ./src

# Compilar la aplicación
RUN mvn clean package -DskipTests

# Etapa final con JRE
FROM openjdk:17-jdk-slim

# Instalar curl para health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar JAR desde builder
COPY --from=builder /app/target/*.jar app.jar

# Copiar JAR desde builder
COPY --from=builder /app/target/*.jar app.jar

# Exponer puerto
EXPOSE 8003

# Variables de entorno por defecto
ENV MONGO_URI=mongodb://localhost:27017
ENV DATABASE_NAME=unxchange_reviews
ENV SECRET_KEY=your-super-secret-key-change-this-in-production-unxchange-2025
ENV CORS_ORIGINS=http://localhost,http://localhost:80,http://localhost:3000

# Comando para ejecutar la aplicación
CMD ["java", "-jar", "app.jar"]

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8003/reviews/health/check || exit 1