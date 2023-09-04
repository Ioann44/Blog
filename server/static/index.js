authToken = ""

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
 * @param {boolean} respIsJson
 * @param {content} init {method: string, headers: {Content-Type: string}, body: string}
 * @param {function} callback 
*/
function fetch_template(url, respIsJson, init, callback) {
	fetch(url, init).then(
		response => {
			if (!response.ok) {
				return response.text().then(errorMessage => {
					throw new Error(errorMessage);
				});
			}
			if (respIsJson) {
				return response.json();
			} else {
				return response.text();
			}
		}
	).then(callback).catch(errorMessage => {
		showTemporaryNotification(errorMessage);
	})
}

// Функция для отправки запроса на авторизацию
function login() {
	var loginName = document.getElementById("loginName").value;
	var loginPassword = document.getElementById("loginPassword").value;

	fetch_template('/auth/login', true,
		{
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ name: loginName, password: loginPassword })
		},
		data => {
			authToken = data.token;
			updatePageOnAutentificationChange();
		});

}

// Функция для отправки запроса на регистрацию с проверкой пароля
function register() {
	var registerName = document.getElementById("registerName").value;
	var registerPassword = document.getElementById("registerPassword").value;
	var confirmPassword = document.getElementById("confirmPassword").value;

	// Проверьте, совпадают ли пароли
	if (registerPassword !== confirmPassword) {
		showTemporaryNotification("Пароли не совпадают");
		return;
	}

	fetch_template('/auth/register', true,
		{
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ name: registerName, password: registerPassword })
		},
		data => {
			authToken = data.token;
			updatePageOnAutentificationChange()
		});

}

function unlogin() {
	updatePageOnAutentificationChange(false);
}

function updatePageOnAutentificationChange(loginned = true) {
	// showTemporaryNotification(`Добро пожаловать, ${loginName}`)
	closeModal();
	if (loginned) {
		setCookie('authToken', authToken, 7);
	} else {
		deleteCookie('authToken');
	}
	window.location.replace('/');
}

// Функция для проверки доступности имени при изменении поля логина
function checkNameAvailability() {
	var registerName = document.getElementById("registerName").value;
	var nameAvailability = document.getElementById("nameAvailability");

	if (!registerName) {
		return;
	}

	const url = `/auth/check_name/${registerName}`;

	fetch_template(url, false, { method: "GET" }, data => {
		if (data) {
			nameAvailability.innerHTML = "Имя доступно";
		} else {
			nameAvailability.innerHTML = "Имя уже занято";
		}
	})
}

// Функция вызова уведомления
function showTemporaryNotification(message, duration = 3000) {
	const notification = document.createElement('div');
	notification.textContent = message;
	notification.classList.add('notification');

	notificationContainer.appendChild(notification);
	notification.style.animation = 'slide-down 0.5s ease-in-out forwards, fade-out 0.5s ease-in-out 2s forwards';

	setTimeout(() => {
		notification.remove()
	}, duration);
}

// Функция сохранения cookie
function setCookie(name, value, days) {
	const expires = new Date();
	expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
	document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

// Функция загрузки cookie
function getCookie(name) {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) {
		return parts.pop().split(';').shift();
	}
	return null;
}

// Функция удаления cookie
function deleteCookie(name) {
	var pastDate = new Date(0);
	document.cookie = `${name}=;expires=${pastDate.toUTCString()};path=/`;
}

function changeBody(authorization = true) {
	var init = { method: 'GET' };
	if (authorization) {
		init = { ...init, headers: { 'Authorization': `Bearer ${getCookie('authToken')}` } }
	}
	fetch('/index', init)
		.then(response => {
			if (!response.ok) {
				throw new Error('Error with loading index page');
			}
			return response.text();
		})
		.then(html => {
			document.body.innerHTML = html;
			setTimeout(init, 1000);
		})
		.catch(error => {
			changeBody(false);
		});
}

function init() {
	var registerNameInput = document.getElementById("registerName");
	registerNameInput.addEventListener("input", checkNameAvailability);

	// Уведомления
	const notificationContainer = document.getElementById('notificationContainer');

	authToken = getCookie('authToken');
}