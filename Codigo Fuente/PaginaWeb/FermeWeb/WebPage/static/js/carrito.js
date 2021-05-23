/*class Item{
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
    }

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

const items = document.getElementById


document.addEventListener('DOMContentLoaded',() =>{
    fetchData()
})

const fetchData= async () =>{
    try {
        const res = await fetch('http://127.0.0.1:8000/api/productos/?format=json')
        const data = await res.json()
        console.log(data)
    } catch (error) {
        console.log(error)
    }
}
*/

//add to cart

$(function(){
    $(document).on('click',"#addToCartBtn",function(){
        var _vm=$(this);
        //var _index=_vm.attr('data-index')
        var _cant=$("#prodCant").val();
        var _prodId=$(".prodId").val();
        var _imagen=$(".imagen").val();
        var _nomProd=$(".nomProd").val();
        var _precio=$(".precio").val();
    
        //console.log(_cant,_prodId,_nomProd,_precio,_vm);

        $.ajax({
            url:'/add-to-cart',
            data:{
                'prodId':_prodId,
                'imagen':_imagen,
                'cant':_cant,
                'nomProd':_nomProd,
                'precio':_precio
            },
            dataType:'json',
            beforeSend:function(){
                _vm.attr('disabled',true);
            },
            success:function(res){
                $(".cart-list").text(res.totalitems);
                _vm.attr('disabled',false);
            } 
        });
    });

    //delete

    $(document).on('click','.delete-item',function(){
        var _pId=$(this).attr('data-item');
        var _vm=$(this);
        //Ajax
        $.ajax({
            url:'/delete-from-cart',
            data:{
                'prodId':_pId,
            },
            dataType:'json',
            beforeSend:function(){
                _vm.attr('disabled',true);
            },
            success:function(res){
                $(".cart-list").text(res.totalitems);
                _vm.attr('disabled',false);
                $("#cartList").html(res.data);
            } 
        });
    });

    // Update item from cart
	$(document).on('click','.update-item',function(){
        var _pId=$(this).attr('data-item');
        var _pCant=$(".cant"+_pId).val();
        var _vm=$(this);
        //Ajax
        $.ajax({
            url:'/update-cart',
            data:{
                'prodId':_pId,
                'cant':_pCant
            },
            dataType:'json',
            beforeSend:function(){
                _vm.attr('disabled',true);
            },
            success:function(res){
                //$(".cart-list").text(res.totalitems);
                _vm.attr('disabled',false);
                $("#cartList").html(res.data);
            } 
        });
    });
});


