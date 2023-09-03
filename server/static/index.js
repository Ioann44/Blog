
// Функция открытия модального окна
function openModal() {
	document.getElementById("authModal").style.display = "block";
}

// Функция закрытия модального окна
function closeModal() {
	document.getElementById("authModal").style.display = "none";
}

// Функция для переключения между формой авторизации и регистрации
function toggleForms() {
	var loginForm = document.getElementById("loginForm");
	var registerForm = document.getElementById("registerForm");
	if (loginForm.style.display === "none") {
		loginForm.style.display = "block";
		registerForm.style.display = "none";
	} else {
		loginForm.style.display = "none";
		registerForm.style.display = "block";
	}
}

/**
 * Fetch cover for suppressing code amount
 * @param {string} url
 * @param {content} init {method: string, headers: {Content-Type: string}, body: string}
 * @param {function} callback 
*/
function fetch_template(url, init, callback) {
	fetch(url, init).then(
		response => {
			if (!response.ok) {

			}
		}
	)
}

// Функция для отправки запроса на авторизацию
function login() {
	var loginName = document.getElementById("loginName").value;
	var loginPassword = document.getElementById("loginPassword").value;

	fetch('https://example.com/api/endpoint', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ name: loginName, password: loginPassword })
	}).then(response => {
		if (!response.ok) {
			return response.text()
		}
		return response.json();
	}).then(data => {
		console.log(data);
	}).catch(error => {
		console.error('There was a problem with the fetch operation:', error);
	});

	closeModal();
}

// Функция для отправки запроса на регистрацию с проверкой пароля
function register() {
	var registerName = document.getElementById("registerName").value;
	var registerPassword = document.getElementById("registerPassword").value;
	var confirmPassword = document.getElementById("confirmPassword").value;

	// Проверьте, совпадают ли пароли
	if (registerPassword !== confirmPassword) {
		alert("Пароли не совпадают");
		return;
	}

	// Отправьте запрос на /auth/create с данными и обработайте jwt_token
	// Сохраните jwt_token в cookies
	// Закройте модальное окно
	// Обновите страницу или выполните другие действия при регистрации
	closeModal();
}

// Функция для проверки доступности имени при изменении поля логина
function checkNameAvailability() {
	var registerName = document.getElementById("registerName").value;
	var nameAvailability = document.getElementById("nameAvailability");

	const url = `/auth/check_name/${registerName}`;

	fetch(url)
		.then(response => {
			if (response.ok) {
				return response.json();
			} else {
				throw new Error('Ошибка при выполнении запроса');
			}
		}).then(data => {
			if (data) {
				nameAvailability.innerHTML = "Имя доступно";
			} else {
				nameAvailability.innerHTML = "Имя уже занято";
			}
		})
}

// Функция вызова уведомления
function showTemporaryNotification(message, duration) {
	const notification = document.createElement('div');
	notification.textContent = message;
	notification.classList.add('notification');

	notificationContainer.appendChild(notification);
	notification.style.animation = 'slide-down 0.5s ease-in-out forwards, fade-out 0.5s ease-in-out 2s forwards';

	setTimeout(() => {
		notification.remove()
	}, duration);
}

// Добавьте событие на изменение поля логина при загрузке страницы
window.onload = function () {
	var registerNameInput = document.getElementById("registerName");
	registerNameInput.addEventListener("input", checkNameAvailability);

	// Уведомления
	const showNotificationButton = document.getElementById('showNotification');
	const notificationContainer = document.getElementById('notificationContainer');
	// Пример вызова уведомления
	showNotificationButton.addEventListener('click', () => {
		const notificationText = 'Это ваш текст уведомления ';
		showTemporaryNotification(notificationText, 3000);
	});
};
