const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

canvas.width = 400;
canvas.height = 600;

// Variables del juego
let jugador = { x: 180, y: 500, width: 40, height: 70, speed: 5 };
let enemigos = [];
let monedas = [];
let decoracion = [];
let score = 0;
let record = localStorage.getItem('record') || 0;
let turbo = false;
let turboTimer = 0;

// Imágenes
const imgJugador = new Image();
imgJugador.src = 'img/f1_rojo.png';

const imgEnemigo = new Image();
imgEnemigo.src = 'img/f1_amarillo.png';

// Entradas
let keys = {};
document.addEventListener('keydown', e => keys[e.key] = true);
document.addEventListener('keyup', e => keys[e.key] = false);

// Crear enemigos
function crearEnemigo() {
    enemigos.push({
        x: Math.random() * (canvas.width - 40),
        y: -70,
        width: 40,
        height: 70,
        speed: 3 + Math.random() * 2
    });
}

// Crear monedas
function crearMoneda() {
    monedas.push({
        x: Math.random() * (canvas.width - 20),
        y: -20,
        radius: 10,
        speed: 3
    });
}

// Crear decoraciones
function crearDecoracion() {
    decoracion.push({
        x: Math.random() < 0.5 ? 5 : canvas.width - 15,
        y: -20,
        width: 10,
        height: 20,
        speed: 4
    });
}

// Movimiento y lógica
function update() {
    // Movimiento
    if (keys['ArrowLeft']) jugador.x -= jugador.speed;
    if (keys['ArrowRight']) jugador.x += jugador.speed;
    if (keys['ArrowUp']) jugador.y -= jugador.speed;
    if (keys['ArrowDown']) jugador.y += jugador.speed;

    // Turbo
    if (keys[' '] && turboTimer <= 0) {
        turbo = true;
        turboTimer = 100;
    }

    if (turbo) {
        jugador.speed = 10;
        turboTimer--;
        if (turboTimer <= 0) {
            turbo = false;
            jugador.speed = 5;
        }
    }

    // Limitar bordes
    jugador.x = Math.max(0, Math.min(canvas.width - jugador.width, jugador.x));
    jugador.y = Math.max(0, Math.min(canvas.height - jugador.height, jugador.y));

    // Actualizar enemigos
    enemigos.forEach(e => e.y += e.speed);
    enemigos = enemigos.filter(e => e.y < canvas.height);

    // Colisiones
    enemigos.forEach(e => {
        if (colision(jugador, e)) reiniciarJuego();
    });

    // Actualizar monedas
    monedas.forEach(m => m.y += m.speed);
    monedas = monedas.filter(m => m.y < canvas.height);

    monedas.forEach((m, i) => {
        if (colisionCirculo(jugador, m)) {
            monedas.splice(i, 1);
            score += 5;
        }
    });

    // Decoración
    decoracion.forEach(d => d.y += d.speed);
    decoracion = decoracion.filter(d => d.y < canvas.height);

    // Aumentar score
    score++;
    if (score > record) {
        record = score;
        localStorage.setItem('record', record);
    }

    // Generar nuevos objetos
    if (Math.random() < 0.015) crearEnemigo();
    if (Math.random() < 0.02) crearMoneda();
    if (Math.random() < 0.1) crearDecoracion();
}

// Detección de colisiones
function colision(a, b) {
    return a.x < b.x + b.width &&
        a.x + a.width > b.x &&
        a.y < b.y + b.height &&
        a.y + a.height > b.y;
}

function colisionCirculo(a, c) {
    const dx = (a.x + a.width / 2) - (c.x + c.radius);
    const dy = (a.y + a.height / 2) - (c.y + c.radius);
    return Math.sqrt(dx * dx + dy * dy) < c.radius + a.width / 2;
}

// Dibujar todo
function draw() {
    ctx.fillStyle = "#111";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Decoración
    ctx.fillStyle = "lime";
    decoracion.forEach(d => ctx.fillRect(d.x, d.y, d.width, d.height));

    // Jugador
    ctx.drawImage(imgJugador, jugador.x, jugador.y, jugador.width, jugador.height);

    // Enemigos
    enemigos.forEach(e => {
        ctx.drawImage(imgEnemigo, e.x, e.y, e.width, e.height);
    });

    // Monedas
    ctx.fillStyle = "yellow";
    monedas.forEach(m => {
        ctx.beginPath();
        ctx.arc(m.x + m.radius, m.y + m.radius, m.radius, 0, Math.PI * 2);
        ctx.fill();
    });

    // Texto
    ctx.fillStyle = "white";
    ctx.font = "16px monospace";
    ctx.fillText(`Puntaje: ${score}`, 10, 20);
    ctx.fillText(`Récord: ${record}`, 10, 40);
    if (turbo) ctx.fillText("🚀 TURBO", canvas.width - 100, 20);
}

// Loop del juego
function loop() {
    update();
    draw();
    requestAnimationFrame(loop);
}

loop();