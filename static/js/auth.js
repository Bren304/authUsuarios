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

// Inicialización mejorada
document.addEventListener('DOMContentLoaded', function() {
    console.log('Aplicación inicializando...');
    
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    
    if (loginForm) {
        console.log('Formulario de login encontrado');
        loginForm.addEventListener('submit', handleLogin);
    }
    
    if (registerForm) {
        console.log('Formulario de registro encontrado');
        registerForm.addEventListener('submit', handleRegister);
    }
    
    // Verificar autenticación en páginas protegidas
    if (window.location.pathname === '/dashboard') {
        console.log('Página dashboard detectada');
        
        const token = localStorage.getItem('auth_token');
        if (!token) {
            console.log('No hay token, redirigiendo a login');
            window.location.href = '/login';
            return;
        }
        
        // Verificar token con el backend
        verifyTokenWithBackend(token)
            .then(isValid => {
                if (isValid) {
                    console.log('Token válido, cargando dashboard');
                    loadUserData();
                } else {
                    console.log('Token inválido, redirigiendo');
                    logout();
                }
            })
            .catch(error => {
                console.log('Error verificando token:', error);
                logout();
            });
    }
    
    // Redirigir desde login/register si ya está autenticado
    if (window.location.pathname === '/login' || window.location.pathname === '/register') {
        const token = localStorage.getItem('auth_token');
        if (token) {
            console.log('Ya autenticado, redirigiendo a dashboard');
            window.location.href = '/dashboard';
        }
    }
});

// Verificar token con backend
async function verifyTokenWithBackend(token) {
    try {
        const response = await fetch('/auth/verify-token', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            return data.valid === true;
        }
        return false;
    } catch (error) {
        console.log('❌ Error en verificación:', error);
        return false;
    }
}

// Dashboard Functions
function loadUserData() {
    const userData = JSON.parse(localStorage.getItem('user_data') || '{}');
    
    // Actualizar UI con datos del usuario
    document.getElementById('user-welcome').textContent += userData.username || 'Usuario';
    document.getElementById('user-username').textContent = userData.username || '-';
    document.getElementById('user-email').textContent = userData.email || '-';
    document.getElementById('user-role').textContent = userData.role || '-';
    document.getElementById('user-dni').textContent = userData.dni || '-';
}

function viewProfile() {
    const userData = JSON.parse(localStorage.getItem('user_data') || '{}');
    
    // Llenar modal con datos del perfil
    document.getElementById('profile-id').textContent = userData.id || '-';
    document.getElementById('profile-username').textContent = userData.username || '-';
    document.getElementById('profile-email').textContent = userData.email || '-';
    document.getElementById('profile-dni').textContent = userData.dni || '-';
    document.getElementById('profile-phone').textContent = userData.phone || 'No especificado';
    document.getElementById('profile-role').textContent = userData.role || '-';
    
    // Mostrar modal
    document.getElementById('profileModal').classList.remove('hidden');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.add('hidden');
}

function manageUsers() {
    showAlert('Funcionalidad de gestión de usuarios en desarrollo', 'success');
}

function viewSettings() {
    showAlert('Configuración en desarrollo', 'success');
}

// En auth.js, mejorar la función logout
async function logout() {
    try {
        // Opcional: llamar al endpoint de logout del backend
        await fetch('/auth/logout', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
                'Content-Type': 'application/json'
            }
        });
    } catch (error) {
        console.log('Error en logout:', error);
    } finally {
        // Siempre limpiar el frontend
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_data');
        
        showAlert('Sesión cerrada correctamente', 'success');
        
        setTimeout(() => {
            window.location.href = '/login';
        }, 1000);
    }
}

