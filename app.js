// Spelling Dictator App
class SpellingDictator {
    constructor() {
        this.selectedWords = [];
        this.customSelectedWords = [];
        this.currentIndex = 0;
        this.isPaused = false;
        this.intervalId = null;
        this.countdownId = null;
        this.remainingTime = 0;
        this.halfwayTimeoutId = null;
        this.synth = window.speechSynthesis;
        this.voices = [];
        this.selectedVoice = null;
        this.currentMode = 'random';
        this.audioCache = {}; // Cache for audio elements
        this.currentAudio = null; // Track currently playing audio
        this.usePreGeneratedAudio = true; // Try pre-generated audio first

        this.initElements();
        this.initEventListeners();
        this.loadVoices();
        this.initWordSelector();
    }

    initElements() {
        // Settings panel elements
        this.gradeLevelSelect = document.getElementById('gradeLevel');
        this.wordCountInput = document.getElementById('wordCount');
        this.intervalInput = document.getElementById('interval');
        this.voiceSelect = document.getElementById('voiceSelect');
        this.speedInput = document.getElementById('speed');
        this.speedValue = document.getElementById('speedValue');
        this.startBtn = document.getElementById('startBtn');

        // Mode selection
        this.modeRadios = document.querySelectorAll('input[name="mode"]');
        this.randomMode = document.getElementById('randomMode');
        this.customMode = document.getElementById('customMode');

        // Custom word selection
        this.wordSelector = document.getElementById('wordSelector');
        this.wordSearch = document.getElementById('wordSearch');
        this.selectAllBtn = document.getElementById('selectAllBtn');
        this.clearAllBtn = document.getElementById('clearAllBtn');
        this.selectedCount = document.getElementById('selectedCount');
        this.randomizeCustom = document.getElementById('randomizeCustom');

        // Saved lists
        this.savedListsSelect = document.getElementById('savedListsSelect');
        this.loadListBtn = document.getElementById('loadListBtn');
        this.deleteListBtn = document.getElementById('deleteListBtn');
        this.listNameInput = document.getElementById('listName');
        this.saveListBtn = document.getElementById('saveListBtn');

        // Dictation panel elements
        this.dictationPanel = document.getElementById('dictationPanel');
        this.currentWordText = document.getElementById('currentWordText');
        this.wordNumber = document.getElementById('wordNumber');
        this.currentWordSpan = document.getElementById('currentWord');
        this.totalWordsSpan = document.getElementById('totalWords');
        this.progressFill = document.getElementById('progressFill');
        this.timer = document.getElementById('timer');

        // Control buttons
        this.prevBtn = document.getElementById('prevBtn');
        this.pauseBtn = document.getElementById('pauseBtn');
        this.nextBtn = document.getElementById('nextBtn');
        this.repeatBtn = document.getElementById('repeatBtn');
        this.stopBtn = document.getElementById('stopBtn');

        // Word list
        this.toggleListBtn = document.getElementById('toggleListBtn');
        this.wordList = document.getElementById('wordList');
        this.wordListItems = document.getElementById('wordListItems');
    }

    initEventListeners() {
        this.startBtn.addEventListener('click', () => this.startDictation());
        this.prevBtn.addEventListener('click', () => this.previousWord());
        this.pauseBtn.addEventListener('click', () => this.togglePause());
        this.nextBtn.addEventListener('click', () => this.nextWord());
        this.repeatBtn.addEventListener('click', () => this.repeatWord());
        this.stopBtn.addEventListener('click', () => this.stopDictation());
        this.toggleListBtn.addEventListener('click', () => this.toggleWordList());
        this.speedInput.addEventListener('input', (e) => {
            this.speedValue.textContent = `${e.target.value}x`;
        });
        this.voiceSelect.addEventListener('change', (e) => {
            this.selectedVoice = this.voices[e.target.value];
        });

        // Mode switching
        this.modeRadios.forEach(radio => {
            radio.addEventListener('change', (e) => this.switchMode(e.target.value));
        });

        // Word selection
        this.wordSearch.addEventListener('input', (e) => this.filterWords(e.target.value));
        this.selectAllBtn.addEventListener('click', () => this.selectAllWords());
        this.clearAllBtn.addEventListener('click', () => this.clearAllWords());

        // Grade level selection
        this.gradeLevelSelect.addEventListener('change', (e) => this.changeGradeLevel(e.target.value));

        // Saved lists management
        this.saveListBtn.addEventListener('click', () => this.saveList());
        this.loadListBtn.addEventListener('click', () => this.loadList());
        this.deleteListBtn.addEventListener('click', () => this.deleteList());
    }

