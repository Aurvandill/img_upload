<script>
	import { API_URL } from '$lib/defines';
	import { addToast, authenticated } from '$lib/stores';
	import { goto } from '$app/navigation';

	async function login() {
		const url = `${API_URL}/Session/login`;
		try {
			const response = await fetch(url, {
				method: 'POST',
				body: JSON.stringify({ username: username, password: pw })
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
			addToast({ message: json.msg, type: 'primary' });
			$authenticated = true;
			goto('/');
		} catch (error) {
			console.error(error.message);
		}
	}

	let username = $state('');
	let pw = $state('');
</script>

<div class="d-flex justify-content-center">
	<div class="col-md-8 col-lg-6 col-xl-4">
		<form onsubmit={() => login()}>
			<div data-mdb-input-init class="form-outline mb-4">
				<label class="form-label" for="nutzername">Nutzername</label>
				<input
					type="text"
					id="nutzername"
					class="form-control form-control-lg"
					placeholder="Beispielnutzer"
					bind:value={username}
					onkeydown={(event) => {
						if (event.key == 'Enter') login();
					}}
				/>
			</div>
			<div data-mdb-input-init class="form-outline mb-3">
				<label class="form-label" for="pwform">Passwort</label>
				<input
					type="password"
					id="pwform"
					class="form-control form-control-lg"
					placeholder="Passwort"
					bind:value={pw}
					onkeydown={(event) => {
						if (event.key == 'Enter') login();
					}}
				/>
			</div>

			<div class="text-center text-lg-start mt-4 pt-2">
				<button
					type="button"
					class="btn btn-primary btn-lg"
					style="padding-left: 2.5rem; padding-right: 2.5rem;"
					onclick={login}
				>
					Login
				</button>
			</div>
		</form>
	</div>
</div>
