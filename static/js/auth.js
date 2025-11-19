// URLs de la API
const API_BASE = '/auth';
const LOGIN_URL = `${API_BASE}/login`;
const REGISTER_URL = `${API_BASE}/register`;

// Mostrar alertas
function showAlert(message, type = 'error') {
    const container = document.getElementById('alert-container');
    const alert = document.createElement('div');
    alert.className = `alert ${type}`;
    alert.textContent = message;
    
    container.appendChild(alert);
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

// Toggle password visibility
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
    input.setAttribute('type', type);
}

// Manejar login
async function handleLogin(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const loginText = document.getElementById('login-text');
    const spinner = document.getElementById('login-spinner');
    
    // Obtener datos del formulario
    const formData = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };
    
    // Validación básica
    if (!formData.email || !formData.password) {
        showAlert('Por favor completa todos los campos');
        return;
    }
    
    // Mostrar loading
    loginText.textContent = 'Iniciando sesión...';
    spinner.classList.remove('hidden');
    submitBtn.disabled = true;
    
    try {
        const response = await fetch(LOGIN_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Guardar token en localStorage
            localStorage.setItem('auth_token', data.token);
            localStorage.setItem('user_data', JSON.stringify(data.user));
            
            showAlert('¡Login exitoso! Redirigiendo...', 'success');
            
            // Redirigir después de 1 segundo
            setTimeout(() => {
                window.location.href = '/dashboard'; // Cambiar por tu ruta
            }, 1000);
            
        } else {
            showAlert(data.error || 'Error en el login');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error de conexión. Intenta nuevamente.');
    } finally {
        // Restaurar botón
        loginText.textContent = 'Iniciar Sesión';
        spinner.classList.add('hidden');
        submitBtn.disabled = false;
    }
}

// Inicializar eventos cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // Verificar si ya está autenticado
    const token = localStorage.getItem('auth_token');
    if (token) {
        // Redirigir si ya está logueado
        window.location.href = '/dashboard';
    }
});