    changeGradeLevel(level) {
        // Update the global SPELLING_WORDS variable
        if (level === 'gr23') {
            SPELLING_WORDS = SPELLING_WORDS_GR23;
        } else {
            SPELLING_WORDS = SPELLING_WORDS_GR45;
        }

        // Update max value for word count input
        this.wordCountInput.max = SPELLING_WORDS.length;

        // Clear custom selections and reinitialize word selector
        this.customSelectedWords = [];
        this.initWordSelector();
    }

    switchMode(mode) {
        this.currentMode = mode;
        if (mode === 'random') {
            this.randomMode.style.display = 'block';
            this.customMode.style.display = 'none';
        } else {
            this.randomMode.style.display = 'none';
            this.customMode.style.display = 'block';
        }
    }

    initWordSelector() {
        this.wordSelector.innerHTML = '';
        SPELLING_WORDS.forEach((word, index) => {
            const div = document.createElement('div');
            div.className = 'word-checkbox';
            div.dataset.word = word;

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = `word-${index}`;
            checkbox.value = word;

            const label = document.createElement('label');
            label.htmlFor = `word-${index}`;
            label.textContent = word;

            checkbox.addEventListener('change', (e) => {
                if (e.target.checked) {
                    this.customSelectedWords.push(word);
                    div.classList.add('checked');
                } else {
                    this.customSelectedWords = this.customSelectedWords.filter(w => w !== word);
                    div.classList.remove('checked');
                }
                this.updateSelectedCount();
            });

            div.appendChild(checkbox);
            div.appendChild(label);
            this.wordSelector.appendChild(div);
        });

        // Load saved lists into dropdown
        this.loadSavedListsDropdown();
    }

    loadSavedListsDropdown() {
        const savedLists = this.getSavedLists();
        this.savedListsSelect.innerHTML = '<option value="">-- Select a saved list --</option>';

        Object.keys(savedLists).forEach(listName => {
            const option = document.createElement('option');
            option.value = listName;
            const list = savedLists[listName];
            option.textContent = `${listName} (${list.words.length} words, Grade ${list.gradeLevel === 'gr23' ? '2-3' : '4-5'})`;
            this.savedListsSelect.appendChild(option);
        });
    }

    getSavedLists() {
        const listsJSON = localStorage.getItem('spellingLists');
        return listsJSON ? JSON.parse(listsJSON) : {};
    }

    saveList() {
        const listName = this.listNameInput.value.trim();

        if (!listName) {
            alert('Please enter a name for this list');
            return;
        }

        if (this.customSelectedWords.length === 0) {
            alert('Please select at least one word to save');
            return;
        }

        const savedLists = this.getSavedLists();

        // Check if list name already exists
        if (savedLists[listName]) {
            if (!confirm(`A list named "${listName}" already exists. Do you want to overwrite it?`)) {
                return;
            }
        }

        // Save the list with grade level information
        savedLists[listName] = {
            words: [...this.customSelectedWords],
            gradeLevel: this.gradeLevelSelect.value,
            createdAt: new Date().toISOString()
        };

        localStorage.setItem('spellingLists', JSON.stringify(savedLists));

        alert(`List "${listName}" saved successfully!`);
        this.listNameInput.value = '';
        this.loadSavedListsDropdown();
    }

