let campo_nombre = $('#id_name');
let campo_descripcion = $('#id_descripcion');

let contador_error = 0;

var regex = /^([a-zA-ZÁ,áéíóúnÑ ]){3,80}$/i;

function validar(){
    var nombre = campo_nombre.val();
    var descripcion = campo_descripcion.val();

    $('.error').remove();

    if (!regex.test(nombre)){
        contador_error += 1;
        campo_nombre.parent().removeClass('has-success has-error');
        campo_nombre.parent().addClass('has-error');
        campo_nombre.parent().append('<label class="control-label error" for="inputError"><i class="fa fa-times-circle-o"></i> Nombre del cargo debe ser mayor a 3 caracteres y a-z</label>')
    }

    if (descripcion.length < 5){
        contador_error += 1;
        campo_descripcion.parent().removeClass('has-success has-error');
        campo_descripcion.parent().addClass('has-error');
        campo_descripcion.parent().append('<label class="control-label error" for="inputError"><i class="fa fa-times-circle-o"></i> Descripción debe ser mayor a 5 caracteres y a-z</label>')
    }
}

function validacion() {
    validar();
    if (!contador_error){
        contador_error = 0;
        return true;
    }else{
        contador_error  = 0;
        return false;
    }
}
