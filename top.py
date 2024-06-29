# defining the size of the actual columns we will create
likelyhoods = [(0,0), (1,0), (2,3), (3,5), (4, 7), (5,9), (6, 11), (7, 13), (8, 11), (9, 9), (10, 7), (11, 5), (12, 3)]


import random

class Die:
    '''Die class'''

    def __init__(self, sidesParam=6):
        '''Die([sidesParam])
        creates a new Die object
        int sidesParam is the number of sides
        (default is 6)
        -or- sidesParam is a list/tuple of sides'''
        # if an integer, create a die with sides
        #  from 1 to sides
        if isinstance(sidesParam, int):
            sidesParam = range(1, sidesParam + 1)
        self.sides = list(sidesParam)
        self.numSides = len(self.sides)
        # roll the die to get a random side on top to start
        self.roll()

    def __str__(self):
        '''str(Die) -> str
        string representation of Die'''
        return 'A ' + str(self.numSides) + '-sided die with ' + \
               str(self.get_top()) + ' on top'

    def roll(self):
        '''Die.roll()
        rolls the die'''
        # pick a random side and put it on top
        self.top = random.choice(self.sides)

    def get_top(self):
        '''Die.get_top() -> object
        returns top of Die'''
        return self.top

    def set_top(self, value):
        '''Die.set_top(value)
        sets the top of the Die to value
        Does nothing if value is illegal'''
        if value in self.sides:
            self.top = value


class Coluna():
    """ represents a player's column in a Can't Stop game, keeping track of the sum col_sum, up to a maximum of size col_size steps"""
    def __init__(self, col_sum, col_size, position = 1):
        self.col_sum = col_sum
        self.col_size = col_size
        self.position = 1
    
    
    def __str__(self):
        return f"Player occupies {self.position} out of {self.col_size} relative to the sum {self.col_sum}."

    def move_fowards(self):
        """if the column is finished, advances one position"""
        if self.position == self.col_size:
           raise ValueError("Cannot advance a finished column")
        self.position += 1

    def set_position(self, position):
        """sets the position of the players marker"""
        self.position = position

    def get_position(self):
        """ returns the current position on the column"""
        return self.position

    def is_done(self):
        """ Checks if the column is finished"""
        return self.position >= self.col_size

    def has_space(self):
        """cheks if it's possible to move twice in this column"""
        return self.position <= self.col_size - 2


    def copy_column(self):
        """creates a copy of the current column"""
        return Coluna(self.col_sum, self.col_size, self.position)


class CantStop:
    """represents a Can't stop Game"""
    def __init__(self, num_players):
        self.num_players = num_players
        self.board = [0]*13
        self.is_finished = False

    def update_board(self, column_list):
        """adiciona colunas a lista de colunas finalizadas, vai para o proximo jogador"""
        for column_num in column_list:
            self.board[column_num] = 1
      

    def end_game(self):
        self.is_finished = True

    def is_on(self):
        return not self.is_finished
    
        
class Player:
    """represents a player in a Can't Stop Game"""
    def __init__(self, game):
        self.game = game
        self.colunas = [Coluna(i, j) for (i,j) in likelyhoods]
        self.points = 0
        self.pinos = []
        self.colunas_temp = []
        self.can_play = True

    def is_clear(self):
        return self.can_play
    
    def throw_dice(self):
        """throws four dice and returns the possible moves the player can make"""
        # rolls the dice
        dice = [Die() for _ in range(4)]
        for die in dice:
            die.roll()
        # possible ways to pair the dice
        pairs = [((0,1),(2,3)), ((0,2), (1,3)), ((0,3),(1,2))]

        #creates a list with the results of the dice, as well as whether we can play them 
        resultado = []
        for pair in pairs:
             movimento = (dice[pair[1][1]].get_top() + dice[pair[1][2]].get_top, dice[pair[1][1]].get_top() + dice[pair[1][2]].get_top)
             jogada = (f"({dice[pair[1][1]].get_top()} + {dice[pair[1][2]].get_top} = {dice[pair[1][1]].get_top() + dice[pair[1][2]].get_top},"
                       f"{dice[pair[1][1]].get_top()} + {dice[pair[1][2]].get_top} = {dice[pair[1][1]].get_top() + dice[pair[1][2]].get_top})")
             resultado.append((jogada, movimento, tailor(movimento)))

        return resultado

    def take_turn(self):
        #throws the dice and identifies valid moves
        input("Press [Enter] to throw dice")
        comb = self.throw_dice()
        moves = [pares for pares in comb if [pares][2] != (False, False)]

        #ends game if no moves are available
        if len(moves) == 0:
            print("Sorry, you can't move")
            self.can_play = False
        
        else:
            #picks the move
            for pares in moves:
                print(pares)
            choice = -1
            while choice not in range(len(moves)):
                choice = input("What columns do you want to advance?")
            move =[moves[choice][1][i] for i in range(1) if moves[choice][2][i]]

            for dice_sum in move:
                if dice_sum not in pinos:
                    pinos.append(dice_sum)
                self.colunas_temp[dice_sum].move_fowards()
            
    def start_turn(self):
        """resets the temporary columns, as well as the pinos"""
        self.pinos = []
        self.colunas_temp = [coluna.copy_column() for coluna in self.colunas()]

    def finish_turn(self):
        """copies the temporary columns into the permanent ones, updates the player's score"""
        self.colunas = [coluna.copy_column() for coluna in self.colunas_temp()]
        self.points = len([coluna for coluna in self.colunas if coluna.is_done()])

    def has_won(self):
        return self.points >= 3

    def advances(self):
        return [num for num in pinos if self.colunas[num].is_done()]
    
    def has_legs(self, dice_sum):
        """checks if we can advance in a given column"""
        
        if len(self.pinos) == 3 and dice_sum not in self.pinos:
            #can't move if already has three pieces in other columns
            return False
        elif self.game.board[dice_sum] == 1:
            #can't move if someone already won that column
            return False
        elif self.colunas_temp[dice_sum].is_done():
            #can't move if they have already finished that column in this turn
            return False
        return True

    def tailor(self, pair):
        """takes a pair of possible column moves and return which moves can be made from them"""
        if pair[0] != pair[1] or not has_legs(pair[0]):
            return (has_legs(pair[0]), has_legs(pair[1]))
        else:
            if self.colunas_temp[pair[0]].has_space():
                return (True, True)
            return (True, False)
                            
def play_cant_stop(num_players):
    """plays a game of can't stop with num_players players"""
    
    game = CantStop(num_players)
    players = [Player(game) for _ in range(num_players)]
    current_player_num = 0
    while game.is_on():
        current_player = players[current_player_num]
        again = "y"
        while again == "y":
             current_player.take_turn()
             if not (current_player.is_clear()):
                 current_player_num = (current_player_num + 1) % num_players
                 break
             else:
                 again = input("Do you want to take another turn?(y/n)")
        if again == "n":
            current_player.finish_turn()
            if current_player.has_won():
                print("Yay! You've won!")
                game.end_game()
            else:
                for num in current_player.advances():
                    game.board[num] = 1
                current_player_num = (current_player_num + 1) % num_players

play_cant_stop(3)
