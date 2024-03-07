from service.minMax import MinMax


class UI:
    def __init__(self, service_minmax):
        service_minmax = MinMax([[0 for _ in range(19)] for _ in range(19)])
        self.__service_minmax = service_minmax

    def start(self):
        while True:
            print("1. Human vs computer")
            print("2. Exit")
            command = input("Enter command: ")
            if command == "1":
                self.__start_game_player_vs_computer()
            elif command == "2":
                break
            else:
                print("Invalid command")
    
    def print_board(self):
        board = self.__service_minmax.board
        index = 0
        print("     1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19")
        print("   -----------------------------------------------------------")
        mapping = {1: 'X', 2: 'O', 0: '.'}
        for row in board:
                index += 1
                row_string = '  '.join(mapping[e] for e in row)
                if index < 10:
                    print(f" {index} | {row_string} |")
                else:
                    print(f"{index} | {row_string} |")
        print("   -----------------------------------------------------------")
    
    def __start_game_player_vs_computer(self):
        while True:
            print("1. Start game")
            print("2. Back")
            command = input("Enter command: ")
            if command == "1":
                self.__start_game_player_vs_computer_game()
            elif command == "2":
                break
            else:
                print("Invalid command")
    
    def reset(self):
        self.__init__(self.__service_minmax)
    
    def __start_game_player_vs_computer_game(self):
        order = 2
        while True:
            self.print_board()
            if order == 1:
                
                print("Player's turn")
                order = 2
                
                while True:
                    try:
                        x = int(input("Enter x: "))
                        y = int(input("Enter y: "))
                        
                        while not self.__service_minmax.check_if_move_is_available(y-1, x-1):
                            print("Invalid move")
                            x = int(input("Enter x: "))
                            y = int(input("Enter y: "))
                    except ValueError:
                        print("Invalid move")
                        continue
                    else:
                        break
                    
                self.__service_minmax.__setitem__((y-1, x-1), 2)
                if self.__service_minmax.check_win(2):
                    self.print_board()
                    print("Player wins")
                    self.reset()
                    break
            else:
                
                print("Computer's turn")
                order = 1

                y, x = self.__service_minmax.min_max()
                
                self.__service_minmax.__setitem__((y, x), 1)
                if self.__service_minmax.check_win(1):
                    self.print_board()
                    print("Computer wins")
                    self.reset()
                    break
                
            if self.__service_minmax.check_draw():
                self.print_board()
                print("Draw")
                self.reset()
                break