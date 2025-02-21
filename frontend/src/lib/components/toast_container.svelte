<script lang="ts">
	import Toast from '$lib/components/toast.svelte';

	import { dismissToast, toasts } from '$lib/stores';
</script>

{#if $toasts}
	<div>
		{#each $toasts as toast (toast.id)}
			<Toast
				type={toast.type}
				message={toast.message}
				heading={toast.heading}
				on:dismiss={() => dismissToast(toast.id)}>{toast.message}</Toast
			>
		{/each}
	</div>
{/if}

<style>
	div {
		position: fixed;
		bottom: 0;
        right: 0;
		width: fit-content;
        height: max-content;
		display: flex;
		margin-top: 1rem;
		justify-content: center;
		flex-direction: column;
		z-index: 1000;
	}
</style>
