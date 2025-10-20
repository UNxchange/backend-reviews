package com.unxchange.reviews.dto;

import com.unxchange.reviews.model.Review;
import io.swagger.v3.oas.annotations.media.Schema;

import java.util.List;

/**
 * DTO para la respuesta paginada de reseñas
 */
@Schema(description = "Respuesta paginada de reseñas")
public class ReviewListResponseDto {
    
    @Schema(description = "Número total de reseñas", example = "50")
    private long total;
    
    @Schema(description = "Límite de resultados por página", example = "20")
    private int limit;
    
    @Schema(description = "Número de resultados omitidos", example = "0")
    private int skip;
    
    @Schema(description = "Lista de reseñas")
    private List<Review> reviews;
    
    // Constructores
    public ReviewListResponseDto() {}
    
    public ReviewListResponseDto(long total, int limit, int skip, List<Review> reviews) {
        this.total = total;
        this.limit = limit;
        this.skip = skip;
        this.reviews = reviews;
    }
    
    // Getters y Setters
    public long getTotal() {
        return total;
    }
    
    public void setTotal(long total) {
        this.total = total;
    }
    
    public int getLimit() {
        return limit;
    }
    
    public void setLimit(int limit) {
        this.limit = limit;
    }
    
    public int getSkip() {
        return skip;
    }
    
    public void setSkip(int skip) {
        this.skip = skip;
    }
    
    public List<Review> getReviews() {
        return reviews;
    }
    
    public void setReviews(List<Review> reviews) {
        this.reviews = reviews;
    }
}