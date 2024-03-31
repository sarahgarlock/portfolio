let board = [
  ['', '', ''],
  ['', '', ''],
  ['', '', '']
];

let currentPlayer = 'X';
let isGameEnded = false;

function checkWinner() {
  for (let i = 0; i < 3; i++) {
    if (board[i][0] !== '' && board[i][0] === board[i][1] && board[i][0] === board[i][2]) {
      return board[i][0];
    }
    if (board[0][i] !== '' && board[0][i] === board[1][i] && board[0][i] === board[2][i]) {
      return board[0][i];
    }
  }
  if (board[0][0] !== '' && board[0][0] === board[1][1] && board[0][0] === board[2][2]) {
    return board[0][0];
  }
  if (board[0][2] !== '' && board[0][2] === board[1][1] && board[0][2] === board[2][0]) {
    return board[0][2];
  }

  // Draw
  let isDraw = true;
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      if (board[i][j] === '') {
        isDraw = false;
        break;
      }
    }
    if (!isDraw) {
      break;
    }
  }
  if (isDraw) {
    return 'draw';
  }

  return null;
}
function handleMove(row, col) {
  if (board[row][col] === '' && !isGameEnded) {
    board[row][col] = currentPlayer;

    const winner = checkWinner();
    if (winner) {
      isGameEnded = true;
      if (winner === 'draw') {
        alert("It's a draw!");
      } else {
        alert(`Player ${winner} wins!`);
      }
      setTimeout(resetGame, 1000);
    } else {
      currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
    }

    updateDisplay();
    const cellIndex = row * 3 + col;
    const cell = document.querySelectorAll('.cell')[cellIndex];
    cell.style.backgroundColor = 'rgba(231, 237, 60, 0.4)';
  }
}
function computerMove() {
  if (!isGameEnded) {
    let emptyCells = [];
    for (let i = 0; i < 3; i++) {
      for (let j = 0; j < 3; j++) {
        if (board[i][j] === '') {
          emptyCells.push({ row: i, col: j });
        }
      }
    }
    if (emptyCells.length > 0) {
      const randomIndex = Math.floor(Math.random() * emptyCells.length);
      const { row, col } = emptyCells[randomIndex];
      handleMove(row, col);
    }
  }
}
function updateDisplay() {
  const cells = document.querySelectorAll('.cell');
  cells.forEach((cell, index) => {
    const row = Math.floor(index / 3);
    const col = index % 3;
    cell.textContent = board[row][col];
  });
}
function resetGame() {
  board = [
    ['', '', ''],
    ['', '', ''],
    ['', '', '']
  ];
  currentPlayer = 'X';
  isGameEnded = false;
  
  const cells = document.querySelectorAll('.cell');
  cells.forEach(cell => {
    cell.style.backgroundColor = '';
  });
  updateDisplay();
}

updateDisplay();