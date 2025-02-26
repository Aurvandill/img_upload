<script>
	import { authenticated } from '$lib/stores';
	import { writable } from 'svelte/store';
	import { addToast } from '$lib/stores';
	import { API_URL, PAGESIZE } from '$lib/defines';
	import ImgContainer from '$lib/components/img_container.svelte';
	import Pagination from '$lib/components/pagination.svelte';

	let images = writable({ image_count: 0, images: {} });
	let currentpage = writable(1);
	let pages = writable(3);

	function blub(e) {
		$currentpage = e.detail;
		get_images();
	}

	$effect(get_images);
	async function get_images() {
		
		const endpoint = `${API_URL}/Image?pagesize=${PAGESIZE}&page=${$currentpage}`;
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
				console.log(json);
				addToast({ message: json.msg, type: 'danger', heading: 'Fehler!' });
				throw new Error(`Response status: ${response.status}`);
			}

			const json = await response.json();
			console.log(json);
			$pages = Math.floor(json.image_count / PAGESIZE);
			if (Math.floor(json.image_count / PAGESIZE) != json.image_count / PAGESIZE){
				$pages = $pages + 1
			}
			console.log($pages);
			$images = json;
			if ($images.images.length == 0 && $currentpage > 1){
				$currentpage = $currentpage - 1
				get_images()
			} 
		} catch (error) {
			console.log(error);
		}
	}
</script>

<h1 class="ms-3">Bilder ({$images.image_count})</h1>
<div class="d-flex justify-content-center">
	<Pagination on:change={blub} pages={$pages} currentpage={$currentpage}></Pagination>
</div>
<div class="ms-3 me-3 d-flex flex-row flex-wrap align-content-start align-items-start justify-content-between">
	{#each $images.images as image}
		<ImgContainer on:del={get_images} {image} />
	{/each}
</div>
<div class="d-flex justify-content-center">
	<Pagination on:change={blub} pages={$pages} currentpage={$currentpage}></Pagination>
</div>
