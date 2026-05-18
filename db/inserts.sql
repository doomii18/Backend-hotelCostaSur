-- =======================================================
-- SEMILLA DE DATOS UNICODE (N) PARA HOTEL COSTA SUR (SSMS)
-- =======================================================

USE HotelCostaSur;
GO

-- 1. Insertar Categorías
INSERT INTO Categorias (id_categoria, NombreCategoria) VALUES
(1, N'Habitación Económica'),
(2, N'Habitación Estándar'),
(3, N'Suite Ejecutiva'),
(4, N'Suite Premium'),
(5, N'Habitación Familiar');
GO

-- 2. Insertar Administrador por defecto (Contraseña: 2026HOTELCOSTASUR en SHA-256)
-- Hash de 2026HOTELCOSTASUR en SHA-256: 7f8bc5fb7c514742a0c4f828a2a4b85c18b76fb083b4b88d4078ad691ccbf568
INSERT INTO usuarios (usuario, correo, contrasena, rol, fecha_registro) VALUES
(N'HCS-ADMINISTRADOR', N'admin@hotelcostasur.com', N'7f8bc5fb7c514742a0c4f828a2a4b85c18b76fb083b4b88d4078ad691ccbf568', N'admin', GETDATE());
GO

-- 3. Insertar Huésped de prueba (Contraseña: 12345 en SHA-256)
-- Hash de 12345: 5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5
INSERT INTO usuarios (usuario, correo, contrasena, rol, fecha_registro) VALUES
(N'huesped1', N'huesped@gmail.com', N'5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5', N'user', GETDATE());
GO

-- 4. Insertar las 25 habitaciones oficiales con sus características serializadas en JSON
INSERT INTO habitaciones (id_habitacion, nombre, tipo, id_categoria, precio, caracteristicas, disponible, televisor, aire) VALUES
(101, N'Económica Single 101', N'Económica', 1, 45.00, N'["1 Cama Individual", "Baño Privado", "Wi-Fi Gratis", "Ventilador"]', 1, 0, 0),
(102, N'Económica Single 102', N'Económica', 1, 45.00, N'["1 Cama Individual", "Baño Privado", "Wi-Fi Gratis", "Ventilador"]', 1, 0, 0),
(103, N'Económica Doble 103', N'Económica', 1, 60.00, N'["2 Camas Individuales", "Baño Privado", "Wi-Fi Gratis", "Ventilador"]', 1, 0, 0),
(104, N'Económica Doble 104', N'Económica', 1, 60.00, N'["2 Camas Individuales", "Baño Privado", "Wi-Fi Gratis", "Ventilador"]', 1, 0, 0),
(105, N'Económica Triple 105', N'Económica', 1, 75.00, N'["3 Camas Individuales", "Baño Privado", "Wi-Fi Gratis", "Ventilador"]', 1, 0, 0),

(201, N'Estándar Matrimonial 201', N'Estándar', 2, 70.00, N'["1 Cama Queen", "Baño Privado", "Wi-Fi Gratis", "Televisor LED 32\\"", "Ventilador"]', 1, 1, 0),
(202, N'Estándar Matrimonial 202', N'Estándar', 2, 70.00, N'["1 Cama Queen", "Baño Privado", "Wi-Fi Gratis", "Televisor LED 32\\"", "Ventilador"]', 1, 1, 0),
(203, N'Estándar Doble 203', N'Estándar', 2, 85.00, N'["2 Camas Matrimoniales", "Baño Privado", "Wi-Fi Gratis", "Televisor LED 32\\"", "Ventilador"]', 1, 1, 0),
(204, N'Estándar Doble 204', N'Estándar', 2, 85.00, N'["2 Camas Matrimoniales", "Baño Privado", "Wi-Fi Gratis", "Televisor LED 32\\"", "Ventilador"]', 1, 1, 0),
(205, N'Estándar Triple 205', N'Estándar', 2, 95.00, N'["3 Camas Individuales", "Baño Privado", "Wi-Fi Gratis", "Televisor LED 32\\"", "Ventilador"]', 1, 1, 0),

(301, N'Suite Ejecutiva 301', N'Suite Ejecutiva', 3, 120.00, N'["1 Cama King Size", "Baño de Lujo con Jacuzzi", "Wi-Fi de Alta Velocidad", "Televisor Smart 43\\"", "Aire Acondicionado Split", "Frigobar", "Escritorio de Trabajo"]', 1, 1, 1),
(302, N'Suite Ejecutiva 302', N'Suite Ejecutiva', 3, 120.00, N'["1 Cama King Size", "Baño de Lujo con Jacuzzi", "Wi-Fi de Alta Velocidad", "Televisor Smart 43\\"", "Aire Acondicionado Split", "Frigobar", "Escritorio de Trabajo"]', 1, 1, 1),
(303, N'Suite Ejecutiva 303', N'Suite Ejecutiva', 3, 120.00, N'["1 Cama King Size", "Baño de Lujo con Jacuzzi", "Wi-Fi de Alta Velocidad", "Televisor Smart 43\\"", "Aire Acondicionado Split", "Frigobar", "Escritorio de Trabajo"]', 1, 1, 1),
(304, N'Suite Ejecutiva Doble 304', N'Suite Ejecutiva', 3, 150.00, N'["2 Camas Queen Size", "Baño de Lujo con Jacuzzi", "Wi-Fi de Alta Velocidad", "Televisor Smart 43\\"", "Aire Acondicionado Split", "Frigobar", "Escritorio de Trabajo"]', 1, 1, 1),
(305, N'Suite Ejecutiva Doble 305', N'Suite Ejecutiva', 3, 150.00, N'["2 Camas Queen Size", "Baño de Lujo con Jacuzzi", "Wi-Fi de Alta Velocidad", "Televisor Smart 43\\"", "Aire Acondicionado Split", "Frigobar", "Escritorio de Trabajo"]', 1, 1, 1),

