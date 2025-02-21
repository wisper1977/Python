class NumberShifting:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.grid = []
        self.moves = []

    def read_input(self):
        # First print the level code
        print("first_level")
        
        # Read grid dimensions
        self.width, self.height = map(int, input().split())
        
        # Read grid
        self.grid = []
        for _ in range(self.height):
            row = list(map(int, input().split()))
            self.grid.append(row)

    def is_valid_move(self, x, y, dx, dy):
        # Check if move is within grid bounds
        value = self.grid[y][x]
        new_x = x + dx * value
        new_y = y + dy * value
        
        if not (0 <= new_x < self.width and 0 <= new_y < self.height):
            return False
            
        # Check if destination has a non-zero number
        if self.grid[new_y][new_x] == 0:
            return False
            
        return True

    def make_move(self, x, y, direction, operation):
        value = self.grid[y][x]
        dx, dy = 0, 0
        
        if direction == 'U':
            dy = -1
        elif direction == 'D':
            dy = 1
        elif direction == 'L':
            dx = -1
        elif direction == 'R':
            dx = 1
            
        new_x = x + dx * value
        new_y = y + dy * value
        
        # Calculate new value
        if operation == '+':
            new_value = abs(self.grid[new_y][new_x] + value)
        else:  # operation == '-'
            new_value = abs(self.grid[new_y][new_x] - value)
            
        # Update grid
        self.grid[y][x] = 0
        self.grid[new_y][new_x] = new_value
        
        # Record move
        self.moves.append(f"{x} {y} {direction} {operation}")

    def find_possible_moves(self):
        possible_moves = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 0:
                    continue
                    
                # Check all directions
                directions = [('U', 0, -1), ('D', 0, 1), ('L', -1, 0), ('R', 1, 0)]
                for direction, dx, dy in directions:
                    if self.is_valid_move(x, y, dx, dy):
                        possible_moves.append((x, y, direction))
        return possible_moves

    def is_solved(self):
        return all(all(cell == 0 for cell in row) for row in self.grid)

    def solve(self):
        while not self.is_solved():
            moves = self.find_possible_moves()
            if not moves:
                return False
                
            # Try first possible move with both operations
            x, y, direction = moves[0]
            for operation in ['+', '-']:
                # Make copy of current state
                old_grid = [row[:] for row in self.grid]
                old_moves = self.moves[:]
                
                # Try move
                self.make_move(x, y, direction, operation)
                
                # If this leads to a solution, keep it
                if self.solve():
                    return True
                    
                # Otherwise backtrack
                self.grid = old_grid
                self.moves = old_moves
                
            return False
        return True

def main():
    game = NumberShifting()
    game.read_input()
    
    if game.solve():
        # Print all moves
        for move in game.moves:
            print(move)
    else:
        print("No solution found")

if __name__ == "__main__":
    main()
