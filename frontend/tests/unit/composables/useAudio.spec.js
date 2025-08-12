import { describe, it, expect, vi, beforeEach } from 'vitest';
import {
  base64ToArray,
  arrayBufferToBase64,
  convertFloat32ToPCM,
} from '../../../src/utils/audio';

describe('audio utils', () => {
  describe('base64ToArray and arrayBufferToBase64', () => {
    it('should convert a base64 string to an ArrayBuffer and back', () => {
      const originalBase64 = 'SGVsbG8sIFdvcmxkIQ=='; // "Hello, World!"
      const arrayBuffer = base64ToArray(originalBase64);
      expect(arrayBuffer).toBeInstanceOf(ArrayBuffer);
      const convertedBase64 = arrayBufferToBase64(arrayBuffer);
      expect(convertedBase64).toBe(originalBase64);
    });
  });

  describe('convertFloat32ToPCM', () => {
    it('should convert a Float32Array to a 16-bit PCM ArrayBuffer', () => {
      const float32Array = new Float32Array([0, 0.5, -0.5, 1, -1]);
      const pcmBuffer = convertFloat32ToPCM(float32Array);
      expect(pcmBuffer).toBeInstanceOf(ArrayBuffer);
      const pcm16Array = new Int16Array(pcmBuffer);
      expect(pcm16Array.length).toBe(float32Array.length);
      expect(pcm16Array[0]).toBe(0);
      expect(pcm16Array[1]).toBe(16383); // 0.5 * 0x7fff
      expect(pcm16Array[2]).toBe(-16383); // -0.5 * 0x7fff
      expect(pcm16Array[3]).toBe(32767); // 1 * 0x7fff
      expect(pcm16Array[4]).toBe(-32767); // -1 * 0x7fff
    });
  });
});

import { useAudio } from '../../../src/composables/useAudio';
import { ref } from 'vue';
import { vi } from 'vitest';

// Mocking browser-specific APIs
vi.stubGlobal('window', {
  atob: (str) => Buffer.from(str, 'base64').toString('binary'),
  btoa: (str) => Buffer.from(str, 'binary').toString('base64'),
});

vi.stubGlobal('navigator', {
  mediaDevices: {
    getUserMedia: vi.fn(() => Promise.resolve({
      getTracks: () => [{ stop: vi.fn() }],
    })),
  },
});

const mockAudioContext = {
  createMediaStreamSource: vi.fn(() => ({
    connect: vi.fn(),
  })),
  createAnalyser: vi.fn(() => ({
    connect: vi.fn(),
    disconnect: vi.fn(),
  })),
  audioWorklet: {
    addModule: vi.fn(() => Promise.resolve()),
  },
  destination: {},
  close: vi.fn(),
};

const mockAudioWorkletNode = {
  connect: vi.fn(),
  disconnect: vi.fn(),
  port: {
    postMessage: vi.fn(),
    onmessage: null,
  },
};

vi.stubGlobal('AudioContext', vi.fn(() => mockAudioContext));
vi.stubGlobal('AudioWorkletNode', vi.fn(() => mockAudioWorkletNode));


describe('useAudio', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should start and stop audio correctly', async () => {
    const websocket = ref({ readyState: WebSocket.OPEN, send: vi.fn() });
    const onAudioData = vi.fn();

    const { startAudio, stopAudio } = useAudio(websocket, onAudioData);

    await startAudio();
    expect(navigator.mediaDevices.getUserMedia).toHaveBeenCalledWith({ audio: { channelCount: 1 } });
    expect(AudioContext).toHaveBeenCalledTimes(2); // one for player, one for recorder

    stopAudio();
    expect(mockAudioContext.close).toHaveBeenCalledTimes(2);
  });
});
