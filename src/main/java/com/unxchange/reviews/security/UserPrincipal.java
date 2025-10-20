package com.unxchange.reviews.security;

import java.security.Principal;

/**
 * Clase que representa el usuario autenticado
 */
public class UserPrincipal implements Principal {
    
    private final String email;
    private final String role;
    
    public UserPrincipal(String email, String role) {
        this.email = email;
        this.role = role;
    }
    
    @Override
    public String getName() {
        return email;
    }
    
    public String getEmail() {
        return email;
    }
    
    public String getRole() {
        return role;
    }
    
    public boolean isAdmin() {
        return "administrador".equalsIgnoreCase(role);
    }
}