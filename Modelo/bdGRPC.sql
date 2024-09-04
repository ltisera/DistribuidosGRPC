-- MySQL Script generated by MySQL Workbench
-- Wed Sep  4 19:59:10 2024
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema bdGRPC
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema bdGRPC
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bdGRPC` DEFAULT CHARACTER SET utf8 ;
USE `bdGRPC` ;

-- -----------------------------------------------------
-- Table `bdGRPC`.`Tienda`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdGRPC`.`Tienda` (
  `idTienda` INT NOT NULL AUTO_INCREMENT,
  `direccion` VARCHAR(45) NULL,
  `ciudad` VARCHAR(45) NULL,
  `provincia` VARCHAR(45) NULL,
  `habilitado` TINYINT NULL,
  PRIMARY KEY (`idTienda`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bdGRPC`.`Usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdGRPC`.`Usuario` (
  `idusuario` INT NOT NULL AUTO_INCREMENT,
  `usuario` VARCHAR(45) NULL,
  `password` VARCHAR(45) NULL,
  `nombre` VARCHAR(45) NULL,
  `apellido` VARCHAR(45) NULL,
  `habilitado` TINYINT NULL,
  `casaCentral` TINYINT NULL,
  `Tienda_idTienda` INT NULL,
  PRIMARY KEY (`idusuario`),
  INDEX `fk_Usuario_Tienda1_idx` (`Tienda_idTienda` ASC) VISIBLE,
  CONSTRAINT `fk_Usuario_Tienda1`
    FOREIGN KEY (`Tienda_idTienda`)
    REFERENCES `bdGRPC`.`Tienda` (`idTienda`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bdGRPC`.`Producto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdGRPC`.`Producto` (
  `idProducto` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `foto` VARCHAR(45) NULL,
  `color` VARCHAR(45) NULL,
  `codigo` VARCHAR(45) NULL,
  PRIMARY KEY (`idProducto`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bdGRPC`.`Stock`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdGRPC`.`Stock` (
  `Tienda_idTienda` INT NOT NULL,
  `cantidad` INT NULL,
  `Talle_idTalle` INT NOT NULL,
  PRIMARY KEY (`Tienda_idTienda`, `Talle_idTalle`),
  INDEX `fk_Producto_has_Tienda_Tienda1_idx` (`Tienda_idTienda` ASC) VISIBLE,
  INDEX `fk_Stock_Talle1_idx` (`Talle_idTalle` ASC) VISIBLE,
  CONSTRAINT `fk_Producto_has_Tienda_Tienda1`
    FOREIGN KEY (`Tienda_idTienda`)
    REFERENCES `bdGRPC`.`Tienda` (`idTienda`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Stock_Talle1`
    FOREIGN KEY (`Talle_idTalle`)
    REFERENCES `bdGRPC`.`Talle` (`idTalle`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bdGRPC`.`Talle`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdGRPC`.`Talle` (
  `Producto_idProducto` INT NOT NULL,
  `talle` INT NULL,
  `idTalle` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`idTalle`),
  CONSTRAINT `fk_Talle_Producto1`
    FOREIGN KEY (`Producto_idProducto`)
    REFERENCES `bdGRPC`.`Producto` (`idProducto`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bdGRPC`.`Stock`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdGRPC`.`Stock` (
  `Tienda_idTienda` INT NOT NULL,
  `cantidad` INT NULL,
  `Talle_idTalle` INT NOT NULL,
  PRIMARY KEY (`Tienda_idTienda`, `Talle_idTalle`),
  INDEX `fk_Producto_has_Tienda_Tienda1_idx` (`Tienda_idTienda` ASC) VISIBLE,
  INDEX `fk_Stock_Talle1_idx` (`Talle_idTalle` ASC) VISIBLE,
  CONSTRAINT `fk_Producto_has_Tienda_Tienda1`
    FOREIGN KEY (`Tienda_idTienda`)
    REFERENCES `bdGRPC`.`Tienda` (`idTienda`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Stock_Talle1`
    FOREIGN KEY (`Talle_idTalle`)
    REFERENCES `bdGRPC`.`Talle` (`idTalle`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
