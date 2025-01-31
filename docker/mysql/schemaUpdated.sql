-- Crear base de datos
DROP DATABASE IF EXISTS StockManager;
CREATE DATABASE StockManager;
USE StockManager;

GRANT ALL PRIVILEGES ON StockManager.* TO 'root'@'%';
FLUSH PRIVILEGES;


-- Crear tabla `categorias_productos`
DROP TABLE IF EXISTS `categorias_productos`;
CREATE TABLE `categorias_productos` (
  `id_categoria` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_categoria`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Crear tabla `clientes`
DROP TABLE IF EXISTS `clientes`;
CREATE TABLE `clientes` (
  `cedula` bigint DEFAULT NULL,
  `nombres` varchar(100) DEFAULT NULL,
  `apellidos` varchar(100) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `correo_electronico` varchar(100) DEFAULT NULL,
  `identificador_c` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`identificador_c`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Crear tabla `proveedores`
DROP TABLE IF EXISTS `proveedores`;
CREATE TABLE `proveedores` (
  `nombre_empresa` varchar(100) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `correo_electronico` varchar(100) DEFAULT NULL,
  `id_proveedor` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id_proveedor`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Crear tabla `productos`
DROP TABLE IF EXISTS `productos`;
CREATE TABLE `productos` (
  `identificador_p` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `descripcion` text,
  `precio` decimal(10,2) DEFAULT NULL,
  `stock` int DEFAULT NULL,
  `fecha_ingreso` date DEFAULT NULL,
  `id_proveedor` int DEFAULT NULL,
  `id_categoria` int DEFAULT NULL,
  PRIMARY KEY (`identificador_p`),
  KEY `fk_proveedor` (`id_proveedor`),
  KEY `fk_categoria` (`id_categoria`),
  CONSTRAINT `fk_categoria` FOREIGN KEY (`id_categoria`) REFERENCES `categorias_productos` (`id_categoria`),
  CONSTRAINT `fk_proveedor` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id_proveedor`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Crear tabla `users`
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id_trabajador` int NOT NULL AUTO_INCREMENT,
  `identification` BIGINT NOT NULL,
  `password` varchar(255) NOT NULL,
  `fullname` varchar(255) DEFAULT NULL,
  `role` enum('user','admin') DEFAULT 'user',
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id_trabajador`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Crear tabla `ventas`
DROP TABLE IF EXISTS `ventas`;
CREATE TABLE `ventas` (
  `id_venta` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `id_cliente` int DEFAULT NULL,
  `fecha_venta` date DEFAULT NULL,
  `hora_venta` time DEFAULT NULL,
  PRIMARY KEY (`id_venta`),
  KEY `id_usuario` (`id_usuario`),
  KEY `fk_cliente` (`id_cliente`),
  CONSTRAINT `fk_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`identificador_c`) ON DELETE CASCADE,
  CONSTRAINT `ventas_ibfk_3` FOREIGN KEY (`id_usuario`) REFERENCES `users` (`id_trabajador`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Crear tabla `compras`
DROP TABLE IF EXISTS `compras`;
CREATE TABLE `compras` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_producto` int NOT NULL,
  `cantidad` int DEFAULT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL,
  `fecha_compra` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `id_proveedor` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_producto` (`id_producto`),
  KEY `fk_compras_proveedor` (`id_proveedor`),
  CONSTRAINT `compras_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`identificador_p`),
  CONSTRAINT `fk_compras_proveedor` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id_proveedor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Crear tabla `detalles_ventas`
DROP TABLE IF EXISTS `detalles_ventas`;
CREATE TABLE `detalles_ventas` (
  `id_detalles` int NOT NULL AUTO_INCREMENT,
  `id_venta` int DEFAULT NULL,
  `id_producto` int NOT NULL,
  `cantidad` int DEFAULT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL,
  `descripcion` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id_detalles`),
  KEY `id_venta` (`id_venta`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `detalles_ventas_ibfk_1` FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id_venta`) ON DELETE CASCADE,
  CONSTRAINT `detalles_ventas_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`identificador_p`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Crear tabla `facturas`
DROP TABLE IF EXISTS `facturas`;
CREATE TABLE `facturas` (
  `id_factura` int NOT NULL AUTO_INCREMENT,
  `numero_factura` varchar(20) NOT NULL,
  `id_venta` int NOT NULL,
  `fecha_emision` date NOT NULL,
  PRIMARY KEY (`id_factura`),
  UNIQUE KEY `numero_factura` (`numero_factura`),
  KEY `fk_factura_venta` (`id_venta`),
  CONSTRAINT `fk_factura_venta` FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id_venta`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Crear tabla `pagos`
DROP TABLE IF EXISTS `pagos`;
CREATE TABLE `pagos` (
  `id_pagos` int NOT NULL AUTO_INCREMENT,
  `id_venta` int DEFAULT NULL,
  `monto` decimal(10,2) DEFAULT NULL,
  `fecha_pago` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `id_cliente` int DEFAULT NULL,
  `hora_pago` time DEFAULT NULL,
  `nota` varchar(400) DEFAULT NULL,
  `id_factura` int DEFAULT NULL,
  PRIMARY KEY (`id_pagos`),
  KEY `id_venta` (`id_venta`),
  KEY `fk_pagos_cliente` (`id_cliente`),
  KEY `fk_pagos_factura` (`id_factura`),
  CONSTRAINT `fk_pagos_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`identificador_c`) ON DELETE CASCADE,
  CONSTRAINT `fk_pagos_factura` FOREIGN KEY (`id_factura`) REFERENCES `facturas` (`id_factura`) ON DELETE CASCADE,
  CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id_venta`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
