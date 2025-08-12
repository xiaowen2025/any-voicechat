import { useConversationWebSocket } from './useConversationWebSocket';

const conversation = useConversationWebSocket();

export function useSharedConversation() {
  return conversation;
}
