package com.unxchange.reviews.exception;

/**
 * Excepción lanzada cuando un usuario no tiene permisos
 */
public class UnauthorizedException extends RuntimeException {
    
    public UnauthorizedException(String message) {
        super(message);
    }
}