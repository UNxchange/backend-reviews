package com.unxchange.reviews.repository;

import com.unxchange.reviews.model.Review;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repositorio para operaciones de base de datos de reseñas
 */
@Repository
public interface ReviewRepository extends MongoRepository<Review, String> {
    
    /**
     * Busca reseñas por ID de convocatoria
     */
    Page<Review> findByConvocatoriaId(String convocatoriaId, Pageable pageable);
    
    /**
     * Busca reseñas por autor
     */
    Page<Review> findByAuthorId(String authorId, Pageable pageable);
    
    /**
     * Busca reseñas por convocatoria y autor
     */
    Page<Review> findByConvocatoriaIdAndAuthorId(String convocatoriaId, String authorId, Pageable pageable);
    
    /**
     * Cuenta reseñas por convocatoria
     */
    long countByConvocatoriaId(String convocatoriaId);
    
    /**
     * Cuenta reseñas por autor
     */
    long countByAuthorId(String authorId);
    
    /**
     * Cuenta reseñas por convocatoria y autor
     */
    long countByConvocatoriaIdAndAuthorId(String convocatoriaId, String authorId);
    
    /**
     * Obtiene todas las reseñas de un usuario específico
     */
    List<Review> findByAuthorIdOrderByCreatedAtDesc(String authorId, Pageable pageable);
    
    /**
     * Obtiene todas las reseñas de una convocatoria para estadísticas
     */
    List<Review> findByConvocatoriaId(String convocatoriaId);
}