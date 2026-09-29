-- ============================================================
-- SISTEMA DE MONITOREO DE INCENDIOS FORESTALES (Sensor BME280)
-- Script de creación de tablas - Ejecutar en Neon > SQL Editor
-- 12 tablas, normalizadas a 3FN
-- ============================================================

-- 1. Zonas forestales monitoreadas
CREATE TABLE zonas_forestales (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(150) NOT NULL,
    area_hectareas NUMERIC(10,2) NOT NULL,
    tipo_vegetacion VARCHAR(80) NOT NULL
);

-- 2. Estaciones físicas de monitoreo dentro de una zona
CREATE TABLE estaciones_monitoreo (
    id SERIAL PRIMARY KEY,
    zona_id INTEGER NOT NULL REFERENCES zonas_forestales(id),
    nombre VARCHAR(100) NOT NULL,
    latitud NUMERIC(9,6) NOT NULL,
    longitud NUMERIC(9,6) NOT NULL,
    altitud NUMERIC(6,2) NOT NULL,
    fecha_instalacion DATE NOT NULL
);

-- 3. Sensores BME280 instalados en cada estación
CREATE TABLE sensores (
    id SERIAL PRIMARY KEY,
    estacion_id INTEGER NOT NULL REFERENCES estaciones_monitoreo(id),
    modelo VARCHAR(50) NOT NULL,
    numero_serie VARCHAR(50) NOT NULL UNIQUE,
    fecha_instalacion DATE NOT NULL,
    estado VARCHAR(20) NOT NULL
);

-- 4. Catálogo de tipos de medición (temperatura, humedad, presión)
CREATE TABLE tipos_medicion (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    unidad_medida VARCHAR(20) NOT NULL
);

-- 5. Lecturas registradas por cada sensor
CREATE TABLE mediciones (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER NOT NULL REFERENCES sensores(id),
    tipo_medicion_id INTEGER NOT NULL REFERENCES tipos_medicion(id),
    valor NUMERIC(8,3) NOT NULL,
    fecha_hora TIMESTAMP NOT NULL
);

-- 6. Catálogo de niveles de riesgo
CREATE TABLE niveles_riesgo (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    descripcion VARCHAR(200) NOT NULL,
    color_alerta VARCHAR(20) NOT NULL
);

-- 7. Umbrales que determinan cuándo se dispara cada nivel de riesgo
CREATE TABLE umbrales_alerta (
    id SERIAL PRIMARY KEY,
    tipo_medicion_id INTEGER NOT NULL REFERENCES tipos_medicion(id),
    nivel_riesgo_id INTEGER NOT NULL REFERENCES niveles_riesgo(id),
    valor_min NUMERIC(8,3) NOT NULL,
    valor_max NUMERIC(8,3) NOT NULL
);

-- 8. Alertas generadas cuando una medición supera un umbral
CREATE TABLE alertas (
    id SERIAL PRIMARY KEY,
    estacion_id INTEGER NOT NULL REFERENCES estaciones_monitoreo(id),
    umbral_id INTEGER NOT NULL REFERENCES umbrales_alerta(id),
    medicion_id INTEGER NOT NULL REFERENCES mediciones(id),
    fecha_hora TIMESTAMP NOT NULL,
    estado VARCHAR(20) NOT NULL
);

-- 9. Brigadas de respuesta asignadas a una zona
CREATE TABLE brigadas (
    id SERIAL PRIMARY KEY,
    zona_asignada_id INTEGER NOT NULL REFERENCES zonas_forestales(id),
    nombre VARCHAR(100) NOT NULL,
    telefono_contacto VARCHAR(20) NOT NULL
);

-- 10. Integrantes de cada brigada
CREATE TABLE personal_brigada (
    id SERIAL PRIMARY KEY,
    brigada_id INTEGER NOT NULL REFERENCES brigadas(id),
    nombre VARCHAR(100) NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    telefono VARCHAR(20) NOT NULL
);

-- 11. Incidentes (incendios) reales, opcionalmente originados por una alerta
CREATE TABLE incidentes (
    id SERIAL PRIMARY KEY,
    zona_id INTEGER NOT NULL REFERENCES zonas_forestales(id),
    alerta_id INTEGER REFERENCES alertas(id),
    brigada_id INTEGER NOT NULL REFERENCES brigadas(id),
    fecha_inicio TIMESTAMP NOT NULL,
    fecha_fin TIMESTAMP,
    area_afectada_ha NUMERIC(10,2) NOT NULL,
    estado VARCHAR(20) NOT NULL
);

-- 12. Historial de mantenimientos técnicos de cada sensor
CREATE TABLE mantenimientos_sensor (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER NOT NULL REFERENCES sensores(id),
    fecha DATE NOT NULL,
    descripcion VARCHAR(200) NOT NULL,
    tecnico_responsable VARCHAR(100) NOT NULL
);
