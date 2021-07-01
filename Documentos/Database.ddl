-- Generado por Oracle SQL Developer Data Modeler 19.4.0.350.1424
--   en:        2021-06-11 21:01:59 CLT
--   sitio:      Oracle Database 11g
--   tipo:      Oracle Database 11g



CREATE TABLE boleta (
    nroboleta      NUMBER NOT NULL,
    fechaemision   DATE NOT NULL,
    total          NUMBER NOT NULL,
    venta_idventa  NUMBER NOT NULL,
    vigente        CHAR(1) NOT NULL
);

ALTER TABLE boleta ADD CONSTRAINT boleta_pk PRIMARY KEY ( nroboleta );

CREATE TABLE cargo (
    idcargo  NUMBER NOT NULL,
    cargo    VARCHAR2(20 CHAR) NOT NULL
);

ALTER TABLE cargo ADD CONSTRAINT cargo_pk PRIMARY KEY ( idcargo );

CREATE TABLE ciudad (
    idciudad         NUMBER NOT NULL,
    nombre           VARCHAR2(30 CHAR) NOT NULL,
    región_idregion  NUMBER NOT NULL
);

ALTER TABLE ciudad ADD CONSTRAINT ciudad_pk PRIMARY KEY ( idciudad );

CREATE TABLE cliente (
    idcliente          NUMBER NOT NULL,
    rut                VARCHAR2(10 CHAR) NOT NULL,
    nombres            VARCHAR2(30 CHAR) NOT NULL,
    apellidopaterno    VARCHAR2(20 CHAR) NOT NULL,
    apellidomaterno    VARCHAR2(20 CHAR) NOT NULL,
    dirección          VARCHAR2(40 CHAR) NOT NULL,
    telefono           VARCHAR2(9 CHAR) NOT NULL,
    email              VARCHAR2(40 CHAR) NOT NULL,
    comuna_idcomuna    NUMBER NOT NULL,
    usuario_idusuario  NUMBER NOT NULL
);

ALTER TABLE cliente ADD CONSTRAINT cliente_pk PRIMARY KEY ( idcliente );

CREATE TABLE comuna (
    idcomuna         NUMBER NOT NULL,
    nombre           VARCHAR2(30 CHAR) NOT NULL,
    ciudad_idciudad  NUMBER NOT NULL
);

ALTER TABLE comuna ADD CONSTRAINT comuna_pk PRIMARY KEY ( idcomuna );

CREATE TABLE detalle (
    iddetalle       NUMBER NOT NULL,
    idventa         NUMBER NOT NULL,
    idproducto      VARCHAR2(17 CHAR) NOT NULL,
    cantidad        NUMBER NOT NULL,
    preciounitario  NUMBER NOT NULL,
    subtotal        NUMBER NOT NULL
);

ALTER TABLE detalle ADD CONSTRAINT detalle_pk PRIMARY KEY ( iddetalle );

CREATE TABLE empleado (
    idempleado       NUMBER NOT NULL,
    rut              VARCHAR2(10 CHAR) NOT NULL,
    nombres          VARCHAR2(30 CHAR) NOT NULL,
    apellidopaterno  VARCHAR2(20 CHAR) NOT NULL,
    apellidomaterno  VARCHAR2(20 CHAR) NOT NULL,
    telefono         VARCHAR2(9 CHAR) NOT NULL,
    direccion        VARCHAR2(40 CHAR) NOT NULL,
    idcargo          NUMBER NOT NULL,
    idcomuna         NUMBER NOT NULL,
    idusuario        NUMBER NOT NULL
);

ALTER TABLE empleado ADD CONSTRAINT empleado_pk PRIMARY KEY ( idempleado );

CREATE TABLE factura (
    nrofactura     INTEGER NOT NULL,
    fechaemision   DATE NOT NULL,
    neto           NUMBER NOT NULL,
    iva            NUMBER NOT NULL,
    total          NUMBER NOT NULL,
    venta_idventa  NUMBER NOT NULL,
    vigente        CHAR(1) NOT NULL
);

ALTER TABLE factura ADD CONSTRAINT factura_pk PRIMARY KEY ( nrofactura );

CREATE TABLE familiaproducto (
    idfamiliaproducto  NUMBER NOT NULL,
    descripcion        VARCHAR2(40 CHAR) NOT NULL
);

