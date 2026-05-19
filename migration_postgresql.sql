-- =====================================================
-- SCRIPT DE BASE DE DATOS PARA PostgreSQL
-- Adaptado del script original SQL Server
-- Proyecto Hotel Costa Sur
-- =====================================================

-- 1. Crear base de datos (si no existe - hacer desde psql directamente)
-- CREATE DATABASE "HotelCostaSur" ENCODING 'UTF8';

-- Conectarse a la base de datos:
-- \c HotelCostaSur

-- =====================================================
-- 2. Tabla de usuarios
-- =====================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    rol VARCHAR(10) DEFAULT 'user' CHECK (rol IN ('user', 'admin')),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 3. Tabla de Categorías
-- =====================================================
CREATE TABLE IF NOT EXISTS "Categorias" (
    id_categoria INTEGER PRIMARY KEY,
    "NombreCategoria" VARCHAR(255) NOT NULL
);

-- =====================================================
-- 4. Tabla de habitaciones
-- =====================================================
CREATE TABLE IF NOT EXISTS habitaciones (
    id_categoria INTEGER NOT NULL,
    id INTEGER PRIMARY KEY,
    "Numero_Habitacion" INTEGER NOT NULL,
    precio NUMERIC(10,2) NOT NULL,
    "Descripcion" TEXT NOT NULL,
    "Estado" BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (id_categoria) REFERENCES "Categorias"(id_categoria) ON DELETE CASCADE
);

-- =====================================================
-- 5. Tabla de Clientes
-- =====================================================
CREATE TABLE IF NOT EXISTS clientes (
    id_usuario INTEGER NOT NULL,
    id INTEGER PRIMARY KEY,
    tipo_documento VARCHAR(10) NOT NULL CHECK (tipo_documento IN ('cedula', 'pasaporte')),
    cedula VARCHAR(20) NULL,
    pais_pasaporte VARCHAR(50) NULL,
    pasaporte VARCHAR(50) NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    sexo VARCHAR(10) NOT NULL CHECK (sexo IN ('Masculino', 'Femenino')),
    fecha_nacimiento DATE NOT NULL,
    nacionalidad VARCHAR(50) NOT NULL,
    procedencia VARCHAR(100) NOT NULL,
    "Estado" BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- =====================================================
-- 6. Tabla de reservas
-- =====================================================
CREATE TABLE IF NOT EXISTS reservas (
    id_reserva SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    id_habitacion INTEGER NOT NULL,
    estado VARCHAR(20) DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'activo', 'completado')),
    fecha_ingreso DATE NOT NULL,
    fecha_salida DATE NOT NULL,
    dias INTEGER NOT NULL,
    "CantidadHuespedes" INTEGER NOT NULL,
    total NUMERIC(10,2) NOT NULL,
    metodo_pago VARCHAR(50) DEFAULT 'presencial',
    fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id) ON DELETE CASCADE,
    FOREIGN KEY (id_habitacion) REFERENCES habitaciones(id) ON DELETE CASCADE
);

