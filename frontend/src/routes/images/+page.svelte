<script>
    import { authenticated } from "$lib/stores";
    import { writable } from "svelte/store";
    import { addToast } from "$lib/stores";
    import { API_URL } from "$lib/defines";

    let images = writable([]);
    $effect(get_images);
	async function get_images() {

        if ($authenticated == false) {
			addToast({ message: "Du Bist nicht angemeldet", type: 'danger', heading: 'Fehler!' });
			return;
		}
		const endpoint = `${API_URL}/Image`;
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
            $images = json
		} catch (error) {
            console.log(error)
		}
    }
</script>

<div class="ms-3 me-3" style="background-color:aqua">
	<h1>Bilder</h1>
</div>