ALTER TABLE familiaproducto ADD CONSTRAINT familiaproducto_pk PRIMARY KEY ( idfamiliaproducto );

CREATE TABLE grupo (
    idgrupo   NUMBER NOT NULL,
    nombre    VARCHAR2(20 CHAR) NOT NULL,
    permisos  XMLTYPE NOT NULL
) XMLTYPE COLUMN permisos STORE AS BINARY XML (
    STORAGE ( PCTINCREASE 0 MINEXTENTS 1 MAXEXTENTS UNLIMITED FREELISTS 1 BUFFER_POOL DEFAULT )
    RETENTION
    ENABLE STORAGE IN ROW
    NOCACHE
);

ALTER TABLE grupo ADD CONSTRAINT grupo_pk PRIMARY KEY ( idgrupo );

CREATE TABLE ordencompra (
    idordencompra  NUMBER NOT NULL,
    idproducto     VARCHAR2(17 CHAR) NOT NULL,
    cantidad       NUMBER NOT NULL,
    total          NUMBER NOT NULL,
    comentario     VARCHAR2(200 CHAR),
    fechapedido    DATE NOT NULL,
    idempleado     NUMBER NOT NULL,
    enviada        CHAR(1) NOT NULL,
    recibido       CHAR(1) NOT NULL,
    valido         CHAR(1) NOT NULL
);

ALTER TABLE ordencompra ADD CONSTRAINT ordencompra_pk PRIMARY KEY ( idordencompra );

CREATE TABLE producto (
    idproducto      VARCHAR2(17 CHAR) NOT NULL,
    nombre          VARCHAR2(30 CHAR) NOT NULL,
    descripcion     VARCHAR2(200 CHAR) NOT NULL,
    precio          NUMBER NOT NULL,
    stock           NUMBER NOT NULL,
    stockcrit       NUMBER NOT NULL,
    imagen          BLOB NOT NULL,
    fvenc           DATE NOT NULL,
    idtipoproducto  NUMBER NOT NULL,
    idproveedor     NUMBER NOT NULL
);

ALTER TABLE producto ADD CONSTRAINT producto_pk PRIMARY KEY ( idproducto );

CREATE TABLE proveedor (
    idproveedor        NUMBER NOT NULL,
    rut                VARCHAR2(10 CHAR) NOT NULL,
    nombres            VARCHAR2(20 CHAR) NOT NULL,
    representante      VARCHAR2(50 CHAR) NOT NULL,
    telefono           VARCHAR2(9 CHAR) NOT NULL,
    direccion          VARCHAR2(40 CHAR) NOT NULL,
    comuna_idcomuna    NUMBER NOT NULL,
    rubro_idrubro      NUMBER NOT NULL,
    usuario_idusuario  NUMBER NOT NULL
);

ALTER TABLE proveedor ADD CONSTRAINT proveedor_pk PRIMARY KEY ( idproveedor );

CREATE TABLE región (
    idregion  NUMBER NOT NULL,
    nombre    VARCHAR2(30 CHAR) NOT NULL
);

ALTER TABLE región ADD CONSTRAINT región_pk PRIMARY KEY ( idregion );

CREATE TABLE rubro (
    idrubro  NUMBER NOT NULL,
    rubro    VARCHAR2(30 CHAR) NOT NULL
);

ALTER TABLE rubro ADD CONSTRAINT rubro_pk PRIMARY KEY ( idrubro );

CREATE TABLE tipoproducto (
    idtipoproducto     NUMBER NOT NULL,
    descripcion        VARCHAR2(40 CHAR) NOT NULL,
    idfamiliaproducto  NUMBER NOT NULL
);

ALTER TABLE tipoproducto ADD CONSTRAINT tipoproducto_pk PRIMARY KEY ( idtipoproducto );

CREATE TABLE usuario (
    idusuario   NUMBER NOT NULL,
    usuario     VARCHAR2(20 CHAR) NOT NULL,
    contraseña  VARCHAR2(20 CHAR) NOT NULL,
    idgrupo     NUMBER NOT NULL
);

ALTER TABLE usuario ADD CONSTRAINT usuario_pk PRIMARY KEY ( idusuario );

CREATE TABLE venta (
    idventa            NUMBER NOT NULL,
    cliente_idcliente  NUMBER NOT NULL,
    fechaventa         DATE NOT NULL,
    total              INTEGER NOT NULL,
    valido             CHAR(1) NOT NULL
);

