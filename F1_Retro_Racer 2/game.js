const road = document.getElementById("road");
const car = document.getElementById("car");
const scoreDisplay = document.getElementById("score");
const highScoreDisplay = document.getElementById("highscore");
const themeSelector = document.getElementById("themeSelector");
const music = document.getElementById("bg-music");

let carX = 130;
let score = 0;
let highScore = localStorage.getItem("highscore") || 0;
let gameRunning = true;
let turboActive = false;
let velocidadObstaculos = 3;

highScoreDisplay.textContent = highScore;

function moveLeft() {
  if (carX > 0) {
    carX -= 65;
    car.style.left = carX + "px";
  }
}

function moveRight() {
  if (carX < 260) {
    carX += 65;
    car.style.left = carX + "px";
  }
}

document.addEventListener("keydown", e => {
  if (e.key === "ArrowLeft") moveLeft();
  if (e.key === "ArrowRight") moveRight();
  if (e.key === " ") activateTurbo();
});

function activateTurbo() {
  if (!turboActive) {
    turboActive = true;
    velocidadObstaculos = 6;
    car.style.filter = "drop-shadow(0 0 10px cyan)";
    setTimeout(() => {
      velocidadObstaculos = 3;
      car.style.filter = "none";
      turboActive = false;
    }, 3000);
  }
}

function createObstacle() {
  const obstacle = document.createElement("div");
  obstacle.className = "obstacle";
  obstacle.style.left = `${[0, 130, 260][Math.floor(Math.random() * 3)]}px`;
  road.appendChild(obstacle);

  let posY = -70;
  const interval = setInterval(() => {
    if (!gameRunning) return;
    posY += velocidadObstaculos;
    obstacle.style.top = posY + "px";
    const obstacleRect = obstacle.getBoundingClientRect();
    const carRect = car.getBoundingClientRect();
    if (
      obstacleRect.top < carRect.bottom &&
      obstacleRect.bottom > carRect.top &&
      obstacleRect.left < carRect.right &&
      obstacleRect.right > carRect.left
    ) {
      alert("💥 ¡Choque! Puntaje: " + score);
      if (score > highScore) {
        localStorage.setItem("highscore", score);
      }
      gameRunning = false;
      location.reload();
    }
    if (posY > 500) {
      obstacle.remove();
      score++;
      scoreDisplay.textContent = score;
    }
  }, 20);
}

setInterval(() => {
  if (gameRunning) createObstacle();
}, 1200);

themeSelector.addEventListener("change", () => {
  road.className = "road " + themeSelector.value;
});