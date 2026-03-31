const thaiLetters = [
    { letter: 'ก', hint: 'ไก่' },
    { letter: 'ข', hint: 'ไข่' },
    { letter: 'ค', hint: 'ควาย' },
    { letter: 'ง', hint: 'งู' },
    { letter: 'จ', hint: 'จาน' },
    { letter: 'ฉ', hint: 'ฉิ่ง' },
    { letter: 'ช', hint: 'ชาง' },
    { letter: 'ซ', hint: 'โซ่' },
    { letter: 'ย', hint: 'ยักษ์' },
    { letter: 'ด', hint: 'เด็ก' },
    { letter: 'ต', hint: 'เตา' },
    { letter: 'ถ', hint: 'ถุง' },
    { letter: 'ท', hint: 'ทหาร' },
    { letter: 'ธ', hint: 'ธง' },
    { letter: 'น', hint: 'หนู' },
    { letter: 'บ', hint: 'แบะ' },
    { letter: 'ป', hint: 'ปลา' },
    { letter: 'ผ', hint: 'ผึ้ง' },
    { letter: 'พ', hint: 'พาน' },
    { letter: 'ฟ', hint: 'ฟัน' },
    { letter: 'ม', hint: 'ม้า' },
    { letter: 'ย', hint: 'ยม' },
    { letter: 'ร', hint: 'เรือ' },
    { letter: 'ล', hint: 'ลิง' },
    { letter: 'ว', hint: 'แหวน' },
    { letter: 'ส', hint: 'เสือ' },
    { letter: 'ห', hint: 'หีบ' },
    { letter: 'อ', hint: 'อ่าง' },
];

const thaiWords = [
    { word: 'สนุก', meaning: 'ความสุข' },
    { word: 'เรียน', meaning: 'ศึกษา' },
    { word: 'หนังสือ', meaning: 'เอกสาร' },
    { word: 'ไทย', meaning: 'ประเทศ' },
    { word: 'สวย', meaning: 'งาม' },
    { word: 'ขมัก', meaning: 'เสียบ' },
    { word: 'บ้าน', meaning: 'อาศัย' },
    { word: 'ครอบครัว', meaning: 'ระบบเกาะกลุ่ม' },
    { word: 'ความสุข', meaning: 'ความเกิดสุข' },
    { word: 'ปลา', meaning: 'สัตว์น้ำ' },
];

