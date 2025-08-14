/**
 * Converts a Base64 string to an ArrayBuffer.
 * @param {string} base64 The Base64 string to convert.
 * @returns {ArrayBuffer} The converted ArrayBuffer.
 */
export function base64ToArray(base64) {
  const binaryString = window.atob(base64);
  const len = binaryString.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  return bytes.buffer;
}

/**
 * Converts an ArrayBuffer to a Base64 string.
 * @param {ArrayBuffer} buffer The ArrayBuffer to convert.
 * @returns {string} The converted Base64 string.
 */
export function arrayBufferToBase64(buffer) {
  let binary = "";
  const bytes = new Uint8Array(buffer);
  const len = bytes.byteLength;
  for (let i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return window.btoa(binary);
}

/**
 * Converts a Float32Array to a 16-bit PCM ArrayBuffer.
 * @param {Float32Array} inputData The Float32Array to convert.
 * @returns {ArrayBuffer} The converted 16-bit PCM ArrayBuffer.
 */
export function convertFloat32ToPCM(inputData) {
  const pcm16 = new Int16Array(inputData.length);
  for (let i = 0; i < inputData.length; i++) {
    pcm16[i] = inputData[i] * 0x7fff;
  }
  return pcm16.buffer;
}
