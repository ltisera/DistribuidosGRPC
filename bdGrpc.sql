-- MySQL Script generated by MySQL Workbench
-- Sun Oct 27 17:20:27 2024
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema bdgrpc
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema bdgrpc
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bdgrpc` DEFAULT CHARACTER SET utf8mb3 ;
USE `bdgrpc` ;

-- -----------------------------------------------------
-- Table `bdgrpc`.`tienda`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdgrpc`.`tienda` (
  `idTienda` INT NOT NULL AUTO_INCREMENT,
  `direccion` VARCHAR(45) NULL DEFAULT NULL,
  `ciudad` VARCHAR(45) NULL DEFAULT NULL,
  `provincia` VARCHAR(45) NULL DEFAULT NULL,
  `habilitado` TINYINT NULL DEFAULT NULL,
  `codigo` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idTienda`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `bdgrpc`.`catalogo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdgrpc`.`catalogo` (
  `idCatalogo` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL DEFAULT NULL,
  `idTienda` INT NOT NULL,
  PRIMARY KEY (`idCatalogo`),
  INDEX `fk_catalogo_tienda1_idx` (`idTienda` ASC) VISIBLE,
  CONSTRAINT `fk_catalogo_tienda1`
    FOREIGN KEY (`idTienda`)
    REFERENCES `bdgrpc`.`tienda` (`idTienda`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `bdgrpc`.`producto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdgrpc`.`producto` (
  `idProducto` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL DEFAULT NULL,
  `foto` VARCHAR(450) NULL DEFAULT NULL,
  `color` VARCHAR(45) NULL DEFAULT NULL,
  `codigo` VARCHAR(45) NULL DEFAULT NULL,
  `habilitado` TINYINT NULL DEFAULT NULL,
  PRIMARY KEY (`idProducto`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `bdgrpc`.`catalogo_has_producto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdgrpc`.`catalogo_has_producto` (
  `idCatalogo` INT NOT NULL,
  `idProducto` INT NOT NULL,
  `talle` VARCHAR(45) NOT NULL,
  INDEX `fk_catalogo_has_producto_producto1_idx` (`idProducto` ASC) VISIBLE,
  INDEX `fk_catalogo_has_producto_catalogo1_idx` (`idCatalogo` ASC) VISIBLE,
  CONSTRAINT `fk_catalogo_has_producto_catalogo1`
    FOREIGN KEY (`idCatalogo`)
    REFERENCES `bdgrpc`.`catalogo` (`idCatalogo`),
  CONSTRAINT `fk_catalogo_has_producto_producto1`
    FOREIGN KEY (`idProducto`)
    REFERENCES `bdgrpc`.`producto` (`idProducto`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `bdgrpc`.`usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdgrpc`.`usuario` (
  `idusuario` INT NOT NULL AUTO_INCREMENT,
  `usuario` VARCHAR(45) NULL DEFAULT NULL,
  `password` VARCHAR(45) NULL DEFAULT NULL,
  `nombre` VARCHAR(45) NULL DEFAULT NULL,
  `apellido` VARCHAR(45) NULL DEFAULT NULL,
  `habilitado` TINYINT NULL DEFAULT NULL,
  `casaCentral` TINYINT NULL DEFAULT NULL,
  `Tienda_idTienda` INT NULL DEFAULT NULL,
  PRIMARY KEY (`idusuario`),
  INDEX `fk_Usuario_Tienda1_idx` (`Tienda_idTienda` ASC) VISIBLE,
  CONSTRAINT `fk_Usuario_Tienda`
    FOREIGN KEY (`Tienda_idTienda`)
    REFERENCES `bdgrpc`.`tienda` (`idTienda`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `bdgrpc`.`filtros`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdgrpc`.`filtros` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) NOT NULL,
  `usuario_id` INT NOT NULL,
  `codigo_producto` VARCHAR(255) NULL DEFAULT NULL,
  `rango_fechas_start` BIGINT NULL DEFAULT NULL,
  `rango_fechas_end` BIGINT NULL DEFAULT NULL,
  `estado` VARCHAR(255) NULL DEFAULT NULL,
  `id_tienda` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `usuario_id` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `filtros_ibfk_1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `bdgrpc`.`usuario` (`idusuario`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `bdgrpc`.`novedades`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdgrpc`.`novedades` (
  `codigo` VARCHAR(100) NOT NULL,
  `nombre` VARCHAR(255) NOT NULL,
  `talle` VARCHAR(50) NOT NULL,
  `color` VARCHAR(50) NOT NULL,
  `url` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`codigo`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `bdgrpc`.`stock`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdgrpc`.`stock` (
  `idStock` INT NOT NULL AUTO_INCREMENT,
  `cantidad` INT NULL DEFAULT NULL,
  `talle` VARCHAR(45) NULL DEFAULT NULL,
  `tienda` INT NOT NULL,
  `producto` INT NOT NULL,
  PRIMARY KEY (`idStock`),
  INDEX `fk_Producto_has_Tienda_Tienda1_idx` (`tienda` ASC) VISIBLE,
  INDEX `fk_Stock_Producto2_idx` (`producto` ASC) VISIBLE,
  CONSTRAINT `fk_Producto_has_Tienda_Tienda1`
    FOREIGN KEY (`tienda`)
    REFERENCES `bdgrpc`.`tienda` (`idTienda`),
  CONSTRAINT `fk_Stock_Producto2`
    FOREIGN KEY (`producto`)
    REFERENCES `bdgrpc`.`producto` (`idProducto`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `bdgrpc`.`ordendecompra`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdgrpc`.`ordendecompra` (
  `idOrdenDeCompra` INT NOT NULL AUTO_INCREMENT,
  `idStock` INT NOT NULL,
  `cantidad` VARCHAR(45) NULL DEFAULT NULL,
  `estado` VARCHAR(45) NULL DEFAULT NULL,
  `observaciones` VARCHAR(450) NULL DEFAULT NULL,
  `fechaSolicitud` BIGINT NULL DEFAULT NULL,
  `fechaRecepcion` BIGINT NULL DEFAULT NULL,
  `ordenDeDespacho` INT NULL DEFAULT NULL,
  PRIMARY KEY (`idOrdenDeCompra`),
  INDEX `fk_ordenDeCompra_stock1_idx` (`idStock` ASC) VISIBLE,
  CONSTRAINT `fk_ordenDeCompra_stock1`
    FOREIGN KEY (`idStock`)
    REFERENCES `bdgrpc`.`stock` (`idStock`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
