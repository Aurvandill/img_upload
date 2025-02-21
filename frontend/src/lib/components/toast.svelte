<script>
	import { createEventDispatcher } from 'svelte';
	import { fade } from 'svelte/transition';

	const dispatch = createEventDispatcher();

	let {type="info", message="test 123", heading="Benachrichtigung"} = $props();
</script>

<div class="toast show m-2 me-3" role="alert" aria-live="assertive" aria-atomic="true" out:fade>
	<div class="toast-header text-bg-{type}">
		<i class="bi bi-exclamation-octagon me-2"></i>
		<strong class="me-auto">{heading}</strong>
		<button type="button" class="btn-close" aria-label="close" onclick={() => dispatch("dismiss")}></button>
	</div>
	<div class="toast-body">{message}</div>
</div>
