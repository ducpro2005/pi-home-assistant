# pi-home-assistant
This is my graduate thesis project: A 100% offline, distributed smart home architecture. 

## Architecture

The system is split into two primary components: the **Satellites** and the **Brain**.

### 1. Satellites (Audio & Control)
   These guys will be the one listening to our command, sending the data to the Raspberry pi 3B+ and later on will execute the command. 
* **Hardware:** ESP32 DevKit V1, INMP441 (I2S Microphone), MAX98357A (I2S Amplifier), 8R3W Speaker, Relay Modules.
* **Firmware:** Dual-core FreeRTOS setup. Core 0 handles real-time 16kHz, 16-bit mono PCM audio streaming via WebSockets. Core 1 listens to MQTT for hardware control commands (lights, fans) and TTS playback.

### 2. Brain (Processing Pipeline)
* **Hardware:** Raspberry Pi 3B+
* **Software Stack:**
  * **Network Ingestion:** Asyncio WebSocket Server.
  * **Speech-to-Text (STT):** [Vosk](https://alphacephei.com/vosk/) (Lightweight `small-en-us` model).
  * **Intent Parsing (NLU):** Snips NLU 
  * **Text-to-Speech (TTS):** [Piper](https://github.com/rhasspy/piper) (Lessac-Medium ONNX model).
  * **Command Routing:** Mosquitto MQTT Broker.

### The Data Flow
1. User speaks -> ESP32 detects wake word and streams binary audio via WebSockets to the Pi.
2. Pi detects `END_OF_AUDIO` and pushes the buffer to a thread-safe Queue.
3. Worker thread pops the session -> **Vosk** transcribes audio to text.
4. **Snips NLU** extracts the intent 
5. System concurrently publishes the MQTT command to trigger the relay AND fires up **Piper** to generate a voice response.
6. TTS audio bytes are routed back to the specific ESP32 via MQTT for playback.
