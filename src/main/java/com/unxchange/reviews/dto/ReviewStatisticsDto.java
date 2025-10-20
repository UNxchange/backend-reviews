package com.unxchange.reviews.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

import java.util.Map;

/**
 * DTO para estadísticas de reseñas por convocatoria
 */
@Schema(description = "Estadísticas detalladas de reseñas para una convocatoria")
public class ReviewStatisticsDto {
    
    @JsonProperty("convocatoria_id")
    @Schema(description = "ID de la convocatoria", example = "60c72b2f9b1e8d001c8e4a31")
    private String convocatoriaId;
    
    @JsonProperty("average_rating")
    @Schema(description = "Calificación promedio", example = "4.3", minimum = "0", maximum = "5")
    private Double averageRating;
    
    @JsonProperty("total_reviews")
    @Schema(description = "Número total de reseñas", example = "25")
    private Long totalReviews;
    
    @JsonProperty("rating_distribution")
    @Schema(description = "Distribución de calificaciones por estrella")
    private Map<String, Long> ratingDistribution;
    
    // Constructores
    public ReviewStatisticsDto() {}
    
    public ReviewStatisticsDto(String convocatoriaId, Double averageRating, Long totalReviews, Map<String, Long> ratingDistribution) {
        this.convocatoriaId = convocatoriaId;
        this.averageRating = averageRating;
        this.totalReviews = totalReviews;
        this.ratingDistribution = ratingDistribution;
    }
    
    // Getters y Setters
    public String getConvocatoriaId() {
        return convocatoriaId;
    }
    
    public void setConvocatoriaId(String convocatoriaId) {
        this.convocatoriaId = convocatoriaId;
    }
    
    public Double getAverageRating() {
        return averageRating;
    }
    
    public void setAverageRating(Double averageRating) {
        this.averageRating = averageRating;
    }
    
    public Long getTotalReviews() {
        return totalReviews;
    }
    
    public void setTotalReviews(Long totalReviews) {
        this.totalReviews = totalReviews;
    }
    
    public Map<String, Long> getRatingDistribution() {
        return ratingDistribution;
    }
    
    public void setRatingDistribution(Map<String, Long> ratingDistribution) {
        this.ratingDistribution = ratingDistribution;
    }
}