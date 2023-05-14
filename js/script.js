const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input');

const expresiones = {
	nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/,
	email: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
	tel: /^\d{7,14}$/
}

const campos = {
    nombre: false,
    email: false,
    tel: false
}

const validarCampo = (expresion, input, campo) => {
    if(expresion.test(input.value)){
        document.getElementById(`${campo}`).classList.remove('grupo_error');
        document.getElementById(`${campo}`).classList.add('grupo_exito');
        document.querySelector(`#${campo} i`).classList.add('fa-circle-check');
        document.querySelector(`#${campo} i`).classList.remove('fa-circle-xmark');
        document.querySelector(`#${campo} .msj_error`).classList.remove('msj_error-activo');
        campos[campo] = true
    } else{
        document.getElementById(`${campo}`).classList.add('grupo_error');
        document.getElementById(`${campo}`).classList.remove('grupo_exito');
        document.querySelector(`#${campo} i`).classList.add('fa-circle-xmark');
        document.querySelector(`#${campo} i`).classList.remove('fa-circle-check');
        document.querySelector(`#${campo} .msj_error`).classList.add('msj_error-activo')
        campos[campo] = false
    }
}

const validarFormulario = (e) => {
    switch (e.target.name) {
        case "nombre":
            validarCampo(expresiones.nombre, e.target, 'nombre')
        break;
        case "email":
            validarCampo(expresiones.email, e.target, 'email')
        break;
        case "tel":
            validarCampo(expresiones.tel, e.target, 'tel')
        break;
    }
}

inputs.forEach((input) => {
    input.addEventListener('keyup', validarFormulario)
    input.addEventListener('blur', validarFormulario)
})

formulario.addEventListener('submit', (e) => {
    e.preventDefault();
    if(campos.nombre && campos.email && campos.tel){
        formulario.reset();
        document.getElementById('exito_formulario').classList.add('exito_formulario-activo');
        setTimeout(() => document.getElementById('exito_formulario').classList.remove('exito_formulario-activo'), 4000);
        document.querySelectorAll('.grupo_exito').forEach((icono) => {
            icono.classList.remove('grupo_exito')
        })
    } else {
        document.getElementById('error_formulario').classList.add('error_formulario-activo')
    }
})