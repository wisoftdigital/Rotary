document.addEventListener('DOMContentLoaded', function() {
    var clickCount = 0;
    var calendar1, calendar2, calendar3;
    var currentEvent;

    // Inicializar elementos arrastrables
    var containerEl = document.getElementById('external-events');
    var Draggable = FullCalendar.Draggable;
    new Draggable(containerEl, {
        itemSelector: '.fc-event',
        eventData: function(eventEl) {
            return {
                title: eventEl.innerText.trim(),
                duration: eventEl.getAttribute('data-duration') || '01:00',
                backgroundColor: eventEl.getAttribute('data-color') || '#3788d8'
            };
        }
    });

    // Función para agregar una nueva tarea
    function addTask(event) {
        const taskData = {
            title: event.title,
            start: event.start.toISOString(),
            end: event.end ? event.end.toISOString() : event.start.toISOString(),
            color: event.backgroundColor
        };

        fetch('/add_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData),
        })
        .then(response => response.json())
        .then(data => {
            event.setProp('id', data.id); // Establecer el ID del evento
            event.remove(); // Eliminar el evento del calendario para evitar duplicados
            // Refrescar los calendarios para reflejar los cambios
            calendar1.refetchEvents();
            calendar2.refetchEvents();
            calendar3.refetchEvents();
            alert('Tarea añadida con éxito!');
        })
        .catch(error => {
            console.error('Error al agregar la tarea:', error);
            event.remove(); // Eliminar el evento si hay un error
            alert('Error al agregar la tarea.');
        });
    }

    // Función para actualizar una tarea existente
    function updateTask(event) {
        const taskData = {
            title: event.title,
            start: event.start.toISOString(),
            end: event.end ? event.end.toISOString() : event.start.toISOString(),
            color: event.backgroundColor
        };

        fetch(`/update_task/${event.id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData),
        })
        .then(response => response.json())
        .then(() => {
            // Refrescar los calendarios para reflejar los cambios
            calendar1.refetchEvents();
            calendar2.refetchEvents();
            calendar3.refetchEvents();
            alert('Tarea actualizada con éxito!');
        })
        .catch(error => {
            console.error('Error al actualizar la tarea:', error);
            alert('Error al actualizar la tarea.');
        });
    }

    // Función para eliminar una tarea
    function deleteTask(eventId) {
        fetch(`/delete_task/${eventId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(() => {
            // Refrescar los calendarios
            calendar1.refetchEvents();
            calendar2.refetchEvents();
            calendar3.refetchEvents();
            alert('Tarea eliminada con éxito!');
        })
        .catch(error => {
            console.error('Error al eliminar la tarea:', error);
            alert('Error al eliminar la tarea.');
        });
    }

    // Configuración común para los calendarios 2 y 3
    var commonConfig = {
        initialView: 'timeGridDay',
        editable: true,
        droppable: true, // Permitir arrastrar elementos externos
        eventDurationEditable: true,
        eventResizableFromStart: true,
        events: '/get_tasks',
        locale: 'es', // Aquí especificas que el calendario debe usar el idioma español
        eventReceive: function(info) {
            // Si el evento no tiene ID, es una nueva tarea
            if (!info.event.id) {
                addTask(info.event);
            } else {
                updateTask(info.event);
            }
            // No eliminar el evento de inmediato, primero actualizar los calendarios
            setTimeout(() => {
                info.event.remove(); // Eliminar después de un breve intervalo para asegurar la propagación
                calendar1.refetchEvents();
                calendar2.refetchEvents();
                calendar3.refetchEvents();
            }, 100); // Intervalo breve para garantizar la actualización de los eventos
        },
        eventDrop: function(info) {
            updateTask(info.event);
        },
        eventResize: function(info) {
            updateTask(info.event);
        },
        eventClick: function(info) {
            currentEvent = info.event;
            document.getElementById('taskTitle').value = info.event.title;
            document.getElementById('taskStart').value = info.event.start.toISOString().slice(0,16);
            document.getElementById('taskEnd').value = info.event.end ? info.event.end.toISOString().slice(0,16) : info.event.start.toISOString().slice(0,16);
            openModal();
        }
    };

    // Inicialización de los calendarios
    var calendarEl1 = document.getElementById('calendar1');
    calendar1 = new FullCalendar.Calendar(calendarEl1, {
        initialView: 'dayGridMonth',
        editable: true,
        events: '/get_tasks',
        locale: 'es', // Aquí especificas que el calendario debe usar el idioma español
        dateClick: function(info) {
            clickCount++;
            if (clickCount === 1) {
                calendar2.gotoDate(info.date);
            } else if (clickCount === 2) {
                calendar3.gotoDate(info.date);
                clickCount = 0;
            }
        }
    });

    var calendarEl2 = document.getElementById('calendar2');
    calendar2 = new FullCalendar.Calendar(calendarEl2, commonConfig);

    var calendarEl3 = document.getElementById('calendar3');
    calendar3 = new FullCalendar.Calendar(calendarEl3, commonConfig);

    calendar1.render();
    calendar2.render();
    calendar3.render();

    // Manejar el envío del formulario en el modal
    document.getElementById('taskForm').addEventListener('submit', function(event) {
        event.preventDefault();

        currentEvent.setProp('title', document.getElementById('taskTitle').value);
        currentEvent.setStart(document.getElementById('taskStart').value);
        currentEvent.setEnd(document.getElementById('taskEnd').value);

        updateTask(currentEvent);
        closeModal();
    });

    // Manejar el clic en el botón de eliminar
    document.getElementById('deleteButton').addEventListener('click', function() {
        if (currentEvent) {
            deleteTask(currentEvent.id);
            currentEvent.remove();
            closeModal();
        }
    });
});

// Funciones para abrir y cerrar el modal
function openModal() {
    document.getElementById('taskModal').classList.add('show');
    document.getElementById('taskModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('taskModal').classList.remove('show');
    document.getElementById('taskModal').style.display = 'none';
}

// Cierra el modal al hacer clic fuera del contenido
document.getElementById('taskModal').addEventListener('click', function(event) {
    if (event.target === this) {
        closeModal();
    }
});
