import { writable } from 'svelte/store'
import type Message from '$lib/types/message'
// import { faker } from '@faker-js/faker'

const API_URL = 'https://chat.nukor.xyz/generate'

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

		const response = await fetch(API_URL, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ question: content })
		})

		const { response: responseContent } = await response.json()

		update(({ messages, ...state }) => ({
			...state,
			messages: [...messages, { content: responseContent, isBot: true }],
			isLoading: false
		}))
	}

	return {
		subscribe,
		sendMessage
	}
}

export default createChat()
