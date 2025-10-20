package com.unxchange.reviews.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

/**
 * Controlador para el endpoint raíz
 */
@RestController
@Tag(name = "Root", description = "Información básica del servicio")
public class RootController {
    
    @Operation(summary = "Información del servicio", 
               description = "Retorna información básica del servicio de reseñas")
    @ApiResponse(responseCode = "200", description = "Información del servicio")
    @GetMapping("/")
    public ResponseEntity<Map<String, Object>> root() {
        Map<String, Object> info = new HashMap<>();
        info.put("service", "UnxChange Reviews API");
        info.put("version", "1.0.1");
        info.put("status", "running");
        info.put("docs", "/docs");
        info.put("health", "/reviews/health/check");
        
        return ResponseEntity.ok(info);
    }
}