const game = {
    bestScore: localStorage.getItem('bestScore') ? parseInt(localStorage.getItem('bestScore')) : 0,
    currentScore: 0,
    gameMode: null,
    currentQuestion: 0,
    totalQuestions: 10,
    hintsUsed: 0,

    // จำตัวหนังสือ
    memoryLetters: [],
    memoryAnswer: '',
    memoryHint: null,

    // เรียงตัวหนังสือ
    currentWord: {},
    currentLetters: [],
    selectedLetters: [],
    rearrangeHint: null,

    // หาตัวหนังสือที่หายไป
    missingWord: {},
    missingLetter: '',
    missingChoices: [],

    showScreen(screenId) {
        document.querySelectorAll('.menu-screen, .game-screen').forEach(el => el.style.display = 'none');
        document.getElementById(screenId).style.display = screenId === 'mainMenu' ? 'flex' : 'block';
    },

    backToMenu() {
        this.currentScore = 0;
        this.currentQuestion = 0;
        this.hintsUsed = 0;
        this.showScreen('mainMenu');
        this.updateBestScore();
        document.getElementById('modal').classList.remove('show');
    },

    updateBestScore() {
        document.getElementById('bestScoreDisplay').textContent = this.bestScore;
    },

    clearMessages() {
        document.querySelectorAll('.response-message').forEach(el => el.style.display = 'none');
    },

    // ===== เกมส์จำตัวหนังสือ =====
    startMemoryGame() {
        this.gameMode = 'memory';
        this.currentScore = 0;
        this.currentQuestion = 0;
        this.hintsUsed = 0;
        this.showScreen('memoryScreen');
        this.nextMemoryQuestion();
    },

    nextMemoryQuestion() {
        this.clearMessages();
        document.getElementById('memoryInput').value = '';
        document.getElementById('hintBox').style.display = 'none';
        document.getElementById('hintBtn').disabled = false;

        if (this.currentQuestion >= this.totalQuestions) {
            this.gameOverMemory();
            return;
        }

        this.currentQuestion++;
        document.getElementById('memoryRound').textContent = `${this.currentQuestion}/${this.totalQuestions}`;
        
        // สุ่มตัวหนังสือ 3-5 ตัว
        const count = Math.floor(Math.random() * 3) + 3;
        this.memoryLetters = [];
        for (let i = 0; i < count; i++) {
            const randomLetter = thaiLetters[Math.floor(Math.random() * thaiLetters.length)];
            this.memoryLetters.push(randomLetter);
        }
        this.memoryAnswer = this.memoryLetters.map(l => l.letter).join('');
        this.memoryHint = this.memoryLetters.map(l => l.hint).join(', ');

        this.showLettersAnimated();
    },

    async showLettersAnimated() {
        const display = document.getElementById('lettersDisplay');
        display.textContent = '';
        
        for (let letterObj of this.memoryLetters) {
            await new Promise(resolve => setTimeout(resolve, 300));
            display.textContent += letterObj.letter;
        }

        await new Promise(resolve => setTimeout(resolve, 2000));
        display.textContent = '?';
        document.getElementById('memoryInput').focus();
    },

    checkMemoryAnswer() {
        const input = document.getElementById('memoryInput').value.trim();
        const messageBox = document.getElementById('memoryMessage');

        if (!input) {
            messageBox.textContent = '⚠️ กรุณากรอกตัวหนังสือ';
            messageBox.className = 'response-message wrong';
            messageBox.style.display = 'block';
            return;
        }

        if (input === this.memoryAnswer) {
            this.currentScore += 10;
            messageBox.textContent = '✓ ถูกต้อง!';
            messageBox.className = 'response-message correct';
            document.getElementById('memoryScore').textContent = this.currentScore;
            messageBox.style.display = 'block';
            
            setTimeout(() => this.nextMemoryQuestion(), 1500);
        } else {
            messageBox.textContent = `✗ ผิด! คำตอบคือ: ${this.memoryAnswer}`;
            messageBox.className = 'response-message wrong';
            messageBox.style.display = 'block';
            
            setTimeout(() => this.nextMemoryQuestion(), 2000);
        }
    },

    showHint() {
        document.getElementById('hintText').textContent = this.memoryHint;
        document.getElementById('hintBox').style.display = 'block';
        document.getElementById('hintBtn').disabled = true;
    },

    repeatMemory() {
        if (this.gameMode !== 'memory') return;
        this.clearMessages();
        document.getElementById('memoryInput').value = '';
        document.getElementById('hintBox').style.display = 'none';
        this.showLettersAnimated();
    },

    skipMemory() {
        this.nextMemoryQuestion();
    },

    gameOverMemory() {
        if (this.currentScore > this.bestScore) {
            this.bestScore = this.currentScore;
            localStorage.setItem('bestScore', this.bestScore);
        }
        const stats = `<strong>คะแนน:</strong> ${this.currentScore}<br><strong>สูงสุด:</strong> ${this.bestScore}`;
        this.showGameOver('🎮 เกมส์จบ!', stats);
    },

    // ===== เกมส์เรียงตัวหนังสือ =====
    startRearrangeGame() {
        this.gameMode = 'rearrange';
        this.currentScore = 0;
        this.currentQuestion = 0;
        this.hintsUsed = 0;
        this.showScreen('rearrangeScreen');
        this.nextRearrangeQuestion();
    },

    nextRearrangeQuestion() {
        this.clearMessages();
        document.getElementById('rearrangeHint').style.display = 'none';
        document.getElementById('rearrangeHintBtn').disabled = false;

        if (this.currentQuestion >= this.totalQuestions) {
            this.gameOverRearrange();
            return;
        }

        this.currentQuestion++;
        document.getElementById('rearrangeRound').textContent = `${this.currentQuestion}/${this.totalQuestions}`;
        
        this.currentWord = thaiWords[Math.floor(Math.random() * thaiWords.length)];
        this.currentLetters = this.currentWord.word.split('').sort(() => Math.random() - 0.5);
        this.selectedLetters = [];

        document.getElementById('wordDisplay').textContent = '?'.repeat(this.currentWord.word.length);
        document.getElementById('answerBox').textContent = '-';
        this.renderRearrangeLetters();
    },

    renderRearrangeLetters() {
        const grid = document.getElementById('lettersGrid');
        grid.innerHTML = '';

        this.currentLetters.forEach((letter, index) => {
            const btn = document.createElement('button');
            btn.className = 'letter-btn';
            btn.textContent = letter;
            btn.onclick = () => this.selectRearrangeLetter(index, letter, btn);
            grid.appendChild(btn);
        });
    },

    selectRearrangeLetter(index, letter, btn) {
        this.selectedLetters.push(letter);
        btn.classList.add('used');

        const answer = this.selectedLetters.join('');
        document.getElementById('answerBox').textContent = answer;

        if (answer === this.currentWord.word) {
            this.currentScore += 10;
            const messageBox = document.getElementById('rearrangeMessage');
            messageBox.textContent = '✓ ถูกต้อง!';
            messageBox.className = 'response-message correct';
            messageBox.style.display = 'block';
            document.getElementById('rearrangeScore').textContent = this.currentScore;

            document.querySelectorAll('.letter-btn').forEach(b => b.disabled = true);
            setTimeout(() => this.nextRearrangeQuestion(), 1500);
        }
    },

    resetRearrange() {
        this.selectedLetters = [];
        document.getElementById('answerBox').textContent = '-';
        this.renderRearrangeLetters();
    },

    showRearrangeHint() {
        document.getElementById('rearrangeHintText').textContent = this.currentWord.meaning;
        document.getElementById('rearrangeHint').style.display = 'block';
        document.getElementById('rearrangeHintBtn').disabled = true;
    },

    skipRearrange() {
        const messageBox = document.getElementById('rearrangeMessage');
        messageBox.textContent = `✗ ข้าม! คำตอบคือ: ${this.currentWord.word}`;
        messageBox.className = 'response-message wrong';
        messageBox.style.display = 'block';
        
        setTimeout(() => this.nextRearrangeQuestion(), 1500);
    },

    gameOverRearrange() {
        if (this.currentScore > this.bestScore) {
            this.bestScore = this.currentScore;
            localStorage.setItem('bestScore', this.bestScore);
        }
        const stats = `<strong>คะแนน:</strong> ${this.currentScore}<br><strong>สูงสุด:</strong> ${this.bestScore}`;
        this.showGameOver('🎮 เกมส์จบ!', stats);
    },

    // ===== เกมส์หาตัวหนังสือที่หายไป =====
    startMissingGame() {
        this.gameMode = 'missing';
        this.currentScore = 0;
        this.currentQuestion = 0;
        this.hintsUsed = 0;
        this.showScreen('missingScreen');
        this.nextMissingQuestion();
    },

    nextMissingQuestion() {
        this.clearMessages();
        document.getElementById('missingHint').style.display = 'none';
        document.getElementById('missingHintBtn').disabled = false;

        if (this.currentQuestion >= this.totalQuestions) {
            this.gameOverMissing();
            return;
        }

        this.currentQuestion++;
        document.getElementById('missingRound').textContent = `${this.currentQuestion}/${this.totalQuestions}`;
        
        this.missingWord = thaiWords[Math.floor(Math.random() * thaiWords.length)];
        const wordLetters = this.missingWord.word.split('');
        const randomIndex = Math.floor(Math.random() * wordLetters.length);
        this.missingLetter = wordLetters[randomIndex];

        // สร้างคำที่มีการเว้นตำแหน่ง
        const displayLetters = wordLetters.map((l, i) => i === randomIndex ? '_' : l);
        document.getElementById('missingLetters').innerHTML = displayLetters.map(l => 
            `<span class="blanks">${l}</span>`
        ).join('');

        // สร้างตัวเลือก
        const choices = [this.missingLetter];
        const allLetters = [...new Set(thaiWords.flatMap(w => w.word.split('')))]
        while (choices.length < 4) {
            const randomLetter = allLetters[Math.floor(Math.random() * allLetters.length)];
            if (!choices.includes(randomLetter)) {
                choices.push(randomLetter);
            }
        }
        
        choices.sort(() => Math.random() - 0.5);
        this.missingChoices = choices;
        this.renderMissingChoices();
    },

    renderMissingChoices() {
        const container = document.getElementById('missingChoices');
        container.innerHTML = '';

        this.missingChoices.forEach(letter => {
            const btn = document.createElement('button');
            btn.className = 'choice-btn';
            btn.textContent = letter;
            btn.onclick = () => this.checkMissingLetter(letter, btn);
            container.appendChild(btn);
        });
    },

    checkMissingLetter(letter, btn) {
        const buttons = document.querySelectorAll('.choice-btn');
        buttons.forEach(b => b.disabled = true);

        const messageBox = document.getElementById('missingMessage');

        if (letter === this.missingLetter) {
            btn.classList.add('correct');
            this.currentScore += 10;
            messageBox.textContent = '✓ ถูกต้อง!';
            messageBox.className = 'response-message correct';
            document.getElementById('missingScore').textContent = this.currentScore;
        } else {
            btn.classList.add('wrong');
            buttons.forEach(b => {
                if (b.textContent === this.missingLetter) {
                    b.classList.add('correct');
                }
            });
            messageBox.textContent = `✗ ผิด! ตัวหนังสือที่ถูก: ${this.missingLetter}`;
            messageBox.className = 'response-message wrong';
        }
        messageBox.style.display = 'block';

        setTimeout(() => this.nextMissingQuestion(), 1500);
    },

    showMissingHint() {
        document.getElementById('missingHintText').textContent = this.missingWord.meaning;
        document.getElementById('missingHint').style.display = 'block';
        document.getElementById('missingHintBtn').disabled = true;
    },

    skipMissing() {
        this.nextMissingQuestion();
    },

    gameOverMissing() {
        if (this.currentScore > this.bestScore) {
            this.bestScore = this.currentScore;
            localStorage.setItem('bestScore', this.bestScore);
        }
        const stats = `<strong>คะแนน:</strong> ${this.currentScore}<br><strong>สูงสุด:</strong> ${this.bestScore}`;
        this.showGameOver('🎮 เกมส์จบ!', stats);
    },

    showGameOver(title, stats) {
        document.getElementById('modalTitle').textContent = title;
        document.getElementById('modalStats').innerHTML = stats;
        document.getElementById('modal').classList.add('show');
    }
};

window.onload = () => {
    game.updateBestScore();
    game.backToMenu();
};