class Game2048{
    constructor(newGame, board, score) {
        if (newGame)
        {
            this.board = Array.from({length: 4}, () => Array(4).fill(0));
            for(let i = 0; i < 2; i++)
                this.addNewTile();
            this.score = 0;
        }       
        else{
            this.board = board;
            this.score = score;
        }
        this.gameOver = false;
        this.won = false;
    }

    move(direction) {
        let hasMoved = false;

        if (["up", "down"].includes(direction)) {
            for (let col = 0; col < this.board[0].length; col++) {
                const columnList = this.board.map(row => row[col]);
                const column = direction === "up" ? columnList : columnList.toReversed();
                const [processedCol, points, check2048] = Game2048.slideAndMergeLine(column);
                for (let row = 0; row < this.board.length; row++) 
                    this.board[row][col] = processedCol[direction === "up" ? row : 3 - row];
                this.score += points;

                if (check2048) 
                    this.win = true;

                const newCol = this.board.map(row => row[col]);
                if (JSON.stringify(columnList) !== JSON.stringify(newCol))
                    hasMoved = true;
            }
        }
    
        else {
            for (let row = 0; row < this.board.length; row++) {
                const oldRow = this.board[row];
                const rowList = direction === "left" ? this.board[row] : this.board[row].toReversed();
                const [processedRow, points, check2048] = Game2048.slideAndMergeLine(rowList);
                this.board[row] = direction === "left" ? processedRow : processedRow.toReversed();
                this.score += points;

                if (JSON.stringify(oldRow) !== JSON.stringify(this.board[row]))
                    hasMoved = true

                if (check2048)
                    this.win = true;
            }
        }
        
        if (hasMoved)
            this.addNewTile();

        const isGameOver = this.isGameOver();
        if (isGameOver)
            this.gameOver = true;
    }

    isGameOver() {
        for (let row = 0; row < this.board.length; row++) {
            const noZeros = this.board[row].filter(box => box !== 0);
            if (noZeros.length < 4)
                return false;
        }

        //check each row for possible merges
        for (let row = 0; row < this.board.length; row++) {
            const [processedRowLeft, , ] = Game2048.slideAndMergeLine(this.board[row]);
            const [processedRowRight, , ] = Game2048.slideAndMergeLine(this.board[row].toReversed());

            if ((JSON.stringify(this.board[row]) !== JSON.stringify(processedRowLeft)) || JSON.stringify(this.board[row]) !== JSON.stringify(processedRowRight.toReversed()))
                return false;
        }

        //check each column for possible merges
        for (let col = 0; col < this.board[0].length; col++) {
            const columnList = this.board.map(row => row[col]);
            const [processedColUp, , ] = Game2048.slideAndMergeLine(columnList);
            const [processedColDown, , ] = Game2048.slideAndMergeLine(columnList.toReversed());
            if ((JSON.stringify(columnList ) !== JSON.stringify(processedColUp)) || (JSON.stringify(columnList) !== JSON.stringify(processedColDown).toReversed()))
                return false;
        }

        return true;
    }

    static slideAndMergeLine(line) {
        const nonZeros = line.filter(box => box !== 0);

        let pointsEarned = 0;
        let check2048 = false;
        let merged = [];
        let skip = false;

        for (let index = 0; index < nonZeros.length; index++) {
            if (skip) {
                skip = false;
                continue;
            }
            if ((index + 1 < nonZeros.length) && (nonZeros[index] === nonZeros[index + 1])) {
                const mergeValue = nonZeros[index] * 2;
                merged.push(mergeValue);
                pointsEarned += mergeValue;
                if (mergedValue === 2048)
                    check2048 = true;
                skip = true;
            }
            else 
                merged.push(nonZeros[index]);
        }

        while (merged.length < 4)
            merged.push(0);

        return [merged, pointsEarned, check2048];
    }

    addNewTile() {
        const emptyBoxes = this.getEmptyBoxes();

        if (emptyBoxes.length === 0)
            return;

        //90% chance to add a 2, 10% chanced to add a 4
        const num = Math.random() < 0.9 ? 2 : 4;

        const randomBox = emptyBoxes[Math.floor(Math.random() * emptyBoxes.length)];
        this.board[randomBox[0]][randomBox[1]] = num;
    }

    getEmptyBoxes() {
        let emptyBoxes = [];

        for (let row = 0; row < this.board.length; row++) {
            for (let col = 0; col < this.board[0].length; col++) {
                if (this.board[row][col] === 0)
                    emptyBoxes.push([row, col]);
            }
        }

        return emptyBoxes;
    }

}


function renderBoard() {
    let game;
    if (!savedGameData) 
    {
        game = new Game2048(true);
    }
    else
    {
        game = new Game2048(false, savedGameData.board, savedGameData.score);
    }

    drawBoard();
}

function drawBoard() {
    const cells = document.querySelectorAll(".board-cell-2048");

    for (let row = 0; row < 4; row++) {
        for (let col = 0; col < 4; col++) {
            const index = row * 4 + col;
            const value = game.board[row][col];
            cells[index].textContent = value === 0 ? "" : value;
        }
    }
}

document.addEventListener("keydown", function(event) {
    if (event.key === "ArrowUp") {
        event.preventDefault();
        game.move("up");
        drawBoard();
    }
    else if (event.key === "ArrowDown") {
        event.preventDefault();
        game.move("down");
        drawBoard();
    }
    else if (event.key === "ArrowRight") {
        event.preventDefault();
        game.move("right");
        drawBoard();
    }
    else if(event.key === "ArrowLeft") {
        event.preventDefault();
        game.move("left");
        drawBoard();
    }
});

document.getElementById("new-game-btn").addEventListener("click", function() {
    fetch("/delete-game-save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({game_name: "2048"})
    });

    renderBoard();
});
