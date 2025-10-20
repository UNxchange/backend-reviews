package com.unxchange.reviews.controller;

import com.unxchange.reviews.dto.*;
import com.unxchange.reviews.model.Review;
import com.unxchange.reviews.security.UserPrincipal;
import com.unxchange.reviews.service.ReviewService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Controlador REST para operaciones de reseñas
 */
@RestController
@RequestMapping("/reviews")
@Tag(name = "Reviews", description = "API para gestión de reseñas de experiencias de movilidad académica")
@SecurityRequirement(name = "bearerAuth")
public class ReviewController {
    
    @Autowired
    private ReviewService reviewService;
    
    @Operation(summary = "Crear una nueva reseña", 
               description = "Crea una nueva reseña para una convocatoria. Requiere autenticación.")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "201", description = "Reseña creada exitosamente"),
        @ApiResponse(responseCode = "400", description = "Datos de entrada inválidos"),
        @ApiResponse(responseCode = "401", description = "No autenticado")
    })
    @PostMapping
    public ResponseEntity<Review> createReview(
            @Valid @RequestBody ReviewCreateDto reviewDto,
            @AuthenticationPrincipal UserPrincipal user) {
        
        Review review = reviewService.createReview(reviewDto, user);
        return ResponseEntity.status(HttpStatus.CREATED).body(review);
    }
    
    @Operation(summary = "Obtener reseñas con filtros", 
               description = "Obtiene una lista paginada de reseñas con filtros opcionales")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Lista de reseñas obtenida exitosamente"),
        @ApiResponse(responseCode = "401", description = "No autenticado")
    })
    @GetMapping
    public ResponseEntity<ReviewListResponseDto> getReviews(
            @Parameter(description = "Filtrar por ID de convocatoria")
            @RequestParam(required = false) String convocatoria_id,
            
            @Parameter(description = "Filtrar por email del autor")
            @RequestParam(required = false) String author_id,
            
            @Parameter(description = "Número máximo de resultados")
            @RequestParam(defaultValue = "20") int limit,
            
            @Parameter(description = "Número de resultados a saltar")
            @RequestParam(defaultValue = "0") int skip,
            
            @Parameter(description = "Campo por el cual ordenar")
            @RequestParam(defaultValue = "createdAt") String sort_by,
            
            @Parameter(description = "Orden: -1 descendente, 1 ascendente")
            @RequestParam(defaultValue = "-1") int sort_order,
            
            @AuthenticationPrincipal UserPrincipal user) {
        
        // Validar límites
        if (limit > 100) limit = 100;
        if (limit < 1) limit = 20;
        if (skip < 0) skip = 0;
        
        ReviewListResponseDto response = reviewService.getReviews(
                convocatoria_id, author_id, limit, skip, sort_by, sort_order);
        
        return ResponseEntity.ok(response);
    }
    
    @Operation(summary = "Obtener reseña por ID", 
               description = "Obtiene una reseña específica por su ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Reseña encontrada"),
        @ApiResponse(responseCode = "404", description = "Reseña no encontrada"),
        @ApiResponse(responseCode = "401", description = "No autenticado")
    })
    @GetMapping("/{id}")
    public ResponseEntity<Review> getReviewById(
            @Parameter(description = "ID de la reseña")
            @PathVariable String id,
            @AuthenticationPrincipal UserPrincipal user) {
        
        Review review = reviewService.getReviewById(id);
        return ResponseEntity.ok(review);
    }
    
    @Operation(summary = "Actualizar reseña", 
               description = "Actualiza una reseña existente. Solo el autor puede editar.")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Reseña actualizada exitosamente"),
        @ApiResponse(responseCode = "403", description = "Sin permisos para editar"),
        @ApiResponse(responseCode = "404", description = "Reseña no encontrada"),
        @ApiResponse(responseCode = "401", description = "No autenticado")
    })
    @PatchMapping("/{id}")
    public ResponseEntity<Review> updateReview(
            @Parameter(description = "ID de la reseña")
            @PathVariable String id,
            @Valid @RequestBody ReviewUpdateDto updateDto,
            @AuthenticationPrincipal UserPrincipal user) {
        
        Review updatedReview = reviewService.updateReview(id, updateDto, user);
        return ResponseEntity.ok(updatedReview);
    }
    
    @Operation(summary = "Eliminar reseña", 
               description = "Elimina una reseña. Solo el autor o un administrador pueden eliminar.")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "204", description = "Reseña eliminada exitosamente"),
        @ApiResponse(responseCode = "403", description = "Sin permisos para eliminar"),
        @ApiResponse(responseCode = "404", description = "Reseña no encontrada"),
        @ApiResponse(responseCode = "401", description = "No autenticado")
    })
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteReview(
            @Parameter(description = "ID de la reseña")
            @PathVariable String id,
            @AuthenticationPrincipal UserPrincipal user) {
        
        reviewService.deleteReview(id, user);
        return ResponseEntity.noContent().build();
    }
    
    @Operation(summary = "Obtener estadísticas de convocatoria", 
               description = "Obtiene estadísticas detalladas de reseñas para una convocatoria específica")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Estadísticas obtenidas exitosamente"),
        @ApiResponse(responseCode = "401", description = "No autenticado")
    })
    @GetMapping("/statistics/{convocatoria_id}")
    public ResponseEntity<ReviewStatisticsDto> getConvocatoriaStatistics(
            @Parameter(description = "ID de la convocatoria")
            @PathVariable String convocatoria_id,
            @AuthenticationPrincipal UserPrincipal user) {
        
        ReviewStatisticsDto statistics = reviewService.getStatisticsByConvocatoria(convocatoria_id);
        return ResponseEntity.ok(statistics);
    }
    
    @Operation(summary = "Obtener mis reseñas", 
               description = "Obtiene todas las reseñas creadas por el usuario autenticado")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Reseñas del usuario obtenidas exitosamente"),
        @ApiResponse(responseCode = "401", description = "No autenticado")
    })
    @GetMapping("/me/reviews")
    public ResponseEntity<List<Review>> getMyReviews(
            @Parameter(description = "Cantidad máxima de resultados")
            @RequestParam(defaultValue = "10") int limit,
            
            @Parameter(description = "Cantidad de resultados a saltar")
            @RequestParam(defaultValue = "0") int skip,
            
            @AuthenticationPrincipal UserPrincipal user) {
        
        // Validar límites
        if (limit > 50) limit = 50;
        if (limit < 1) limit = 10;
        if (skip < 0) skip = 0;
        
        List<Review> reviews = reviewService.getUserReviews(user.getEmail(), limit, skip);
        return ResponseEntity.ok(reviews);
    }
    
    @Operation(summary = "Health check", 
               description = "Verifica que el servicio de reseñas esté funcionando correctamente")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Servicio funcionando correctamente")
    })
    @GetMapping("/health/check")
    public ResponseEntity<Map<String, Object>> healthCheck() {
        Map<String, Object> health = new HashMap<>();
        health.put("status", "healthy");
        health.put("service", "reviews-service");
        health.put("timestamp", LocalDateTime.now());
        
        return ResponseEntity.ok(health);
    }
}