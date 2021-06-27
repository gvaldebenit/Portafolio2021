/* Funciones de Validacion de Formulario de Producto */

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

// Validar Precio
function validarPrecio(){
    var pre = document.getElementById("txtprecio").value;
    if(pre <= 0){
        alert("El precio debe ser mayor a 0")
        return false;
    }
    else {
        return true;
    }
}

// Validar Stock
function validarStock(){
    var pre = document.getElementById("txtstock").value;
    if(pre < 0){
        alert("El Stock debe ser mayor o igual a 0")
        return false;
    }
    else {
        return true;
    }
}

// Validar Stock Critico
function validarStockCrit(){
    var pre = document.getElementById("txtstockcritico").value;
    if(pre <= 1){
        alert("El Stock Critico debe ser mayor a 1")
        return false;
    }
    else {
        return true;
    }
}

// Validar Descripción
function validarDescripcion(){
    var desc = document.getElementById("txtdescripcion").value;
    var largo = desc.replace(/ /g, "").length;
    if(largo >= 3 && largo <= 200){
        return true;
    }
    else {
        alert("El nombre debe tener entre 3 y 200 caracteres sin incluir espacios en blanco");
        return false;
    }
}

/* Metodo que que llamara a los otra validaciones, si hay algo que tenga malo va a enviar un false*/
function validarForRegistro(){ 
    var resp;
    resp = validarNombre(); // Nombre
    if (resp == false){
        return false;
    }
    resp = validarPrecio(); // Precio
    if (resp == false){
        return false;
    }
    resp = validarStock(); // Stock
    if (resp == false){
        return false;
    }
    resp = validarStockCrit(); // Stock Critico
    if (resp == false){
        return false;
    }
    resp = validarDescripcion(); // Descripcion
    if (resp == false){
        return false;
    }
    return true;
}

    
