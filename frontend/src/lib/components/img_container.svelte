<script>
	import { authenticated } from '$lib/stores';
	import { API_URL } from '$lib/defines';
	let { image } = $props();
	let show_modal = $state(false);

	async function fetch_thumbnail() {
		console.log(image);
		if ($authenticated == false) {
			//$username = "unauthorized";
			return;
		}
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
		console.log(image);
		if ($authenticated == false) {
			//$username = "unauthorized";
			return;
		}
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
			<div class="d-flex justify-content-end" style="width:100vw">
				<button
					class="btn btn-outline-danger bi bi-x-octagon fs-1 me-3"
					aria-label="Close"
					onclick={() => (show_modal = false)}
				></button>
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