(401, N'Suite Premium Vista al Mar 401', N'Suite Premium', 4, 180.00, N'["1 Cama California King Size", "Baño de Mármol con Jacuzzi y Ducha Española", "Terraza Privada con Vista al Mar", "Wi-Fi de Alta Velocidad", "Smart TV 55\\"", "Aire Acondicionado Central", "Frigobar Premium", "Cafetera Nespresso", "Batas y Zapatillas de Baño"]', 1, 1, 1),
(402, N'Suite Premium Vista al Mar 402', N'Suite Premium', 4, 180.00, N'["1 Cama California King Size", "Baño de Mármol con Jacuzzi y Ducha Española", "Terraza Privada con Vista al Mar", "Wi-Fi de Alta Velocidad", "Smart TV 55\\"", "Aire Acondicionado Central", "Frigobar Premium", "Cafetera Nespresso", "Batas y Zapatillas de Baño"]', 1, 1, 1),
(403, N'Suite Premium Vista al Mar 403', N'Suite Premium', 4, 180.00, N'["1 Cama California King Size", "Baño de Mármol con Jacuzzi y Ducha Española", "Terraza Privada con Vista al Mar", "Wi-Fi de Alta Velocidad", "Smart TV 55\\"", "Aire Acondicionado Central", "Frigobar Premium", "Cafetera Nespresso", "Batas y Zapatillas de Baño"]', 1, 1, 1),
(404, N'Suite Premium Presidencial 404', N'Suite Premium', 4, 250.00, N'["1 Cama California King Size", "Sala de Estar Independiente", "Cocina Equipada", "Baño con Jacuzzi Doble", "Terraza Panorámica con Piscina Privada", "Wi-Fi de Alta Velocidad", "Smart TV 65\\"", "Aire Acondicionado", "Servicio a la Habitación 24/7"]', 1, 1, 1),
(405, N'Suite Premium Presidencial 405', N'Suite Premium', 4, 250.00, N'["1 Cama California King Size", "Sala de Estar Independiente", "Cocina Equipada", "Baño con Jacuzzi Doble", "Terraza Panorámica con Piscina Privada", "Wi-Fi de Alta Velocidad", "Smart TV 65\\"", "Aire Acondicionado", "Servicio a la Habitación 24/7"]', 1, 1, 1),

(501, N'Familiar Confort 501', N'Familiar', 5, 110.00, N'["1 Cama Matrimonial y 2 Camas Individuales", "Baño Amplio Familiar", "Área de Juegos Infantil", "Wi-Fi Gratis", "Televisor LED 40\\"", "Aire Acondicionado Split", "Microondas y Frigobar"]', 1, 1, 1),
(502, N'Familiar Confort 502', N'Familiar', 5, 110.00, N'["1 Cama Matrimonial y 2 Camas Individuales", "Baño Amplio Familiar", "Área de Juegos Infantil", "Wi-Fi Gratis", "Televisor LED 40\\"", "Aire Acondicionado Split", "Microondas y Frigobar"]', 1, 1, 1),
(503, N'Familiar Confort 503', N'Familiar', 5, 110.00, N'["1 Cama Matrimonial y 2 Camas Individuales", "Baño Amplio Familiar", "Área de Juegos Infantil", "Wi-Fi Gratis", "Televisor LED 40\\"", "Aire Acondicionado Split", "Microondas y Frigobar"]', 1, 1, 1),
(504, N'Familiar Grand 504', N'Familiar', 5, 140.00, N'["2 Camas Matrimoniales y 2 Camas Individuales (Habitaciones Conectadas)", "2 Baños Completos", "Sala de Estar Pequeña", "Wi-Fi de Alta Velocidad", "2 Smart TV 40\\"", "Aire Acondicionado", "Cocina Pequeña"]', 1, 1, 1),
(505, N'Familiar Grand 505', N'Familiar', 5, 140.00, N'["2 Camas Matrimoniales y 2 Camas Individuales (Habitaciones Conectadas)", "2 Baños Completos", "Sala de Estar Pequeña", "Wi-Fi de Alta Velocidad", "2 Smart TV 40\\"", "Aire Acondicionado", "Cocina Pequeña"]', 1, 1, 1);
GO
