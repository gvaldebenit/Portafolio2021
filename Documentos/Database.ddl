-- Generado por Oracle SQL Developer Data Modeler 19.4.0.350.1424
--   en:        2021-05-03 16:58:11 CLT
--   sitio:      Oracle Database 11g
--   tipo:      Oracle Database 11g



CREATE TABLE boleta (
    nroboleta      NUMBER NOT NULL,
    fecha_emision  DATE NOT NULL,
    totalboleta    NUMBER NOT NULL,
    venta_idvent   NUMBER NOT NULL
);

ALTER TABLE boleta ADD CONSTRAINT boleta_pk PRIMARY KEY ( nroboleta );

CREATE TABLE ciudad (
    idciudad         NUMBER NOT NULL,
    nombre           VARCHAR2(30 CHAR) NOT NULL,
    región_idregion  NUMBER NOT NULL
);

ALTER TABLE ciudad ADD CONSTRAINT ciudad_pk PRIMARY KEY ( idciudad );

CREATE TABLE cliente (
    idcliente              NUMBER NOT NULL,
    rut                    VARCHAR2(10 CHAR) NOT NULL,
    nombres                VARCHAR2(30 CHAR) NOT NULL,
    apellidopaterno        VARCHAR2(20 CHAR) NOT NULL,
    apellidomaterno        VARCHAR2(20 CHAR) NOT NULL,
    dirección              VARCHAR2(40 CHAR) NOT NULL,
    telefono               VARCHAR2(9 CHAR) NOT NULL,
    email                  VARCHAR2(40 CHAR) NOT NULL,
    comuna_idcomuna        NUMBER NOT NULL,
    tipousuario_idtipou    NUMBER NOT NULL,
    credenciales_idcuenta  INTEGER NOT NULL
);

ALTER TABLE cliente ADD CONSTRAINT cliente_pk PRIMARY KEY ( idcliente );

CREATE TABLE comuna (
    idcomuna         NUMBER NOT NULL,
    nombre           VARCHAR2(30 CHAR) NOT NULL,
    ciudad_idciudad  NUMBER NOT NULL
);

ALTER TABLE comuna ADD CONSTRAINT comuna_pk PRIMARY KEY ( idcomuna );

CREATE TABLE credenciales (
    idcuenta    INTEGER NOT NULL,
    usuario     VARCHAR2(20) NOT NULL,
    contraseña  VARCHAR2(20) NOT NULL
);

ALTER TABLE credenciales ADD CONSTRAINT credenciales_pk PRIMARY KEY ( idcuenta );

CREATE TABLE detalle (
    iddetalle            NUMBER NOT NULL,
    cantidad             NUMBER NOT NULL,
    valorunitario        NUMBER NOT NULL,
    sub_total            NUMBER NOT NULL,
    producto_idproducto  VARCHAR2(17 CHAR) NOT NULL,
    venta_idvent         NUMBER NOT NULL
);

ALTER TABLE detalle ADD CONSTRAINT detalle_pk PRIMARY KEY ( iddetalle );

CREATE TABLE empleado (
    idempleado             NUMBER NOT NULL,
    rut                    VARCHAR2(10 CHAR) NOT NULL,
    nombres                VARCHAR2(30 CHAR) NOT NULL,
    apellidopaterno        VARCHAR2(20 CHAR) NOT NULL,
    apellidomaterno        VARCHAR2(20 CHAR) NOT NULL,
    telefono               VARCHAR2(9 CHAR) NOT NULL,
    direccion              VARCHAR2(40 CHAR) NOT NULL,
    cargo                  NUMBER NOT NULL,
    tipousuario_idtipou    NUMBER NOT NULL,
    credenciales_idcuenta  INTEGER NOT NULL
);

ALTER TABLE empleado ADD CONSTRAINT empleado_pk PRIMARY KEY ( idempleado );

CREATE TABLE factura (
    nrofactura    INTEGER NOT NULL,
    fecemision    DATE NOT NULL,
    neto          NUMBER NOT NULL,
    iva           NUMBER NOT NULL,
    total         NUMBER NOT NULL,
    venta_idvent  NUMBER NOT NULL
);

