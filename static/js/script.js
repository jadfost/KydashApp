const signinBtn = document.querySelector('.signinBtn');
const signupBtn = document.querySelector('.signupBtn');
const formBx = document.querySelector('.formBx');
const body = document.querySelector('body')

signupBtn.onclick = function () {
    formBx.classList.add('active')
    body.classList.add('active')
}

signinBtn.onclick = function () {
    formBx.classList.remove('active')
    body.classList.remove('active')
}

// Seleccionar todos los elementos con la clase 'alert' y ocultarlos después de un tiempo específico
setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.style.display = 'none';
    });
}, 3000); // Cambia este valor (en milisegundos) según el tiempo que desees que permanezcan los mensajes antes de desaparecer

document.addEventListener("DOMContentLoaded", function() {
    var jadfostElement = document.getElementById("jadfost");
    jadfostElement.addEventListener("click", function() {
    window.location.href = 'https://github.com/jadfost';
    });
});

document.addEventListener("DOMContentLoaded", function() {
    var jadfostElement = document.getElementById("jadfost2");
    jadfostElement.addEventListener("click", function() {
    window.location.href = 'https://github.com/jadfost';
    });
});