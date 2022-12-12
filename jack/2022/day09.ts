import { readFileSync } from "fs";

const answer = { part1: 0, part2: 0, }

/** 
 * Board is built by following H and dynamically changing min and max
 * for rows and columns as H moves out of bounds
 * @param {String[]} directions - format: <dir> <distance>
 */
function buildBoard(directions: string[]) {
  let hIy = 0, hIx = 0;
  let hIyMin = 0, hIyMax = 0, hIxMin = 0, hIxMax = 0

  for (const move of directions) {
    const [dir, xy] = move.split(' ')
    const distance = parseInt(xy)
    switch (dir) {
      case 'L':
        hIx = hIx - distance;
        hIxMin = hIx < hIxMin ? hIx : hIxMin
        break;
      case 'R':
        hIx = hIx + distance;
        hIxMax = hIx > hIxMax ? hIx : hIxMax
        break;
      case 'U':
        hIy = hIy - distance;
        hIyMin = hIy < hIyMin ? hIy : hIyMin
        break;
      case 'D':
        hIy = hIy + distance;
        hIyMax = hIy > hIyMax ? hIy : hIyMax
        break;
    }
  }
  const boardW = hIxMax - hIxMin
  const boardH = hIyMax - hIyMin

  const board = []
  for (let i = 0; i < boardH + 1; i++) {
    board[i] = []
    for (let j = 0; j < boardW + 1; j++) {
      board[i][j] = 0;
    }
  }
  //X and Y starting positions
  const sX = Math.abs(hIxMin)
  const sY = Math.abs(hIyMin)
  return { board, sX, sY };
}

function snakeGame(allMoves, board, sX, sY, tailIndex) {
  // Head and Tail(s) indicies
  let hIy = sY, hIx = sX
  const snakeMaker = () => [
    [hIy, hIx], [sY, sX], [sY, sX], [sY, sX], [sY, sX],
    [sY, sX], [sY, sX], [sY, sX], [sY, sX], [sY, sX],
  ]

  let snake = snakeMaker()
  for (const move of allMoves) {
    const [dir, xy] = move.split(' ')
    const distance = parseInt(xy)
    for (let i = 0; i < distance; i++) {
      if (dir === 'L') { snake[0][1]-- }
      if (dir === 'R') { snake[0][1]++ }
      if (dir === 'U') { snake[0][0]-- }
      if (dir === 'D') { snake[0][0]++ }
      for (let i = 0; i < snake.length - 1; i++) {
        //N Direction 
        if ((snake[i][0] - snake[i + 1][0]) === -2) {
          if (snake[i][1] - snake[i + 1][1] > 0) {
            snake[i + 1][1]++
          }
          if (snake[i][1] - snake[i + 1][1] < 0) {
            snake[i + 1][1]--
          }
          snake[i + 1][0]--
        }
        //S Direction
        if ((snake[i][0] - snake[i + 1][0]) === 2) {
          if (snake[i][1] - snake[i + 1][1] > 0) {
            snake[i + 1][1]++
          }
          if (snake[i][1] - snake[i + 1][1] < 0) {
            snake[i + 1][1]--
          }
          snake[i + 1][0]++
        }
        //E direction
        if ((snake[i][1] - snake[i + 1][1]) === 2) {
          if (snake[i][0] - snake[i + 1][0] > 0) {
            snake[i + 1][0]++
          }
          if (snake[i][0] - snake[i + 1][0] < 0) {
            snake[i + 1][0]--
          }
          snake[i + 1][1]++
        }
        // W direction
        if ((snake[i][1] - snake[i + 1][1]) === -2) {
          if (snake[i][0] - snake[i + 1][0] > 0) {
            snake[i + 1][0]++
          }
          if (snake[i][0] - snake[i + 1][0] < 0) {
            snake[i + 1][0]--
          }
          snake[i + 1][1]--
        }
      }
      board[snake[tailIndex][0]][snake[tailIndex][1]] =
        board[snake[tailIndex][0]][snake[tailIndex][1]] + 1;
    }
  }
  return (board
    .map((row) => row.filter((num) => num > 0))
    .reduce((acc, row) => acc + row.length, 0)
  )
}

function day9(filePath: string) {
  const allMoves = readFileSync(filePath).toString().replace(/\n$/, "").split('\n')
  {
    const { board, sX, sY } = buildBoard(allMoves)
    answer.part1 = snakeGame(allMoves, board, sX, sY, 1)
  }
  {
    const { board, sX, sY } = buildBoard(allMoves)
    answer.part2 = snakeGame(allMoves, board, sX, sY, 9)
  }
  console.log(answer)
  return answer;
}

export { day9 }