-- =====================================================
-- 7. Tabla de participantes del sorteo
-- =====================================================
CREATE TABLE IF NOT EXISTS participantes_sorteo (
    id SERIAL PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    departamento VARCHAR(50) NOT NULL,
    sexo VARCHAR(20) NOT NULL,
    edad INTEGER NOT NULL,
    ocupacion VARCHAR(100) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- DATOS INICIALES
-- =====================================================

-- Insertar Categorías
INSERT INTO "Categorias" (id_categoria, "NombreCategoria") VALUES
(1, 'Habitación Económica'),
(2, 'Habitación Estándar'),
(3, 'Suite Ejecutiva')
ON CONFLICT (id_categoria) DO NOTHING;

-- Insertar Habitaciones (exactamente 25 habitaciones)
INSERT INTO habitaciones (id_categoria, id, "Numero_Habitacion", precio, "Descripcion", "Estado") VALUES
-- Categoría 1: Económicas
(1, 1, 1, 500, '2 camas, Matrimonial e Individual, Baño privado', TRUE),
(1, 2, 2, 500, '2 camas, Matrimonial e Individual, Baño privado', TRUE),
(1, 3, 3, 400, 'Cama matrimonial, Baño privado', TRUE),
(1, 4, 4, 500, '2 camas Individuales, Baño privado', TRUE),
(1, 5, 5, 400, 'Cama matrimonial, Baño privado', TRUE),
(1, 6, 6, 400, 'Cama matrimonial, Baño privado', TRUE),
(1, 9, 9, 450, 'Cama matrimonial, Baño privado, Televisor', TRUE),
(1, 10, 10, 450, 'Cama matrimonial, Baño privado, Televisor', TRUE),
(1, 11, 11, 450, 'Cama matrimonial, Baño privado, Televisor', TRUE),
(1, 12, 12, 450, 'Cama matrimonial, Baño privado, Televisor', TRUE),
(1, 13, 13, 450, 'Cama matrimonial, Baño privado, Televisor', TRUE),
(1, 14, 14, 450, 'Cama matrimonial, Baño privado, Televisor', TRUE),
(1, 15, 15, 400, 'Cama matrimonial, Baño privado', TRUE),
(1, 16, 16, 500, '2 camas Individuales, Baño privado', TRUE),
(1, 17, 17, 400, 'Cama matrimonial, Baño privado', TRUE),
(1, 18, 18, 400, 'Cama matrimonial, Baño privado', TRUE),

-- Categoría 2: Estándar
(2, 7, 7, 550, '2 camas Individuales, Baño privado, Televisor', TRUE),
(2, 8, 8, 550, '2 camas Individuales, Baño privado, Televisor', TRUE),
(2, 19, 19, 700, '2 camas matrimoniales, Baño privado', TRUE),
(2, 20, 20, 900, '4 camas individuales, Baño privado', TRUE),
(2, 21, 21, 700, '3 camas individuales, Baño privado', TRUE),
(2, 22, 22, 550, '2 camas Individuales, Baño privado, Televisor', TRUE),

-- Categoría 3: Ejecutiva
(3, 23, 23, 1100, 'Cama Queen, Baño privado, Aire Acondicionado, Televisor', TRUE),
(3, 24, 24, 1100, 'Cama Queen, Baño privado, Aire Acondicionado, Televisor', TRUE),
(3, 25, 25, 1100, 'Cama Queen, Baño privado, Aire Acondicionado, Televisor', TRUE)
ON CONFLICT (id) DO NOTHING;

-- =====================================================
-- VERIFICAR DATOS CARGADOS
-- =====================================================

-- Verificar categorías
SELECT 'Categorías' as tabla, COUNT(*) as total FROM "Categorias";

-- Verificar habitaciones
SELECT 'Habitaciones' as tabla, COUNT(*) as total FROM habitaciones;

-- Mostrar distribución de habitaciones por categoría
SELECT
  c."NombreCategoria" as Categoria,
  COUNT(h.id) as Cantidad,
  AVG(h.precio) as Precio_Promedio,
  MIN(h.precio) as Precio_Minimo,
  MAX(h.precio) as Precio_Maximo
FROM habitaciones h
JOIN "Categorias" c ON h.id_categoria = c.id_categoria
GROUP BY c."NombreCategoria", h.id_categoria
ORDER BY h.id_categoria;

-- Mostrar todas las habitaciones con su categoría
SELECT
  h.id,
  h."Numero_Habitacion",
  c."NombreCategoria",
  h.precio,
  h."Descripcion",
  CASE WHEN h."Estado" = true THEN 'Disponible' ELSE 'No disponible' END as Estado
FROM habitaciones h
LEFT JOIN "Categorias" c ON h.id_categoria = c.id_categoria
ORDER BY h.id;
