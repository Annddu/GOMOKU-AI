class Score:
    '''
    evaluate score for a given board
    board: 20*20 list represent a board
    point: chess position (x,y)
    rule: 0 empty ; 1 occupied by AI ; 2 occupied by opponent
    '''

    def __init__(self, board):
        self.board = board
        self.size = len(self.board)

    def checkWinner(self, check_pattern):
        AI_lens = [key[0] for key in check_pattern[1].keys()]
        if len(AI_lens) > 0 and max(AI_lens) >= 5:
            return 1
        OP_lens = [key[0] for key in check_pattern[2].keys()]
        if len(OP_lens) > 0 and max(OP_lens) >= 5:
            return 2
        return 0

    def total_score(self, total_pattern, role):
        '''
        return total score, which equals score of role minus score of opponent
        :param total_pattern: dict save AI pattern and opponent pattern
        :param role: AI or opponent
        :return: total score
        '''
        AI_score = self.get_score(total_pattern[role])
        opponent_score = self.get_score(total_pattern[3 - role])
        total_score = AI_score - 1.4 * opponent_score
        return total_score

    def get_score(self, score_pattern):
        '''
        keys of score dict are (length of chess in a line for specified direction, number of live nodes)
        :return: score of pattern
        '''
        score = 0
        # score_dic = {
        #     (1, 1): 1,
        #     (1, 2): 10,
        #     (2, 1): 10,
        #     (2, 2): 100,
        #     (3, 1, "S"): 100,
        #     (3, 2, "S"): 1000,
        #     (3, 1): 100,
        #     (3, 2): 1000,
        #     (4, 0, "S"): 1100,
        #     (4, 1, "S"): 1100,
        #     (4, 2, "S"): 100000,
        #     (4, 1): 1100,
        #     (4, 2): 100000}

        #imposible?
        # score_dic = {
        # (1, 1): 1,
        # (1, 2): 10,
        # (2, 1): 10,
        # (2, 2): 100,
        # (3, 1, "S"): 1000,
        # (3, 2, "S"): 10000,
        # (3, 1): 10000,
        # (3, 2): 100000,
        # (4, 0, "S"): 1000000,
        # (4, 1, "S"): 10000000,
        # (4, 2, "S"): 100000000,
        # (4, 1): 1000000000,
        # (4, 2): 10000000000,
        # (5, 0, "S"): 100000000000,
        # (5, 1, "S"): 1000000000000,
        # (5, 2, "S"): 10000000000000,
        # (5, 1): 100000000000000,
        # (5, 2): 1000000000000000,
        # }
        
        # score_dic = {
        #     (1, 1): 1,
        #     (1, 2): 10,
        #     (2, 1): 10,
        #     (2, 2): 100,
        #     (3, 1, "S"): 100,
        #     (3, 2, "S"): 1000,
        #     (3, 1): 1000,
        #     (3, 2): 10000,
        #     (4, 0, "S"): 10000,
        #     (4, 1, "S"): 15000,
        #     (4, 2, "S"): 100000,
        #     (4, 1): 200000,
        #     (4, 2): 1000000}
        
        # score_dic = {
#     (1, 1): 1,
#     (1, 2): 10,
#     (2, 1): 10,
#     (2, 2): 100,
#     (3, 1, "S"): 100,
#     (3, 2, "S"): 1000,
#     (3, 1): 1000,
#     (3, 2): 10000,
#     (4, 0, "S"): 10000,
#     (4, 1, "S"): 15000,
#     (4, 2, "S"): 100000,
#     (4, 1): 200000,
#     (4, 2): 2000000  # Increased score
# }
        
        #hard
        score_dic = {
            (1, 1): 1,
            (1, 2): 10,
            (2, 1): 10,
            (2, 2): 100,
            (3, 1, "S"): 100,
            (3, 2, "S"): 1000,
            (3, 1): 1000,
            (3, 2): 10000,
            (4, 0, "S"): 10000,
            (4, 1, "S"): 15000,
            (4, 2, "S"): 100000,
            (4, 1): 200000,
            (4, 2): 1000000,
            (5, 0, "S"): 1000000,
            (5, 1, "S"): 1000000,
            (5, 2, "S"): 1000000,
            (5, 1): 1000000,
            (5, 2): 1000000
            }
        
        live3_count = 0
        for key in score_pattern.keys():
            length = key[0]
            if key == (3, 2) or key == (3, 1, "S"):
                live3_count += score_pattern[key]
            if length >= 5:
                #hard
                score += 100000000000000000000000000
            else:
                score += score_dic[key] * score_pattern[key]
        if live3_count >= 2:
            score += 300
        return score
    
        # score_pattern = score_dic  # Assuming this function returns a dictionary of patterns and their counts

        # Add scores based on score_dic
        # for key, count in score_pattern.items():
        #     if key in score_dic:
        #         score += score_dic[key] * count

        # # Add bonus for threats
        # threat_bonus = 500000
        # if (4, 1) in score_pattern or (4, 2) in score_pattern:
        #     score += threat_bonus

        # # Add bonus for double threats
        # double_threat_bonus = 1000000
        # live3_count = score_pattern.get((3, 2), 0) + score_pattern.get((3, 1, "S"), 0)
        # if live3_count >= 2:
        #     score += double_threat_bonus

        # return score