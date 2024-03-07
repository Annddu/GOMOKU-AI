import copy
from memory_repository.board import Board
from memory_repository.score import Score

class Kill:
    '''
    implement method to judge the possibility to conduct a kill or to be killed in the future
    '''

    def __init__(self, board, max_depth):
        self.max_depth = max_depth
        self.board = board

    def kill(self, role, kill_pattern, last_point):
        return self.killer(role, kill_pattern, self.max_depth, last_point, 0)

    def check_kill(self, kill_pattern, role):
        '''
        check if the pattern satisfies the kill conditions
        :param kill_pattern: the current pattern to be checked
        :param role: AI or Opponent
        :return: True or False
        '''
        kills = {(4, 1): 0, (3, 2): 0, (3, 2, "S"): 0, (4, 0, "S"): 0, (4, 1, "S"): 0, (4, 2, "S"): 0}
        for key in kill_pattern[role].keys():
            length = key[0]
            if length == 5:
                return True, 3
            if key == (4, 2):
                return True, 2
            if key == (4, 2, "S"):
                return True, 2
            if key in kills.keys():
                kills[key] += kill_pattern[role][key]
        if (kills[(4, 1)] > 0 + kills[(4, 1, "S")] + kills[(4, 0, "S")] > 0) and kills[(4, 1, "S")] + kills[(4, 1)] + \
                kills[(3, 2)] + kills[(3, 2, "S")] + kills[(4, 0, "S")] >= 2:
            return True, 2
        elif kills[(3, 2)] >= 2 or kills[(3, 2, "S")] >= 2:
            return True, 1
        return False, 0

    def killer(self, role, kill_pattern, depth, last_point, kill_score):
        '''
        Judge if the role could conduct a kill
        :param role: AI or Opponent
        :param kill_pattern: the current pattern
        :param depth: the depth have reached
        :param last_point: the last move of opponent
        :return: True(kill successed) or False(kill failed)
        '''

        winner = Score(self.board).checkWinner(kill_pattern)
        if winner == role:
            return True

        elif winner == 3 - role:
            return False

        if depth == 0:
            return False

        # search the most potential positions
        frees = Board(self.board).candidates(kill_pattern, role, last_point)
        for point, next_pattern in frees[:20]:
            x, y = point

            # check if I could conduct a kill
            check, score_new = self.check_kill(next_pattern, role)
            if check and score_new > kill_score:
                # move to the position
                self.board[x][y] = role

                # check if the opponent could conduct a kill(for defense)
                my_kill = not self.killer(3 - role, next_pattern, depth - 1, (x, y), score_new)

                # move back
                self.board[x][y] = 0
                if my_kill:
                    return True
        return False