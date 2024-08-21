<script lang="ts">
	import { fly } from 'svelte/transition'
</script>

<p class="loader" in:fly={{ duration: 300, y: 20, opacity: 0.5 }} aria-label="Cargando...">
	<span class="loader__dot" aria-hidden="true"></span>
	<span class="loader__dot" aria-hidden="true"></span>
	<span class="loader__dot" aria-hidden="true"></span>
</p>

<style lang="scss">
	.loader {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 0.5rem;

		&__dot {
			display: inline-block;
			width: 0.5rem;
			height: 0.5rem;
			background-color: var(--primary-color);
			border-radius: 50%;
			animation: loader 1s infinite;

			&:nth-child(2) {
				animation-delay: 0.1s;
			}

			&:nth-child(3) {
				animation-delay: 0.2s;
			}
		}
	}

	@keyframes loader {
		0%,
		100% {
			transform: translateY(0);
		}

		50% {
			transform: translateY(-1rem);
		}
	}
</style>