ALTER TABLE venta ADD CONSTRAINT venta_pk PRIMARY KEY ( idventa );

ALTER TABLE boleta
    ADD CONSTRAINT boleta_venta_fk FOREIGN KEY ( venta_idventa )
        REFERENCES venta ( idventa )
            ON DELETE CASCADE;

ALTER TABLE ciudad
    ADD CONSTRAINT ciudad_región_fk FOREIGN KEY ( región_idregion )
        REFERENCES región ( idregion );

ALTER TABLE cliente
    ADD CONSTRAINT cliente_comuna_fk FOREIGN KEY ( comuna_idcomuna )
        REFERENCES comuna ( idcomuna );

ALTER TABLE cliente
    ADD CONSTRAINT cliente_usuario_fk FOREIGN KEY ( usuario_idusuario )
        REFERENCES usuario ( idusuario );

ALTER TABLE comuna
    ADD CONSTRAINT comuna_ciudad_fk FOREIGN KEY ( ciudad_idciudad )
        REFERENCES ciudad ( idciudad );

ALTER TABLE detalle
    ADD CONSTRAINT detalle_producto_fk FOREIGN KEY ( idproducto )
        REFERENCES producto ( idproducto )
            ON DELETE CASCADE;

ALTER TABLE detalle
    ADD CONSTRAINT detalle_venta_fk FOREIGN KEY ( idventa )
        REFERENCES venta ( idventa );

ALTER TABLE empleado
    ADD CONSTRAINT empleado_cargo_fk FOREIGN KEY ( idcargo )
        REFERENCES cargo ( idcargo );

ALTER TABLE empleado
    ADD CONSTRAINT empleado_comuna_fk FOREIGN KEY ( idcomuna )
        REFERENCES comuna ( idcomuna );

ALTER TABLE empleado
    ADD CONSTRAINT empleado_usuario_fk FOREIGN KEY ( idusuario )
        REFERENCES usuario ( idusuario );

ALTER TABLE factura
    ADD CONSTRAINT factura_venta_fk FOREIGN KEY ( venta_idventa )
        REFERENCES venta ( idventa )
            ON DELETE CASCADE;

ALTER TABLE tipoproducto
    ADD CONSTRAINT famprodpk FOREIGN KEY ( idfamiliaproducto )
        REFERENCES familiaproducto ( idfamiliaproducto );

ALTER TABLE ordencompra
    ADD CONSTRAINT ordencompra_empleado_fk FOREIGN KEY ( idempleado )
        REFERENCES empleado ( idempleado );

ALTER TABLE ordencompra
    ADD CONSTRAINT ordencompra_producto_fk FOREIGN KEY ( idproducto )
        REFERENCES producto ( idproducto );

ALTER TABLE producto
    ADD CONSTRAINT producto_proveedor_fk FOREIGN KEY ( idproveedor )
        REFERENCES proveedor ( idproveedor );

ALTER TABLE producto
    ADD CONSTRAINT producto_tipoproducto_fk FOREIGN KEY ( idtipoproducto )
        REFERENCES tipoproducto ( idtipoproducto );

ALTER TABLE proveedor
    ADD CONSTRAINT proveedor_comuna_fk FOREIGN KEY ( comuna_idcomuna )
        REFERENCES comuna ( idcomuna );

ALTER TABLE proveedor
    ADD CONSTRAINT proveedor_rubro_fk FOREIGN KEY ( rubro_idrubro )
        REFERENCES rubro ( idrubro );

ALTER TABLE proveedor
    ADD CONSTRAINT proveedor_usuario_fk FOREIGN KEY ( usuario_idusuario )
        REFERENCES usuario ( idusuario );

ALTER TABLE usuario
    ADD CONSTRAINT usuario_grupo_fk FOREIGN KEY ( idgrupo )
        REFERENCES grupo ( idgrupo );

ALTER TABLE venta
    ADD CONSTRAINT venta_cliente_fk FOREIGN KEY ( cliente_idcliente )
        REFERENCES cliente ( idcliente )
            ON DELETE CASCADE;



-- Informe de Resumen de Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                            18
-- CREATE INDEX                             0
-- ALTER TABLE                             39
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   3
-- WARNINGS                                 0
