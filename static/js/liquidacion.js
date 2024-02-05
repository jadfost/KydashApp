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

document.getElementById('anocanal').addEventListener('change', function () {
    const selectedYear = this.value;

    // Fetch months for the selected year
    fetch(`/liquidacion/get_months?ano=${selectedYear}`)
        .then(response => response.json())
        .then(data => {
            // Update the months select element
            const mesSelect = document.getElementById('mescanal');
            mesSelect.innerHTML = ""; // Clear existing options
            data.forEach(month => {
                const option = document.createElement('option');
                option.value = month;
                option.text = month;
                mesSelect.appendChild(option);
            });
        });

    // Fetch channels for the selected year
    fetch(`/liquidacion/get_channels?ano=${selectedYear}`)
        .then(response => response.json())
        .then(data => {
            // Update the channels select element
            const canalSelect = document.getElementById('medicioncanal');
            canalSelect.innerHTML = ""; // Clear existing options
            data.forEach(channel => {
                const option = document.createElement('option');
                option.value = channel;
                option.text = channel;
                canalSelect.appendChild(option);
            });
        });

    // Fetch executives for the selected year
    fetch(`/liquidacion/get_executives?ano=${selectedYear}`)
        .then(response => response.json())
        .then(data => {
            // Update the executives select element
            const ejecutivoSelect = document.getElementById('ejecutivo');
            ejecutivoSelect.innerHTML = ""; // Clear existing options
            data.forEach(executive => {
                const option = document.createElement('option');
                option.value = executive;
                option.text = executive;
                ejecutivoSelect.appendChild(option);
            });
        });
});

// Add event listener for the change event on medicioncanal
document.getElementById('medicioncanal').addEventListener('change', function () {
    const selectedYear = document.getElementById('anocanal').value;

    // Fetch executives based on the selected canal and year
    const selectedCanal = this.value;
    fetch(`/liquidacion/get_executives?ano=${selectedYear}&canal=${selectedCanal}`)
        .then(response => response.json())
        .then(data => {
            // Update the executives select element
            const ejecutivoSelect = document.getElementById('ejecutivo');
            ejecutivoSelect.innerHTML = ""; // Clear existing options
            data.forEach(executive => {
                const option = document.createElement('option');
                option.value = executive;
                option.text = executive;
                ejecutivoSelect.appendChild(option);
            });
        });
});

document.getElementById('applyFiltersBtn').addEventListener('click', function () {
    showLoader();

    const ano = document.getElementById('anocanal').value;
    const mes = document.getElementById('mescanal').value;
    const canalMedicion = document.getElementById('medicioncanal').value;
    const ejecutivo = document.getElementById('ejecutivo').value;

    // Build URL with non-empty parameters only
    const params = new URLSearchParams();
    if (ano) params.set('ano', ano);
    if (mes) params.set('mes', mes);
    if (canalMedicion) params.set('canal_medicion', canalMedicion);
    if (ejecutivo) params.set('ejecutivo', ejecutivo);

    const url = `?${params.toString()}`;
    window.location.href = url;
});

/// Limpiar Filtros
document.getElementById('clearFiltersBtn').addEventListener('click', function () {
    // Clear the selected options in the dropdowns
    document.getElementById('anocanal').value = "";
    document.getElementById('mescanal').value = "";
    document.getElementById('medicioncanal').value = "";
    document.getElementById('ejecutivo').value = "";

    // Trigger the click event on applyFiltersBtn to reload the page without filters
    document.getElementById('applyFiltersBtn').click();
});

