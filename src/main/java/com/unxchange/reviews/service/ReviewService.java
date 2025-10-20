package com.unxchange.reviews.service;

import com.unxchange.reviews.dto.*;
import com.unxchange.reviews.exception.ReviewNotFoundException;
import com.unxchange.reviews.exception.UnauthorizedException;
import com.unxchange.reviews.model.Review;
import com.unxchange.reviews.repository.ReviewRepository;
import com.unxchange.reviews.security.UserPrincipal;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * Servicio para operaciones CRUD de reseñas
 */
@Service
public class ReviewService {
    
    @Autowired
    private ReviewRepository reviewRepository;
    
    /**
     * Crea una nueva reseña
     */
    public Review createReview(ReviewCreateDto reviewDto, UserPrincipal user) {
        Review review = new Review(
                user.getEmail(),
                reviewDto.getConvocatoriaId(),
                reviewDto.getRating(),
                reviewDto.getContent()
        );
        
        return reviewRepository.save(review);
    }
    
    /**
     * Obtiene una reseña por ID
     */
    public Review getReviewById(String id) {
        return reviewRepository.findById(id)
                .orElseThrow(() -> new ReviewNotFoundException("Reseña con id " + id + " no encontrada"));
    }
    
    /**
     * Obtiene reseñas con filtros y paginación
     */
    public ReviewListResponseDto getReviews(String convocatoriaId, String authorId, 
                                          int limit, int skip, String sortBy, int sortOrder) {
        
        Sort.Direction direction = sortOrder == 1 ? Sort.Direction.ASC : Sort.Direction.DESC;
        Pageable pageable = PageRequest.of(skip / limit, limit, Sort.by(direction, sortBy));
        
        Page<Review> reviewPage;
        long total;
        
        if (convocatoriaId != null && authorId != null) {
            reviewPage = reviewRepository.findByConvocatoriaIdAndAuthorId(convocatoriaId, authorId, pageable);
            total = reviewRepository.countByConvocatoriaIdAndAuthorId(convocatoriaId, authorId);
        } else if (convocatoriaId != null) {
            reviewPage = reviewRepository.findByConvocatoriaId(convocatoriaId, pageable);
            total = reviewRepository.countByConvocatoriaId(convocatoriaId);
        } else if (authorId != null) {
            reviewPage = reviewRepository.findByAuthorId(authorId, pageable);
            total = reviewRepository.countByAuthorId(authorId);
        } else {
            reviewPage = reviewRepository.findAll(pageable);
            total = reviewRepository.count();
        }
        
        return new ReviewListResponseDto(total, limit, skip, reviewPage.getContent());
    }
    
    /**
     * Actualiza una reseña existente
     */
    public Review updateReview(String id, ReviewUpdateDto updateDto, UserPrincipal user) {
        Review review = getReviewById(id);
        
        // Verificar que el usuario sea el autor
        if (!review.getAuthorId().equals(user.getEmail())) {
            throw new UnauthorizedException("No tienes permisos para editar esta reseña");
        }
        
        // Aplicar actualizaciones
        if (updateDto.getRating() != null) {
            review.setRating(updateDto.getRating());
        }
        
        if (updateDto.getContent() != null && !updateDto.getContent().trim().isEmpty()) {
            review.setContent(updateDto.getContent());
        }
        
        review.setUpdatedAt(LocalDateTime.now());
        
        return reviewRepository.save(review);
    }
    
    /**
     * Elimina una reseña
     */
    public void deleteReview(String id, UserPrincipal user) {
        Review review = getReviewById(id);
        
        // Verificar permisos: autor o administrador
        boolean isAuthor = review.getAuthorId().equals(user.getEmail());
        boolean isAdmin = user.isAdmin();
        
        if (!isAuthor && !isAdmin) {
            throw new UnauthorizedException("No tienes permisos para eliminar esta reseña");
        }
        
        reviewRepository.deleteById(id);
    }
    
    /**
     * Obtiene estadísticas de una convocatoria
     */
    public ReviewStatisticsDto getStatisticsByConvocatoria(String convocatoriaId) {
        List<Review> reviews = reviewRepository.findByConvocatoriaId(convocatoriaId);
        
        if (reviews.isEmpty()) {
            Map<String, Long> emptyDistribution = new HashMap<>();
            emptyDistribution.put("1", 0L);
            emptyDistribution.put("2", 0L);
            emptyDistribution.put("3", 0L);
            emptyDistribution.put("4", 0L);
            emptyDistribution.put("5", 0L);
            
            return new ReviewStatisticsDto(convocatoriaId, 0.0, 0L, emptyDistribution);
        }
        
        // Calcular estadísticas
        double averageRating = reviews.stream()
                .mapToInt(Review::getRating)
                .average()
                .orElse(0.0);
        
        long totalReviews = reviews.size();
        
        // Distribución de ratings
        Map<String, Long> distribution = new HashMap<>();
        distribution.put("1", reviews.stream().filter(r -> r.getRating() == 1).count());
        distribution.put("2", reviews.stream().filter(r -> r.getRating() == 2).count());
        distribution.put("3", reviews.stream().filter(r -> r.getRating() == 3).count());
        distribution.put("4", reviews.stream().filter(r -> r.getRating() == 4).count());
        distribution.put("5", reviews.stream().filter(r -> r.getRating() == 5).count());
        
        return new ReviewStatisticsDto(
                convocatoriaId,
                Math.round(averageRating * 100.0) / 100.0,
                totalReviews,
                distribution
        );
    }
    
    /**
     * Obtiene las reseñas de un usuario
     */
    public List<Review> getUserReviews(String authorId, int limit, int skip) {
        Pageable pageable = PageRequest.of(skip / limit, limit);
        return reviewRepository.findByAuthorIdOrderByCreatedAtDesc(authorId, pageable);
    }
}