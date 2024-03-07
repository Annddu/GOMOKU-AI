from memory_repository.score import Score
from memory_repository.patern import Pattern

class Board:
    '''
    implement movements on the board
    '''

    def __init__(self, board):
        '''
        initialize Board class
        :param board: a list of 20*20
        '''
        self.board = board
        self.size = len(board)

    def candidates(self, old_pattern, role, last_point):
        '''
        search the most potential positions
        :param old_pattern:  current board pattern
        :param role: AI or Opponent
        :param last_point: the last move of opponent (x,y)
        :return: list contain point and respond new pattern, for example：［(1,1) {[3,2]: 1}］
        '''
        pos = []

        limit = (self.get_limit() + 2) * 2

        directions = self.sort_directions(last_point)
        iteration = 1
        while iteration < limit:
            pos = self.sort_steps(directions, iteration, last_point, old_pattern, role, pos)
            iteration += 1
        pos_list = sorted(pos, key=lambda item: item[1][0], reverse=True)
        pattern_list = [(p[0], p[1][1]) for p in pos_list]
        return pattern_list

    def get_limit(self):
        """
        get the limit of search
        :return: the limit of search
        """	
        rows = [sum(self.board[i]) == 0 for i in range(self.size)]
        cols = [sum(self.board[:][j]) == 0 for j in range(self.size)]
        mid_rows = rows[rows.index(False) + 1:]
        mid_rows.reverse()

        if False in mid_rows:
            limit_rows = mid_rows.index(False)
        else:
            limit_rows = 0

        mid_cols = cols[cols.index(False) + 1:]
        mid_cols.reverse()
        if False in mid_cols:
            limit_cols = mid_cols.index(False)
        else:
            limit_cols = 0
        return max(limit_cols, limit_rows)

    def sort_directions(self, point):
        '''
        search directions with more room near opponent's last move
        :param point: last move (x,y)
        :return: sorted directions dic
        '''
        directions = dict()
        x, y = point
        if x > self.size - x - 1:
            directions["dx"] = (-1, 1)
        else:
            directions["dx"] = (1, -1)
        if y > self.size - y - 1:
            directions["dy"] = (-1, 1)
        else:
            directions["dy"] = (1, -1)
        return directions

    def sort_steps(self, directions, iteration, point, old_pattern, role, pos):
        '''
        for given iteration, search the empty points and score it
        :param directions: the sorted directions define in self.sort_directions
        :param iteration: the total number of steps
        :param point: (x,y) the last movement of opponent
        :param old_pattern: the current board pattern
        :param role: AI or opponent
        :param pos: list to save points which have been searched
        :return:
        '''
        x0, y0 = point

        for x1, y1 in [(x0 + iteration * directions["dx"][0], y0), (x0 + iteration * directions["dx"][1], y0),
                       (x0, y0 + iteration * directions["dy"][0]), (x0, y0 + iteration * directions["dy"][1])]:
            if 0 <= x1 < self.size and 0 <= y1 < self.size and self.board[x1][y1] == 0:
                # choice the position important to both AI and Opponent
                update_AI_pattern = Pattern(self.board).update(old_pattern, (x1, y1), role)
                update_OP_pattern = Pattern(self.board).update(old_pattern, (x1, y1), 3 - role)
                # score = Score(self.board).total_score(update_AI_pattern, role) + Score(self.board).total_score(
                    # update_OP_pattern, 3 - role)
                score = Score(self.board).total_score(update_AI_pattern, role)
                pos.append([(x1, y1), [score, update_AI_pattern]])

        step_x = 1
        while step_x < iteration:
            for dx in directions["dx"]:
                for dy in directions["dy"]:
                    x2 = step_x * dx + x0
                    y2 = (iteration - step_x) * dy + y0
                    if 0 <= x2 < self.size and 0 <= y2 < self.size and self.board[x2][y2] == 0:
                        # choice the position important to both AI and Opponent
                        update_AI_pattern = Pattern(self.board).update(old_pattern, (x2, y2), role)
                        update_OP_pattern = Pattern(self.board).update(old_pattern, (x2, y2), 3 - role)
                        # score = Score(self.board).total_score(update_AI_pattern, role) + Score(self.board).total_score(
                            # update_OP_pattern, 3 - role)
                        score = Score(self.board).total_score(update_AI_pattern, role)
                        pos.append([(x2, y2), [score, update_AI_pattern]])
            step_x += 1
        return pos