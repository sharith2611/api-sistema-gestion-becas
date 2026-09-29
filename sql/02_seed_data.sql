-- ============================================================
-- DATOS DE PRUEBA (mínimo 10 registros por tabla)
-- Ejecutar DESPUÉS de 01_schema.sql
-- ============================================================

-- 1. zonas_forestales
INSERT INTO zonas_forestales (nombre, ubicacion, area_hectareas, tipo_vegetacion) VALUES
('Bosque El Roble', 'Sector norte, cordillera oriental', 450.50, 'Bosque nativo'),
('Reserva Los Cedros', 'Sector centro-occidente', 620.00, 'Bosque mixto'),
('Cerro Verde', 'Ladera sur del volcán', 310.75, 'Matorral'),
('Parque La Esperanza', 'Zona rural noroccidente', 890.20, 'Pino y eucalipto'),
('Valle Seco', 'Zona árida sur', 275.00, 'Vegetación xerófila'),
('Bosque Andino Alto', 'Zona montañosa central', 540.30, 'Bosque andino'),
('Reserva El Pinar', 'Sector oriental', 410.00, 'Coníferas'),
('Cañón del Río', 'Ribera del río principal', 195.60, 'Bosque de galería'),
('Sabana Norte', 'Llanura norte', 730.40, 'Pastizal'),
('Loma Alta', 'Sector suroriente', 260.90, 'Bosque secundario'),
('Reserva Cascada Azul', 'Zona húmeda occidental', 505.10, 'Bosque húmedo'),
('Montaña El Águila', 'Zona alta central', 380.00, 'Páramo');

-- 2. estaciones_monitoreo
INSERT INTO estaciones_monitoreo (zona_id, nombre, latitud, longitud, altitud, fecha_instalacion) VALUES
(1, 'Estación Roble-01', 4.123456, -74.123456, 2100.50, '2025-01-10'),
(1, 'Estación Roble-02', 4.130200, -74.118900, 2150.00, '2025-01-15'),
(2, 'Estación Cedros-01', 4.256700, -74.345600, 1980.30, '2025-02-01'),
(3, 'Estación Cerro Verde-01', 4.056700, -74.089900, 2450.00, '2025-02-10'),
(4, 'Estación Esperanza-01', 4.310500, -74.201200, 1750.60, '2025-03-05'),
(5, 'Estación Valle Seco-01', 3.980100, -74.150300, 1200.00, '2025-03-20'),
(6, 'Estación Andino Alto-01', 4.400900, -74.278800, 2800.40, '2025-04-01'),
(7, 'Estación Pinar-01', 4.190300, -74.050600, 2050.20, '2025-04-15'),
(8, 'Estación Cañón-01', 4.220800, -74.310400, 1600.00, '2025-05-01'),
(9, 'Estación Sabana Norte-01', 4.510200, -74.190700, 900.80, '2025-05-15'),
(10, 'Estación Loma Alta-01', 4.080600, -74.070200, 2000.00, '2025-06-01'),
(11, 'Estación Cascada Azul-01', 4.350400, -74.400100, 1850.70, '2025-06-10');

-- 3. sensores (BME280)
INSERT INTO sensores (estacion_id, modelo, numero_serie, fecha_instalacion, estado) VALUES
(1, 'BME280', 'SN-0001-A', '2025-01-10', 'activo'),
(2, 'BME280', 'SN-0002-A', '2025-01-15', 'activo'),
(3, 'BME280', 'SN-0003-A', '2025-02-01', 'activo'),
(4, 'BME280', 'SN-0004-A', '2025-02-10', 'activo'),
(5, 'BME280', 'SN-0005-A', '2025-03-05', 'activo'),
(6, 'BME280', 'SN-0006-A', '2025-03-20', 'mantenimiento'),
(7, 'BME280', 'SN-0007-A', '2025-04-01', 'activo'),
(8, 'BME280', 'SN-0008-A', '2025-04-15', 'activo'),
(9, 'BME280', 'SN-0009-A', '2025-05-01', 'inactivo'),
(10, 'BME280', 'SN-0010-A', '2025-05-15', 'activo'),
(11, 'BME280', 'SN-0011-A', '2025-06-01', 'activo'),
(12, 'BME280', 'SN-0012-A', '2025-06-10', 'activo');

