function triggerToast(text, success = false, enable_html = false) {
	const toastTrigger = document.getElementById('liveToastBtn')
	const toastLive = document.getElementById('liveToast')
	const toast = new bootstrap.Toast(toastLive)
	if (success) {
		toastLive.classList.remove('text-bg-danger');
		toastLive.classList.add('text-bg-success');
	} else {
		toastLive.classList.add('text-bg-danger');
		toastLive.classList.remove('text-bg-success');
	}

	if (enable_html)
		document.getElementById('toast_body').innerHTML = text;
	else
		document.getElementById('toast_body').innerText = text;

	toast.show()
}

function setButton(waiting, button_descriptor) {
	let button = document.querySelector(button_descriptor);
	if (!button) return;
	if (button.querySelector('.fa-solid')) {
		button.querySelector('.fa-solid').style.display = waiting ? 'none' : '';
		button.querySelector('.spinner-border').hidden = !waiting;
	}
	button.disabled = waiting;
}

function addFriend(name, button_descriptor, auto_reload = false) {
	return new Promise((resolve) => {
		setButton(true, button_descriptor);
		fetch('/friends/add/' + name).then((response) => {
			setButton(false, button_descriptor);
			if (response.status === 200) {
				triggerToast(`${name} est ajouté à votre liste de contacts.<br>` +
					"<a href='#' onclick='location.reload();'>Cliquez ici pour rafraichir la page</a>", true, true);
				if (auto_reload)
					setTimeout(() => {
						location.reload()
					}, 230);
			} else
				triggerToast(name + ' est introuvable');
			resolve(response.status);
		});
	});
}

function deleteFriend(friend_name, button_descriptor, auto_reload = false) {
	return new Promise((resolve) => {
		setButton(true, button_descriptor);
		fetch('/friends/remove/' + friend_name).then((response) => {
			setButton(false, button_descriptor);
			if (response.status === 200) {
				triggerToast(friend_name + ' a été supprimé de votre liste de contact', true);
				if (auto_reload)
					setTimeout(() => {
						location.reload()
					}, 200);
			} else {
				triggerToast("Une erreur s'est produite pendant la suppression.");
			}
			resolve(response.status);
		});
	});
}

function setRelation(friend_name, relation, button_descriptor, auto_reload = false) {
	console.log(relation)
	return new Promise((resolve) => {
		setButton(true, button_descriptor);
		fetch('/friends/set_relation/' + friend_name + '/' + relation).then((response) => {
			setButton(false, button_descriptor);
			if (response.status === 200) {
				triggerToast("Relation modifiée avec succès", true);
				if (auto_reload)
					setTimeout(() => {
						location.reload()
					}, 200);
			} else {
				triggerToast("Une erreur s'est produite pendant la modification.");
			}
			resolve(response.status);
		});
	});
}