    loadList() {
        const listName = this.savedListsSelect.value;

        if (!listName) {
            alert('Please select a list to load');
            return;
        }

        const savedLists = this.getSavedLists();
        const list = savedLists[listName];

        if (!list) {
            alert('List not found');
            return;
        }

        // Switch to the correct grade level if needed
        if (list.gradeLevel !== this.gradeLevelSelect.value) {
            this.gradeLevelSelect.value = list.gradeLevel;
            this.changeGradeLevel(list.gradeLevel);
        }

        // Clear current selection
        this.clearAllWords();

        // Load the words from the saved list
        this.customSelectedWords = [...list.words];

        // Check the checkboxes for the loaded words
        const checkboxes = this.wordSelector.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            if (this.customSelectedWords.includes(checkbox.value)) {
                checkbox.checked = true;
                checkbox.closest('.word-checkbox').classList.add('checked');
            }
        });

        this.updateSelectedCount();
        alert(`List "${listName}" loaded successfully!`);
    }

    deleteList() {
        const listName = this.savedListsSelect.value;

        if (!listName) {
            alert('Please select a list to delete');
            return;
        }

        if (!confirm(`Are you sure you want to delete the list "${listName}"?`)) {
            return;
        }

        const savedLists = this.getSavedLists();
        delete savedLists[listName];
        localStorage.setItem('spellingLists', JSON.stringify(savedLists));

        alert(`List "${listName}" deleted successfully!`);
        this.loadSavedListsDropdown();
    }

    filterWords(searchTerm) {
        const term = searchTerm.toLowerCase();
        const checkboxes = this.wordSelector.querySelectorAll('.word-checkbox');

        checkboxes.forEach(div => {
            const word = div.dataset.word.toLowerCase();
            if (word.includes(term)) {
                div.style.display = 'flex';
            } else {
                div.style.display = 'none';
            }
        });
    }

    selectAllWords() {
        const checkboxes = this.wordSelector.querySelectorAll('input[type="checkbox"]');
        const visibleCheckboxes = Array.from(checkboxes).filter(cb => {
            return cb.closest('.word-checkbox').style.display !== 'none';
        });

        visibleCheckboxes.forEach(checkbox => {
            if (!checkbox.checked) {
                checkbox.checked = true;
                const word = checkbox.value;
                if (!this.customSelectedWords.includes(word)) {
                    this.customSelectedWords.push(word);
                }
                checkbox.closest('.word-checkbox').classList.add('checked');
            }
        });
        this.updateSelectedCount();
    }

    clearAllWords() {
        const checkboxes = this.wordSelector.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = false;
            checkbox.closest('.word-checkbox').classList.remove('checked');
        });
        this.customSelectedWords = [];
        this.updateSelectedCount();
    }

    updateSelectedCount() {
        this.selectedCount.textContent = this.customSelectedWords.length;
    }

    loadVoices() {
        const loadVoicesList = () => {
            this.voices = this.synth.getVoices();
            this.voiceSelect.innerHTML = '';

            // Filter for English voices and prioritize quality voices
            const englishVoices = this.voices.filter(voice =>
                voice.lang.startsWith('en')
            );

            if (englishVoices.length > 0) {
                englishVoices.forEach((voice, index) => {
                    const option = document.createElement('option');
                    option.value = this.voices.indexOf(voice);
                    option.textContent = `${voice.name} (${voice.lang})`;

                    // Set default voice (prefer enhanced or premium voices)
                    if (voice.name.includes('Enhanced') ||
                        voice.name.includes('Premium') ||
                        voice.name.includes('Samantha') ||
                        index === 0) {
                        option.selected = true;
                        this.selectedVoice = voice;
                    }

                    this.voiceSelect.appendChild(option);
                });
            } else {
                // Fallback to all voices if no English voices found
                this.voices.forEach((voice, index) => {
                    const option = document.createElement('option');
                    option.value = index;
                    option.textContent = `${voice.name} (${voice.lang})`;
                    if (index === 0) {
                        option.selected = true;
                        this.selectedVoice = voice;
                    }
                    this.voiceSelect.appendChild(option);
                });
            }
        };

        loadVoicesList();
        if (this.synth.onvoiceschanged !== undefined) {
            this.synth.onvoiceschanged = loadVoicesList;
        }
    }

    startDictation() {
        const interval = parseInt(this.intervalInput.value);

        if (interval < 1) {
            alert('Please enter an interval of at least 1 second');
            return;
        }

        // Select words based on mode
        if (this.currentMode === 'random') {
            const wordCount = parseInt(this.wordCountInput.value);
            if (wordCount < 1 || wordCount > SPELLING_WORDS.length) {
                alert(`Please enter a number between 1 and ${SPELLING_WORDS.length}`);
                return;
            }
            this.selectedWords = this.getRandomWords(wordCount);
        } else {
            // Custom mode
            if (this.customSelectedWords.length === 0) {
                alert('Please select at least one word from the list');
                return;
            }
            // Use the words in the order they were selected, or randomize if checkbox is checked
            if (this.randomizeCustom.checked) {
                this.selectedWords = this.shuffleArray([...this.customSelectedWords]);
            } else {
                this.selectedWords = [...this.customSelectedWords];
            }
        }

        this.currentIndex = 0;
        this.isPaused = false;

        // Update UI
        this.showDictationPanel();
        this.totalWordsSpan.textContent = this.selectedWords.length;
        this.displayWordList();

        // Start dictation
        this.speakCurrentWord();
        this.startTimer(interval);
    }

    getRandomWords(count) {
        const shuffled = [...SPELLING_WORDS].sort(() => Math.random() - 0.5);
        return shuffled.slice(0, count);
    }

    shuffleArray(array) {
        // Fisher-Yates shuffle algorithm
        const shuffled = [...array];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
    }

    showDictationPanel() {
        document.querySelector('.settings-panel').style.display = 'none';
        this.dictationPanel.style.display = 'block';
    }

    showSettingsPanel() {
        document.querySelector('.settings-panel').style.display = 'block';
        this.dictationPanel.style.display = 'none';
    }

    speakCurrentWord() {
        if (this.currentIndex >= this.selectedWords.length) {
            this.completeDictation();
            return;
        }

        const word = this.selectedWords[this.currentIndex];
        this.currentWordText.textContent = word;
        this.wordNumber.textContent = `#${this.currentIndex + 1}`;
        this.currentWordSpan.textContent = this.currentIndex + 1;
        this.updateProgress();

        // Clear any existing halfway timeout
        if (this.halfwayTimeoutId) {
            clearTimeout(this.halfwayTimeoutId);
            this.halfwayTimeoutId = null;
        }

        // Speak the word immediately (first time)
        this.speak(word);

        // Schedule the word to be repeated halfway through the interval
        const interval = parseInt(this.intervalInput.value);
        const halfwayTime = (interval * 1000) / 2; // Convert to milliseconds and divide by 2

        this.halfwayTimeoutId = setTimeout(() => {
            if (!this.isPaused) {
                this.speak(word);
            }
        }, halfwayTime);
    }

    sanitizeFilename(word) {
        // Convert word to safe filename (lowercase, keep hyphens, replace spaces with underscores)
        let filename = word.toLowerCase();
        filename = filename.replace(/\s+/g, '_');
        // Keep only alphanumeric, hyphens, and underscores
        filename = filename.replace(/[^a-z0-9_-]/g, '');
        return filename;
    }

    getAudioPath(word) {
        // Determine the correct audio path based on current grade level
        const gradeLevel = this.gradeLevelSelect.value;
        const sanitized = this.sanitizeFilename(word);
        return `audio/${gradeLevel}/${sanitized}.mp3`;
    }

    async speak(text) {
        // Stop any currently playing audio
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio.currentTime = 0;
        }

        // Cancel any ongoing speech synthesis
        this.synth.cancel();

        if (this.usePreGeneratedAudio) {
            try {
                const audioPath = this.getAudioPath(text);

                // Check if audio is already cached
                if (this.audioCache[audioPath]) {
                    this.currentAudio = this.audioCache[audioPath];
                } else {
                    // Create new audio element
                    const audio = new Audio(audioPath);

                    // Wait for audio to load to verify it exists
                    await new Promise((resolve, reject) => {
                        audio.addEventListener('canplaythrough', resolve, { once: true });
                        audio.addEventListener('error', reject, { once: true });
                        audio.load();
                    });

                    // Cache the audio element
                    this.audioCache[audioPath] = audio;
                    this.currentAudio = audio;
                }

                // Apply playback rate (speed)
                this.currentAudio.playbackRate = parseFloat(this.speedInput.value);

                // Play the audio
                await this.currentAudio.play();
                return;
            } catch (error) {
                console.warn(`Pre-generated audio not found for "${text}", falling back to Web Speech API`, error);
                // Fall through to Web Speech API fallback
            }
        }

        // Fallback to Web Speech API
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = parseFloat(this.speedInput.value);
        utterance.pitch = 1;
        utterance.volume = 1;

        if (this.selectedVoice) {
            utterance.voice = this.selectedVoice;
        }

        this.synth.speak(utterance);
    }

    startTimer(interval) {
        this.remainingTime = interval;
        this.updateTimerDisplay();

        this.countdownId = setInterval(() => {
            if (!this.isPaused) {
                this.remainingTime--;
                this.updateTimerDisplay();

                if (this.remainingTime <= 0) {
                    this.currentIndex++;
                    if (this.currentIndex < this.selectedWords.length) {
                        this.speakCurrentWord();
                        this.remainingTime = interval;
                    } else {
                        this.completeDictation();
                    }
                }
            }
        }, 1000);
    }

    updateTimerDisplay() {
        this.timer.textContent = `${this.remainingTime}s`;
    }

    updateProgress() {
        const progress = ((this.currentIndex + 1) / this.selectedWords.length) * 100;
        this.progressFill.style.width = `${progress}%`;
    }

    togglePause() {
        this.isPaused = !this.isPaused;

        if (this.isPaused) {
            this.pauseBtn.innerHTML = '▶ Resume';
            this.pauseBtn.classList.add('paused');
            // Stop any playing audio
            if (this.currentAudio) {
                this.currentAudio.pause();
            }
            this.synth.cancel();
        } else {
            this.pauseBtn.innerHTML = '⏸ Pause';
            this.pauseBtn.classList.remove('paused');
        }
    }

    previousWord() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.speakCurrentWord();
            this.remainingTime = parseInt(this.intervalInput.value);
        }
    }

    nextWord() {
        if (this.currentIndex < this.selectedWords.length - 1) {
            this.currentIndex++;
            this.speakCurrentWord();
            this.remainingTime = parseInt(this.intervalInput.value);
        } else {
            this.completeDictation();
        }
    }

    repeatWord() {
        const word = this.selectedWords[this.currentIndex];
        this.speak(word);
    }

    stopDictation() {
        if (confirm('Are you sure you want to stop the dictation?')) {
            this.cleanup();
            this.showSettingsPanel();
        }
    }

    completeDictation() {
        this.cleanup();
        this.currentWordText.textContent = 'Dictation Complete!';
        this.wordNumber.textContent = '🎉';
        this.timer.textContent = '✓';

        // Disable navigation buttons
        this.prevBtn.disabled = true;
        this.nextBtn.disabled = true;
        this.pauseBtn.disabled = true;
        this.repeatBtn.disabled = true;
    }

    cleanup() {
        if (this.countdownId) {
            clearInterval(this.countdownId);
            this.countdownId = null;
        }
        if (this.halfwayTimeoutId) {
            clearTimeout(this.halfwayTimeoutId);
            this.halfwayTimeoutId = null;
        }
        // Stop any playing audio
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio.currentTime = 0;
        }
        this.synth.cancel();
    }

    toggleWordList() {
        const isVisible = this.wordList.style.display !== 'none';
        this.wordList.style.display = isVisible ? 'none' : 'block';
        this.toggleListBtn.textContent = isVisible ? 'Show Word List' : 'Hide Word List';
    }

    displayWordList() {
        this.wordListItems.innerHTML = '';
        this.selectedWords.forEach((word, index) => {
            const li = document.createElement('li');
            li.textContent = word;
            li.dataset.index = index;

            // Highlight current word
            if (index === this.currentIndex) {
                li.classList.add('current');
            }

            this.wordListItems.appendChild(li);
        });

        // Update current word highlighting
        setInterval(() => {
            if (!this.isPaused) {
                const items = this.wordListItems.querySelectorAll('li');
                items.forEach((item, index) => {
                    if (index === this.currentIndex) {
                        item.classList.add('current');
                        item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    } else {
                        item.classList.remove('current');
                    }
                });
            }
        }, 100);
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new SpellingDictator();
});
