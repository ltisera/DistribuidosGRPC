CREATE TABLE filtros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    usuario_id INT NOT NULL,
    codigo_producto VARCHAR(255),
    rango_fechas_start BIGINT,
    rango_fechas_end BIGINT,
    estado VARCHAR(255),
    id_tienda INT,
    FOREIGN KEY (usuario_id) REFERENCES usuario(idusuario) ON DELETE CASCADE
);