-- 4. tipos_medicion
INSERT INTO tipos_medicion (nombre, unidad_medida) VALUES
('Temperatura', '°C'),
('Humedad relativa', '%'),
('Presión atmosférica', 'hPa');

-- 5. mediciones (varias por sensor)
INSERT INTO mediciones (sensor_id, tipo_medicion_id, valor, fecha_hora) VALUES
(1, 1, 34.5, '2026-08-20 08:00:00'),
(1, 2, 22.3, '2026-08-20 08:00:00'),
(1, 3, 1012.4, '2026-08-20 08:00:00'),
(2, 1, 38.9, '2026-08-20 08:05:00'),
(2, 2, 18.1, '2026-08-20 08:05:00'),
(3, 1, 29.2, '2026-08-20 08:10:00'),
(3, 2, 45.6, '2026-08-20 08:10:00'),
(4, 1, 41.7, '2026-08-20 08:15:00'),
(5, 1, 26.4, '2026-08-20 08:20:00'),
(7, 1, 33.0, '2026-08-20 08:25:00'),
(8, 1, 30.5, '2026-08-20 08:30:00'),
(10, 1, 27.8, '2026-08-20 08:35:00');

-- 6. niveles_riesgo
INSERT INTO niveles_riesgo (nombre, descripcion, color_alerta) VALUES
('Bajo', 'Condiciones normales, sin riesgo relevante', 'verde'),
('Medio', 'Condiciones de vigilancia, posible riesgo', 'amarillo'),
('Alto', 'Condiciones favorables para inicio de incendio', 'naranja'),
('Crítico', 'Riesgo inminente de incendio forestal', 'rojo');

-- 7. umbrales_alerta (temperatura y humedad, por nivel de riesgo)
INSERT INTO umbrales_alerta (tipo_medicion_id, nivel_riesgo_id, valor_min, valor_max) VALUES
(1, 1, 0.0, 25.0),
(1, 2, 25.1, 32.0),
(1, 3, 32.1, 38.0),
(1, 4, 38.1, 60.0),
(2, 1, 50.0, 100.0),
(2, 2, 30.0, 49.9),
(2, 3, 15.0, 29.9),
(2, 4, 0.0, 14.9),
(3, 1, 1000.0, 1030.0),
(3, 2, 990.0, 999.9),
(3, 3, 980.0, 989.9),
(3, 4, 900.0, 979.9);

-- 8. alertas
INSERT INTO alertas (estacion_id, umbral_id, medicion_id, fecha_hora, estado) VALUES
(1, 3, 1, '2026-08-20 08:00:00', 'activa'),
(2, 4, 4, '2026-08-20 08:05:00', 'activa'),
(3, 2, 6, '2026-08-20 08:10:00', 'atendida'),
(4, 4, 8, '2026-08-20 08:15:00', 'activa'),
(5, 2, 9, '2026-08-20 08:20:00', 'atendida'),
(1, 6, 2, '2026-08-20 08:00:00', 'activa'),
(7, 3, 10, '2026-08-20 08:25:00', 'activa'),
(8, 2, 11, '2026-08-20 08:30:00', 'atendida'),
(2, 3, 4, '2026-08-20 08:05:00', 'cerrada'),
(10, 2, 12, '2026-08-20 08:35:00', 'activa');

-- 9. brigadas
INSERT INTO brigadas (zona_asignada_id, nombre, telefono_contacto) VALUES
(1, 'Brigada Roble Norte', '3001112233'),
(2, 'Brigada Cedros', '3002223344'),
(3, 'Brigada Cerro Verde', '3003334455'),
(4, 'Brigada Esperanza', '3004445566'),
(5, 'Brigada Valle Seco', '3005556677'),
(6, 'Brigada Andina', '3006667788'),
(7, 'Brigada El Pinar', '3007778899'),
(8, 'Brigada Cañón', '3008889900'),
(9, 'Brigada Sabana', '3009990011'),
(10, 'Brigada Loma Alta', '3010001122');