ALTER TABLE factura ADD CONSTRAINT factura_pk PRIMARY KEY ( nrofactura );

CREATE TABLE familiaproducto (
    idfamproducto  NUMBER NOT NULL,
    descripcion    VARCHAR2(40 CHAR) NOT NULL
);

ALTER TABLE familiaproducto ADD CONSTRAINT familiaproducto_pk PRIMARY KEY ( idfamproducto );

CREATE TABLE ordencompra (
    idordcompra          NUMBER NOT NULL,
    cantidad             NUMBER NOT NULL,
    total                NUMBER NOT NULL,
    comentario           VARCHAR2(200 CHAR),
    empleado_idempleado  NUMBER NOT NULL,
    producto_idproducto  VARCHAR2(17 CHAR) NOT NULL
);

ALTER TABLE ordencompra ADD CONSTRAINT ordencompra_pk PRIMARY KEY ( idordcompra );

CREATE TABLE producto (
    idproducto                     VARCHAR2(17 CHAR) NOT NULL,
    nombre                         VARCHAR2(30 CHAR) NOT NULL,
    descripcion                    VARCHAR2(200 CHAR) NOT NULL,
    precio                         NUMBER NOT NULL,
    stock                          NUMBER NOT NULL,
    stockcrit                      NUMBER NOT NULL,
    fvenc                          DATE NOT NULL,
    familiaproducto_idfamproducto  NUMBER NOT NULL,
    tipoproducto_idtipoprod        NUMBER NOT NULL,
    proveedor_idproveedor          NUMBER NOT NULL,
    proveedor_idrubro              NUMBER NOT NULL
);

ALTER TABLE producto ADD CONSTRAINT producto_pk PRIMARY KEY ( idproducto );

CREATE TABLE proveedor (
    idproveedor            NUMBER NOT NULL,
    rut                    VARCHAR2(10 CHAR) NOT NULL,
    nombre                 VARCHAR2(20 CHAR) NOT NULL,
    representante          VARCHAR2(50 CHAR) NOT NULL,
    telefono               VARCHAR2(9 CHAR) NOT NULL,
    direccion              VARCHAR2(40 CHAR) NOT NULL,
    comuna_idcomuna        NUMBER NOT NULL,
    tipousuario_idtipou    NUMBER NOT NULL,
    credenciales_idcuenta  INTEGER NOT NULL,
    rubro_idrubro          NUMBER NOT NULL
);

ALTER TABLE proveedor ADD CONSTRAINT proveedor_pk PRIMARY KEY ( idproveedor,
                                                                rubro_idrubro );

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
    idtipoprod   NUMBER NOT NULL,
    descripcion  VARCHAR2(40 CHAR) NOT NULL
);

ALTER TABLE tipoproducto ADD CONSTRAINT tipoproducto_pk PRIMARY KEY ( idtipoprod );

CREATE TABLE tipousuario (
    idtipou      NUMBER NOT NULL,
    descripcion  VARCHAR2(50) NOT NULL
);

ALTER TABLE tipousuario ADD CONSTRAINT tipousuario_pk PRIMARY KEY ( idtipou );

CREATE TABLE venta (
    idvent             NUMBER NOT NULL,
    cliente_idcliente  NUMBER NOT NULL,
    fecventa           DATE NOT NULL,
    total              INTEGER NOT NULL,
    estado             NUMBER NOT NULL
);

--  ERROR: No Discriminator Column found in Arc Arc_2 - check constraint cannot be generated

ALTER TABLE venta ADD CONSTRAINT venta_pk PRIMARY KEY ( idvent );

ALTER TABLE boleta
    ADD CONSTRAINT boleta_venta_fk FOREIGN KEY ( venta_idvent )
        REFERENCES venta ( idvent )
            ON DELETE CASCADE;

ALTER TABLE ciudad
    ADD CONSTRAINT ciudad_región_fk FOREIGN KEY ( región_idregion )
        REFERENCES región ( idregion );

ALTER TABLE cliente
    ADD CONSTRAINT cliente_comuna_fk FOREIGN KEY ( comuna_idcomuna )
        REFERENCES comuna ( idcomuna );

