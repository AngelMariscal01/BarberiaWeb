-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 17-01-2024 a las 21:05:43
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `barberia`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Barberia`
--

CREATE TABLE `Barberia` (
  `BarberiaId` int(10) NOT NULL,
  `Ubicacion` varchar(100) DEFAULT NULL,
  `Nombre` varchar(100) DEFAULT NULL,
  `Calificacion` smallint(5) DEFAULT NULL,
  `Servicios` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Barberos`
--

CREATE TABLE `Barberos` (
  `BarberoID` int(100) NOT NULL,
  `UserID` int(100) DEFAULT NULL,
  `Precios` varchar(100) DEFAULT NULL,
  `Especialidad` varchar(100) DEFAULT NULL,
  `Horario` varchar(100) DEFAULT NULL,
  `BarberiaID` int(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Carrito`
--

CREATE TABLE `Carrito` (
  `CarritoID` int(10) NOT NULL,
  `UserID` int(10) DEFAULT NULL,
  `ProductoID` int(10) DEFAULT NULL,
  `Cantidad` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Comentarios`
--

CREATE TABLE `Comentarios` (
  `ComentarioID` int(10) NOT NULL,
  `PublicacionID` int(10) DEFAULT NULL,
  `UserID` int(10) DEFAULT NULL,
  `Contenido` varchar(100) DEFAULT NULL,
  `Fecha` date DEFAULT NULL,
  `Hora` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `HistorialCompra`
--

CREATE TABLE `HistorialCompra` (
  `HistorialId` int(10) NOT NULL,
  `UserId` int(10) DEFAULT NULL,
  `ProductoId` int(10) DEFAULT NULL,
  `Cantidad` int(7) DEFAULT NULL,
  `Fecha` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Productos`
--

CREATE TABLE `Productos` (
  `ProductoID` int(100) NOT NULL,
  `Nombre` varchar(100) DEFAULT NULL,
  `Descripcion` varchar(100) DEFAULT NULL,
  `Precio` float DEFAULT NULL,
  `Stock` int(10) DEFAULT NULL,
  `Foto` mediumblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Publicaciones`
--

CREATE TABLE `Publicaciones` (
  `PublicacionID` int(10) NOT NULL,
  `BarberoID` int(10) DEFAULT NULL,
  `Titulo` varchar(100) DEFAULT NULL,
  `Contenido` varchar(100) DEFAULT NULL,
  `Fecha` date DEFAULT NULL,
  `Hora` time DEFAULT NULL,
  `foto` mediumblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Usuarios`
--

CREATE TABLE `Usuarios` (
  `UserID` int(10) NOT NULL,
  `Nombre` varchar(100) DEFAULT NULL,
  `Apellido` varchar(100) DEFAULT NULL,
  `Correo` varchar(100) DEFAULT NULL,
  `Contrasena` varchar(100) DEFAULT NULL,
  `Telefono` varchar(12) DEFAULT NULL,
  `FechaNacimiento` date DEFAULT NULL,
  `Sexo` tinyint(1) DEFAULT NULL,
  `foto` mediumblob DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `Barberia`
--
ALTER TABLE `Barberia`
  ADD PRIMARY KEY (`BarberiaId`);

--
-- Indices de la tabla `Barberos`
--
ALTER TABLE `Barberos`
  ADD PRIMARY KEY (`BarberoID`),
  ADD KEY `UserID` (`UserID`),
  ADD KEY `BarberiaID` (`BarberiaID`);

--
-- Indices de la tabla `Carrito`
--
ALTER TABLE `Carrito`
  ADD PRIMARY KEY (`CarritoID`),
  ADD KEY `UserID` (`UserID`),
  ADD KEY `ProductoID` (`ProductoID`);

--
-- Indices de la tabla `Comentarios`
--
ALTER TABLE `Comentarios`
  ADD PRIMARY KEY (`ComentarioID`),
  ADD KEY `UserID` (`UserID`),
  ADD KEY `Comentarios_ibfk_3` (`PublicacionID`);

--
-- Indices de la tabla `HistorialCompra`
--
ALTER TABLE `HistorialCompra`
  ADD PRIMARY KEY (`HistorialId`),
  ADD KEY `UsuarioId` (`UserId`),
  ADD KEY `ProductoId` (`ProductoId`);

--
-- Indices de la tabla `Productos`
--
ALTER TABLE `Productos`
  ADD PRIMARY KEY (`ProductoID`);

--
-- Indices de la tabla `Publicaciones`
--
ALTER TABLE `Publicaciones`
  ADD PRIMARY KEY (`PublicacionID`),
  ADD KEY `BarberoID` (`BarberoID`);

--
-- Indices de la tabla `Usuarios`
--
ALTER TABLE `Usuarios`
  ADD PRIMARY KEY (`UserID`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `Barberia`
--
ALTER TABLE `Barberia`
  MODIFY `BarberiaId` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `Barberos`
--
ALTER TABLE `Barberos`
  MODIFY `BarberoID` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `Carrito`
--
ALTER TABLE `Carrito`
  MODIFY `CarritoID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `Comentarios`
--
ALTER TABLE `Comentarios`
  MODIFY `ComentarioID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `HistorialCompra`
--
ALTER TABLE `HistorialCompra`
  MODIFY `HistorialId` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `Publicaciones`
--
ALTER TABLE `Publicaciones`
  MODIFY `PublicacionID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `Usuarios`
--
ALTER TABLE `Usuarios`
  MODIFY `UserID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `Barberos`
--
ALTER TABLE `Barberos`
  ADD CONSTRAINT `Barberos_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `Usuarios` (`UserID`),
  ADD CONSTRAINT `Barberos_ibfk_2` FOREIGN KEY (`UserID`) REFERENCES `Usuarios` (`UserID`),
  ADD CONSTRAINT `Barberos_ibfk_3` FOREIGN KEY (`BarberiaID`) REFERENCES `Barberia` (`BarberiaId`),
  ADD CONSTRAINT `Barberos_ibfk_4` FOREIGN KEY (`BarberiaID`) REFERENCES `Barberia` (`BarberiaId`),
  ADD CONSTRAINT `Barberos_ibfk_5` FOREIGN KEY (`BarberiaID`) REFERENCES `Barberia` (`BarberiaId`),
  ADD CONSTRAINT `Barberos_ibfk_6` FOREIGN KEY (`BarberiaID`) REFERENCES `Barberia` (`BarberiaId`);

--
-- Filtros para la tabla `Carrito`
--
ALTER TABLE `Carrito`
  ADD CONSTRAINT `Carrito_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `Usuarios` (`UserID`),
  ADD CONSTRAINT `Carrito_ibfk_2` FOREIGN KEY (`ProductoID`) REFERENCES `Productos` (`ProductoID`),
  ADD CONSTRAINT `Carrito_ibfk_3` FOREIGN KEY (`UserID`) REFERENCES `Usuarios` (`UserID`),
  ADD CONSTRAINT `Carrito_ibfk_4` FOREIGN KEY (`ProductoID`) REFERENCES `Productos` (`ProductoID`);

--
-- Filtros para la tabla `Comentarios`
--
ALTER TABLE `Comentarios`
  ADD CONSTRAINT `Comentarios_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `Usuarios` (`UserID`),
  ADD CONSTRAINT `Comentarios_ibfk_3` FOREIGN KEY (`PublicacionID`) REFERENCES `Publicaciones` (`PublicacionID`),
  ADD CONSTRAINT `Comentarios_ibfk_4` FOREIGN KEY (`UserID`) REFERENCES `Usuarios` (`UserID`);

--
-- Filtros para la tabla `HistorialCompra`
--
ALTER TABLE `HistorialCompra`
  ADD CONSTRAINT `HistorialCompra_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `Usuarios` (`UserID`),
  ADD CONSTRAINT `HistorialCompra_ibfk_2` FOREIGN KEY (`ProductoId`) REFERENCES `Productos` (`ProductoID`);

--
-- Filtros para la tabla `Publicaciones`
--
ALTER TABLE `Publicaciones`
  ADD CONSTRAINT `Publicaciones_ibfk_1` FOREIGN KEY (`BarberoID`) REFERENCES `Barberos` (`BarberoID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
