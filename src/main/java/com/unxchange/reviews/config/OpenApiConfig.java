package com.unxchange.reviews.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.security.SecurityScheme;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Configuración de OpenAPI/Swagger
 */
@Configuration
public class OpenApiConfig {
    
    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .components(new Components()
                        .addSecuritySchemes("bearerAuth",
                                new SecurityScheme()
                                        .type(SecurityScheme.Type.HTTP)
                                        .scheme("bearer")
                                        .bearerFormat("JWT")))
                .info(new Info()
                        .title("API de Reseñas UnxChange")
                        .version("1.0.1")
                        .description("""
                                Microservicio para gestionar reseñas de estudiantes sobre sus experiencias de movilidad académica.
                                
                                ## Funcionalidades principales
                                
                                * **Crear reseñas** - Los usuarios pueden compartir sus experiencias
                                * **Consultar reseñas** - Filtrar por convocatoria, autor, con paginación
                                * **Editar reseñas** - Solo el autor puede modificar sus reseñas
                                * **Eliminar reseñas** - Autor o administrador pueden eliminar
                                * **Estadísticas** - Obtener promedios y distribución de ratings por convocatoria
                                * **Autenticación JWT** - Todos los endpoints requieren autenticación
                                
                                ## Seguridad
                                
                                Todos los endpoints están protegidos con JWT. Incluye el token en el header:
                                
                                ```
                                Authorization: Bearer <tu-token-jwt>
                                ```
                                """));
    }
}