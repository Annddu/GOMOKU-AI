import operator

from memory_repository.board import Board
from memory_repository.patern import Pattern
from memory_repository.score import Score
from service.utils import Kill

class MinMax:
    '''
    Implement minMax algorithm
    '''

    def __init__(self, board_MinMax):
        '''
        configure parameters
        :param board 20*20 list
        '''
        self.board = board_MinMax
        self.size = len(board_MinMax)
        #hard#######################
        #self.max_depth = 5
        #self.kill_depth = 15
        ##############################
        #imposible###################
        self.max_depth = 3
        self.kill_depth = 5
        ##############################
        self.last_point = (int(self.size / 2), int(self.size / 2))
        self.role = 1
        self.move = (0, 0)
        self.Kill = Kill(self.board, self.kill_depth)
        self.Score = Score(self.board)
        self.Pattern = Pattern(self.board)
        self.Board_ = Board(self.board)
        self.pattern = self.Pattern.get_total_pattern(self.role)
        self.transposition_table = dict()

    def __getitem__(self, point):
        '''
        class could be called from outside
        :param point:
        :return:
        '''
        i, j = point
        return self.board[j][i]

    def __setitem__(self, point, role):
        '''
        class.board value could be set from outside
        :param point:  coordinate(x,y) convert to list[y][x]
        :param role: AI or opponent
        :return:
        '''
        i, j = point
        self.board[j][i] = role
        self.pattern = self.Pattern.update(self.pattern, (j, i), role)
        self.role = 3 - role
        self.last_point = (j, i)
        # print("last_point" + str(self.last_point))

    def difficulty(self, level):
        if level == 1:
            self.max_depth = 4
            self.kill_depth = 20
        elif level == 2:
            self.max_depth = 5
            self.kill_depth = 30
        elif level == 3:
            self.max_depth = 6
            self.kill_depth = 40
        
    def reset(self):
        '''
        reset the all to start
        :return:
        '''
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.__init__(self.board)
    
    def check_draw(self):
        '''
        Check if the game is a draw
        :return: True if the game is a draw, False otherwise
        '''
        board = self.board
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == 0:
                    return False
        return True  # Return True if the board is full
      
    def check_win(self, player):
        '''	
        Check if the player has won the game
        :param player: 1 for AI, 2 for opponent
        :return: True if the player has won the game, False otherwise
        '''
        board = self.board
        for i in range(19):
            for j in range(19):
                if j < 15 and all(board[i][j+k] == player for k in range(5)):
                    return True
                if i < 15 and all(board[i+k][j] == player for k in range(5)):
                    return True
                if i < 15 and j < 15 and all(board[i+k][j+k] == player for k in range(5)):
                    return True
                if i < 15 and j >= 4 and all(board[i+k][j-k] == player for k in range(5)):
                    return True
        return False  # Return False if no win condition is found in the entire board
    
    def find_winning_move(self, player):
        '''
        Find a winning move if it exists
        :return: (x, y) coordinates of the winning move, None otherwise
        '''
        board = self.board
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == 0:  # Check only empty spots
                    # Temporarily make the move
                    board[i][j] = player
                    if self.check_win(player):  # Check if the move is a winning move
                        return (i, j)
                    # Undo the move
                    board[i][j] = 0
        return None  # Return None if no winning move is found
        
    def check_if_move_is_available(self, x, y):
        board = self.board
        if x < 0 or x > 19 or y < 0 or y > 19:
            return False
        if board[x][y] == 0:
            return True
        return False
    
    def min_max(self):
            # If the board is empty, return the coordinate in the center of the board
            if operator.eq(self.board, [[0 for _ in range(self.size)] for _ in range(self.size)]):
                self.move = int(self.size / 2 ), int(self.size / 2 )
                return self.move[1], self.move[0]
            
            # Check for a winning move
            winning_move = self.find_winning_move(1)
            if winning_move is not None:
                return winning_move[1], winning_move[0]
            else: 
                losing_move = self.find_winning_move(2)
                if losing_move is not None:
                    return losing_move[1], losing_move[0]
            
            # Implememt negative_max algorithm
            self.negamax(self.max_depth, alpha=-float("inf"), beta=float("inf"), role=self.role,
                        pattern=self.pattern, last_point=self.last_point)
            return self.move[1], self.move[0]

    def negamax(self, depth, alpha, beta, role, pattern, last_point):
        '''
        implemet negative_max method, which have the same rule as the Min_Max method
        :param depth: define max_depth of min_max search, must be odd, for example: 5
        :param alpha: the alpha value for alpha beta pruning
        :param beta: the beta value for alpha beta pruning
        :param role: AI (role)or Opponent(3-role)
        :param pattern: A dict save the board pattern message
        :param last_point: the last move position of opponent
        :return: in the end of alpha_beta search, return nothing, but define self.move during search process
        '''
        if depth == 0:
            return self.Score.total_score(pattern, role)

        # search the most potential positions
        free = self.Board_.candidates(pattern, role, last_point)
        candidates = []
        count = 0
        if depth == self.max_depth:
            while len(candidates) < 3 and count < 10 and count < len(free):
                point, new_pattern = free[count]
                x, y = point
                self.board[x][y] = role
                kill_opponent = self.Kill.kill(3 - role, new_pattern, point)
                self.board[x][y] = 0
                if not kill_opponent:
                    candidates.append(free[count])
                count += 1
        else:
            candidates = free[:2]
        # if have no candidates to defend, return first point directly
        if len(candidates) == 0:
            candidates = free[:1]

        iteration = 0
        value = -99999
        for point, new_pattern in candidates:
            x, y = point
            self.board[x][y] = role
            # print(iteration)
            v_new = -self.negamax(depth - 1, -beta, -alpha, 3 - role, new_pattern, (x, y))
            if v_new > value:
                value = v_new
            self.board[x][y] = 0
            alpha_old =  alpha
            alpha = max(alpha, value)

            # do alpha_beta pruning
            if value > alpha_old:
                if depth == self.max_depth:
                    self.move = (x, y)
            if alpha >= beta:
                break
        return value

    def get_key(self):
        key = ""
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y]=="1":
                    key += "1"
                elif self.board[x][y]=="2":
                    key += "2"
                else:
                    key += "0"
        return key


# board_initialize = [[0 for _ in range(20)] for _ in range(20)]
# board = MinMax(board_initialize)

class TTEntry:
    def __init__(self, value=0, depth=0, flag=""):
        self.value = value
        self.depth = depth
        self.flag = flag
