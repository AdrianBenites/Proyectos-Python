const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Jugador
let jugador = {
    x: 180,
    y: 500,
    ancho: 40,
    alto: 80,
    velocidad: 5,
    turbo: false,
    turboTiempo: 0,
    imagen: new Image()
};
jugador.imagen.src = "img/auto_rojo.png";

// Control
let teclas = {};
let enemigos = [];
let monedas = [];
let puntaje = 0;
let recogidas = 0;
let velocidadJuego = 4;
const sonidos = {
    turbo: new Audio("musica/turbo.wav"),
};

const enemigosImgs = [
    "auto_azul.png",
    "auto_verde.png",
    "auto_amarillo.png",
    "auto_morado.png",
    "auto_gris.png"
];

// Eventos teclado
document.addEventListener("keydown", (e) => teclas[e.key] = true);
document.addEventListener("keyup", (e) => teclas[e.key] = false);

// Cambiar tema
function cambiarTema() {
    const selector = document.getElementById("temaSelector");
    document.getElementById("temaCSS").href = "temas/" + selector.value;
}

// Turbo
function activarTurbo() {
    if (!jugador.turbo) {
        jugador.turbo = true;
        jugador.turboTiempo = 60;
        jugador.velocidad = 10;
        sonidos.turbo.play();
    }
}

// Crear enemigo
function crearEnemigo() {
    const img = new Image();
    img.src = "img/" + enemigosImgs[Math.floor(Math.random() * enemigosImgs.length)];
    return {
        x: Math.floor(Math.random() * 4) * 100 + 20,
        y: -100,
        ancho: 40,
        alto: 80,
        imagen: img
    };
}

// Crear moneda
function crearMoneda() {
    return {
        x: Math.floor(Math.random() * 4) * 100 + 30,
        y: -100,
        radio: 10
    };
}

// Movimiento del jugador
function moverJugador() {
    if (teclas["ArrowLeft"] && jugador.x > 0) jugador.x -= jugador.velocidad;
    if (teclas["ArrowRight"] && jugador.x + jugador.ancho < canvas.width) jugador.x += jugador.velocidad;
    if (teclas["ArrowUp"] && jugador.y > 0) jugador.y -= jugador.velocidad;
    if (teclas["ArrowDown"] && jugador.y + jugador.alto < canvas.height) jugador.y += jugador.velocidad;
}

// Colisión
function detectarColision(a, b) {
    return (
        a.x < b.x + b.ancho &&
        a.x + a.ancho > b.x &&
        a.y < b.y + b.alto &&
        a.y + a.alto > b.y
    );
}

// Actualizar
function actualizar() {
    moverJugador();

    if (jugador.turbo) {
        jugador.turboTiempo--;
        if (jugador.turboTiempo <= 0) {
            jugador.turbo = false;
            jugador.velocidad = 5;
        }
    }

    // Enemigos
    if (Math.random() < 0.025) enemigos.push(crearEnemigo());
    enemigos.forEach((e, i) => {
        e.y += velocidadJuego;
        if (detectarColision(jugador, e)) reiniciarJuego();
        if (e.y > canvas.height) enemigos.splice(i, 1);
    });

    // Monedas
    if (Math.random() < 0.01) monedas.push(crearMoneda());
    monedas.forEach((m, i) => {
        m.y += velocidadJuego;
        if (
            jugador.x < m.x + m.radio &&
            jugador.x + jugador.ancho > m.x - m.radio &&
            jugador.y < m.y + m.radio &&
            jugador.y + jugador.alto > m.y - m.radio
        ) {
            puntaje += 10;
            recogidas++;
            monedas.splice(i, 1);
        }
        if (m.y > canvas.height) monedas.splice(i, 1);
    });

    document.getElementById("puntaje").textContent = `Puntaje: ${puntaje}`;
    document.getElementById("monedas").textContent = `Monedas: ${recogidas}`;
}

// Dibujar
function dibujar() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(jugador.imagen, jugador.x, jugador.y, jugador.ancho, jugador.alto);

    enemigos.forEach(e => {
        ctx.drawImage(e.imagen, e.x, e.y, e.ancho, e.alto);
    });

    monedas.forEach(m => {
        ctx.fillStyle = "yellow";
        ctx.beginPath();
        ctx.arc(m.x, m.y, m.radio, 0, Math.PI * 2);
        ctx.fill();
    });
}

// Reiniciar juego
function reiniciarJuego() {
    jugador.x = 180;
    jugador.y = 500;
    enemigos = [];
    monedas = [];
    puntaje = 0;
    recogidas = 0;
}

// Bucle
function bucle() {
    actualizar();
    dibujar();
    requestAnimationFrame(bucle);
}

bucle();