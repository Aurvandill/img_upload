<script>
	import 'bootstrap/scss/bootstrap.scss';
	import 'bootstrap-icons/font/bootstrap-icons.css';

	let { children } = $props();
	import NavBar from '$lib/nav_bar.svelte';
	import '../app.css';
</script>

<NavBar />
{@render children()}
