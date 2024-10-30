// Asegúrate de que el código JS se ejecute después de que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Obtener elementos del DOM
    const modal = document.getElementById('modal');
    const openModalBtn = document.getElementById('openModal');
    const closeModalBtn = document.getElementById('closeModal');
    const saveBtn = document.getElementById('saveBtn');
    const deleteBtn = document.getElementById('deleteBtn');
    const activateBtn = document.getElementById('activateBtn');
    const deactivateBtn = document.getElementById('deactivateBtn');

    // Abrir el modal
    openModalBtn.addEventListener('click', () => {
        modal.style.display = 'block';
    });

    // Cerrar el modal
    closeModalBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Cerrar modal al hacer clic fuera de él
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Funciones de botones
    saveBtn.addEventListener('click', () => {
        alert('Datos guardados');
    });

    deleteBtn.addEventListener('click', () => {
        alert('Datos eliminados');
    });

    activateBtn.addEventListener('click', () => {
        document.getElementById('inputCheckbox').checked = true;
        alert('Activado');
    });

    deactivateBtn.addEventListener('click', () => {
        document.getElementById('inputCheckbox').checked = false;
        alert('Desactivado');
    });
});
