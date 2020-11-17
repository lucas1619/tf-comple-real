import networkx as nx
import math


class Player:
    def __init__(self, path_finder, start, goal, wall_strategy):
        self.current = start
        self.goal = goal
        self.walls = None
        self.path_finder = path_finder
        self.wall_strategy = wall_strategy

    def path_find(self, board):
        try:
            lista = self.path_finder(board, self.current, self.goal)
            return lista
        except:
            return []

    def is_winner(self):
        return self.goal == self.current

    def has_walls(self):
        return self.walls > 0

    def move_pawn(self, board, is_real_move=False):
        if is_real_move:
            print(f'movio peon de {self.current} a ', end='')
        if len(self.path_find(board)) == 1:
            self.current = self.goal
        else:
            self.current = self.path_find(board)[1]
        if is_real_move:
            print(self.current)


class Board:
    def __init__(self, size, G=None):
        self.size = size
        if G is None:
            self.G = nx.Graph()
            for i in range(size ** 2):
                self.G.add_node(i)
            for i in range(self.size ** 2):
                if i % self.size != self.size - 1:
                    self.G.add_edge(i, i + 1)
                    self.G.add_edge(i + 1, i)
                if i + self.size < self.size * self.size:
                    self.G.add_edge(i, i + self.size)
                    self.G.add_edge(i + self.size, i)
        else:
            self.G = G

    def copy(self):
        new_one = Board(self.size, self.G)
        return new_one

    def add_wall(self, a1, b1, a2, b2, players):
        if ((self.size ** 2) > a1 >= 0) and ((self.size ** 2) > b1 >= 0) and ((self.size ** 2) > a2 >= 0) and (
                (self.size ** 2) > b2 >= 0):  # valida bordes
            pass
        else:
            return False  # valida bordes
        if self.G.has_edge(a1, a2) and self.G.has_edge(b1, b2) and self.G.has_edge(a1, b1) and self.G.has_edge(a2,
                                                                                                               b2):  # valida conexion entre nodos
            self.G.remove_edge(a1, b1)
            self.G.remove_edge(a2, b2)
        for player in players:
            if not player.path_find(self.G):
                self.G.add_edge(a1, b1)
                self.G.add_edge(b1, a1)
                self.G.add_edge(a2, b2)
                self.G.add_edge(b2, a2)
                return False
        return True


