# Ejemplo de Token JWT para Pruebas

## Estructura del Token JWT Esperado

El microservicio espera un token JWT con la siguiente estructura:

```json
{
  "sub": "usuario@ejemplo.com",
  "role": "usuario",
  "iat": 1634567890,
  "exp": 1634654290
}
```

## Campos Requeridos

- **sub**: Email del usuario (se usa como author_id)
- **role**: Rol del usuario ("usuario" o "administrador")
- **iat**: Timestamp de emisión
- **exp**: Timestamp de expiración

## Ejemplo de Token para Pruebas

**Usuario normal:**
```
Payload: {"sub": "juan@ejemplo.com", "role": "usuario", "iat": 1634567890, "exp": 1634654290}
```

**Administrador:**
```
Payload: {"sub": "admin@ejemplo.com", "role": "administrador", "iat": 1634567890, "exp": 1634654290}
```

## Cómo usar en Swagger

1. Ve a http://localhost:8003/swagger-ui.html
2. Haz clic en el botón "Authorize" 🔒
3. Ingresa: `Bearer tu-token-jwt-aqui`
4. Haz clic en "Authorize"

## Nota de Seguridad

⚠️ **IMPORTANTE**: Este archivo es solo para documentación. En producción:
- Los tokens deben ser generados por el microservicio de autenticación
- Deben tener una clave secreta segura
- Deben tener tiempos de expiración apropiados