from memory_repository.board import Board
from memory_repository.patern import Pattern
from memory_repository.score import Score
from service.utils import *
from service.minMax import *
import unittest

class TestBoard(unittest.TestCase):
    def setUp(self):
        # You can initialize any necessary objects or variables here
        self.board = [[0] * 20 for _ in range(20)]
        self.test_board = Board(self.board)

    def test_init(self):
        self.assertEqual(self.test_board.board, self.board)
        self.assertEqual(self.test_board.size, 20)

    def test_sort_directions(self):
        # Test sort_directions when the point is closer to the left and upper boundaries
        self.assertEqual(self.test_board.sort_directions((5, 5)), {"dx": (1, -1), "dy": (1, -1)})

        # Test sort_directions when the point is closer to the right and lower boundaries
        self.assertEqual(self.test_board.sort_directions((15, 15)), {"dx": (-1, 1), "dy": (-1, 1)})
    
class TestScore(unittest.TestCase):
    def setUp(self):
        self.board = [[0] * 20 for _ in range(20)]
        self.size = len(self.board)
    
    def test_checkWinner(self):
        # Test checkWinner when there is no winner
        self.score = Score(self.board)
        self.assertEqual(self.score.checkWinner({1: {}, 2: {}}), 0)
        
        # Test checkWinner when AI wins
        self.score = Score(self.board)
        self.assertEqual(self.score.checkWinner({1: {(5, 5): 1}, 2: {}}), 1)
        
        # Test checkWinner when opponent wins
        self.score = Score(self.board)
        self.assertEqual(self.score.checkWinner({1: {}, 2: {(5, 5): 1}}), 2)

class TestBoard(unittest.TestCase):

    # def test_candidates(self):
    #     board = [[0] * 20 for _ in range(20)]
    #     test_board = Board(board)
    #     old_pattern = {}
    #     role = 1
    #     last_point = (10, 10)
        
    def test_get_limit(self):
        board = [[0] * 20 for _ in range(20)]
        test_board = Board(board)
        

    def test_sort_directions(self):
        board = [[0] * 20 for _ in range(20)]
        test_board = Board(board)
        point = (10, 10)
        result = test_board.sort_directions(point)
        

    # def test_sort_steps(self):
    #     board = [[0] * 20 for _ in range(20)]
    #     test_board = Board(board)
    #     directions = {'dx': (1, -1), 'dy': (1, -1)}
    #     iteration = 2
    #     last_point = (10, 10)
    #     old_pattern = {}
    #     role = 1
    #     pos = []
        

class TestPattern(unittest.TestCase):

    def test_get_total_pattern(self):
        board = [[0] * 20 for _ in range(20)]
        test_pattern = Pattern(board)
        role = 1
        result = test_pattern.get_total_pattern(role)
        assert result == {1: {}, 2: {}}
        

    def test_get_pattern(self):
        board = [[0] * 20 for _ in range(20)]
        test_pattern = Pattern(board)
        role = 1
        result = test_pattern.get_pattern(role)
        assert result == {}
       

    def test_direct_search(self):
        board = [[0] * 20 for _ in range(20)]
        test_pattern = Pattern(board)
        point = (10, 10)
        direct = (1, 1)
        role = 1
        direct_pattern = {}
        result = test_pattern.direct_search(point, direct, role, direct_pattern)
        assert result == {}

class TestScore(unittest.TestCase):

    def test_checkWinner(self):
        board = [[0] * 20 for _ in range(20)]
        test_score = Score(board)
        check_pattern = {1: {(5, 0): 1}, 2: {}}
        result = test_score.checkWinner(check_pattern)
        assert result == 1

    def test_total_score(self):
        board = [[0] * 20 for _ in range(20)]
        test_score = Score(board)
        total_pattern = {1: {(3, 1): 1}, 2: {}}
        role = 1
        result = test_score.total_score(total_pattern, role)
        #assert result == 1

    def test_get_score(self):
        board = [[0] * 20 for _ in range(20)]
        test_score = Score(board)
        score_pattern = {(3, 1): 1}
        result = test_score.get_score(score_pattern)
        assert result == 1