class Game:
    def __init__(self, n_players, size):
        self.board = Board(size)
        self.players = [None] * n_players
        key_pos1 = size // 2
        key_pos2 = (size // 2) * size
        if len(self.players) == 2:
            self.players[0] = Player(nx.dijkstra_path, key_pos1, key_pos1 + (size * (size - 1)), 1)
            self.players[1] = Player(nx.bellman_ford_path, key_pos1 + (size * (size - 1)), key_pos1, 1)
        elif len(self.players) == 4:
            self.players[0] = Player(nx.dijkstra_path, key_pos1, key_pos1 + (size * (size - 1)), 1)
            self.players[1] = Player(nx.bellman_ford_path, key_pos1 + (size * (size - 1)), key_pos1, 1)

            self.players[2] = Player(nx.astar_path, key_pos2, key_pos2 + (size - 1), 1)
            self.players[3] = Player(nx.dijkstra_path, key_pos2 + (size - 1), key_pos2, 1)
        for player in self.players:
            if size % 2 == 0:
                player.walls = size / len(self.players)
            else:
                player.walls = (size + 1) / len(self.players)

    def evaluate_position(self, player, players, board):
        if player.is_winner():
            return float('inf')
        score = len(player.path_find(board))
        for p in players:
            if p != player:
                score -= len(p.path_find(board))
        return score

    def validate_direction(self, start_node, end_node):
        validate = start_node - end_node
        if validate == self.board.size:
            return 0  # arriba a abajo
        elif validate == -self.board.size:
            return 1  # arriba a abajo
        elif validate == -1:
            return 2  # izquierda a derecha
        elif validate == 1:
            return 3  # derecha a izquierda

    def offensive_wall(self, objective_player, board, players, real_wall=False):
        if real_wall == False:
            it_could = True
            for i in range(len(objective_player.path_find(board.G)) - 1):
                indicator = self.validate_direction(objective_player.path_find(board.G)[i],
                                                    objective_player.path_find(board.G)[i + 1])
                # 0 arriba, 1 abajo, 2 derecha, 3 izquierda
                if indicator == 0:
                    if board.add_wall(objective_player.path_find(board.G)[i],
                                      objective_player.path_find(board.G)[i] - self.board.size,
                                      objective_player.path_find(board.G)[i] + 1,
                                      objective_player.path_find(board.G)[i] - self.board.size + 1, players):
                        break
                    else:
                        continue
                elif indicator == 1:
                    if board.add_wall(objective_player.path_find(board.G)[i],
                                      objective_player.path_find(board.G)[i] + self.board.size,
                                      objective_player.path_find(board.G)[i] + 1,
                                      objective_player.path_find(board.G)[i] + self.board.size + 1, players):
                        break
                    else:
                        continue
                elif indicator == 2:
                    if board.add_wall(objective_player.path_find(board.G)[i],
                                      objective_player.path_find(board.G)[i] + 1,
                                      objective_player.path_find(board.G)[i] + self.board.size,
                                      objective_player.path_find(board.G)[i] + self.board.size + 1, players):
                        break
                    else:
                        continue
                elif indicator == 3:
                    if board.add_wall(objective_player.path_find(board.G)[i],
                                      objective_player.path_find(board.G)[i] - 1,
                                      objective_player.path_find(board.G)[i] + self.board.size,
                                      objective_player.path_find(board.G)[i] + self.board.size - 1, players):
                        break
                    else:
                        continue
                if i == len(objective_player.path_find(board.G)) - 2:
                    # no se pudo poner pared
                    it_could = False
            return it_could
        else:
            it_could = True
            for i in range(len(objective_player.path_find(board.G)) - 1):
                indicator = self.validate_direction(objective_player.path_find(board.G)[i],
                                                    objective_player.path_find(board.G)[i + 1])
                # 0 arriba, 1 abajo, 2 derecha, 3 izquierda
                if indicator == 0:
                    if self.board.add_wall(objective_player.path_find(self.board.G)[i],
                                           objective_player.path_find(self.board.G)[i] - self.board.size,
                                           objective_player.path_find(self.board.G)[i] + 1,
                                           objective_player.path_find(self.board.G)[i] - self.board.size + 1, players):
                        break
                    else:
                        continue
                elif indicator == 1:
                    if self.board.add_wall(objective_player.path_find(self.board.G)[i],
                                           objective_player.path_find(self.board.G)[i] + self.board.size,
                                           objective_player.path_find(self.board.G)[i] + 1,
                                           objective_player.path_find(self.board.G)[i] + self.board.size + 1, players):
                        break
                    else:
                        continue
                elif indicator == 2:
                    if self.board.add_wall(objective_player.path_find(self.board.G)[i],
                                           objective_player.path_find(self.board.G)[i] + 1,
                                           objective_player.path_find(self.board.G)[i] + self.board.size,
                                           objective_player.path_find(self.board.G)[i] + self.board.size + 1, players):
                        break
                    else:
                        continue
                elif indicator == 3:
                    if self.board.add_wall(objective_player.path_find(self.board.G)[i],
                                           objective_player.path_find(self.board.G)[i] - 1,
                                           objective_player.path_find(self.board.G)[i] + self.board.size,
                                           objective_player.path_find(self.board.G)[i] + self.board.size - 1, players):
                        break
                    else:
                        continue
                if i == len(objective_player.path_find(self.board.G)) - 2:
                    # no se pudo poner pared
                    it_could = False
            return it_could

    def deffensive_wall(self, objective_player: Player, board):
        print('deffensive_wall')

    def play(self):
        winner_id = None
        turn = 0
        best_score = None
        score = None
        while 1:
            max_score = float('-inf')
            before_current = self.players[turn].current
            before_board = self.board.copy()
            movement = {'type': 'm', 'target': -1}
            # Primero es mover
            self.players[turn].move_pawn(self.board.G)
            score = self.paranoid(self.board, 1, (turn + 1) % len(self.players), self.players.copy())
            max_score = max(score, max_score)
            self.players[turn].current = before_current
            if self.players[turn].has_walls():
                for i, p in enumerate(self.players):
                    if i != turn:
                        if self.players[turn].wall_strategy == 1:
                            self.offensive_wall(p, self.board, self.players)
                            self.players[turn].walls -= 1
                        score = self.paranoid(self.board, 1, (turn + 1) % len(self.players), self.players.copy())
                        if score > max_score:
                            movement['type'] = 'w'
                            movement['target'] = i
                        self.board = before_board
                        self.players[turn].walls += 1
            if movement['type'] == 'm':
                print(f'jugador {turn + 1} movio peon')
                self.players[turn].move_pawn(self.board.G, True)
            else:
                if self.players[turn].wall_strategy == 1:
                    print(f'jugador {turn + 1} puso muro ofensivo')
                    self.offensive_wall(self.players[movement['target']], self.board, self.players)
                self.players[turn].walls -= 1
            if self.players[turn].is_winner():
                winner_id = turn
                break
            turn = (turn + 1) % len(self.players)
        print(f'The winner is the player {winner_id + 1}')

    def paranoid(self, board, depth, player, players):
        if depth == 4:
            return self.evaluate_position(players[player], players, board.G)
        if depth % len(self.players) == 0:
            max_score = float('-inf')
            before_current = players[player].current
            before_board = board.copy()
            # Primero es mover
            players[player].move_pawn(board.G)
            score = self.paranoid(board, depth + 1, (player + 1) % len(players), players)
            max_score = max(score, max_score)
            players[player].current = before_current
            for i, p in enumerate(players):
                if i != player:
                    if players[player].wall_strategy == 1:
                        self.offensive_wall(p, board, players)
                        players[player].walls -= 1
                    score = self.paranoid(board.copy(), depth + 1, (player + 1) % len(players), players)
                    max_score = max(score, max_score)
                    board = before_board
                    players[player].walls += 1
            return max_score
        else:
            min_score = float('inf')
            before_current = players[player].current
            before_board = board.copy()
            # Primero es mover
            players[player].move_pawn(board.G)
            score = self.paranoid(board, depth + 1, (player + 1) % len(players), players)
            min_score = min(score, min_score)
            players[player].current = before_current
            for i, p in enumerate(players):
                if i != player:
                    if players[player].wall_strategy == 1:
                        self.offensive_wall(p, board, players, True)
                        players[player].walls -= 1
                    score = self.paranoid(board.copy(), depth + 1, (player + 1) % len(players), players)
                    min_score = min(score, min_score)
                    board = before_board
                    players[player].walls += 1
            return min_score


game = Game(2, 9)
game.play()
