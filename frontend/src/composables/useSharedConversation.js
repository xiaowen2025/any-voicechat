import { useConversationWebSocket } from './useConversationWebSocket';

const state = useConversationWebSocket();

export function useSharedConversation() {
  return state;
}
