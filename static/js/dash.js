const sideLinks = document.querySelectorAll('.sidebar .side-menu li a:not(.logout)');

sideLinks.forEach(item => {
    const li = item.parentElement;
    item.addEventListener('click', () => {
        sideLinks.forEach(i => {
            i.parentElement.classList.remove('active');
        })
        li.classList.add('active');
    })
});

const menuBar = document.querySelector('.content nav .bx.bx-menu');
const sideBar = document.querySelector('.sidebar');

menuBar.addEventListener('click', () => {
    sideBar.classList.toggle('close');
});

window.addEventListener('resize', () => {
    if (window.innerWidth < 768) {
        sideBar.classList.add('close');
    } else {
        sideBar.classList.remove('close');
    }
    if (window.innerWidth > 576) {
        searchBtnIcon.classList.replace('bx-x', 'bx-search');
        searchForm.classList.remove('show');
    }
});

const toggler = document.getElementById('theme-toggle');

toggler.addEventListener('change', function () {
    if (this.checked) {
        document.body.classList.add('dark');
    } else {
        document.body.classList.remove('dark');
    }
});

window.onload = function() {
    const yearSelect = document.getElementById("anoTradiconal");
    const monthSelect = document.getElementById("mesTradiconal");
    const forms = document.querySelectorAll("[id^='formTradiconal']");

    forms.forEach(form => form.style.display = "none");

    function showForm(formId) {
        forms.forEach(form => {
            if (form.id === formId) {
                form.style.display = "block";
            } else {
                form.style.display = "none";
            }
        });
    }

    // NOVEDADES -------------------------------------------------------
    function updateForms(year, month) {
        forms.forEach(form => form.style.display = "none");
        if (year === "2023") {
            monthSelect.innerHTML = '<option value="diciembre">Diciembre</option>';
            showForm("formTradiconalDic2023");
        } else if (year === "2024") {
            monthSelect.innerHTML = '<option value="enero">Enero</option><option value="febrero">Febrero</option>';
            if (month === "enero" || month === "febrero") {
                showForm(`formTradiconal${month.charAt(0).toUpperCase() + month.slice(1)}`);
            } else {
                showForm("formTradiconalEnero"); // Puedes mostrar el de enero por defecto
            }
        }
    }

    yearSelect.addEventListener("change", function() {
        updateForms(yearSelect.value, monthSelect.value);
    });

    monthSelect.addEventListener("change", function() {
        showForm(`formTradiconal${monthSelect.value.charAt(0).toUpperCase() + monthSelect.value.slice(1)}`);
    });

    // Mostrar el formulario correspondiente al cargar la página
    updateForms(yearSelect.value, monthSelect.value);
};


function mesPanalera() {
    var mesSeleccionado = document.getElementById("mesPanalera").value;
    if (mesSeleccionado === "enero") {
        document.getElementById("formPanaleroEnero").style.display = "block";
        document.getElementById("formPanaleroFebrero").style.display = "none";
    } else if (mesSeleccionado === "febrero") {
        document.getElementById("formPanaleroEnero").style.display = "none";
        document.getElementById("formPanaleroFebrero").style.display = "block";
    }
}

// LIQUIDACIONES -------------------------------------------------------