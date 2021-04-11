function validarNombre(){
    var nom = document.getElementById("txtnombre").value;
    var largo = nom.replace(/ /g, "").length;
    if(largo >= 3 && largo <= 80){
        return true;
    }
    else {
        alert("El nombre debe tener entre 3 y 80 caracteres sin incluir espacios en blanco");
        return false;
    }
} 

function validarApellido(){
    var nom = document.getElementById("txtapellido").value;
    var largo = nom.replace(/ /g, "").length;
    if(largo >= 3 && largo <= 80){
        return true;
    } 
    else {
        alert("El apellido debe tener entre 3 y 80 caracteres sin incluir espacios en blanco");
        return false;
    }
}
function validarForRegistro(){ /*metodo que que llamara a los otra validaciones, si hay algo que tenga malo va a enviar un false*/
    var resp;
    resp = validarNombre();
    if (resp == false){
        return false;
    }
    resp = validarApellido();
    if (resp == false){
        return false;
    }
    return true;
}