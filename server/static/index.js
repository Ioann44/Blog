authToken = "";

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
 * @param {string} err_message replaces error message if specified
*/
function fetch_template(url, respIsJson, init, callback, err_message = null) {
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
		if (err_message === null) {
			showTemporaryNotification(errorMessage);
		} else {
			showTemporaryNotification(err_message);
		}
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

	fetch_template('/auth/create', true,
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

function toggleLike(postId) {
	if (!authToken) {
		showTemporaryNotification("Для взаимодействия с лайками нужно авторизоваться");
		return;
	}
	fetch_template(`/api/change_like/${postId}`, true,
		{
			method: "POST",
			headers: {
				"Authorization": `Bearer ${authToken}`
			}
		},
		data => {
			var postElement = document.getElementById("post-" + postId);
			if (postElement) {
				var likeButton = postElement.querySelector(".like-heart");
				likeButton.classList.remove("liked");
				likeButton.classList.remove("not-liked");

				if (data.is_liked) {
					likeButton.classList.add("liked");
				} else {
					likeButton.classList.add("not-liked");
				}
				var likeCount = postElement.getElementsByClassName("like-count")[0]
				likeCount.textContent = data.likes;
			}
		},
		"Попробуйте авторизоваться заново"
	)
}

// Функция для добавления выбранных файлов и их превью в список файлов
function handleFiles() {
	const fileList = document.getElementById("fileList");
	fileList.innerHTML = ""; // Очищаем список файлов
	selectedFiles = []; // Очищаем массив выбранных файлов

	const fileInput = document.getElementById("fileInput");
	const files = fileInput.files;

	for (let i = 0; i < files.length; i++) {
		const file = files[i];
		selectedFiles.push(file); // Добавляем файл в массив выбранных файлов

		const fileItem = document.createElement("div");
		fileItem.classList.add("file-preview");

		const fileImage = document.createElement("img");
		fileImage.src = URL.createObjectURL(file);

		const fileInfo = document.createElement("div");
		fileInfo.classList.add("file-info");

		const fileName = document.createElement("p");
		fileName.classList.add("file-name");
		fileName.textContent = file.name;

		const removeButton = document.createElement("button");
		removeButton.textContent = "Удалить";
		removeButton.style.display = "none";
		removeButton.addEventListener("click", () => {
			// Удаляем файл из массива выбранных файлов
			selectedFiles.splice(selectedFiles.indexOf(file), 1);

			// Удаляем файл из списка в HTML
			fileList.removeChild(fileItem);

			// Обновляем счетчик файлов на странице
			updateFileCounter();
		});

		fileInfo.appendChild(fileName);
		fileItem.appendChild(fileImage);
		fileItem.appendChild(fileInfo);
		fileItem.appendChild(removeButton);
		fileList.appendChild(fileItem);
	}
}

function uploadPost(postTheme, postContent, files, id = 0) {
	if (postTheme.trim() === "") {
		showTemporaryNotification("Тема не должна быть пустой");
		return;
	}
	var postLines = postContent.split(/\n+/).filter((line) => line.trim() !== "");
	if (postLines.length == 0) {
		showTemporaryNotification("Содержимое поста не может быть пустым");
		return;
	}

	var promices = [];
	for (var i = 0; i < files.length; i++) {
		var formData = new FormData()
		formData.set("file", files[i]);
		promices.push(
			fetch('/file/upload',
				{
					method: "POST",
					headers: {
						"Authorization": `Bearer ${authToken}`
					},
					body: formData
				}).then(
					response => {
						if (!response.ok) {
							response.text().then(errorMessage => {
								showTemporaryNotification(errorMessage);
							});
						}
						return response.json();
					}
				))

	}

	Promise.allSettled(promices).then(jsons => {
		var uploadedFilesUuids = [];
		for (const json of jsons) {
			if (json) {
				uploadedFilesUuids.push(json.value.uuid);
			}
		}
		fetch_template("/api/save", true,
			{
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"Authorization": `Bearer ${authToken}`
				},
				body: JSON.stringify({
					id: id,
					theme: postTheme,
					content: postLines,
					filenames: uploadedFilesUuids
				})
			}, data => {
				location.reload();
			});
	})
}

// Функция для отправки поста
function createPost() {
	const postTheme = document.getElementById("postTheme").value;
	const postContent = document.getElementById("postContent").value;

	// Получите выбранные файлы и обработайте их по необходимости
	const fileInput = document.getElementById("fileInput");
	const files = fileInput.files;

	uploadPost(postTheme, postContent, files);
}

function editPost(postId) {
	var editModal = document.getElementById("editModal");
	editModal.style.display = "block";
	document.getElementById("editFileList").innerHTML = "";

	var post = document.getElementById(`post-${postId}`);

	document.getElementById("editPostTheme").value = post.getElementsByClassName("post-title")[0].textContent;

	var contentArray = [];
	var postContentElement = post.getElementsByClassName("post-content")[0];
	// Перебрать все элементы <p> внутри "post-content"
	var paragraphElements = postContentElement.getElementsByTagName('p');
	for (const paragraph of paragraphElements) {
		// Извлечь текст из элемента <p> и добавить его в массив
		contentArray.push(paragraph.textContent);
	}
	document.getElementById("editPostContent").value = contentArray.join("\n");

	// Обработчик изменения файла для input type="file"
	document.getElementById("editFileInput").addEventListener("change", function () {
		var fileInput = document.getElementById("editFileInput");
		var fileList = document.getElementById("editFileList");

		fileList.innerHTML = "";

		for (var i = 0; i < fileInput.files.length; i++) {
			var file = fileInput.files[i];

			// Создайте элемент для отображения выбранных файлов
			var filePreview = document.createElement("div");
			filePreview.className = "file-preview";

			var fileImage = document.createElement("img");
			fileImage.src = URL.createObjectURL(file);
			filePreview.appendChild(fileImage);

			var fileInfo = document.createElement("div");
			fileInfo.className = "file-info";

			var fileName = document.createElement("p");
			fileName.className = "file-name";
			fileName.textContent = file.name;
			fileInfo.appendChild(fileName);

			filePreview.appendChild(fileInfo);
			fileList.appendChild(filePreview);
		}
	});

	document.getElementById("saveEditButton").onclick = function () {
		var updatedTheme = document.getElementById("editPostTheme").value;
		var updatedContent = document.getElementById("editPostContent").value;

		// Получите список выбранных файлов
		var selectedFiles = document.getElementById("editFileInput").files;

		// Выполните логику обновления данных на сервере и закройте модальное окно
		uploadPost(updatedTheme, updatedContent, selectedFiles, postId);
	};
}

function closeEditModal() {
	var editModal = document.getElementById("editModal");
	editModal.style.display = "none";

	// Очистите поля формы редактирования поста
	document.getElementById("editPostTheme").value = "";
	document.getElementById("editPostContent").value = "";

	// Очистите отображение выбранных файлов и сбросьте input type="file"
	var fileInput = document.getElementById("editFileInput");
	fileInput.value = ""; // Это сбросит выбранные файлы
	var fileList = document.getElementById("editFileList");
	fileList.innerHTML = "";
}

function confirmDelete(postId) {
	const confirmDelete = window.confirm("Вы уверены, что хотите удалить этот пост?");
	if (confirmDelete) {
		fetch_template(`/api/delete/${postId}`, false,
			{
				method: "POST",
				headers: {
					"Authorization": `Bearer ${authToken}`
				}
			},
			data => {
				const post = document.getElementById(`post-${postId}`);
				post.parentNode.removeChild(post);
				showTemporaryNotification("Пост успешно удалён");
			}
		);
	}
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
	document.cookie = `${name} = ${value}; expires = ${expires.toUTCString()}; path = /`;
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
			setTimeout(window.init, 1000);
		})
		.catch(error => {
			deleteCookie('authToken');
			changeBody(false);
		});
}

window.init = function init() {
	var registerNameInput = document.getElementById("registerName");
	registerNameInput.addEventListener("input", checkNameAvailability);

	// Уведомления
	const notificationContainer = document.getElementById('notificationContainer');

	authToken = getCookie('authToken');

	// Получение элемента input типа file
	const fileInput = document.getElementById("fileInput");

	// Добавление обработчика события change для элемента fileInput
	fileInput.addEventListener("change", handleFiles);
}