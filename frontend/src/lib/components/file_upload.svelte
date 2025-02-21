<script>
	import Dropzone from 'dropzone';
	import { onMount } from 'svelte';
	import 'dropzone/dist/dropzone.css';
	import 'dropzone/dist/basic.css';
	import { API_URL } from '$lib/defines';

	onMount(() => {
		let myDropzone = new Dropzone('#my-awesome-dropzone', {
			withCredentials: true,
			headers: {
				'Cache-Control': '',
				'X-Requested-With': ''
			}
		});
	});
</script>

<form
	action={`${API_URL}/Image`}
	onsubmitcapture={(event) => {
		event.preventDefault();
	}}
	class="dropzone ms-5 me-5"
	id="my-awesome-dropzone"
></form>

<style>
    .dropzone{
        max-height: 60vh;
        height: 60vh;
    }
</style>
