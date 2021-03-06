/* Funciones de Validacion de Formulario de Cliente y Proveedor */

/* Validar Nombre Registro */
function validarNombre(){
    var nom = document.getElementById("txtnombre").value;
    var largo = nom.replace(/ /g, "").length;
    if(largo >= 3 && largo <= 30){
        return true;
    }
    else {
        alert("El nombre debe tener entre 3 y 30 caracteres sin incluir espacios en blanco");
        return false;
    }
} 
 
/* Validar Apellido Paterno */
function validarApaterno(){
    var nom = document.getElementById("txtapaterno").value;
    var largo = nom.replace(/ /g, "").length;
    if(largo >= 3 && largo <= 20){
        return true;
    } 
    else {
        alert("El apellido paterno debe tener entre 3 y 20 caracteres sin incluir espacios en blanco");
        return false;
    }
}

/* Validar Apellido Materno */
function validarAmaterno(){
    var nom = document.getElementById("txtamaterno").value;
    var largo = nom.replace(/ /g, "").length;
    if(largo >= 3 && largo <= 20){
        return true;
    } 
    else {
        alert("El apellido materno debe tener entre 3 y 20 caracteres sin incluir espacios en blanco");
        return false;
    }
}

/* Validar Rut */
function validarRut(){
    var rut = document.getElementById("txtrut").value;
    var largo = rut.replace(/ /g, "").length;
    if(largo == 9 || largo == 10){
        // Funcion de Verificación de Rut en Internet
        rut = rut.replace('-','');
        cuerpo = rut.slice(0,-1);
        dv = rut.slice(-1).toUpperCase();
        rut.value = cuerpo + '-'+ dv;
        //Calcular DV
        suma = 0;
        multiplo = 2;
        for(i=1;i<=cuerpo.length;i++) {
            // Obtener su Producto con el Múltiplo Correspondiente
            index = multiplo * valor.charAt(cuerpo.length - i);
            // Sumar al Contador General
            suma = suma + index;
            // Consolidar Múltiplo dentro del rango [2,7]
            if(multiplo < 7) { multiplo = multiplo + 1; } else { multiplo = 2; }
        }    
        // Calcular Dígito Verificador en base al Módulo 11
        dvEsperado = 11 - (suma % 11);
        // Casos Especiales (0 y K)
        dv = (dv == 'K')?10:dv;
        dv = (dv == 0)?11:dv;
        if(dvEsperado != dv) {
            alert("Rut Invalido");
            return false; 
        }
        else {
            return true;
        }
    }
    else {
        alert("El Rut debe tener entre 9 y 10 caracteres sin incluir espacios en blanco");
        return false;
    }
}

// Validar Direccion
function validarDireccion(){
    var nom = document.getElementById("txtdireccion").value;
    var largo = nom.replace(/ /g, "").length;
    if(largo >= 5 && largo <= 40){
        return true;
    } 
    else {
        alert("La direccion debe tener entre 5 y 40 caracteres sin incluir espacios en blanco");
        return false;
    }
}

// Validar Telefono
function validarTelefono(){
    var nom = document.getElementById("txtnumero").value;
    var largo = nom.replace(/ /g, "").length;
    if(largo == 9){
        return /^\d+$/.test(nom);
    } 
    else {
        alert("El telefono debe ser numérico y de 9 digitos");
        return false;
    }
}

// Validar Representante
function validarRepresentante(){
    var rep = document.getElementById("txtrepresentante");
    if(rep){ //Valida si existe o no, para usar en dos paginas
        var nom = rep.value;
        var largo = nom.replace(/ /g, "").length;
        if(largo >= 5 && largo <= 50){
            return true;
        } 
        else {
            alert("El Representante debe tener entre 5 y 50 caracteres sin incluir espacios en blanco");
            return false;
        }
    }
    else{
        return true;
    }
    
}

// Validar Email
function validarMail(){
    var nom = document.getElementById("txtcorreo").value;
    var largo = nom.replace(/ /g, "").length;
    if(largo >= 5 && largo <= 30){
        return true;
    } 
    else {
        alert("El Correo debe tener entre 5 y 30 caracteres sin incluir espacios en blanco");
        return false;
    }
}

/* Metodo que que llamara a los otra validaciones, si hay algo que tenga malo va a enviar un false*/
function validarForRegistro(){ 
    var resp;
    resp = validarRut();
    if (resp == false){
        return false;
    }
    resp = validarNombre();
    if (resp == false){
        return false;
    }
    resp = validarApaterno();
    if (resp == false){
        return false;
    }
    resp = validarAmaterno();
    if (resp == false){
        return false;
    }
    resp = validarDireccion();
    if (resp == false){
        return false;
    }
    resp = validarTelefono();
    if (resp == false){
        return false;
    }
    resp = validarRepresentante();
    if (resp == false){
        return false;
    }
    resp = validarMail();
    if (resp == false){
        return false;
    }
    return true;
}

    
