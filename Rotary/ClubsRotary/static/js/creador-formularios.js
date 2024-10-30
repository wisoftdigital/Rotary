document.addEventListener('DOMContentLoaded', function() {
    const formBuilder = document.getElementById('form-builder');
    const draggableItems = document.querySelectorAll('.draggable-item');
    
    draggableItems.forEach(item => {
        item.addEventListener('dragstart', function(e) {
            e.dataTransfer.setData('text/plain', e.target.getAttribute('data-type'));
        });
    });

    formBuilder.addEventListener('dragover', function(e) {
        e.preventDefault();
    });

    formBuilder.addEventListener('drop', function(e) {
        e.preventDefault();
        const type = e.dataTransfer.getData('text');
        addField(type);
    });

    function addField(type) {
        const fieldContainer = document.createElement('div');
        fieldContainer.className = 'field-container';

        let fieldHTML = '';
        let fieldLabel = '';
        let fieldPlaceholder = '';
        
        switch (type) {
            case 'text':
                fieldLabel = 'Texto';
                fieldPlaceholder = 'Introduce texto';
                fieldHTML = '<input type="text" class="form-control">';
                break;
            case 'email':
                fieldLabel = 'Correo Electrónico';
                fieldPlaceholder = 'Introduce correo electrónico';
                fieldHTML = '<input type="email" class="form-control">';
                break;
            case 'number':
                fieldLabel = 'Números';
                fieldPlaceholder = 'Introduce números';
                fieldHTML = '<input type="number" class="form-control">';
                break;
            case 'address':
                fieldLabel = 'Dirección';
                fieldPlaceholder = 'Introduce dirección';
                fieldHTML = '<input type="text" class="form-control">';
                break;
            case 'location':
                fieldLabel = 'Ciudad, Departamento';
                fieldPlaceholder = 'Introduce ciudad y departamento';
                fieldHTML = '<input type="text" class="form-control">';
                break;
            case 'date':
                fieldLabel = 'Fecha';
                fieldPlaceholder = 'Selecciona una fecha';
                fieldHTML = '<input type="date" class="form-control">';
                break;
            case 'textarea':
                fieldLabel = 'Área de Texto';
                fieldPlaceholder = 'Introduce texto largo';
                fieldHTML = '<textarea class="form-control"></textarea>';
                break;
            default:
                fieldLabel = 'Campo';
                fieldPlaceholder = 'Introduce datos';
                fieldHTML = '<input type="text" class="form-control">';
        }

        fieldContainer.innerHTML = `
            <div class="field-controls">
                <input type="text" class="form-control field-name" value="${fieldLabel}" placeholder="Nombre del campo">
                <input type="text" class="form-control field-placeholder" value="${fieldPlaceholder}" placeholder="Placeholder">
            </div>
            ${fieldHTML}
            <div class="field-actions">
                <button class="move-up btn btn-primary btn-sm">Subir</button>
                <button class="move-down btn btn-primary btn-sm">Bajar</button>
                <button class="remove-field btn btn-danger btn-sm">Eliminar</button>
            </div>
        `;
        formBuilder.appendChild(fieldContainer);

        updatePlaceholder();
        addRemoveFieldListener(fieldContainer);
        addMoveListeners(fieldContainer);
    }

    function updatePlaceholder() {
        const fields = formBuilder.querySelectorAll('.field-container');
        if (fields.length > 0) {
            formBuilder.querySelector('.placeholder')?.remove();
        } else {
            formBuilder.innerHTML = '<p class="placeholder">Arrastra y suelta los campos aquí</p>';
        }
    }

    function addRemoveFieldListener(container) {
        container.querySelector('.remove-field').addEventListener('click', function() {
            container.remove();
            updatePlaceholder();
        });
    }

    function addMoveListeners(container) {
        container.querySelector('.move-up').addEventListener('click', function() {
            const prev = container.previousElementSibling;
            if (prev) {
                formBuilder.insertBefore(container, prev);
            }
        });

        container.querySelector('.move-down').addEventListener('click', function() {
            const next = container.nextElementSibling;
            if (next) {
                formBuilder.insertBefore(next, container);
            }
        });
    }
});