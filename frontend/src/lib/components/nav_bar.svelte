<script>
	import { authenticated, addToast } from '$lib/stores';
	import { API_URL } from '$lib/defines';
	import { writable } from 'svelte/store';
	authenticated;

	let username = writable('EXAMPLE_USER');
	let pw = $state('');

	$effect(check_session);

	async function logout() {
		$authenticated = false;
	}

	async function check_session() {
		if ($authenticated == false) {
			//$username = "unauthorized";
			return;
		}
		setTimeout(check_session, 60000);
		const endpoint = `${API_URL}/Session`;
		try {
			const response = await fetch(endpoint, {
				method: 'GET',
				//credentials: 'same-origin',
				credentials: 'include'
			});
			if (!response.ok) {
				let json = { msg: 'unbekannter Fehler' };
				try {
					json = await response.json();
				} catch (error) {
					json = { msg: 'unbekannter Fehler' };
				}

				addToast({ message: json.msg, type: 'danger', heading: 'Fehler!' });
				throw new Error(`Response status: ${response.status}`);
			}

			const json = await response.json();
			console.log(json);
			$username = json.user.username;
		} catch (error) {
			$username = 'unbekannt';
			$authenticated = false;
		}
	}
</script>

<header class="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom">
	<a
		href="/"
		class="d-flex align-items-center ms-5 me-md-auto link-body-emphasis text-decoration-none"
	>
		<i class="bi bi-envelope"></i>
		<span class="fs-4 ms-2">Nellys und Erics Hochzeit</span>
	</a>
	<ul class="nav nav-pills me-5">
		{#if !$authenticated}
			<li class="nav-item">
				<a href="/login" class="nav-link active" aria-current="page">Login</a>
			</li>
		{:else}
			<li class="nav-item me-1">
				<a href="/users" class="nav-link" aria-current="page">Nutzer</a>
			</li>
			<li class="nav-item me-1">
				<a href="/images/upload" class="nav-link" aria-current="page">Bilder</a>
			</li>
			<li class="nav-item me-3 btn btn-outline-primary">
				<div class="d-flex justify-content-center align-items-center">
					<i class="bi bi-person-circle me-2"></i>
					<p class="mb-0">{$username}</p>
				</div>
			</li>
			<li class="nav-item">
				<button class="btn btn-danger" aria-current="page" onclick={logout}>Logout</button>
			</li>
		{/if}
	</ul>
</header>

<style>
</style>