class TestPlayer(unittest.TestCase):
    def setUp(self):
        # You can initialize any necessary objects or variables here
        self.board = [[0] * 20 for _ in range(20)]
        self.test_board = Board(self.board)

    def test_init(self):
        self.assertEqual(self.test_board.board, self.board)
        self.assertEqual(self.test_board.size, 20)

    def test_sort_directions(self):
        # Test sort_directions when the point is closer to the left and upper boundaries
        self.assertEqual(self.test_board.sort_directions((5, 5)), {"dx": (1, -1), "dy": (1, -1)})

        # Test sort_directions when the point is closer to the right and lower boundaries
        self.assertEqual(self.test_board.sort_directions((15, 15)), {"dx": (-1, 1), "dy": (-1, 1)})
    
class TestAI(unittest.TestCase):
    def setUp(self):
        self.board = [[0] * 20 for _ in range(20)]
        self.size = len(self.board)
    
    def test_checkWinner(self):
        # Test checkWinner when there is no winner
        self.score = Score(self.board)
        self.assertEqual(self.score.checkWinner({1: {}, 2: {}}), 0)
        
        # Test checkWinner when AI wins
        self.score = Score(self.board)
        self.assertEqual(self.score.checkWinner({1: {(5, 5): 1}, 2: {}}), 1)
        
        # Test checkWinner when opponent wins
        self.score = Score(self.board)
        self.assertEqual(self.score.checkWinner({1: {}, 2: {(5, 5): 1}}), 2)

# class TestMove(unittest.TestCase):

#     def test_candidates(self):
#         board = [[0] * 20 for _ in range(20)]
#         test_board = Board(board)
#         old_pattern = {}
#         role = 1
#         last_point = (10, 10)
        
#     def test_get_limit(self):
#         board = [[0] * 20 for _ in range(20)]
#         test_board = Board(board)
        

#     def test_sort_directions(self):
#         board = [[0] * 20 for _ in range(20)]
#         test_board = Board(board)
#         point = (10, 10)
#         result = test_board.sort_directions(point)
        

#     def test_sort_steps(self):
#         board = [[0] * 20 for _ in range(20)]
#         test_board = Board(board)
#         directions = {'dx': (1, -1), 'dy': (1, -1)}
#         iteration = 2
#         last_point = (10, 10)
#         old_pattern = {}
#         role = 1
#         pos = []
        

class TestMinMax(unittest.TestCase):

    def test_get_total_pattern(self):
        board = [[0] * 20 for _ in range(20)]
        test_pattern = Pattern(board)
        role = 1
        result = test_pattern.get_total_pattern(role)
        

    def test_get_pattern(self):
        board = [[0] * 20 for _ in range(20)]
        test_pattern = Pattern(board)
        role = 1
        result = test_pattern.get_pattern(role)
       

    def test_direct_search(self):
        board = [[0] * 20 for _ in range(20)]
        test_pattern = Pattern(board)
        point = (10, 10)
        direct = (1, 1)
        role = 1
        direct_pattern = {}
        result = test_pattern.direct_search(point, direct, role, direct_pattern)

class TestService(unittest.TestCase):

    def test_checkWinner(self):
        board = [[0] * 20 for _ in range(20)]
        test_score = Score(board)
        check_pattern = {1: {(5, 0): 1}, 2: {}}
        result = test_score.checkWinner(check_pattern)
        assert result == 1

    def test_total_score(self):
        board = [[0] * 20 for _ in range(20)]
        test_score = Score(board)
        total_pattern = {1: {(3, 1): 1}, 2: {}}
        role = 1
        result = test_score.total_score(total_pattern, role)

    def test_get_score(self):
        board = [[0] * 20 for _ in range(20)]
        test_score = Score(board)
        score_pattern = {(3, 1): 1}
        result = test_score.get_score(score_pattern)
        
class TestKill(unittest.TestCase):
    def setUp(self):
        self.board = [[0] * 20 for _ in range(20)]
        self.size = len(self.board)
    
    def test_checkWinner(self):
        # Test checkWinner when there is no winner
        self.score = Score(self.board)
        self.assertEqual(self.score.checkWinner({1: {}, 2: {}}), 0)
        
        # Test checkWinner when AI wins
        self.score = Score(self.board)
        self.assertEqual(self.score.checkWinner({1: {(5, 5): 1}, 2: {}}), 1)
        
        # Test checkWinner when opponent wins
        self.score = Score(self.board)
        self.assertEqual(self.score.checkWinner({1: {}, 2: {(5, 5): 1}}), 2)