const player = document.getElementById("player");
const container = document.querySelector(".game-container");
let score = 0;
let currentLevel = 0;

const gravity = 2;
const jumpForce = 25;
const moveSpeed = 10;
const groundHeight = 40;

let posX = 50;
let posY = 100;
let velocityY = 0;
let jumping = false;
let keys = { left: false, right: false };

const scoreDisplay = document.getElementById("score");

// Niveles
const levels = [{
        platforms: [
            { left: 200, bottom: 150 },
            { left: 400, bottom: 220 }
        ],
        enemies: [
            { left: 600, bottom: 40 }
        ],
        coins: [
            { left: 250, bottom: 170 },
            { left: 420, bottom: 240 }
        ]
    },
    {
        platforms: [
            { left: 150, bottom: 100 },
            { left: 300, bottom: 160 },
            { left: 500, bottom: 200 }
        ],
        enemies: [
            { left: 200, bottom: 40 },
            { left: 550, bottom: 40 }
        ],
        coins: [
            { left: 170, bottom: 120 },
            { left: 320, bottom: 180 },
            { left: 520, bottom: 220 }
        ]
    }
];

// Crear nivel
function cargarNivel(n) {
    container.querySelectorAll(".platform, .enemy, .coin").forEach(el => el.remove());
    const nivel = levels[n];

    nivel.platforms.forEach(p => {
        const el = document.createElement("div");
        el.className = "platform";
        el.style.left = `${p.left}px`;
        el.style.bottom = `${p.bottom}px`;
        container.appendChild(el);
    });

    nivel.enemies.forEach(e => {
        const el = document.createElement("div");
        el.className = "enemy";
        el.style.left = `${e.left}px`;
        el.style.bottom = `${e.bottom}px`;
        container.appendChild(el);
    });

    nivel.coins.forEach(c => {
        const el = document.createElement("div");
        el.className = "coin";
        el.style.left = `${c.left}px`;
        el.style.bottom = `${c.bottom}px`;
        container.appendChild(el);
    });
}

// Colisiones
function checkPlatformCollision() {
    const platforms = document.querySelectorAll(".platform");
    for (const plat of platforms) {
        const platRect = plat.getBoundingClientRect();
        const playerRect = player.getBoundingClientRect();

        if (
            playerRect.bottom >= platRect.top &&
            playerRect.bottom <= platRect.top + 15 &&
            playerRect.right > platRect.left &&
            playerRect.left < platRect.right &&
            velocityY <= 0
        ) {
            posY = container.offsetHeight - plat.offsetTop;
            velocityY = 0;
            jumping = false;
            return;
        }
    }

    // Suelo
    if (posY <= groundHeight) {
        posY = groundHeight;
        velocityY = 0;
        jumping = false;
    }
}

// Lógica principal
function gameLoop() {
    // Movimiento lateral
    if (keys.left && posX > 0) posX -= moveSpeed;
    if (keys.right && posX < container.offsetWidth - player.offsetWidth) posX += moveSpeed;

    // Gravedad
    velocityY -= gravity;
    posY += velocityY;

    // Revisar colisiones
    checkPlatformCollision();

    // Aplicar posición
    player.style.left = `${posX}px`;
    player.style.bottom = `${posY}px`;

    // Enemigos
    document.querySelectorAll(".enemy").forEach(enemy => {
        const rect1 = player.getBoundingClientRect();
        const rect2 = enemy.getBoundingClientRect();
        if (
            rect1.left < rect2.right &&
            rect1.right > rect2.left &&
            rect1.bottom > rect2.top &&
            rect1.top < rect2.bottom
        ) {
            posX = 50;
            posY = 100;
            score = 0;
            scoreDisplay.textContent = score;
            cargarNivel(currentLevel);
        }
    });

    // Monedas
    document.querySelectorAll(".coin").forEach(coin => {
        if (!coin.classList.contains("collected")) {
            const rect1 = player.getBoundingClientRect();
            const rect2 = coin.getBoundingClientRect();
            if (
                rect1.left < rect2.right &&
                rect1.right > rect2.left &&
                rect1.bottom > rect2.top &&
                rect1.top < rect2.bottom
            ) {
                coin.classList.add("collected");
                coin.style.visibility = "hidden";
                score++;
                scoreDisplay.textContent = score;

                if (document.querySelectorAll(".coin:not(.collected)").length === 0) {
                    setTimeout(() => {
                        currentLevel++;
                        if (currentLevel < levels.length) {
                            alert("¡Nivel completado!");
                            posX = 50;
                            posY = 100;
                            cargarNivel(currentLevel);
                        } else {
                            alert("¡Has ganado el juego completo! 🎉");
                            currentLevel = 0;
                            score = 0;
                            scoreDisplay.textContent = score;
                            posX = 50;
                            posY = 100;
                            cargarNivel(currentLevel);
                        }
                    }, 300);
                }
            }
        }
    });

    requestAnimationFrame(gameLoop);
}

// Salto
function jump() {
    if (!jumping) {
        velocityY = jumpForce;
        jumping = true;
    }
}

// Teclado
document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") keys.left = true;
    if (e.key === "ArrowRight") keys.right = true;
    if (e.key === " " || e.key === "ArrowUp") jump();
});
document.addEventListener("keyup", (e) => {
    if (e.key === "ArrowLeft") keys.left = false;
    if (e.key === "ArrowRight") keys.right = false;
});

// Controles táctiles
function setupTouchControls() {
    const leftBtn = document.createElement("button");
    const rightBtn = document.createElement("button");
    const jumpBtn = document.createElement("button");

    leftBtn.innerText = "⬅️";
    rightBtn.innerText = "➡️";
    jumpBtn.innerText = "⬆️";

    leftBtn.className = rightBtn.className = jumpBtn.className = "touch-btn";

    const controls = document.createElement("div");
    controls.className = "touch-controls";
    controls.append(leftBtn, jumpBtn, rightBtn);
    document.body.appendChild(controls);

    leftBtn.ontouchstart = () => keys.left = true;
    leftBtn.ontouchend = () => keys.left = false;

    rightBtn.ontouchstart = () => keys.right = true;
    rightBtn.ontouchend = () => keys.right = false;

    jumpBtn.ontouchstart = () => jump();
}

setupTouchControls();
cargarNivel(currentLevel);
gameLoop();