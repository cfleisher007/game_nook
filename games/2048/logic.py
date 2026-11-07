import random as rd

class Game2048:
    def __init__(self):
        self.board = [[0 for _ in range(4)] for _ in range(4)]
        for _ in range(2): self.add_new_tile()
        self.score = 0
        self.game_over = False
        self.win = False


    def move(self, direction):
        if direction in ("up", "down"):
            for c in range(4):
                column_list = [self.board[r][c] for r in range(4)]
                column = column_list if direction == "up" else column_list[::-1]
                processed_col, points, check_2048 = Game2048.slide_and_merge_line(column)
                for r in range(4):
                    self.board[r][c] = processed_col[(r if direction == "up" else 3 - r)]
                self.score += points
        else:
            for row_index, row in enumerate(self.board):
                row_list = row if direction == "left" else row[::-1]
                processed_row, points, check_2048 = Game2048.slide_and_merge_line(row_list)
                self.board[row_index] = processed_row if direction == "left" else processed_row[::-1]
                self.score += points

        self.add_new_tile()
        
        game_over = self.is_game_over()
        if game_over:
            self.game_over = True

        if check_2048:
            self.win = True


    def is_game_over(self):
        for row in self.board:
            no_zeros = [box for box in row if box != 0 ]
            if len(no_zeros) < 4:
                return False

        #check each row for possible merges
        for row in self.board:
            processed_row_left, _, _ = Game2048.slide_and_merge_line(row)
            processed_row_right, _, _ = Game2048.slide_and_merge_line(row[::-1])
            if (row != processed_row_left) or (row != processed_row_right[::-1]):
                return False

        # check each column for possible merges
        for c in range(4):
            column_list = [self.board[r][c] for r in range(4)]  
            processed_col_up, _, _ = Game2048.slide_and_merge_line(column_list)
            processed_col_down, _, _ = Game2048.slide_and_merge_line(column_list[::-1]) 
            if (column_list != processed_col_up) or (column_list != processed_col_down[::-1]):
                return False

        return True   


    @staticmethod
    def slide_and_merge_line(line):
        non_zeros = [num for num in line if num != 0]

        points_earned = 0
        check_2048 = False
        merged = []
        skip = False
        for i in range(len(non_zeros)):
            if skip:
                skip = False
                continue
            if i + 1 < len(non_zeros) and non_zeros[i] == non_zeros[i + 1]:
                merge_value = non_zeros[i] * 2
                merged.append(merge_value)
                points_earned += merge_value
                if merge_value == 2048:
                    check_2048 = True
                skip = True
            else:
                merged.append(non_zeros[i])

        while len(merged) < 4:
            merged.append(0)

        return merged, points_earned, check_2048


    def add_new_tile(self):
        empty_boxes = self.get_empty_boxes()

        if len(empty_boxes) == 0:
            return

        #90% chance to add a 2, 10% chance to add a 4
        rdm = rd.randint(1, 100)
        num = 2
        if rdm > 90:
            num = 4

        rd_box = rd.choice(empty_boxes)
        self.board[rd_box[0]][rd_box[1]] = num


    def get_empty_boxes(self):
        empty_boxes = []

        for i, row in enumerate(self.board):
            for j, box in enumerate(row):
                if self.board[i][j] == 0:
                    empty_boxes.append([i, j])

        return empty_boxes