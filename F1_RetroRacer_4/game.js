const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let jugador = {
  x: 180,
  y: 500,
  ancho: 40,
  alto: 80,
  velocidad: 5,
  turbo: false,
  turboTiempo: 0
};

let teclas = {};
let enemigos = [];
let monedas = [];
let lineas = [];
let velocidadJuego = 4;
let puntaje = 0;
let imagenesEnemigos = ["auto_rojo", "auto_azul", "auto_verde", "auto_amarillo"];
let recogidas = 0;

document.addEventListener("keydown", (e) => teclas[e.key] = true);
document.addEventListener("keyup", (e) => teclas[e.key] = false);

function crearLinea(y) {
  return { x: 195, y: y, largo: 30 };
}

for (let i = 0; i < 20; i++) {
  lineas.push(crearLinea(i * 50));
}

function crearEnemigo() {
  return {
    x: Math.floor(Math.random() * 4) * 100 + 20,
    y: -100,
    ancho: 40,
    alto: 80,
    tipo: imagenesEnemigos[Math.floor(Math.random() * imagenesEnemigos.length)]
  };
}

function crearMoneda() {
  return {
    x: Math.floor(Math.random() * 4) * 100 + 30,
    y: -100,
    radio: 10
  };
}

function activarTurbo() {
  jugador.turbo = true;
  jugador.turboTiempo = 60;
}

function moverJugador() {
  if (teclas["ArrowLeft"] && jugador.x > 0) jugador.x -= jugador.velocidad;
  if (teclas["ArrowRight"] && jugador.x + jugador.ancho < canvas.width) jugador.x += jugador.velocidad;
  if (teclas["ArrowUp"] && jugador.y > 0) jugador.y -= jugador.velocidad;
  if (teclas["ArrowDown"] && jugador.y + jugador.alto < canvas.height) jugador.y += jugador.velocidad;
}

function detectarColision(obj1, obj2) {
  return (
    obj1.x < obj2.x + obj2.ancho &&
    obj1.x + obj1.ancho > obj2.x &&
    obj1.y < obj2.y + obj2.alto &&
    obj1.y + obj1.alto > obj2.y
  );
}

function actualizar() {
  moverJugador();

  if (jugador.turbo) {
    jugador.velocidad = 10;
    jugador.turboTiempo--;
    if (jugador.turboTiempo <= 0) {
      jugador.turbo = false;
      jugador.velocidad = 5;
    }
  }

  lineas.forEach(l => {
    l.y += velocidadJuego;
    if (l.y > canvas.height) l.y = -50;
  });

  if (Math.random() < 0.03) enemigos.push(crearEnemigo());

  enemigos.forEach((e, i) => {
    e.y += velocidadJuego;
    if (detectarColision(jugador, e)) reiniciarJuego();
    if (e.y > canvas.height) enemigos.splice(i, 1);
  });

  if (Math.random() < 0.015) monedas.push(crearMoneda());

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
}

function dibujar() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "#fff";
  lineas.forEach(l => ctx.fillRect(l.x, l.y, 10, l.largo));

  ctx.fillStyle = "#00f";
  ctx.fillRect(jugador.x, jugador.y, jugador.ancho, jugador.alto);

  enemigos.forEach(e => {
    ctx.fillStyle = "#f00";
    ctx.fillRect(e.x, e.y, e.ancho, e.alto);
  });

  ctx.fillStyle = "#ff0";
  monedas.forEach(m => {
    ctx.beginPath();
    ctx.arc(m.x, m.y, m.radio, 0, Math.PI * 2);
    ctx.fill();
  });

  ctx.fillStyle = "#0f0";
  ctx.font = "16px monospace";
  ctx.fillText(`Puntaje: ${puntaje}`, 10, 20);
  ctx.fillText(`Monedas: ${recogidas}`, 10, 40);
}

function reiniciarJuego() {
  jugador.x = 180;
  jugador.y = 500;
  enemigos = [];
  monedas = [];
  puntaje = 0;
  recogidas = 0;
}

function bucle() {
  actualizar();
  dibujar();
  requestAnimationFrame(bucle);
}

bucle();