function isValidURL(string) {
	let res = string.match(/(http(s)?:\/\/.)(www\.)?[-a-zA-Z0-9@:%._+~#=]{1,40}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_+.~#?&/=]*)/g);
	return (res !== null)
}

function getURLDomain(str) {
	if (!isValidURL(str))
		return str.trim()
	let a = document.createElement('a');
	a.href = str;
	return a.hostname;
}

function getURLPath(str) {
	if (!isValidURL(str))
		return str.trim()
	let a = document.createElement('a');
	a.href = str;
	return a.pathname.substr(1)
}

function openFriend(name, auto_reload = false) {
	function config_bio(data) {
		function set_link(elem, data, path = false) {
			if (!data) {
				elem.hidden = true;
				return;
			}
			elem.hidden = false;
			if (path)
				elem.querySelector('a').innerText = getURLPath(data);
			else
				elem.querySelector('a').innerText = getURLDomain(data);
			if (isValidURL(data))
				elem.querySelector('a').href = data;
		}

		let bio = document.getElementById('FP-bio');
		let social_row = document.getElementById('FP-socials-row');
		let website = document.getElementById('FP-website');
		let github = document.getElementById('FP-github');
		let discord = document.getElementById('FP-discord');
		let recit = document.getElementById('FP-text');

		let shown = !!(data.discord || data.website || data.github || data.recit);
		bio.hidden = !shown;
		if (!shown)
			return;
		let social_shown = !!(data.discord || data.website || data.github)
		social_row.hidden = !social_shown;
		if (social_shown) {
			set_link(website, data.website);
			set_link(github, data.github, true);
			set_link(discord, data.discord);
		}
		recit.hidden = !(recit);
		if (data.recit)
			recit.innerText = data.recit;
		else
			recit.innerText = "";
	}

	return new Promise(async (resolve) => {
		fetch("/getuser/" + name).then(res => {
			if (res.status !== 200) {
				triggerToast("Une erreur s'est produite.")
				return resolve(400);
			}
			res.json().then(data => {
				let openFriendLabelAddFriend = document.getElementById("openFriendLabelAddFriend");
				let openFriendLabelDeleteFriend = document.getElementById("openFriendLabelDeleteFriend");
				let openFriendModalName = document.getElementById("openFriendModalName");
				let addCloseFriend = document.getElementById("addCloseFriend");
				let removeCloseFriend = document.getElementById("removeCloseFriend");
				let openFriendProfile = document.getElementById("openFriendProfile");
				let openFriendShowCluster = document.getElementById('openFriendShowCluster');
				let isAdmin = document.getElementById('modal-admin');
				let pool = openFriendModalName.querySelector('.pool')
				let modal_name = openFriendModalName.querySelector('.name')

				openFriendLabelAddFriend.hidden = data.is_friend !== false;
				openFriendLabelDeleteFriend.hidden = data.is_friend === false;
				addCloseFriend.hidden = data.is_friend === false ? false : data.is_friend !== 0;
				removeCloseFriend.hidden = data.is_friend === false || data.is_friend !== 1;
				if (data.is_friend === false)
					addCloseFriend.hidden = true;

				config_bio(data)
				openFriendShowCluster.disabled = !(data['position'] !== null);
				isAdmin.hidden = !(data.admin !== false);
				if (data.admin)
					isAdmin.innerHTML = data.admin.tag;

				openFriendShowCluster.onclick = () => {
					if (!data.position[0])
						return;
					// i hate it
					if (data.position[0] === 'e' || data.position[0] === 'c' || data.position.includes('bess') || data.position.includes('paul')
						|| data.position.includes('made')) {
						let cluster = data.position.split('r')[0]
						if (data.position.includes('bess') || data.position.includes('paul')) {
							let lastChar = cluster[cluster.length - 1];
							if (lastChar === 'A' || lastChar === 'B')
								cluster = cluster.slice(0, -1);
						}
						location.href = `/?cluster=${cluster}&p=${data.position}`
					}
				}
				openFriendLabelAddFriend.onclick = () => {
					addFriend(name, '#openFriendLabelAddFriend', auto_reload)
				}
				openFriendLabelDeleteFriend.onclick = () => {
					deleteFriend(name, '#openFriendLabelDeleteFriend', auto_reload)
				}
				let changeRelation = async (relation, hide) => {
					const ret = await setRelation(name, relation, '#openFriendLabelAddBestFriend')
					if (ret !== 200) return;

					addCloseFriend.hidden = hide;
					removeCloseFriend.hidden = !hide;
				}
				addCloseFriend.onclick = () => {
					changeRelation(1, true)
				};
				removeCloseFriend.onclick = () => {
					changeRelation(0, false)
				};
				openFriendProfile.onclick = () => {
					location.href = "https://profile.intra.42.fr/users/" + name;
				}
				document.getElementById('openFriendModalPic').src = data.image;
				if (data.pool)
					pool.innerText = "Piscine de " + data.pool
				modal_name.innerText = name;
				document.getElementById("openFriendLabel").innerText = name;

				const modal = new bootstrap.Modal('#openFriendModal', {});
				openFriendModal = modal;
				modal.show();
				resolve(200)
			})
		})
	})
}

function does_user_exists(login) {
	return new Promise(async (resolve) => {
		fetch("/getuser/" + login).then(res => {
			if (res.status === 200)
				resolve(200);
			else
				resolve(res.status);
		});
	});
}

function open(url) {
	window.location.href = url;
}

function newTab(url) {
	window.open(url, '_blank').focus();
}

function isTouchDevice() {
	return (('ontouchstart' in window) ||
		(navigator.maxTouchPoints > 0) ||
		(navigator.msMaxTouchPoints > 0));
}

(() => {
	let globalAddFriend = document.getElementById('globalAddFriend');
	let globalSearchInput = document.getElementById('globalSearch');
	let globalSearchButton = document.getElementById('globalSearchButton');

	async function redirect_profile(login) {
		login = login.trim().toLowerCase()
		if (login === "" || login.length <= 3) {
			globalSearchInput.focus();
			return;
		}
		if (await does_user_exists(login) === 200)
			location.href = '/profile/' + login;
		else
			triggerToast("L'utilisateur est introuvable", false);
	}

	function fillGlobalSuggestions(element, suggestions) {
		let list = document.querySelector(element);

		list.innerHTML = ''
		suggestions.forEach(function (item) {
			let option = document.createElement('option');
			option.value = item['s'];
			option.innerText = item['v'];
			list.appendChild(option);
		});
	}

	/*
	globalAddFriend.addEventListener('click', async () => {
		let val = globalSearchInput.value.trim();

		if (val === "") {
			globalSearchInput.focus();
			return;
		}
		await addFriend(globalSearchInput.value, '#globalAddFriend', true);
	});
	*/
	function search_text(text, callback) {
		fetch('/search/' + encodeURIComponent(text) + "/0").then((response) => {
			response.json().then((json) => {
				callback(json);
			})
		})
	}

	if (globalSearchInput) {
		let lastSearch = "";
		globalSearchInput.addEventListener('keyup', async (e) => {
			let val = globalSearchInput.value.trim().toLowerCase();

			if (e.key === 'Enter') {
				if (val.length <= 3)
					await redirect_profile(val);
				else {
					search_text(val, (json) => {
						let found = 0;
						json.forEach((item) => {
							if (item['v'].toLowerCase() === val || item['s'].toLowerCase() === val) {
								if (item['type'] === 'user') {
									redirect_profile(item['s']);
									found = 1;
								} else if (item['type'] === 'project') {
									open('/mates/' + item['s']);
									found = 1;
								}
							}
						})
						if (found === 0)
							triggerToast(`Aucun résultat pour ${val}`
							)
					});
				}
			}
			if (val.length >= 3) {
				setTimeout(() => {
					if (val !== globalSearchInput.value.trim().toLowerCase()) return;
					if (val === lastSearch) return;
					console.log(val, globalSearchInput.value.trim().toLowerCase())
					lastSearch = val;
					search_text(val, (json) => {
						fillGlobalSuggestions('#global_suggestions', json)
					});
				}, 200)

			}
		});

		globalSearchButton.addEventListener('click', async () => {
			let val = globalSearchInput.value.trim().toLowerCase();
			await redirect_profile(val);
		})
	}
})();

(() => {
	let cluster = document.getElementById('qc-cluster');
	let friends = document.getElementById('qc-friends');

	if (cluster && friends) {
		if (location.pathname === '/')
			friends.hidden = false;
		else
			cluster.hidden = false;
		cluster.addEventListener('click', () => {
			location.href = '/';
		})
		friends.addEventListener('click', () => {
			location.href = '/friends/';
		})
	}
})();