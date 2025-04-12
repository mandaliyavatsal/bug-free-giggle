# bug-free-giggle

## Project Overview

This project is a standalone macOS application that generates music (MIDI format) offline using an AI model, optimized for M1 (Apple Silicon) Macs. The app includes a simple GUI, uses Magenta’s MusicVAE model, and is packaged as a native ARM64 `.app` bundle.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mandaliyavatsal/bug-free-giggle.git
   cd bug-free-giggle
   ```

2. **Set up a virtual environment**:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download and extract the model checkpoint**:
   ```bash
   mkdir -p models
   curl -O https://storage.googleapis.com/magentadata/models/music_vae/checkpoints/cat-mel_2bar_small.tar
   tar -xvf cat-mel_2bar_small.tar -C models/
   ```

## Build Instructions

1. **Package the app using PyInstaller**:
   ```bash
   pyinstaller --noconfirm --onefile --windowed --name MusicGenerator \
       --add-data "models/cat-mel_2bar_small:models/cat-mel_2bar_small" \
       --target-architecture arm64 \
       --exclude-module torch.distributed \
       --exclude-module torch.cuda \
       music_app.py
   ```

2. **Clean up the bundle to remove x86_64 libraries**:
   ```bash
   find dist/MusicGenerator.app -name "*.so" -exec file {} \; | grep x86_64 | xargs rm
   ```

## Usage Guide

1. **Run the app**:
   ```bash
   open dist/MusicGenerator.app
   ```

2. **Generate and save music**:
   - Select the music type from the dropdown (e.g., “Melody” or “Drums”).
   - Click the “Generate Music” button to create a 2-bar MIDI sequence.
   - Click the “Save Music” button to export the MIDI file.

## Dependencies

- `torch==2.2.0`
- `magenta==2.1.4`
- `pretty_midi==0.2.10`
- `pyqt5==5.15.9`
- `pyinstaller==6.3.0`
- `tensorflow-macos==2.15.0`

## Running Tests

1. **Run the test suite**:
   ```bash
   pytest tests/
   ```

2. **Test MIDI generation**:
   - Ensure the app generates and saves a MIDI file offline.
   - Verify the MIDI file plays correctly in a media player.
