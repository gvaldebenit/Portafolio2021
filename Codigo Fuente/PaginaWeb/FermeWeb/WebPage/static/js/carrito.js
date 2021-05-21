class Item{
    constructor(id,imagen,nombre,precio,cant){
        this.id = id;
        this.imagen = imagen;
        this.nombre = nombre;
        this.precio = precio;
        this.cant = cant;
    }
}

class Carrito{
    carrito = [];
    
    /*constructor(carrito){
        this.carrito = carrito;
    }*/

    agregarProducto(item){
        const found = carrito.some(carItem => carItem.id === item.id);
        if (!found){ 
            carrito.push(item);
        }else{
            const iMod = carrito.find(carItem => carItem.id === item.id);
            this.modificar(item,iMod.cant + 1);
        }
    }

    eliminarProducto(item){
        carrito.splice(carrito.indexOf(item), 1);
    }

    modificar(item, cantidad){
        var mod= carrito[carrito.indexOf(item)];
        mod.cant=cantidad;
    }
}

