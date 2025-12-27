// ../memory-cards-game/memory-card-game.js

// ----- Konfigūracija -----

const ALL_CARDS = [
  "apple",
  "bactris-gasipaes",
  "banana",
  "coconut",
  "dragon-fruit",
  "kumquat",
  "papaya",
  "soursop",
  "avocado",
  "maclura",
  "yumberry",
  "tangerine",
  "fig",
  "acai",
  "wax-apple",
  "guarana",
  "strawberry",
  "candied-fruit",
  "pitahaya",
  "strawberry_2",
  "raspberry",
  "lime",
  "orange",
  "vanil",
  "group",
  "wat",
  "melo",
  "citr",
  "che",
  "avo",
  "org",
  "ann",
];

// poros + stulpelių skaičius + kortelės px
const DIFFICULTY = {
  easy: { pairs: 8, cols: 4, cardSize: 120 }, // 4×4
  medium: { pairs: 18, cols: 6, cardSize: 110 }, // 6×6
  hard: { pairs: 32, cols: 8, cardSize: 90 }, // 8×8
};

// ----- DOM -----

const gameBoard = document.querySelector(".game-board");
const difficultyButtons = document.querySelectorAll(".diff-btn");
const timeEl = document.getElementById("time");
const movesEl = document.getElementById("moves");
const bestEl = document.getElementById("best");
const restartBtn = document.getElementById("restart");
const statusEl = document.getElementById("status");

// ----- State -----

let currentDiff = "easy";
let cards = [];
let firstCard = null;
let secondCard = null;
let lock = false;
let moves = 0;
let matchedPairs = 0;
let totalPairs = 0;

let startTime = null;
let timerInterval = null;

// ----- Init -----

init();

function init() {
  // difficulty mygtukai
  difficultyButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      difficultyButtons.forEach((b) => b.classList.remove("is-active"));
      btn.classList.add("is-active");
      currentDiff = btn.dataset.diff;
      startNewGame();
    });
  });

  // restart
  if (restartBtn) {
    restartBtn.addEventListener("click", () => {
      startNewGame();
      announce("Žaidimas pradėtas iš naujo.");
    });
  }

  startNewGame();
}

// ----- Naujas žaidimas -----

function startNewGame() {
  const { pairs, cols, cardSize } = DIFFICULTY[currentDiff];

  totalPairs = pairs;
  matchedPairs = 0;
  moves = 0;
  movesEl.textContent = "0";

  stopTimer(true);
  startTime = null;
  timeEl.textContent = "00:00";

  // lenta pagal lygį
  gameBoard.style.gridTemplateColumns = `repeat(${cols}, ${cardSize}px)`;
  gameBoard.style.setProperty("--card-size", `${cardSize}px`);

  // pasirenkam korteles
  const selectedNames = ALL_CARDS.slice(0, pairs);
  cards = shuffle([...selectedNames, ...selectedNames]).map((name) => ({
    name,
    img: `../memory-cards-game/img/${name}.png`,
  }));

  renderBoard();
  loadBestTime();
  announce(`Lygis: ${getDiffLabel(currentDiff)}. Žaidimas iš naujo.`);
}

// ----- Lentos atvaizdavimas -----

function renderBoard() {
  gameBoard.innerHTML = "";

  cards.forEach((card) => {
    const el = document.createElement("button");
    el.type = "button";
    el.className = "g-card";
    el.dataset.name = card.name;
    el.setAttribute("role", "gridcell");
    el.setAttribute("aria-label", "Paslėpta kortelė");

    el.innerHTML = `
      <div class="g-card-inner">
        <div class="g-card-front"></div>
        <div class="g-card-back">
          <img src="${card.img}" alt="${card.name}" />
        </div>
      </div>
    `;

    el.addEventListener("click", () => handleFlip(el));
    gameBoard.appendChild(el);
  });
}

// ----- Žaidimo logika -----

function handleFlip(cardEl) {
  if (lock) return;
  if (cardEl === firstCard) return;

  if (!startTime) startTimer();

  cardEl.classList.add("flipped");

  if (!firstCard) {
    firstCard = cardEl;
    return;
  }

  secondCard = cardEl;
  moves++;
  movesEl.textContent = String(moves);

  checkMatch();
}

function checkMatch() {
  const isMatch = firstCard.dataset.name === secondCard.dataset.name;

  if (isMatch) {
    firstCard.setAttribute(
      "aria-label",
      `${firstCard.dataset.name}, rasta pora`
    );
    secondCard.setAttribute(
      "aria-label",
      `${secondCard.dataset.name}, rasta pora`
    );

    matchedPairs++;
    resetSelection();

    if (matchedPairs === totalPairs) {
      const elapsed = stopTimer();
      saveBest(elapsed);
      announce(`Pergalė! Laikas: ${formatTime(elapsed)}, ėjimai: ${moves}.`);
    }
  } else {
    lock = true;
    setTimeout(() => {
      firstCard.classList.remove("flipped");
      secondCard.classList.remove("flipped");
      firstCard.setAttribute("aria-label", "Paslėpta kortelė");
      secondCard.setAttribute("aria-label", "Paslėpta kortelė");
      resetSelection();
      lock = false;
    }, 650);
  }
}

function resetSelection() {
  firstCard = null;
  secondCard = null;
}

// ----- Laikmatis / geriausias laikas -----

function startTimer() {
  startTime = performance.now();
  timerInterval = setInterval(() => {
    const ms = performance.now() - startTime;
    timeEl.textContent = formatTime(ms);
  }, 100);
}

function stopTimer(onlyClear = false) {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
  if (!onlyClear && startTime) {
    const ms = performance.now() - startTime;
    startTime = null;
    return ms;
  }
  startTime = null;
  return 0;
}

function formatTime(ms) {
  const totalSec = Math.floor(ms / 1000);
  const m = String(Math.floor(totalSec / 60)).padStart(2, "0");
  const s = String(totalSec % 60).padStart(2, "0");
  return `${m}:${s}`;
}

function bestKey() {
  return `mem_best_time_ms_${currentDiff}`;
}

function loadBestTime() {
  const best = localStorage.getItem(bestKey());
  bestEl.textContent = best ? formatTime(+best) : "—";
}

function saveBest(ms) {
  const key = bestKey();
  const best = localStorage.getItem(key);
  if (!best || ms < +best) {
    localStorage.setItem(key, String(ms));
    bestEl.textContent = formatTime(ms);
  }
}

// ----- Pagalbinės -----

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function announce(msg) {
  if (statusEl) statusEl.textContent = msg;
}

function getDiffLabel(diff) {
  switch (diff) {
    case "easy":
      return "Lengvas";
    case "medium":
      return "Vidutinis";
    case "hard":
      return "Sunkus";
    default:
      return diff;
  }
}
