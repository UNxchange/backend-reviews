package com.unxchange.reviews.model;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.*;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.LocalDateTime;

/**
 * Modelo principal de la Reseña
 */
@Document(collection = "reviews")
@Schema(description = "Reseña de una experiencia de movilidad académica")
public class Review {
    
    @Id
    @JsonProperty("id")
    @Schema(description = "ID único de la reseña", example = "60c72b2f9b1e8d001c8e4a2f")
    private String id;
    
    @NotBlank(message = "El ID del autor es obligatorio")
    @Email(message = "El ID del autor debe ser un email válido")
    @JsonProperty("author_id")
    @Schema(description = "Email del autor de la reseña", example = "usuario@ejemplo.com")
    private String authorId;
    
    @NotBlank(message = "El ID de la convocatoria es obligatorio")
    @JsonProperty("convocatoria_id")
    @Schema(description = "ID de la convocatoria reseñada", example = "60c72b2f9b1e8d001c8e4a31")
    private String convocatoriaId;
    
    @NotNull(message = "La calificación es obligatoria")
    @Min(value = 1, message = "La calificación mínima es 1")
    @Max(value = 5, message = "La calificación máxima es 5")
    @Schema(description = "Calificación de 1 a 5 estrellas", example = "4", minimum = "1", maximum = "5")
    private Integer rating;
    
    @NotBlank(message = "El contenido es obligatorio")
    @Size(min = 10, max = 2000, message = "El contenido debe tener entre 10 y 2000 caracteres")
    @Schema(description = "Contenido de la reseña", example = "Excelente experiencia de movilidad.")
    private String content;
    
    @CreatedDate
    @JsonProperty("created_at")
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss'Z'")
    @Schema(description = "Fecha de creación", example = "2025-07-08T12:00:00Z")
    private LocalDateTime createdAt;
    
    @LastModifiedDate
    @JsonProperty("updated_at")
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss'Z'")
    @Schema(description = "Fecha de última actualización", example = "2025-07-08T14:30:00Z")
    private LocalDateTime updatedAt;
    
    // Constructores
    public Review() {}
    
    public Review(String authorId, String convocatoriaId, Integer rating, String content) {
        this.authorId = authorId;
        this.convocatoriaId = convocatoriaId;
        this.rating = rating;
        this.content = content.trim();
    }
    
    // Getters y Setters
    public String getId() {
        return id;
    }
    
    public void setId(String id) {
        this.id = id;
    }
    
    public String getAuthorId() {
        return authorId;
    }
    
    public void setAuthorId(String authorId) {
        this.authorId = authorId;
    }
    
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
        this.content = content != null ? content.trim() : null;
    }
    
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
    
    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
    
    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }
    
    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }
}