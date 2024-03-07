import copy

class Pattern:
    '''
    enumerate common pattern on board
    '''

    def __init__(self, board):
        self.board = board
        self.size = len(board)
        self.status = {"N": {"length": 0, "end": 0}, "S": {"length": [0, 0], "end": 0}}
        self.size = len(self.board)
        
    
    def get_total_pattern(self, role):
        '''
        get AI pattern and opponent pattern by search the whole board
        :param role: AI or Opponent
        :return:
        '''
        AI_pattern = self.get_pattern(role)
        opponent_pattern = self.get_pattern(3 - role)
        total_pattern = {role: AI_pattern, 3 - role: opponent_pattern}
        return total_pattern

    def get_pattern(self, role):
        '''
        get pattern(AI or Opponent) by search the whole board
        :param role: AI or Opponent
        :return: pattern
        '''
        role_pattern = dict()
        direct = (0, 1)
        for x in range(self.size):
            y = 0
            role_pattern = self.direct_search((x, y), direct, role, role_pattern)
        direct = (1, 0)
        for y in range(self.size):
            x = 0
            role_pattern = self.direct_search((x, y), direct, role, role_pattern)

        direct = (1, 1)
        for x in range(self.size):
            y = 0
            role_pattern = self.direct_search((x, y), direct, role, role_pattern)
        for y in range(1, self.size, 1):
            x = 0
            role_pattern = self.direct_search((x, y), direct, role, role_pattern)
        direct = (-1, 1)
        for x in range(self.size):
            y = 0
            role_pattern = self.direct_search((x, y), direct, role, role_pattern)
        for y in range(1, self.size, 1):
            x = self.size - 1
            role_pattern = self.direct_search((x, y), direct, role, role_pattern)

        return role_pattern

    def direct_search(self, point, direct, role, direct_pattern):
        '''
        search the whole board from different directions
        :param point: the start point, always located in the edge of board
        :param direct: one of the 8 directions on board, for example: (1,1)
        :param role: AI or Opponent
        :param direct_pattern: the dict to save point which have been searched
        :return: the updated pattern dict
        '''

        x, y = point
        dx, dy = direct
        state = copy.deepcopy(self.status)
        start = 3 - role
        while 0 <= x < self.size and 0 <= y < self.size:
            if self.board[x][y] == role:
                state["N"]["length"] += 1
            if self.board[x][y] == 0:
                if state["N"]["length"] > 0:
                    self.get_next_length((x, y), direct, role, state)
                    if start == 0:
                        state["N"]["end"] += 1
                        state["S"]["end"] += 1
                    state["N"]["end"] += 1
                    if (state["N"]["length"], state["N"]["0"]) in direct_pattern.keys():
                        direct_pattern[(state["N"]["length"], state["N"]["end"])] += 1
                    else:
                        direct_pattern[(state["N"]["length"], state["N"]["end"])] = 1
                    if state["S"]["length"] > 0 and state["S"]["length"] + state["N"]["length"] == 3:
                        if start == 0 or state["S"]["end"] == 1:
                            end = state["S"]["end"]
                            if start == 0:
                                end += 1
                            if end > 0:
                                if (3, end, "S") in direct_pattern.keys():
                                    direct_pattern[(3, end, "S")] += 1
                                else:
                                    direct_pattern[(3, end, "S")] = 1
                    if state["S"]["length"] > 0 and state["S"]["length"] + state["N"]["length"] == 4:
                        if start == 0 or state["S"]["end"] == 1:
                            end = state["S"]["end"]
                            if start == 0:
                                end += 1
                            if (4, end, "S") in direct_pattern.keys():
                                direct_pattern[(4, end, "S")] += 1
                            else:
                                direct_pattern[(4, end, "S")] = 1
                state = copy.deepcopy(self.status)
                start = 0
            if self.board[x][y] == 3 - role:
                if state["N"]["length"] > 0:
                    if start == 0:
                        state["N"]["end"] += 1
                    if state["N"]["end"] > 0:
                        if (state["N"]["length"], state["N"]["end"]) in direct_pattern.keys():
                            direct_pattern[(state["length"], state["end"])] += 1
                        else:
                            direct_pattern[(state["length"], state["end"])] = 1
                state = copy.deepcopy(self.status)
                start = 3 - role
            x += dx
            y += dy
        if state["N"]["length"] > 0:
            if start == 0:
                state["end"] += 1
            if state["N"]["end"] > 0:
                if (state["length"], state["end"]) in direct_pattern.keys():
                    direct_pattern[(state["length"], state["end"])] += 1
                else:
                    direct_pattern[(state["length"], state["end"])] = 1
        return direct_pattern

    def update(self, old_pattern, point, role):
        '''
        update the old pattern by search area near target point
        :param old_pattern: pattern dict contain AI(1) and Opponent Pattern(2)
        [{AI:{[length, number of live end]: count}}{Opponent:{[length, number of live end]:count}}]
        for example [{1:{[3, 2]:1}}{2:{[2,1]:1,[1,2]:1}}]
        :param point: the target point, for example(10,10)
        :param role: AI(1) or Opponent(2)
        :return: updated pattern
        '''
        update_pattern = copy.deepcopy(old_pattern)
        point_AI_pattern, point_OP_pattern = self.get_point(point, role)
        for key in [(1, 0), (1, 1), (0, 1), (-1, 1)]:
            dx, dy = key
            len_AI, end_AI = point_AI_pattern[(dx, dy)]["N"]["length"], point_AI_pattern[(dx, dy)]["N"]["end"]
            len_OP, end_OP = point_OP_pattern[(dx, dy)]["N"]["length"], point_OP_pattern[(dx, dy)]["N"]["end"]
            len_AI_N, end_AI_N = point_AI_pattern[(-dx, -dy)]["N"]["length"], point_AI_pattern[(-dx, -dy)]["N"]["end"]
            len_OP_N, end_OP_N = point_OP_pattern[(-dx, -dy)]["N"]["length"], point_OP_pattern[(-dx, -dy)]["N"]["end"]

            len_S_AI, end_S_AI = point_AI_pattern[(dx, dy)]["S"]["length"], point_AI_pattern[(dx, dy)]["S"]["end"]
            len_S_AI_N, end_S_AI_N = point_AI_pattern[(-dx, -dy)]["S"]["length"], point_AI_pattern[(-dx, -dy)]["S"][
                "end"]
            len_S_OP, end_S_OP = point_OP_pattern[(dx, dy)]["S"]["length"], point_OP_pattern[(dx, dy)]["S"]["end"]
            len_S_OP_N, end_S_OP_N = point_OP_pattern[(-dx, -dy)]["S"]["length"], point_OP_pattern[(-dx, -dy)]["S"][
                "end"]

            # update split pattern
            # update AI (Split 4)
            cond1 = sum(len_S_AI) == 1 and len_AI_N == 1
            cond2 = sum(len_S_AI) == 2 and len_AI_N == 0
            cond3 = sum(len_S_AI_N) == 1 and len_AI == 1
            cond4 = sum(len_S_AI_N) == 2 and len_AI == 0
            if cond1 or cond2:
                end = end_S_AI + end_AI_N
                if end > 0:
                    key = (3, end, "S")
                    if key in update_pattern[role].keys():
                        update_pattern[role][key] += 1
                    else:
                        update_pattern[role][key] = 1
            if cond3 or cond4:
                end = end_S_AI_N + end_AI
                if end > 0:
                    key = (3, end, "S")
                    if key in update_pattern[role].keys():
                        update_pattern[role][key] += 1
                    else:
                        update_pattern[role][key] = 1

            if len_AI_N + len_AI == 3 and (len_AI != 0 and len_AI_N != 0):
                end = end_AI + end_AI_N
                if end > 0:
                    update_pattern[role][(3, end, "S")] -= 1

            # update AI(Split 5)
            cond1 = sum(len_S_AI) == 1 and len_AI_N == 2
            cond2 = sum(len_S_AI) == 2 and len_AI_N == 1
            cond3 = sum(len_S_AI) == 3 and len_AI_N == 0
            cond4 = sum(len_S_AI_N) == 1 and len_AI == 2
            cond5 = sum(len_S_AI_N) == 2 and len_AI == 1
            cond6 = sum(len_S_AI_N) == 3 and len_AI == 0
            if cond1 or cond2 or cond3:
                end = end_S_AI + end_AI_N
                key = (4, end, "S")
                if key in update_pattern[role].keys():
                    update_pattern[role][key] += 1
                else:
                    update_pattern[role][key] = 1
            if cond4 or cond5 or cond6:
                end = end_S_AI_N + end_AI
                key = (4, end, "S")
                if key in update_pattern[role].keys():
                    update_pattern[role][key] += 1
                else:
                    update_pattern[role][key] = 1

            if len_AI_N + len_AI == 4 and (len_AI != 0 and len_AI_N != 0):
                end = end_AI + end_AI_N
                update_pattern[role][(4, end, "S")] -= 1

            # update opponent (Split 4)
            if len_OP + len_OP_N == 3 and len_OP != 0 and len_OP_N != 0:
                end = end_OP + end_OP_N
                if end > 0:
                    update_pattern[3 - role][(3, end, "S")] -= 1

            if sum(len_S_OP) == 3 and len_S_OP[0] > 0:
                end = end_S_OP + 1
                update_pattern[3 - role][(3, end, "S")] -= 1
                if end_S_OP > 0:
                    if (3, end_S_OP, "S") in update_pattern[3 - role].keys():
                        update_pattern[3 - role][(3, end_S_OP, "S")] += 1
                    else:
                        update_pattern[3 - role][(3, end_S_OP, "S")] = 1

            if sum(len_S_OP_N) == 3 and len_S_OP_N[0] > 0:
                end = end_S_OP_N + 1
                update_pattern[3 - role][(3, end, "S")] -= 1
                if end_S_OP_N > 0:
                    if (3, end_S_OP_N, "S") in update_pattern[3 - role].keys():
                        update_pattern[3 - role][(3, end_S_OP_N, "S")] += 1
                    else:
                        update_pattern[3 - role][(3, end_S_OP_N, "S")] = 1

            # update opponent (Split 5)
            if len_OP + len_OP_N == 4 and len_OP != 0 and len_OP_N != 0:
                end = end_OP + end_OP_N
                update_pattern[3 - role][(4, end, "S")] -= 1

            if sum(len_S_OP) == 4 and len_S_OP[0] > 0:
                end = end_S_OP + 1
                update_pattern[3 - role][(4, end, "S")] -= 1
                if (4, end_S_OP, "S") in update_pattern[3 - role].keys():
                    update_pattern[3 - role][(4, end_S_OP, "S")] += 1
                else:
                    update_pattern[3 - role][(4, end_S_OP, "S")] = 1

            if sum(len_S_OP_N) == 4 and len_S_OP_N[0] > 0:
                end = end_S_OP_N + 1
                update_pattern[3 - role][(4, end, "S")] -= 1
                if (4, end_S_OP_N, "S") in update_pattern[3 - role].keys():
                    update_pattern[3 - role][(4, end_S_OP_N, "S")] += 1
                else:
                    update_pattern[3 - role][(4, end_S_OP_N, "S")] = 1

            # update normal pattern
            if len_AI > 0:
                update_pattern[role][len_AI, end_AI + 1] -= 1

            elif len_OP > 0:
                if end_OP > 0:
                    if (len_OP, end_OP) in update_pattern[3 - role].keys():
                        update_pattern[3 - role][len_OP, end_OP] += 1
                    else:
                        update_pattern[3 - role][len_OP, end_OP] = 1

                update_pattern[3 - role][len_OP, end_OP + 1] -= 1

            if len_AI_N > 0:
                update_pattern[role][len_AI_N, end_AI_N + 1] -= 1

            elif len_OP_N > 0:
                if end_OP_N > 0:
                    if (len_OP_N, end_OP_N) in update_pattern[3 - role].keys():
                        update_pattern[3 - role][len_OP_N, end_OP_N] += 1
                    else:
                        update_pattern[3 - role][len_OP_N, end_OP_N] = 1
                update_pattern[3 - role][len_OP_N, end_OP_N + 1] -= 1
            next_length = len_AI + len_AI_N + 1
            next_end = end_AI + end_AI_N
            if next_end > 0 or next_length ==5:
                if (next_length, next_end) in update_pattern[role].keys():
                    update_pattern[role][next_length, next_end] += 1
                else:
                    update_pattern[role][next_length, next_end] = 1

        return update_pattern

    def get_point(self, point, role):
        '''
        get the AI and Opponent distribution info near the point
        :param point: for example (10,10)
        :param role: AI(1) or Opponent(2)
        :return: AI point pattern and Opponent point pattern
        '''
        point_AI_pattern = dict()
        point_OP_pattern = dict()
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if i != 0 or j != 0:
                    point_AI_pattern[(i, j)] = self.get_length(point, role, (i, j))
                    point_OP_pattern[(i, j)] = self.get_length(point, 3 - role, (i, j))
        return point_AI_pattern, point_OP_pattern

    def get_length(self, point, role, direction):
        '''
        get the AI or Opponent distribution info on one of the 8 directions
        :param point: target point, for example: (10,10)
        :param role: AI or Opponent
        :param direction: one of the 8 directions on the board
        :return: direction status dict
        '''
        dx, dy = direction
        x, y = point
        status = copy.deepcopy(self.status)
        while True:
            x += dx
            y += dy
            if 0 <= x < self.size and 0 <= y < self.size:
                if self.board[x][y] == role:
                    status["N"]["length"] += 1
                else:
                    if self.board[x][y] == 0:
                        status["N"]["end"] = 1
                        status = self.get_next_length((x, y), direction, role, status)
                        if status["S"]["length"][1] > 0:
                            status["S"]["length"][0] = copy.deepcopy(status["N"]["length"])
                            return status
                    return status
            else:
                return status

    def get_next_length(self, point, direction, role, status):
        dx, dy = direction
        x, y = point
        while True:
            x += dx
            y += dy
            if 0 <= x < self.size and 0 <= y < self.size:
                if self.board[x][y] == role:
                    status["S"]["length"][1] += 1
                else:
                    if self.board[x][y] == 0:
                        status["S"]["end"] = 1
                    return status
            else:
                return status