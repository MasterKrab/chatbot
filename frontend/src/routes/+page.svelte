<script lang="ts">
	import Messages from '$lib/components/Messages.svelte'
	import TextBox from '$lib/components/TextBox.svelte'
</script>

<svelte:head>
	<title>Chatbot</title>
</svelte:head>

<main class="main">
	<Messages />

	<TextBox />
</main>

<style lang="scss">
	.main {
		display: grid;
		grid-template-rows: 1fr max-content;
		gap: 1rem;
		padding: 0.5rem 1.5rem;

		height: 100vh;
		max-width: 850px;
		margin-left: auto;
		margin-right: auto;
	}
</style>
