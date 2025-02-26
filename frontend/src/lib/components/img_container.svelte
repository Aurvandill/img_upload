<script>
	import { authenticated, user_id, admin, addToast } from '$lib/stores';
	import { API_URL } from '$lib/defines';
	let { image } = $props();
	let show_modal = $state(false);
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();

	async function get_uploader(uid) {
		if ($authenticated == false) {
			//$username = "unauthorized";
			return;
		}
		const endpoint = `${API_URL}/User/${uid}`;
		try {
			const response = await fetch(endpoint, {
				method: 'GET',
				//credentials: 'same-origin',
				credentials: 'include'
			});
			if (response.ok) {
				const json = await response.json();
				return json.username;
			}
		} catch (error) {
			return 'unbekannt';
		}
	}

	async function fetch_thumbnail() {
		const endpoint = `${API_URL}/Image/${image.uuid}/thumbnail`;
		try {
			const response = await fetch(endpoint, {
				method: 'GET',
				//credentials: 'same-origin',
				credentials: 'include'
			});
			if (response.ok) {
				const blob = await response.blob();
				return URL.createObjectURL(blob);
			}
		} catch (error) {
			alert('loading image failed');
			return 'wtf';
		}
	}

	async function fetch_img() {
		const endpoint = `${API_URL}/Image/${image.uuid}`;
		try {
			const response = await fetch(endpoint, {
				method: 'GET',
				//credentials: 'same-origin',
				credentials: 'include'
			});
			if (response.ok) {
				const blob = await response.blob();
				return URL.createObjectURL(blob);
			}
		} catch (error) {
			alert('loading image failed');
			return 'wtf';
		}
	}

	async function delete_img() {
		if ($authenticated == false) {
			//$username = "unauthorized";
			return;
		}
		const endpoint = `${API_URL}/Image/${image.uuid}`;
		try {
			const response = await fetch(endpoint, {
				method: 'DELETE',
				//credentials: 'same-origin',
				credentials: 'include'
			});
			if (response.ok) {
				addToast({ message: 'Bild gelöscht', type: 'success' });
			} else {
				let json = { msg: 'unbekannter Fehler' };
				try {
					json = await response.json();
				} catch (error) {
					json = { msg: 'unbekannter Fehler' };
				}
				throw new Error(json.msg);
			}
		} catch (error) {
			addToast({ message: error, type: 'danger', heading: 'Fehler!' });
		} finally {
			show_modal = false;
			dispatch('del');
		}
	}
</script>

<div class="imgcontainer">
	{#await fetch_thumbnail()}
		<div
			style="width:250px;height: 250px; background-color:rgba(0,0,0,0.1)"
			class="d-flex justify-content-center align-items-center rounded shadow border border-dark-subtle"
		>
			<p class="spinner-border" role="status"></p>
		</div>
	{:then blo}
		<img
			class="shadow bg-white rounded border border-dark-subtle"
			src={blo}
			onclick={() => (show_modal = true)}
		/>
	{/await}
</div>

{#if show_modal}
	<div id="backdrop"></div>

	<div class="modal" style="display: block">
		<div class="img_flex d-flex flex-column">
			<div
				class="d-flex justify-content-between align-items-center mb-3"
				style="width:100vw; background-color:rgba(0,0,0,0.25)"
			>
				{#await get_uploader(image.uploader)}
					<p class="mb-0 text-bg-dark p-3 ms-1">Hochgeladen von unbekannt</p>
				{:then username}
					<p class="mb-0 text-bg-dark p-3 ms-1">Hochgeladen von {username}</p>
				{/await}
				<p class="mb-0 text-bg-dark p-3">{image.filename}</p>
				<div>
					{#if $admin || $user_id == image.uploader}
						<button
							class="btn btn-outline-danger bi-trash3 fs-1 me-3"
							aria-label="Close"
							onclick={delete_img}
						></button>
					{/if}
					<button
						class="btn btn-outline-danger bi-x-octagon fs-1 me-3"
						aria-label="Close"
						onclick={() => (show_modal = false)}
					></button>
				</div>
			</div>
			{#await fetch_img()}
				<div class="d-flex justify-content-center align-items-center flex_img">
					<p class="spinner-border" role="status"></p>
				</div>
			{:then blo}
				<img class="flex-shrink-1 flex_img mb-3" src={blo} onclick={() => (show_modal = true)} />
			{/await}
		</div>
	</div>
{/if}

<style>
	button {
		border-style: none;
	}
	.imgcontainer {
		max-height: 250px;
		height: 250px;
		margin: 1rem;
	}

	#backdrop {
		width: 100%;
		height: 100%;
		position: fixed;
		top: 0;
		left: 0;
		background-color: rgba(0, 0, 0, 0.5);
		backdrop-filter: blur(5px);
		z-index: 1031;
	}
	.modal {
		z-index: 1032;
	}

	.img_flex {
		max-height: 100vh !important;
		height: 100vh;
	}
	.flex_img {
		object-fit: contain;
		width: 100%;
		height: 100%;
	}
</style>
