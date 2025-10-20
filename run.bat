@echo off
echo 🚀 Iniciando microservicio de reseñas UnxChange...
echo.

REM Verificar si Java está instalado
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Java no está instalado o no está en el PATH
    echo Por favor instala Java 17 o superior
    pause
    exit /b 1
)

REM Verificar si Maven está disponible
call mvnw.cmd --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Maven Wrapper no está disponible
    pause
    exit /b 1
)

echo ✅ Java y Maven detectados correctamente
echo.

REM Compilar el proyecto
echo 📦 Compilando el proyecto...
call mvnw.cmd clean compile
if %errorlevel% neq 0 (
    echo ❌ Error en la compilación
    pause
    exit /b 1
)

echo ✅ Compilación exitosa
echo.

REM Ejecutar la aplicación
echo 🚀 Iniciando la aplicación en http://localhost:8003
echo 📝 Documentación disponible en: http://localhost:8003/docs
echo.
echo Presiona Ctrl+C para detener el servicio
echo.

call mvnw.cmd spring-boot:run

pause