-- 10. personal_brigada
INSERT INTO personal_brigada (brigada_id, nombre, cargo, telefono) VALUES
(1, 'Carlos Ramírez', 'Jefe de brigada', '3101112233'),
(1, 'Ana Torres', 'Bombero forestal', '3101112234'),
(2, 'Luis Gómez', 'Jefe de brigada', '3101112235'),
(2, 'María Pérez', 'Bombero forestal', '3101112236'),
(3, 'Jorge Salazar', 'Jefe de brigada', '3101112237'),
(4, 'Diana Ruiz', 'Bombero forestal', '3101112238'),
(5, 'Pedro Molina', 'Jefe de brigada', '3101112239'),
(6, 'Laura Castillo', 'Bombero forestal', '3101112240'),
(7, 'Andrés Vega', 'Jefe de brigada', '3101112241'),
(8, 'Camila Rojas', 'Bombero forestal', '3101112242'),
(9, 'Felipe Ortiz', 'Jefe de brigada', '3101112243'),
(10, 'Sofía Mendoza', 'Bombero forestal', '3101112244');

-- 11. incidentes
INSERT INTO incidentes (zona_id, alerta_id, brigada_id, fecha_inicio, fecha_fin, area_afectada_ha, estado) VALUES
(1, 1, 1, '2026-08-20 09:00:00', '2026-08-20 15:00:00', 12.50, 'controlado'),
(2, 2, 2, '2026-08-20 09:10:00', NULL, 8.30, 'en curso'),
(3, NULL, 3, '2026-08-15 10:00:00', '2026-08-15 18:00:00', 4.10, 'controlado'),
(4, 4, 4, '2026-08-20 09:20:00', NULL, 20.00, 'en curso'),
(5, NULL, 5, '2026-08-10 07:00:00', '2026-08-10 12:00:00', 2.75, 'controlado'),
(6, NULL, 6, '2026-08-05 06:00:00', '2026-08-05 14:00:00', 6.60, 'controlado'),
(7, 7, 7, '2026-08-20 09:25:00', NULL, 15.20, 'en curso'),
(8, NULL, 8, '2026-08-01 08:00:00', '2026-08-01 11:00:00', 1.90, 'controlado'),
(9, NULL, 9, '2026-07-28 09:00:00', '2026-07-28 20:00:00', 30.40, 'controlado'),
(10, 10, 10, '2026-08-20 09:35:00', NULL, 9.80, 'en curso');

-- 12. mantenimientos_sensor
INSERT INTO mantenimientos_sensor (sensor_id, fecha, descripcion, tecnico_responsable) VALUES
(6, '2026-07-01', 'Calibración de sensor de presión', 'Técnico Ricardo López'),
(1, '2026-06-15', 'Limpieza de carcasa y revisión de batería', 'Técnico Ricardo López'),
(2, '2026-06-16', 'Cambio de batería', 'Técnico Elena Vargas'),
(3, '2026-06-20', 'Revisión general', 'Técnico Elena Vargas'),
(4, '2026-06-25', 'Calibración de sensor de temperatura', 'Técnico Ricardo López'),
(5, '2026-07-02', 'Revisión de conectividad', 'Técnico Elena Vargas'),
(9, '2026-07-05', 'Reemplazo de sensor dañado', 'Técnico Ricardo López'),
(7, '2026-07-10', 'Limpieza de sensor', 'Técnico Elena Vargas'),
(8, '2026-07-12', 'Revisión general', 'Técnico Ricardo López'),
(10, '2026-07-15', 'Calibración completa', 'Técnico Elena Vargas'),
(11, '2026-07-20', 'Revisión de conectividad', 'Técnico Ricardo López'),
(12, '2026-07-22', 'Limpieza de carcasa', 'Técnico Elena Vargas');
