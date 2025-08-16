import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useConversationStore } from '../../src/stores/conversation';

describe('useConversationStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('should have the correct initial state', () => {
    const store = useConversationStore();
    expect(store.websocket).toBe(null);
    expect(store.messages).toEqual([]);
    expect(store.notes).toBe('');
    expect(store.analysis).toBe(null);
    expect(store.isAnalysing).toBe(false);
    expect(store.activeTab).toBe('transcription');
    expect(store.isConnecting).toBe(false);
    expect(store.conversationStarted).toBe(false);
    expect(store.conversationFinished).toBe(false);
  });

  it('setActiveTab should update the active tab', () => {
    const store = useConversationStore();
    store.setActiveTab('analysis');
    expect(store.activeTab).toBe('analysis');
  });

  it('disconnect should close the websocket and update state', () => {
    const store = useConversationStore();
    const mockSocket = {
      close: vi.fn(),
      readyState: 1, // OPEN
    };
    store.websocket = mockSocket;

    store.disconnect();

    expect(mockSocket.close).toHaveBeenCalled();
    expect(store.conversationStarted).toBe(false);
    expect(store.isConnecting).toBe(false);
    expect(store.conversationFinished).toBe(true);
  });
});
