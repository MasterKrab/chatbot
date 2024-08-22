<script lang="ts">
	import { afterUpdate } from 'svelte'
	import { fly } from 'svelte/transition'

	import chat from '$lib/stores/chat'

	import Loader from '$lib/components/Loader.svelte'

	let list: HTMLElement

	afterUpdate(() => {
		list.scrollTop = list.scrollHeight
	})
</script>

<ul class="messages" bind:this={list}>
	{#each $chat.messages as { content, isBot }}
		<li
			class="message"
			class:message--user={!isBot}
			transition:fly={{ duration: 500, y: 10, opacity: 0.5 }}
		>
			{content}
		</li>
	{/each}

	{#if $chat.isLoading}
		<Loader />
	{/if}
</ul>

<style lang="scss">
	.messages {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		list-style: none;
		margin-top: 0;
		margin-bottom: 1.5rem;
		padding: 1rem 2rem 2rem 1rem;
		overflow-y: auto;

		&::-webkit-scrollbar {
			width: 0.25rem;
		}

		&::-webkit-scrollbar-track {
			background-color: transparent;
		}

		&::-webkit-scrollbar-thumb {
			background-color: var(--cuaternary-color);
			border-radius: 0.5rem;
		}
	}

	.message {
		padding: 0.6rem 0.5rem;
		line-height: 1.3rem;

		&--user {
			background-color: var(--primary-color);
			box-shadow: 0.15rem 0.15rem 0.4rem rgba(255, 255, 255, 0.2);
			max-width: 100%;
			min-width: fit-content;
			word-wrap: break-word;
			padding-left: 1rem;
			padding-right: 1rem;
			align-self: end;
			border-radius: 1rem;
			text-align: justify;
		}
	}
</style>
