// Елементи DOM
const loginTab = document.getElementById('login-tab');
const signupTab = document.getElementById('signup-tab');
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const loginBtn = document.getElementById('login-btn');
const signupBtn = document.getElementById('signup-btn');
const welcomeSection = document.getElementById('welcome-section');
const logoutBtn = document.getElementById('logout-btn');
const welcomeMessage = document.getElementById('welcome-message');

// Перемикання між вкладками
loginTab.addEventListener('click', () => {
    loginTab.classList.add('active');
    signupTab.classList.remove('active');
    loginForm.style.display = 'block';
    signupForm.style.display = 'none';
});

signupTab.addEventListener('click', () => {
    signupTab.classList.add('active');
    loginTab.classList.remove('active');
    loginForm.style.display = 'none';
    signupForm.style.display = 'block';
});

// Реєстрація
signupBtn.addEventListener('click', () => {
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;

    if (email && password) {
        // Збереження користувача в localStorage
        localStorage.setItem(email, password);
        alert('Реєстрація успішна! Увійдіть у систему.');
        loginTab.click();
    } else {
        alert('Будь ласка, заповніть усі поля.');
    }
});

// Авторизація
loginBtn.addEventListener('click', () => {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    // Перевірка даних у localStorage
    if (localStorage.getItem(email) === password) {
        loginForm.style.display = 'none';
        signupForm.style.display = 'none';
        document.querySelector('.auth-section').style.display = 'none';
        welcomeSection.style.display = 'block';
        welcomeMessage.textContent = `Вітаємо, ${email}!`;
    } else {
        alert('Невірний email або пароль.');
    }
});

// Вихід із системи
logoutBtn.addEventListener('click', () => {
    welcomeSection.style.display = 'none';
    document.querySelector('.auth-section').style.display = 'block';
    loginTab.click();
});
