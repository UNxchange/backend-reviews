package com.unxchange.reviews;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestPropertySource;

@SpringBootTest
@TestPropertySource(properties = {
    "spring.data.mongodb.uri=mongodb://localhost:27017/test_reviews",
    "spring.security.jwt.secret-key=test-secret-key-for-testing-purposes-only"
})
class ReviewsServiceApplicationTests {

    @Test
    void contextLoads() {
        // Test que verifica que el contexto de Spring se carga correctamente
    }
}