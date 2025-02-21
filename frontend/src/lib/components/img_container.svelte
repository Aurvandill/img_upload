<script>
    import { authenticated } from "$lib/stores";
    let {img_uid} = $props()


    async function get_img(){
        if ($authenticated == false) {
			//$username = "unauthorized";
			return;
		}
		setTimeout(check_session, 15000);
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

