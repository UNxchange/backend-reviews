package com.unxchange.reviews.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.*;

/**
 * DTO para crear una nueva reseña
 */
@Schema(description = "Datos para crear una nueva reseña")
public class ReviewCreateDto {
    
    @NotBlank(message = "El ID de la convocatoria es obligatorio")
    @JsonProperty("convocatoria_id")
    @Schema(description = "ID de la convocatoria a reseñar", example = "60c72b2f9b1e8d001c8e4a31", required = true)
    private String convocatoriaId;
    
    @NotNull(message = "La calificación es obligatoria")
    @Min(value = 1, message = "La calificación mínima es 1")
    @Max(value = 5, message = "La calificación máxima es 5")
    @Schema(description = "Calificación de 1 a 5 estrellas", example = "5", minimum = "1", maximum = "5", required = true)
    private Integer rating;
    
    @NotBlank(message = "El contenido es obligatorio")
    @Size(min = 10, max = 2000, message = "El contenido debe tener entre 10 y 2000 caracteres")
    @Schema(description = "Contenido de la reseña", 
            example = "¡Excelente experiencia! Aprendí mucho y conocí personas increíbles.", 
            required = true)
    private String content;
    
    // Constructores
    public ReviewCreateDto() {}
    
    public ReviewCreateDto(String convocatoriaId, Integer rating, String content) {
        this.convocatoriaId = convocatoriaId;
        this.rating = rating;
        this.content = content;
    }
    
    // Getters y Setters
    public String getConvocatoriaId() {
        return convocatoriaId;
    }
    
    public void setConvocatoriaId(String convocatoriaId) {
        this.convocatoriaId = convocatoriaId;
    }
    
    public Integer getRating() {
        return rating;
    }
    
    public void setRating(Integer rating) {
        this.rating = rating;
    }
    
    public String getContent() {
        return content;
    }
    
    public void setContent(String content) {
        this.content = content;
    }
}