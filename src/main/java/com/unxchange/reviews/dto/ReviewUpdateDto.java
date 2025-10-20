package com.unxchange.reviews.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Size;

/**
 * DTO para actualizar una reseña existente
 */
@Schema(description = "Datos para actualizar una reseña existente")
public class ReviewUpdateDto {
    
    @Min(value = 1, message = "La calificación mínima es 1")
    @Max(value = 5, message = "La calificación máxima es 5")
    @Schema(description = "Nueva calificación", example = "4", minimum = "1", maximum = "5")
    private Integer rating;
    
    @Size(min = 10, max = 2000, message = "El contenido debe tener entre 10 y 2000 caracteres")
    @Schema(description = "Nuevo contenido", 
            example = "Actualizo mi reseña: muy buena experiencia, pero podría mejorar en algunos aspectos.")
    private String content;
    
    // Constructores
    public ReviewUpdateDto() {}
    
    public ReviewUpdateDto(Integer rating, String content) {
        this.rating = rating;
        this.content = content;
    }
    
    // Getters y Setters
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
    
    // Método para verificar si hay campos para actualizar
    public boolean hasUpdates() {
        return rating != null || (content != null && !content.trim().isEmpty());
    }
}