ALTER TABLE cliente
    ADD CONSTRAINT cliente_credenciales_fk FOREIGN KEY ( credenciales_idcuenta )
        REFERENCES credenciales ( idcuenta );

ALTER TABLE cliente
    ADD CONSTRAINT cliente_tipousuario_fk FOREIGN KEY ( tipousuario_idtipou )
        REFERENCES tipousuario ( idtipou )
            ON DELETE CASCADE;

ALTER TABLE comuna
    ADD CONSTRAINT comuna_ciudad_fk FOREIGN KEY ( ciudad_idciudad )
        REFERENCES ciudad ( idciudad );

ALTER TABLE detalle
    ADD CONSTRAINT detalle_producto_fk FOREIGN KEY ( producto_idproducto )
        REFERENCES producto ( idproducto )
            ON DELETE CASCADE;

ALTER TABLE detalle
    ADD CONSTRAINT detalle_venta_fk FOREIGN KEY ( venta_idvent )
        REFERENCES venta ( idvent );

ALTER TABLE empleado
    ADD CONSTRAINT empleado_credenciales_fk FOREIGN KEY ( credenciales_idcuenta )
        REFERENCES credenciales ( idcuenta );

ALTER TABLE empleado
    ADD CONSTRAINT empleado_tipousuario_fk FOREIGN KEY ( tipousuario_idtipou )
        REFERENCES tipousuario ( idtipou )
            ON DELETE CASCADE;

ALTER TABLE factura
    ADD CONSTRAINT factura_venta_fk FOREIGN KEY ( venta_idvent )
        REFERENCES venta ( idvent )
            ON DELETE CASCADE;

ALTER TABLE ordencompra
    ADD CONSTRAINT ordencompra_empleado_fk FOREIGN KEY ( empleado_idempleado )
        REFERENCES empleado ( idempleado );

ALTER TABLE ordencompra
    ADD CONSTRAINT ordencompra_producto_fk FOREIGN KEY ( producto_idproducto )
        REFERENCES producto ( idproducto );

ALTER TABLE producto
    ADD CONSTRAINT producto_familiaproducto_fk FOREIGN KEY ( familiaproducto_idfamproducto )
        REFERENCES familiaproducto ( idfamproducto );

ALTER TABLE producto
    ADD CONSTRAINT producto_proveedor_fk FOREIGN KEY ( proveedor_idproveedor,
                                                       proveedor_idrubro )
        REFERENCES proveedor ( idproveedor,
                               rubro_idrubro );

ALTER TABLE producto
    ADD CONSTRAINT producto_tipoproducto_fk FOREIGN KEY ( tipoproducto_idtipoprod )
        REFERENCES tipoproducto ( idtipoprod );

ALTER TABLE proveedor
    ADD CONSTRAINT proveedor_comuna_fk FOREIGN KEY ( comuna_idcomuna )
        REFERENCES comuna ( idcomuna );

ALTER TABLE proveedor
    ADD CONSTRAINT proveedor_credenciales_fk FOREIGN KEY ( credenciales_idcuenta )
        REFERENCES credenciales ( idcuenta );

ALTER TABLE proveedor
    ADD CONSTRAINT proveedor_rubro_fk FOREIGN KEY ( rubro_idrubro )
        REFERENCES rubro ( idrubro );

ALTER TABLE proveedor
    ADD CONSTRAINT proveedor_tipousuario_fk FOREIGN KEY ( tipousuario_idtipou )
        REFERENCES tipousuario ( idtipou )
            ON DELETE CASCADE;

ALTER TABLE venta
    ADD CONSTRAINT venta_cliente_fk FOREIGN KEY ( cliente_idcliente )
        REFERENCES cliente ( idcliente )
            ON DELETE CASCADE;

--  ERROR: No Discriminator Column found in Arc Arc_2 - constraint trigger for Arc cannot be generated 

--  ERROR: No Discriminator Column found in Arc Arc_2 - constraint trigger for Arc cannot be generated



-- Informe de Resumen de Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                            17
-- CREATE INDEX                             0
-- ALTER TABLE                             38
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
