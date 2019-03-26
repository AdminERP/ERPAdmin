let campo_nombre = $('#id_first_name');
let campo_apellido = $('#id_last_name');
let campo_cedula = $('#id_cedula');
let campo_correo = $('#id_email');
let campo_telefono = $('#id_telefono');
let campo_direccion = $('#id_direccion');

let contador_error = 0;

var regex = /^([a-zA-ZÁ,áéíóúñÑ ]){3,20}$/i;
var regex_cedula = /^([0-9]){8,11}$/;
var regex_correo = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
var regex_telefono = /^([0-9]){7,11}$/;

function validarNombres(){
    var nombre = campo_nombre.val();
    var apellido = campo_apellido.val();
    var cedula = campo_cedula.val();
    var correo = campo_correo.val();
    var telefono = campo_telefono.val();
    var direccion = campo_direccion.val();

    $('.error').remove();

    if (!regex.test(nombre)){
        contador_error += 1;
        campo_nombre.parent().removeClass('has-success has-error');
        campo_nombre.parent().addClass('has-error');
        campo_nombre.parent().append('<label class="control-label error" for="inputError"><i class="fa fa-times-circle-o"></i> Nombre debe ser mayor a 3 caracteres y a-z</label>')
    }

    if (!regex.test(apellido)){
        contador_error += 1;
        campo_apellido.parent().removeClass('has-success has-error');
        campo_apellido.parent().addClass('has-error');
        campo_apellido.parent().append('<label class="control-label error" for="inputError"><i class="fa fa-times-circle-o"></i> Apellido debe ser mayor a 3 caracteres y a-z</label>')
    }

    if(!regex_cedula.test(cedula)){
        contador_error += 1;
        campo_cedula.parent().removeClass('has-success has-error');
        campo_cedula.parent().addClass('has-error');
        campo_cedula.parent().append('<label class="control-label error" for="inputError"><i class="fa fa-times-circle-o"></i> Cédula debe ser numérica entre 8 y 11 números</label>')
    }

    if (!regex_correo.test(correo)){
        contador_error += 1;
        campo_correo.parent().removeClass('has-success has-error');
        campo_correo.parent().addClass('has-error');
        campo_correo.parent().append('<label class="control-label error" for="inputError"><i class="fa fa-times-circle-o"></i> Correo inválido</label>')
    }

    if (!regex_telefono.test(telefono)){
        contador_error += 1;
        campo_telefono.parent().removeClass('has-success has-error');
        campo_telefono.parent().addClass('has-error');
        campo_telefono.parent().append('<label class="control-label error" for="inputError"><i class="fa fa-times-circle-o"></i> Teléfono deber ser entre 7 y 11 números</label>')
    }
}

function validacion() {
    validarNombres();
    if (!contador_error){
        contador_error = 0;
        return true;
    }else{
        contador_error  = 0;
        return false;
    }
}

