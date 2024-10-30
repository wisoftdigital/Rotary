document.addEventListener('DOMContentLoaded', function () {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    const navLinks = document.querySelectorAll('.nav-list a');
    const profileBtn = document.getElementById('profile-btn');
    const profileMenu = document.querySelector('.profile-menu');

    // Manejo del cambio de tema
    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark');
        const icon = themeToggle.querySelector('i');
        if (body.classList.contains('dark')) {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        } else {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        }
    });

    // Manejo de los enlaces de navegación
    navLinks.forEach(link => {
        link.addEventListener('click', function () {
            navLinks.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Manejo del menú de perfil
    profileBtn.addEventListener('click', function () {
        profileMenu.classList.toggle('hidden');
    });

    // Cierra el menú si se hace clic fuera de él
    document.addEventListener('click', function (event) {
        if (!profileBtn.contains(event.target) && !profileMenu.contains(event.target)) {
            profileMenu.classList.add('hidden');
        }
    });
});


function openTab(tabName, element) {
    var i, tabcontent, sidebarLinks;

    // Ocultar todo el contenido de las pestañas
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].classList.remove("active");
    }

    // Eliminar la clase "activo" de todos los enlaces de la barra lateral
    sidebarLinks = document.getElementsByClassName("enlace");
    for (i = 0; i < sidebarLinks.length; i++) {
        sidebarLinks[i].classList.remove("activo");
    }

    // Mostrar la pestaña actual y agregar la clase "activo" al enlace que abrió la pestaña
    document.getElementById(tabName).classList.add("active");
    element.classList.add("activo");
}


document.addEventListener('DOMContentLoaded', function () {
    inicializarGraficaAmbiental();
    inicializarGraficaPagos();
});

function webdomotycort() {
    var url = 'https://yomar009.github.io/domyclip/';
    window.open(url, '_blank');
}

document.querySelectorAll('.whatsapp_link').forEach(function(element) {
    element.addEventListener('click', function(event) {
        event.preventDefault(); // Evita que el enlace funcione normalmente
        
        // Obtén el número de teléfono y elimina los caracteres no numéricos
        var numeroCelular = this.textContent.replace(/\D/g, '');
        
        // Abre WhatsApp con el número de teléfono
        window.open('https://wa.me/57' + numeroCelular);
    });
});

// Cierra el modal si el usuario hace clic fuera de él
window.onclick = function(event) {
    var modals = document.querySelectorAll('.modal');
    modals.forEach(function(modal) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });
}

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('open');
}
