import networkx as nx
class Player:
    def __init__(self, path_finder, start, goal):
        self.current = start
        self.goal = goal
        self.walls = None
        self.path_finder = path_finder
    def path_find(self, board):
        return self.path_finder(board, self.current, self.goal)
    def ai(self, board):
        print('ai')
class Board:
    def __init__(self, size):
        self.G = nx.Graph()
        self.size = size
        for i in range(size**2):
            self.G.add_node(i)
        for i in range(self.size ** 2):
            if i % self.size != self.size - 1:
                self.G.add_edge(i, i + 1)
                self.G.add_edge(i + 1, i)
            if i + self.size < self.size * self.size:
                self.G.add_edge(i, i + self.size)
                self.G.add_edge(i + self.size, i)
    def add_wall(self, a1, a2, b1, b2):
        if self.G.has_edge(a1, b1) and self.G.has_edge(a2, b2):
            self.G.remove_edge(a1, b1)
            self.G.remove_edge(a2, b2)
class Game:
    def __init__(self, n_players, size):
        self.board = Board(size)
        self.players = [None]*n_players
        key_pos1 = size//2
        key_pos2 = (size//2) * size
        if len(self.players) == 2:
            self.players[0] = Player(nx.dijkstra_path, key_pos1, key_pos1 + (size*(size - 1)))
            self.players[1] = Player(nx.bellman_ford_path, key_pos1 + (size*(size - 1)), key_pos1)
        elif len(self.players) == 4:
            self.players[0] = Player(nx.dijkstra_path, key_pos1, key_pos1 + (size * (size - 1)))
            self.players[1] = Player(nx.bellman_ford_path, key_pos1 + (size * (size - 1)), key_pos1)

            self.players[2] = Player(nx.astar_path, key_pos2, key_pos2 + (size - 1))
            self.players[3] = Player(nx.dijkstra_path, key_pos2 + (size - 1), key_pos2)
        for player in self.players:
            if size%2 == 0:
                player.walls = size/len(self.players)
            else:
                player.walls = (size+1)/len(self.players)
            print(player.path_find(self.board.G))
Game(4, 9)