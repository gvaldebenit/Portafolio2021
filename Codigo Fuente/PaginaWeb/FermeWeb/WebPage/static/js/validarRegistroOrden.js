/* Funciones de Validacion de Formulario de Orden de Compra */

// Validar Precio
function validarPrecio(){
    var pre = document.getElementById("txtValor").value;
    if(pre <= 0){
        alert("El Valor Unitario debe ser mayor a 0")
        return false;
    }
    else {
        return true;
    }
}

// Validar Cantidad
function validarCantidad(){
    var pre = document.getElementById("txtCantidad").value;
    if(pre <= 0){
        alert("El Stock debe ser mayor a 0")
        return false;
    }
    else {
        return true;
    }
}

// Validar Valor Total
function validarTotal(){
    var pre = document.getElementById("txtTotal").value;
    if(pre == null || pre == ""){
        alert("Se debe Rellenar el Valor Unitario y la Cantidad para calcular el Total")
        return false;
    }
    else {
        return true;
    }
}

// Validar Descripción
function validarDescripcion(){
    var desc = document.getElementById("txtDescripcion").value;
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
    resp = validarPrecio(); // Precio
    if (resp == false){
        return false;
    }
    resp = validarCantidad(); // Stock
    if (resp == false){
        return false;
    }
    resp = validarTotal(); // Total
    if (resp == false){
        return false;
    }
    resp = validarDescripcion(); // Descripcion
    if (resp == false){
        return false;
    }
    return true;
}

    
