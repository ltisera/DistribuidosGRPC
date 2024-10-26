INSERT INTO bdgrpc.tienda (direccion, ciudad, provincia, habilitado) VALUES ('CASACENTRAL', 'CASACENTRAL', 'CASACENTRAL', TRUE);
INSERT INTO bdgrpc.tienda (direccion, ciudad, provincia, habilitado) VALUES ('dirTienda1', 'ciuTienda1', 'provTienda1', TRUE);
INSERT INTO bdgrpc.usuario (usuario, password, nombre, apellido, habilitado, casaCentral, Tienda_idTienda) VALUES ( 'root', 'root', 'root', 'root', TRUE, TRUE, '1');
INSERT INTO bdgrpc.usuario (usuario, password, nombre, apellido, habilitado, casaCentral, Tienda_idTienda) VALUES ( 'cami', 'cami', 'cami', 'cami', TRUE, FALSE, '2');
INSERT INTO bdgrpc.producto (nombre, foto, color, codigo, habilitado) VALUES ('remera', 'https://dcdn.mitiendanube.com/stores/002/140/898/products/remera-azul1-f298c4d74417595e9616513267212895-640-0.jpg', 'azul', 'hAdEriTu9l', '1');
INSERT INTO bdgrpc.stock (cantidad, talle, tienda, producto) VALUES (0, "XXL", 1, 1)