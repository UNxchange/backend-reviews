package com.unxchange.reviews;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.mongodb.config.EnableMongoAuditing;

/**
 * Aplicación principal del microservicio de reseñas UnxChange
 * 
 * Este microservicio gestiona las reseñas de experiencias de movilidad académica.
 * Permite a los estudiantes compartir sus experiencias y calificar las convocatorias.
 */
@SpringBootApplication
@EnableMongoAuditing
public class ReviewsServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(ReviewsServiceApplication.class, args);
        System.out.println("🚀 Servicio de reseñas iniciado correctamente");
        System.out.println("📝 Documentación disponible en: http://localhost:8003/docs");
    }
}