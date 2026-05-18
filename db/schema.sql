-- =======================================================
-- SCRIPT DE BASE DE DATOS PARA SQL SERVER MANAGEMENT STUDIO (SSMS)
-- Proyecto: Hotel Costa Sur - Estructura T-SQL Oficial
-- =======================================================

USE master;
GO
IF EXISTS (SELECT name FROM sys.databases WHERE name = 'HotelCostaSur')
BEGIN
    ALTER DATABASE HotelCostaSur SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE HotelCostaSur;
END
GO
CREATE DATABASE HotelCostaSur;
GO
USE HotelCostaSur;
GO

IF OBJECT_ID('dbo.participantes_sorteo', 'U') IS NOT NULL DROP TABLE dbo.participantes_sorteo;
IF OBJECT_ID('dbo.reservas', 'U') IS NOT NULL DROP TABLE dbo.reservas;
IF OBJECT_ID('dbo.habitaciones', 'U') IS NOT NULL DROP TABLE dbo.habitaciones;
IF OBJECT_ID('dbo.Categorias', 'U') IS NOT NULL DROP TABLE dbo.Categorias;
IF OBJECT_ID('dbo.usuarios', 'U') IS NOT NULL DROP TABLE dbo.usuarios;
GO

CREATE TABLE usuarios (
    id_usuario INT IDENTITY(1,1) PRIMARY KEY,
    usuario NVARCHAR(50) UNIQUE NOT NULL,
    correo NVARCHAR(100) UNIQUE NOT NULL,
    contrasena NVARCHAR(255) NOT NULL,
    rol NVARCHAR(10) DEFAULT 'user' CHECK (rol IN ('user', 'admin')),
    fecha_registro DATETIME DEFAULT GETDATE()
);
GO

CREATE TABLE Categorias (
    id_categoria INT PRIMARY KEY,
    NombreCategoria NVARCHAR(50) NOT NULL
);
GO

CREATE TABLE habitaciones (
    id_habitacion INT PRIMARY KEY,
    nombre NVARCHAR(50) NOT NULL,
    tipo NVARCHAR(50) NOT NULL,
    id_categoria INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    caracteristicas NVARCHAR(MAX) NOT NULL,
    disponible BIT DEFAULT 1,
    televisor BIT DEFAULT 0,
    aire BIT DEFAULT 0,
    FOREIGN KEY (id_categoria) REFERENCES Categorias(id_categoria) ON DELETE CASCADE
);
GO

CREATE TABLE reservas (
    id_reserva INT IDENTITY(1,1) PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_habitacion INT NOT NULL,
    estado NVARCHAR(20) DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'activo', 'completado')),
    fecha_ingreso DATE NOT NULL,
    fecha_salida DATE NOT NULL,
    dias INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    nombres NVARCHAR(50) NOT NULL,
    apellidos NVARCHAR(50) NOT NULL,
    tipo_documento NVARCHAR(20) NOT NULL,
    cedula NVARCHAR(20) NULL,
    pais_pasaporte NVARCHAR(50) NULL,
    pasaporte NVARCHAR(50) NULL,
    sexo NVARCHAR(10) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    nacionalidad NVARCHAR(50) NOT NULL,
    procedencia NVARCHAR(100) NOT NULL,
    num_huespedes INT NOT NULL,
    metodo_pago NVARCHAR(50) NOT NULL,
    fecha_reserva DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_habitacion) REFERENCES habitaciones(id_habitacion)
);
GO

CREATE TABLE participantes_sorteo (
    id_participante INT IDENTITY(1,1) PRIMARY KEY,
    nombres NVARCHAR(50) NOT NULL,
    apellidos NVARCHAR(50) NOT NULL,
    email NVARCHAR(100) UNIQUE NOT NULL,
    telefono NVARCHAR(20) NOT NULL,
    departamento NVARCHAR(50) NOT NULL,
    sexo NVARCHAR(10) NOT NULL,
    edad INT NOT NULL,
    ocupacion NVARCHAR(50) NOT NULL,
    fecha_registro DATETIME DEFAULT GETDATE()
);
GO
