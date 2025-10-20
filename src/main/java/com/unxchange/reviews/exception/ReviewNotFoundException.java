package com.unxchange.reviews.exception;

/**
 * Excepción lanzada cuando no se encuentra una reseña
 */
public class ReviewNotFoundException extends RuntimeException {
    
    public ReviewNotFoundException(String message) {
        super(message);
    }
}