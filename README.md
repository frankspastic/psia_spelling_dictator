# PSIA Spelling Dictator

A web-based spelling dictation application for PSIA (Private Schools Interscholastic Association) spelling lists for grades 2-3 and 4-5 (2025-2026 school year).

## Features

- 📚 **Two Grade Levels**: 600 words for Grades 2-3, 800 words for Grades 4-5
- 🎲 **Random or Custom Selection**: Choose random words or select specific words
- 🔊 **High-Quality Voice**: Uses professional Google Cloud Text-to-Speech audio
- ⏱️ **Customizable Timing**: Set interval between words
- 🎯 **Word Repetition**: Each word is spoken twice (immediately and at halfway point)
- 💾 **Save Custom Lists**: Create and save your own word lists
- ⏯️ **Full Playback Controls**: Pause, previous, next, repeat
- 📊 **Progress Tracking**: Visual progress bar and word counter
- 🎨 **Modern Interface**: Clean, responsive design that works on any device

## How to Use (For Non-Technical Users)

### Option 1: Download and Run Locally (Easiest)

1. **Download the application**:
   - Click the green `Code` button at the top of this page
   - Select `Download ZIP`
   - Save the file to your computer (e.g., Downloads folder)

2. **Extract the files**:
   - Find the downloaded ZIP file (usually named `psia-spelling-dictator-main.zip`)
   - Double-click to extract/unzip it
   - You'll see a folder named `psia-spelling-dictator-main`

3. **Open the application**:
   - Open the extracted folder
   - Find the file named `index.html`
   - Double-click `index.html` to open it in your web browser
   - The application will start automatically!

### Option 2: Use Online (If hosted)

If this application is hosted online, simply visit the URL and start using it immediately - no download required!

## How to Use the Application

### Getting Started

1. **Select Grade Level**: Choose between Grades 2-3 or Grades 4-5
2. **Choose Mode**:
   - **Random Words**: Specify how many random words you want
   - **Select Specific Words**: Pick individual words from the complete list

### Random Words Mode

1. Select "Random Words"
2. Enter the number of words you want (1-600 for gr2-3, 1-800 for gr4-5)
3. Set the interval in seconds (how long between each word)
4. Click "Start Dictation"

### Custom Word Selection Mode

1. Select "Select Specific Words"
2. Use the search box to find specific words (optional)
3. Check the boxes next to the words you want
4. **Save your list** (optional):
   - Enter a name for your list (e.g., "Week 1 Practice")
   - Click "Save List"
5. **Load a saved list** (if you saved one before):
   - Select from the dropdown menu
   - Click "Load"
6. Click "Start Dictation"

### During Dictation

- **Pause/Resume**: Click to pause or resume the dictation
- **Previous/Next**: Navigate to previous or next word
- **Repeat Word**: Hear the current word again
- **Stop & Reset**: End the dictation and return to settings
- **Show Word List**: See all words in your current session

### Settings

- **Interval**: Time between words (default: 5 seconds)
- **Voice**: Choose from available voices (if using fallback mode)
- **Speech Rate**: Adjust how fast words are spoken (0.5x - 1.5x)

## Tips for Best Results

1. **Test Your Sound**: Make sure your computer volume is on and audible
2. **Use Headphones**: For better audio quality during practice
3. **Save Custom Lists**: Create themed lists for focused practice (e.g., "Hard Words", "Week 1")
4. **Adjust Interval**: Start with longer intervals (8-10 seconds) for beginners
5. **Word Repetition**: Each word is automatically repeated halfway through the interval - perfect for writing practice!

## System Requirements

- Any modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (only needed for initial download)
- Computer speakers or headphones
- Works on: Windows, Mac, iPad, Chromebook, or any device with a web browser

## Troubleshooting

### The application won't open
- Make sure you extracted the ZIP file first (don't try to open `index.html` from inside the ZIP)
- Try a different web browser
- Make sure JavaScript is enabled in your browser

### No sound is playing
- Check your computer volume
- Try clicking "Repeat Word" to test audio
- The app will automatically fall back to your browser's built-in voice if audio files can't be loaded

### Words are skipping or not playing
- The first time you use each word, it needs to load. Subsequent plays will be instant
- Check your internet connection if audio files aren't loading
- Try refreshing the page

### I can't find my saved list
- Saved lists are stored in your browser. If you clear browser data, saved lists will be deleted
- Make sure you're using the same browser and computer where you saved the list

## For Teachers

This application is perfect for:
- Classroom spelling practice
- Remote learning assignments
- Self-paced student practice
- Creating weekly spelling tests
- Differentiating instruction (different word lists for different students)

Create custom word lists for each week, save them, and reuse them throughout the year!

## Technical Information

- **Audio Quality**: Google Cloud Text-to-Speech (Standard female voice, en-US)
- **Total Words**: 1,400 pre-generated audio files
- **File Size**: Approximately 15-20 MB (including all audio files)
- **Privacy**: All data saved locally in your browser - no information is sent to servers

## For Developers

See the [scripts/README.md](scripts/README.md) file for information about:
- Regenerating audio files
- Extracting word lists from PDFs
- Python dependencies
- Development setup

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- PSIA Spelling Lists (2025-2026)
- Google Cloud Text-to-Speech API
- Built with vanilla HTML, CSS, and JavaScript

## Support

If you encounter any issues or have suggestions, please open an issue on GitHub.

---

**Happy Spelling Practice! 📝✨**
