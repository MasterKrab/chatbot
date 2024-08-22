<script lang="ts">
	import { afterUpdate } from 'svelte'

	import chat from '$lib/stores/chat'
	import SendIcon from '$lib/components/Icons/SendIcon.svelte'

	let content = ''

	let submitElement: HTMLButtonElement
	let textareaElement: HTMLTextAreaElement

	const handleSubmit = () => {
		chat.sendMessage(content)
		content = ''
	}

	const handleKeyDown = (event: KeyboardEvent) => {
		if (event.key !== 'Enter' || event.shiftKey) return

		event.preventDefault()
		submitElement.click()
	}

	afterUpdate(() => {
		textareaElement.style.height = 'auto'
		textareaElement.style.height = `${textareaElement.scrollHeight}px`
	})
</script>

<form class="form" on:submit|preventDefault={handleSubmit}>
	<textarea
		class="form__textarea"
		bind:this={textareaElement}
		bind:value={content}
		on:keydown={handleKeyDown}
		required
	/>
	<button
		class="form__button"
		bind:this={submitElement}
		disabled={!content.trim() || $chat.isLoading}
	>
		<SendIcon />
	</button>
</form>

<style lang="scss">
	.form {
		display: grid;
		grid-template-columns: 1fr 3.25rem;
		gap: 1rem;
		background-color: var(--cuaternary-color);
		border-radius: 1.25rem;
		padding: 0.1rem;

		&__textarea {
			box-sizing: border-box;
			background-color: transparent;
			border: none;
			resize: none;
			margin: 0.5rem;
			padding: 0.2rem 1rem;
			color: var(--tertiary-color);
			overflow-y: hidden;
			min-height: 2.5rem;
			max-height: 8rem;
		}

		&__button {
			background-color: var(--primary-color);
			color: var(--tertiary-color);
			width: 2.5rem;
			height: 2.5rem;
			padding: 0.6rem;
			margin-top: auto;
			margin-bottom: 0.5rem;
			border-radius: 50%;
			transition: background-color 0.2s;

			&:hover {
				background-color: var(--tertiary-color);
				color: var(--primary-color);
			}
		}
	}
</style>