// Manejar registro
async function handleRegister(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const registerText = document.getElementById('register-text');
    const spinner = document.getElementById('register-spinner');
    
    // Obtener datos del formulario
    const formData = {
        dni: document.getElementById('dni').value,
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        phone: document.getElementById('phone').value || null
    };
    
    const confirmPassword = document.getElementById('confirm_password').value;
    
    // Validaciones
    if (formData.password !== confirmPassword) {
        showAlert('Las contraseñas no coinciden');
        return;
    }
    
    if (formData.password.length < 6) {
        showAlert('La contraseña debe tener al menos 6 caracteres');
        return;
    }
    
    // Mostrar loading
    registerText.textContent = 'Creando cuenta...';
    spinner.classList.remove('hidden');
    submitBtn.disabled = true;
    
    try {
        const response = await fetch(REGISTER_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert('¡Cuenta creada exitosamente! Redirigiendo al login...', 'success');
            
            // Redirigir al login después de 2 segundos
            setTimeout(() => {
                window.location.href = '/login';
            }, 2000);
            
        } else {
            showAlert(data.error || 'Error en el registro');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error de conexión. Intenta nuevamente.');
    } finally {
        // Restaurar botón
        registerText.textContent = 'Crear Cuenta';
        spinner.classList.add('hidden');
        submitBtn.disabled = false;
    }
}

// Inicializar eventos del dashboard
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
    
    // Cargar datos del usuario en el dashboard
    if (window.location.pathname === '/dashboard') {
        const token = localStorage.getItem('auth_token');
        if (!token) {
            window.location.href = '/login';
            return;
        }
        loadUserData();
    }
    
    // Cerrar modal al hacer click fuera
    document.addEventListener('click', function(event) {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.classList.add('hidden');
            }
        });
    });
});

// En auth.js falta manejar cuando el token expira
// En auth.js - REEMPLAZA la función de verificación
function checkAuth() {
    const token = localStorage.getItem('auth_token');
    const userData = localStorage.getItem('user_data');
    
    console.log('Verificando autenticación...');
    console.log('Token en localStorage:', token ? '✅ Existe' : '❌ No existe');
    console.log('User data en localStorage:', userData ? '✅ Existe' : '❌ No existe');
    
    if (!token) {
        console.log('No hay token, redirigiendo a login');
        // Solo redirigir si no estamos ya en login/register
        if (!window.location.pathname.includes('/login') && 
            !window.location.pathname.includes('/register')) {
            window.location.href = '/login';
        }
        return false;
    }
    
    // Verificar si el token es válido (estructura básica)
    try {
        const tokenParts = token.split('.');
        if (tokenParts.length !== 3) {
            console.log('Token con formato inválido');
            logout();
            return false;
        }
        
        console.log('Token válido encontrado');
        return true;
    } catch (error) {
        console.log('Error verificando token:', error);
        logout();
        return false;
    }
}

// Función logout mejorada
async function logout() {
    console.log('Cerrando sesión...');
    
    try {
        const token = localStorage.getItem('auth_token');
        if (token) {
            await fetch('/auth/logout', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
        }
    } catch (error) {
        console.log('Error en logout del backend:', error);
    } finally {
        // Siempre limpiar el frontend
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_data');
        sessionStorage.clear();
        
        console.log('Sesión cerrada, redirigiendo...');
        window.location.href = '/login';
    }
}

// Cargar datos del usuario en el dashboard
function loadUserData() {
    console.log('Cargando datos del usuario...');
    
    try {
        const userData = JSON.parse(localStorage.getItem('user_data') || '{}');
        console.log('Datos del usuario:', userData);
        
        if (!userData.id) {
            console.log('No hay datos de usuario válidos');
            logout();
            return;
        }
        
        // Actualizar UI con datos del usuario
        const welcomeElement = document.getElementById('user-welcome');
        if (welcomeElement) {
            welcomeElement.textContent = `Bienvenido, ${userData.username || 'Usuario'}`;
        }
        
        document.getElementById('user-username').textContent = userData.username || '-';
        document.getElementById('user-email').textContent = userData.email || '-';
        document.getElementById('user-role').textContent = userData.role || '-';
        document.getElementById('user-dni').textContent = userData.dni || '-';
        
        console.log('Datos del usuario cargados en UI');
        
    } catch (error) {
        console.log('Error cargando datos del usuario:', error);
        logout();
    }
}