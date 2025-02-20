<script>
	import { API_URL } from '$lib/defines';

	async function login() {
		console.log(username, password);
		const url = `${API_URL}/Session/login`;
		try {
			const response = await fetch(url, {
                method: "POST",
                body: JSON.stringify({"username":username, "password":password})
            });
			if (!response.ok) {
				throw new Error(`Response status: ${response.status}`);
			}

			const json = await response.json();
			console.log(json);
		} catch (error) {
			console.error(error.message);
		}
	}

	let username = '';
	let password = '';
</script>

<div class="row d-flex justify-content-center">
	<div class="col-md-8 col-lg-6 col-xl-4">
		<form>
			<div data-mdb-input-init class="form-outline mb-4">
				<label class="form-label" for="nutzername">Nutzername</label>
				<input
					type="text"
					id="nutzername"
					class="form-control form-control-lg"
					placeholder="example_user"
					bind:value={username}
				/>
			</div>
			<div data-mdb-input-init class="form-outline mb-3">
				<label class="form-label" for="pwform">Passwort</label>
				<input
					type="password"
					id="pwform"
					class="form-control form-control-lg"
					placeholder=""
					bind:value={password}
				/>
			</div>

			<div class="text-center text-lg-start mt-4 pt-2">
				<button
					type="button"
					data-mdb-button-init
					data-mdb-ripple-init
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
