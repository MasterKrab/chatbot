import { writable } from 'svelte/store'
import type Message from '$lib/types/message'
import { faker } from '@faker-js/faker'

const createChat = () => {
	const { subscribe, update } = writable<{
		messages: Message[]
		isLoading: boolean
	}>({
		messages: [],
		isLoading: false
	})

	const sendMessage = async (content: string) => {
		update(({ messages, ...state }) => ({
			...state,
			messages: [...messages, { content, isBot: false }],

			isLoading: true
		}))

		await new Promise((resolve) => setTimeout(resolve, 500))

		update(({ messages, ...state }) => ({
			...state,
			messages: [...messages, { content: faker.lorem.text(), isBot: true }],
			isLoading: false
		}))
	}

	return {
		subscribe,
		sendMessage
	}
}

export default createChat()
