// Obtén referencias a los elementos HTML que necesitas
const image = document.getElementById('image');
const imageName = document.getElementById('imageName');
const resultDiv = document.getElementById('resultado');
const fileInput = document.querySelector('input[name="imagen"]');
const clearButton = document.querySelector('.btn-danger');

// Función para limpiar la imagen y el nombre
function clearDressImageAndName() {
    image.src = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSarae41EWHPQNxccyPZyWK4iHQAZPsnm6ptpvgitXplQ&s";
    imageName.textContent = '';
    resultDiv.textContent = '';
    fileInput.value = ''; // Restablecer el valor del input de archivo
}

// Escuchar el evento 'submit' del formulario y enviar la imagen al servidor
document.querySelector('form').addEventListener('submit', function (e) {
    e.preventDefault(); // Evitar que el formulario se envíe normalmente

    // Crear un objeto FormData para enviar la imagen al servidor
    const formData = new FormData();
    formData.append('imagen', fileInput.files[0]);

    fetch('/guardar-imagen', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        // Manejar la respuesta (puede mostrar la URL de la imagen si lo deseas)
        const imageUrl = data.url;
        spectogramConvert();
    })
    .catch(error => {
        console.error(error);
    });
});

// Función para cargar el espectograma y mostrar la imagen
function spectogramConvert() {
    fetch('/procesar-imagen', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        const dressName = data.dressName;
        if (dressName === 'Desconocido') {
            image.src = "https://cdn.pixabay.com/photo/2013/07/12/16/24/alphabet-150831_640.png";
        } else {
            // Hacer una solicitud para obtener la URL de la imagen relacionada con el nombre del vestido
            fetch('/obtener-imagen?nombre=' + dressName, {
                method: 'GET',
            })
            .then(response => response.json())
            .then(data => {
                const imageUrl = data.url;
                if (imageUrl) {
                    image.src = imageUrl;
                } else {
                    // Si no se encuentra una imagen, muestra una imagen predeterminada
                    image.src = "https://cdn.pixabay.com/photo/2013/07/12/16/24/alphabet-150831_640.png";
                }
            })
            .catch(error => {
                console.error(error);
            });
        }
        imageName.textContent = dressName;
    })
    .catch(error => {
        console.error(error);
    });
}

// Escuchar el evento 'click' del botón para limpiar imagen y nombre
clearButton.addEventListener('click', clearDressImageAndName);
