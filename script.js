
const canvas = document.getElementById("board");
const ctx = canvas.getContext("2d");
const scoreDisplay = document.getElementById("score");
const message = document.getElementById("message");
const startButton = document.getElementById("start");

const cell = 20;
const count = canvas.width / cell;

let snake, food, dx, dy, score, timer, running;

function resetGame() {
  clearInterval(timer);

  snake = [{ x: 10, y: 10 }];
  dx = 1;
  dy = 0;
  score = 0;
  running = true;
  scoreDisplay.textContent = score;
  message.textContent = "Good luck!";

  placeFood();
  draw();

  timer = setInterval(update, 180);
}

function placeFood() {
  do {
    food = {
      x: Math.floor(Math.random() * count),
      y: Math.floor(Math.random() * count)
    };
  } while (snake.some(part => part.x === food.x && part.y === food.y));
}

function update() {
  if (!running) return;

  const head = {
    x: snake[0].x + dx,
    y: snake[0].y + dy
  };

  const eating = head.x === food.x && head.y === food.y;

  const body = eating ? snake : snake.slice(0, -1);

  if (
    head.x < 0 || head.x >= count ||
    head.y < 0 || head.y >= count ||
    body.some(part => part.x === head.x && part.y === head.y)
  ) {
    running = false;
    clearInterval(timer);
    message.textContent = "Game Over! Press Start to try again.";
    draw();
    return;
  }

  snake.unshift(head);

  if (eating) {
    score++;
    scoreDisplay.textContent = score;
    placeFood();
  } else {
    snake.pop();
  }

  draw();
}

function draw() {
  ctx.fillStyle = "#17251f";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "#ff5c65";
  ctx.fillRect(food.x * cell, food.y * cell, cell - 2, cell - 2);

  snake.forEach((part, index) => {
    ctx.fillStyle = index === 0 ? "#a3ffc1" : "#42d982";
    ctx.fillRect(
      part.x * cell,
      part.y * cell,
      cell - 2,
      cell - 2
    );
  });
}

document.addEventListener("keydown", event => {
  const keys = {
    ArrowUp: [0, -1],
    w: [0, -1],
    ArrowDown: [0, 1],
    s: [0, 1],
    ArrowLeft: [-1, 0],
    a: [-1, 0],
    ArrowRight: [1, 0],
    d: [1, 0]
  };

  const key = event.key.length === 1
    ? event.key.toLowerCase()
    : event.key;

  if (!keys[key]) return;
  event.preventDefault();

  const [newDx, newDy] = keys[key];

  if (newDx !== -dx || newDy !== -dy) {
    dx = newDx;
    dy = newDy;
  }
});

startButton.addEventListener("click", resetGame);

drawInitial();

function drawInitial() {
  snake = [{ x: 10, y: 10 }];
  food = { x: 15, y: 10 };
  dx = 1;
  dy = 0;
  score = 0;
  running = false;
  draw();
}
