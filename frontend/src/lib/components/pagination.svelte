<script>
    let {currentpage, pages} = $props();
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();

    function page_change(new_value){
        currentpage = new_value;
        dispatch('change', new_value);
    }

</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->

{#if pages > 1}
	<ul class="pagination">
		{#if currentpage > 2}	
			<li class="page-item page-link" on:click={() => page_change(1)}>&lt;&lt;</li>
		{:else}
			<li class="page-item page-link hidden">&lt;&lt;</li>
		{/if}
		{#if currentpage != 1}
			<li class="page-item page-link" on:click={() => page_change(currentpage - 1)}>&lt;</li>
			<li class="page-item page-link" on:click={() => page_change(currentpage - 1)}>{currentpage - 1}</li>
		{:else}
			<li class="page-item page-link hidden">&lt;</li>
			<li class="page-item page-link hidden">{currentpage - 1}</li>
		{/if}
		<li class="page-item page-link active">{currentpage}</li>
		{#if currentpage != pages}
			<li class="page-item page-link" on:click={() => page_change(currentpage + 1)}>{currentpage + 1}</li>
			<li class="page-item page-link" on:click={() => page_change(currentpage + 1)}>&gt;</li>
		{:else}
			<li class="page-item page-link hidden">{currentpage + 1}</li>
			<li class="page-item page-link hidden">&gt;</li>
		{/if}
		{#if pages - currentpage > 1}
			<li class="page-item page-link" on:click={() => page_change(pages)}>&gt;&gt;</li>
		{:else}
			<li class="page-item page-link hidden">&gt;&gt;</li>
		{/if}
	</ul>
{/if}

<style>
	.hidden{
		opacity: 0;
	}
</style>
