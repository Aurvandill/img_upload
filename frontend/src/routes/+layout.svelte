<script>
	import 'bootstrap/scss/bootstrap.scss';
	import 'bootstrap-icons/font/bootstrap-icons.css';
	import ToastContainer from '$lib/components/toast_container.svelte';

	let { children } = $props();
	import NavBar from '$lib/components/nav_bar.svelte';
	import '../app.css';
</script>

<NavBar />
<div class="content">
{@render children()}
</div>

<ToastContainer />
<style>
	.content{
		max-width: 100vw;
	}
</style>
