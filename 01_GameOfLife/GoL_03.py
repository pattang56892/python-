import random
import os
import time
import sys
import json
from collections import deque

def initialize_grid(rows, cols, density=0.2):
    """Initialize a random grid with given density"""
    return [[1 if random.random() < density else 0 
             for _ in range(cols)] for _ in range(rows)]

def load_pattern(pattern_name):
    """Load common Game of Life patterns"""
    patterns = {
        'glider': [
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1]
        ],
        'blinker': [
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0]
        ],
        'block': [
            [1, 1],
            [1, 1]
        ],
        'beehive': [
            [0, 1, 1, 0],
            [1, 0, 0, 1],
            [0, 1, 1, 0]
        ],
        'loaf': [
            [0, 1, 1, 0],
            [1, 0, 0, 1],
            [0, 1, 0, 1],
            [0, 0, 1, 0]
        ],
        'boat': [
            [1, 1, 0],
            [1, 0, 1],
            [0, 1, 0]
        ],
        'tub': [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0]
        ],
        'beacon': [
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 0, 1, 1]
        ],
        'toad': [
            [0, 1, 1, 1],
            [1, 1, 1, 0]
        ],
        'pulsar': [
            [0,0,1,1,1,0,0,0,1,1,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [0,0,1,1,1,0,0,0,1,1,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,1,0,0,0,1,1,1,0,0],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,1,0,0,0,1,1,1,0,0]
        ],
        'gosper_gun': [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ],
        'penta_decathlon': [
            [0,0,1,0,0,0,0,1,0,0],
            [1,1,0,1,1,1,1,0,1,1],
            [0,0,1,0,0,0,0,1,0,0]
        ],
        'lightweight_spaceship': [
            [1,0,0,1,0],
            [0,0,0,0,1],
            [1,0,0,0,1],
            [0,1,1,1,1]
        ]
    }
    return patterns.get(pattern_name.lower(), [])

def create_pattern_preview(pattern, size=80):
    """Generate a small preview image of a pattern"""
    try:
        from PIL import Image, ImageDraw, ImageTk
        if not pattern:
            return None
        
        rows, cols = len(pattern), len(pattern[0])
        if rows == 0 or cols == 0:
            return None
            
        # Calculate cell size to fit in preview
        cell_size = max(1, min(size // max(rows, cols), 8))
        
        # Create image with padding
        img_width = cols * cell_size + 10
        img_height = rows * cell_size + 10
        img = Image.new('RGB', (img_width, img_height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Draw border
        draw.rectangle([0, 0, img_width-1, img_height-1], outline='gray')
        
        # Draw pattern centered
        offset_x = (img_width - cols * cell_size) // 2
        offset_y = (img_height - rows * cell_size) // 2
        
        for i in range(rows):
            for j in range(cols):
                if pattern[i][j]:
                    x1 = offset_x + j * cell_size
                    y1 = offset_y + i * cell_size
                    x2 = x1 + cell_size
                    y2 = y1 + cell_size
                    draw.rectangle([x1, y1, x2, y2], fill='black')
        
        return ImageTk.PhotoImage(img)
    except ImportError:
        return None
    except Exception:
        return None

def place_pattern(grid, pattern, start_row, start_col):
    """Place a pattern on the grid at specified position"""
    if not pattern:
        return grid
    
    rows, cols = len(grid), len(grid[0])
    pattern_rows, pattern_cols = len(pattern), len(pattern[0])
    
    # Create a copy of the grid
    new_grid = [row[:] for row in grid]
    
    for i in range(pattern_rows):
        for j in range(pattern_cols):
            new_row = (start_row + i) % rows
            new_col = (start_col + j) % cols
            new_grid[new_row][new_col] = pattern[i][j]
    
    return new_grid

def save_state(grid, generation, filename="game_save.json"):
    """Save current game state to file"""
    try:
        state = {
            'grid': grid,
            'generation': generation,
            'rows': len(grid),
            'cols': len(grid[0]) if grid else 0
        }
        with open(filename, 'w') as f:
            json.dump(state, f)
        return True, f"Game saved to {filename}"
    except Exception as e:
        return False, f"Error saving game: {str(e)}"

def load_state(filename="game_save.json"):
    """Load game state from file"""
    try:
        with open(filename, 'r') as f:
            state = json.load(f)
        return True, state['grid'], state['generation']
    except FileNotFoundError:
        return False, None, 0
    except Exception as e:
        return False, None, 0

def export_as_image(grid, filename="generation.png", cell_size=10):
    """Export current grid as PNG image"""
    try:
        from PIL import Image, ImageDraw
        
        rows, cols = len(grid), len(grid[0])
        img_width = cols * cell_size
        img_height = rows * cell_size
        
        img = Image.new('RGB', (img_width, img_height), 'white')
        draw = ImageDraw.Draw(img)
        
        for i in range(rows):
            for j in range(cols):
                if grid[i][j]:
                    x1, y1 = j * cell_size, i * cell_size
                    x2, y2 = x1 + cell_size, y1 + cell_size
                    draw.rectangle([x1, y1, x2, y2], fill='black')
        
        img.save(filename)
        return True, f"Image exported to {filename}"
    except ImportError:
        return False, "PIL library not available for image export"
    except Exception as e:
        return False, f"Error exporting image: {str(e)}"

def export_gif(grid_history, filename="simulation.gif", cell_size=10, duration=200):
    """Export history as animated GIF"""
    try:
        from PIL import Image, ImageDraw
        
        if not grid_history:
            return False, "No history to export"
        
        frames = []
        for grid in grid_history[-50:]:  # Last 50 frames to avoid huge files
            rows, cols = len(grid), len(grid[0])
            img_width = cols * cell_size
            img_height = rows * cell_size
            
            img = Image.new('RGB', (img_width, img_height), 'white')
            draw = ImageDraw.Draw(img)
            
            for i in range(rows):
                for j in range(cols):
                    if grid[i][j]:
                        x1, y1 = j * cell_size, i * cell_size
                        x2, y2 = x1 + cell_size, y1 + cell_size
                        draw.rectangle([x1, y1, x2, y2], fill='black')
            frames.append(img)
        
        if frames:
            frames[0].save(filename, save_all=True, append_images=frames[1:], 
                          duration=duration, loop=0)
            return True, f"Animation saved to {filename} ({len(frames)} frames)"
        else:
            return False, "No frames to export"
    except ImportError:
        return False, "PIL library not available for GIF export"
    except Exception as e:
        return False, f"Error exporting GIF: {str(e)}"

def export_web(grid, filename="gameoflife.html"):
    """Export current grid as interactive HTML file"""
    try:
        rows, cols = len(grid), len(grid[0])
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Game of Life - Generation Export</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
        canvas {{ border: 2px solid #333; display: block; margin: 20px auto; background: white; }}
        .controls {{ text-align: center; margin: 20px 0; }}
        button {{ padding: 10px 20px; margin: 5px; background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; }}
        button:hover {{ background: #45a049; }}
        .info {{ text-align: center; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <h1 style="text-align: center; color: #333;">Conway's Game of Life</h1>
        <div class="info">
            <p>Grid Size: {rows} × {cols} | Live Cells: <span id="liveCells">0</span></p>
            <p>Generation: <span id="generation">0</span> | Status: <span id="status">Paused</span></p>
        </div>
        <canvas id="gameCanvas" width="{cols*8}" height="{rows*8}"></canvas>
        <div class="controls">
            <button onclick="togglePlay()">Play/Pause</button>
            <button onclick="step()">Step</button>
            <button onclick="reset()">Reset</button>
            <button onclick="clear()">Clear</button>
            <button onclick="randomize()">Random</button>
        </div>
        <div class="info">
            <p>Click cells to toggle • Exported from Enhanced Game of Life</p>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const cellSize = 8;
        const rows = {rows};
        const cols = {cols};
        
        let grid = {json.dumps(grid)};
        let originalGrid = JSON.parse(JSON.stringify(grid));
        let generation = 0;
        let playing = false;
        let animationId;
        
        function drawGrid() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Draw cells
            ctx.fillStyle = '#000';
            let liveCells = 0;
            for(let i = 0; i < rows; i++) {{
                for(let j = 0; j < cols; j++) {{
                    if(grid[i][j]) {{
                        ctx.fillRect(j * cellSize, i * cellSize, cellSize, cellSize);
                        liveCells++;
                    }}
                }}
            }}
            
            // Draw grid lines
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 0.5;
            for(let i = 0; i <= rows; i++) {{
                ctx.beginPath();
                ctx.moveTo(0, i * cellSize);
                ctx.lineTo(cols * cellSize, i * cellSize);
                ctx.stroke();
            }}
            for(let j = 0; j <= cols; j++) {{
                ctx.beginPath();
                ctx.moveTo(j * cellSize, 0);
                ctx.lineTo(j * cellSize, rows * cellSize);
                ctx.stroke();
            }}
            
            document.getElementById('liveCells').textContent = liveCells;
            document.getElementById('generation').textContent = generation;
        }}
        
        function countNeighbors(grid, row, col) {{
            let count = 0;
            for(let dr = -1; dr <= 1; dr++) {{
                for(let dc = -1; dc <= 1; dc++) {{
                    if(dr === 0 && dc === 0) continue;
                    let nr = (row + dr + rows) % rows;
                    let nc = (col + dc + cols) % cols;
                    count += grid[nr][nc];
                }}
            }}
            return count;
        }}
        
        function nextGeneration() {{
            let newGrid = Array(rows).fill().map(() => Array(cols).fill(0));
            
            for(let i = 0; i < rows; i++) {{
                for(let j = 0; j < cols; j++) {{
                    let neighbors = countNeighbors(grid, i, j);
                    let current = grid[i][j];
                    
                    if(current === 1) {{
                        if(neighbors < 2 || neighbors > 3) {{
                            newGrid[i][j] = 0;
                        }} else {{
                            newGrid[i][j] = 1;
                        }}
                    }} else {{
                        if(neighbors === 3) {{
                            newGrid[i][j] = 1;
                        }}
                    }}
                }}
            }}
            
            grid = newGrid;
            generation++;
            drawGrid();
        }}
        
        function togglePlay() {{
            playing = !playing;
            document.getElementById('status').textContent = playing ? 'Running' : 'Paused';
            if(playing) {{
                animate();
            }} else {{
                cancelAnimationFrame(animationId);
            }}
        }}
        
        function animate() {{
            if(playing) {{
                nextGeneration();
                animationId = setTimeout(() => requestAnimationFrame(animate), 200);
            }}
        }}
        
        function step() {{
            nextGeneration();
        }}
        
        function reset() {{
            grid = JSON.parse(JSON.stringify(originalGrid));
            generation = 0;
            playing = false;
            document.getElementById('status').textContent = 'Paused';
            drawGrid();
        }}
        
        function clear() {{
            grid = Array(rows).fill().map(() => Array(cols).fill(0));
            originalGrid = JSON.parse(JSON.stringify(grid));
            generation = 0;
            playing = false;
            document.getElementById('status').textContent = 'Paused';
            drawGrid();
        }}
        
        function randomize() {{
            for(let i = 0; i < rows; i++) {{
                for(let j = 0; j < cols; j++) {{
                    grid[i][j] = Math.random() < 0.25 ? 1 : 0;
                }}
            }}
            originalGrid = JSON.parse(JSON.stringify(grid));
            generation = 0;
            playing = false;
            document.getElementById('status').textContent = 'Paused';
            drawGrid();
        }}
        
        canvas.addEventListener('click', function(e) {{
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const col = Math.floor(x / cellSize);
            const row = Math.floor(y / cellSize);
            
            if(row >= 0 && row < rows && col >= 0 && col < cols) {{
                grid[row][col] = 1 - grid[row][col];
                drawGrid();
            }}
        }});
        
        // Initial draw
        drawGrid();
    </script>
</body>
</html>
        """
        
        with open(filename, 'w') as f:
            f.write(html)
        return True, f"Interactive HTML exported to {filename}"
    except Exception as e:
        return False, f"Error exporting HTML: {str(e)}"

class GameStats:
    """Advanced statistics tracking for Game of Life"""
    def __init__(self):
        self.population_history = deque(maxlen=1000)  # Store last 1000 generations
        self.generation = 0
        self.max_population = 0
        self.min_population = float('inf')
        self.stable_count = 0
        self.last_population = 0
        
    def update(self, grid, gen):
        live_cells = sum(sum(row) for row in grid)
        self.population_history.append((gen, live_cells))
        self.generation = gen
        
        # Track extremes
        self.max_population = max(self.max_population, live_cells)
        if live_cells > 0:
            self.min_population = min(self.min_population, live_cells)
        
        # Track stability
        if live_cells == self.last_population:
            self.stable_count += 1
        else:
            self.stable_count = 0
        self.last_population = live_cells
        
    def get_growth_rate(self, window=10):
        """Calculate growth rate over recent generations"""
        if len(self.population_history) < 2:
            return 0
        recent = list(self.population_history)[-window:]
        if len(recent) < 2:
            return 0
        
        total_change = recent[-1][1] - recent[0][1]
        time_span = recent[-1][0] - recent[0][0]
        return total_change / time_span if time_span > 0 else 0
    
    def get_current_population(self):
        """Get current population"""
        if self.population_history:
            return self.population_history[-1][1]
        return 0
    
    def is_stable(self, threshold=5):
        """Check if population has been stable"""
        return self.stable_count >= threshold
    
    def is_extinct(self):
        """Check if population is extinct"""
        return self.get_current_population() == 0
    
    def get_summary(self):
        """Get statistics summary"""
        current_pop = self.get_current_population()
        growth_rate = self.get_growth_rate()
        
        status = "Active"
        if self.is_extinct():
            status = "Extinct"
        elif self.is_stable():
            status = "Stable"
        elif abs(growth_rate) < 0.1:
            status = "Near Stable"
        
        return {
            'current_population': current_pop,
            'max_population': self.max_population,
            'min_population': self.min_population if self.min_population != float('inf') else 0,
            'growth_rate': growth_rate,
            'status': status,
            'generation': self.generation,
            'stable_count': self.stable_count
        }

def find_patterns_in_grid(grid):
    """Scan grid for known patterns"""
    patterns_found = []
    pattern_library = {
        'block': load_pattern('block'),
        'beehive': load_pattern('beehive'),
        'loaf': load_pattern('loaf'),
        'boat': load_pattern('boat'),
        'tub': load_pattern('tub'),
        'blinker': load_pattern('blinker'),
        'toad': load_pattern('toad'),
        'beacon': load_pattern('beacon')
    }
    
    for name, pattern in pattern_library.items():
        if pattern and pattern_exists_in_grid(grid, pattern):
            patterns_found.append(name)
    
    return patterns_found

def pattern_exists_in_grid(grid, pattern):
    """Check if pattern exists anywhere in grid"""
    if not pattern or not grid:
        return False
        
    rows, cols = len(grid), len(grid[0])
    p_rows, p_cols = len(pattern), len(pattern[0])
    
    if p_rows > rows or p_cols > cols:
        return False
    
    for i in range(rows - p_rows + 1):
        for j in range(cols - p_cols + 1):
            match = True
            for pi in range(p_rows):
                for pj in range(p_cols):
                    if grid[i+pi][j+pj] != pattern[pi][pj]:
                        match = False
                        break
                if not match:
                    break
            if match:
                return True
    return False

def count_neighbors(grid, row, col):
    """Count live neighbors for a cell at (row, col)"""
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
                
            # Wrap around edges (toroidal universe)
            nr = (row + dr) % rows
            nc = (col + dc) % cols
            
            count += grid[nr][nc]
            
    return count

def next_generation(grid):
    """Compute the next generation based on current grid"""
    rows, cols = len(grid), len(grid[0])
    new_grid = [[0] * cols for _ in range(rows)]
    
    for i in range(rows):
        for j in range(cols):
            neighbors = count_neighbors(grid, i, j)
            current_state = grid[i][j]
            
            # Apply Conway's rules
            if current_state == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[i][j] = 0  # Dies from under/overpopulation
                else:
                    new_grid[i][j] = 1  # Survives
            else:
                if neighbors == 3:
                    new_grid[i][j] = 1  # Reproduction
                    
    return new_grid

def print_grid_terminal(grid, generation, paused, history_pos, max_history, stats=None):
    """Print the grid with visual representation in terminal"""
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux/Mac
        os.system('clear')
    
    for row in grid:
        print(' '.join(['■' if cell else '.' for cell in row]))
    
    status = 'PAUSED' if paused else 'RUNNING'
    history_info = f" | History: {history_pos}/{max_history}" if max_history > 0 else ""
    print(f"\nGeneration: {generation} | {status}{history_info}")
    
    # Show statistics if available
    if stats:
        summary = stats.get_summary()
        print(f"Population: {summary['current_population']} | Growth Rate: {summary['growth_rate']:.2f} | Status: {summary['status']}")
        
        # Show detected patterns
        patterns = find_patterns_in_grid(grid)
        if patterns:
            print(f"Patterns Detected: {', '.join(patterns).title()}")
    
    print("Controls: [Space] Play/Pause | [→] Forward | [←] Backward | [R]eset | [P]attern | [S]ave | [L]oad")
    print("Advanced: [E]xport PNG | [G]IF Export | [W]eb Export | [A]nalytics | [GUI] Switch | [Q]uit")

def get_key():
    """Get single keypress without Enter - Windows compatible"""
    try:
        import msvcrt
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\x03':  # Ctrl+C
                raise KeyboardInterrupt
            elif key == b'\xe0':  # Special key prefix
                key2 = msvcrt.getch()
                if key2 == b'M':  # Right arrow
                    return 'right'
                elif key2 == b'K':  # Left arrow
                    return 'left'
                return None
            elif key == b' ':  # Space bar
                return 'space'
            try:
                return key.decode('utf-8').lower()
            except UnicodeDecodeError:
                return None
    except ImportError:
        try:
            import tty, termios, select
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.cbreak(fd)
                if select.select([sys.stdin], [], [], 0)[0]:
                    key = sys.stdin.read(1)
                    if key == '\x1b':  # Escape sequence
                        key += sys.stdin.read(2)
                        if key == '\x1b[C':  # Right arrow
                            return 'right'
                        elif key == '\x1b[D':  # Left arrow
                            return 'left'
                        return None
                    elif key == ' ':  # Space bar
                        return 'space'
                    return key.lower()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except ImportError:
            pass
    return None

def show_pattern_menu():
    """Show available patterns and get user selection"""
    patterns = ['glider', 'blinker', 'block', 'beehive', 'loaf', 'boat', 'tub', 
                'beacon', 'toad', 'pulsar', 'gosper_gun', 'penta_decathlon', 'lightweight_spaceship']
    
    print("\nAvailable Patterns:")
    for i, pattern in enumerate(patterns, 1):
        print(f"{i:2}. {pattern.replace('_', ' ').title()}")
    
    while True:
        try:
            choice = input(f"\nEnter pattern number (1-{len(patterns)}) or 0 to cancel: ").strip()
            if choice == '0':
                return None
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(patterns):
                return patterns[choice_idx]
            else:
                print(f"Please enter a number between 1 and {len(patterns)}")
        except ValueError:
            print("Please enter a valid number")

def show_analytics(stats, grid=None):
    """Display detailed analytics"""
    print("\n" + "="*50)
    print("GAME OF LIFE ANALYTICS")
    print("="*50)
    
    summary = stats.get_summary()
    
    print(f"Generation: {summary['generation']}")
    print(f"Current Population: {summary['current_population']}")
    print(f"Maximum Population: {summary['max_population']}")
    print(f"Minimum Population: {summary['min_population']}")
    print(f"Growth Rate: {summary['growth_rate']:.3f} cells/generation")
    print(f"Status: {summary['status']}")
    if summary['stable_count'] > 0:
        print(f"Stable for: {summary['stable_count']} generations")
    
    # Show population trend
    if len(stats.population_history) > 1:
        recent_pops = [p[1] for p in list(stats.population_history)[-10:]]
        print(f"Recent Population: {' → '.join(map(str, recent_pops))}")
    
    # Pattern detection
    patterns = find_patterns_in_grid(grid) if 'grid' in globals() else []
    if patterns:
        print(f"Detected Patterns: {', '.join(patterns).title()}")
    else:
        print("No common patterns detected")
    
    print("="*50)
    input("Press Enter to continue...")

def run_terminal_version():
    """Run the enhanced terminal version"""
    rows, cols = 25, 50
    grid = initialize_grid(rows, cols, 0.25)
    generation = 0
    paused = False
    last_update_time = time.time()
    
    # Enhanced features
    history = [grid]
    history_pos = 0
    stats = GameStats()
    stats.update(grid, generation)
    
    print("Conway's Game of Life - ULTIMATE Terminal Edition")
    print("Features: Patterns • Analytics • GIF Export • Web Export • Pattern Detection")
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    print_grid_terminal(grid, generation, paused, history_pos, len(history)-1, stats)
    
    try:
        while True:
            current_time = time.time()
            key = get_key()
            should_redraw = False
            
            if key == 'space': 
                paused = not paused
                should_redraw = True
            elif key == 'right':
                if history_pos < len(history) - 1:
                    history_pos += 1
                    grid = [row[:] for row in history[history_pos]]
                    generation = history_pos
                else:
                    new_grid = next_generation(grid)
                    history.append([row[:] for row in new_grid])
                    if len(history) > 1000:
                        history.pop(0)
                    else:
                        history_pos += 1
                    grid = new_grid
                    generation += 1
                stats.update(grid, generation)
                should_redraw = True
            elif key == 'left':
                if history_pos > 0:
                    history_pos -= 1
                    grid = [row[:] for row in history[history_pos]]
                    generation = history_pos
                    stats.update(grid, generation)
                    should_redraw = True
            elif key == 'r': 
                grid = initialize_grid(rows, cols, 0.25)
                generation = 0
                history = [grid]
                history_pos = 0
                stats = GameStats()
                stats.update(grid, generation)
                should_redraw = True
            elif key == 'p':
                pattern_name = show_pattern_menu()
                if pattern_name:
                    pattern = load_pattern(pattern_name)
                    if pattern:
                        start_row = (rows - len(pattern)) // 2
                        start_col = (cols - len(pattern[0])) // 2
                        grid = place_pattern(grid, pattern, start_row, start_col)
                        generation = 0
                        history = [grid]
                        history_pos = 0
                        stats = GameStats()
                        stats.update(grid, generation)
                        should_redraw = True
                        print(f"\n{pattern_name.replace('_', ' ').title()} placed!")
                        time.sleep(1)
            elif key == 's':
                success, message = save_state(grid, generation)
                print(f"\n{message}")
                time.sleep(2)
                should_redraw = True
            elif key == 'l':
                success, loaded_grid, loaded_gen = load_state()
                if success:
                    grid = loaded_grid
                    generation = loaded_gen
                    history = [grid]
                    history_pos = 0
                    stats = GameStats()
                    stats.update(grid, generation)
                    print("\nGame loaded successfully!")
                else:
                    print("\nNo save file found!")
                time.sleep(2)
                should_redraw = True
            elif key == 'e':
                success, message = export_as_image(grid, f"generation_{generation}.png")
                print(f"\n{message}")
                time.sleep(2)
                should_redraw = True
            elif key == 'g':  # GIF export
                if len(history) > 1:
                    success, message = export_gif(history, f"simulation_{generation}.gif")
                    print(f"\n{message}")
                else:
                    print("\nNeed more history for GIF export!")
                time.sleep(2)
                should_redraw = True
            elif key == 'w':  # Web export
                success, message = export_web(grid, f"gameoflife_{generation}.html")
                print(f"\n{message}")
                time.sleep(2)
                should_redraw = True
            elif key == 'a':  # Analytics
                show_analytics(stats, grid)
                should_redraw = True
            elif key.startswith('gui') or key == 'u':
                return run_gui_version()
            elif key == 'q': 
                print("\nGoodbye!")
                return
            
            # Auto-advance if not paused
            if not paused and current_time - last_update_time >= 0.3:
                if history_pos < len(history) - 1:
                    history_pos += 1
                    grid = [row[:] for row in history[history_pos]]
                    generation = history_pos
                else:
                    new_grid = next_generation(grid)
                    history.append([row[:] for row in new_grid])
                    if len(history) > 1000:
                        history.pop(0)
                    else:
                        history_pos += 1
                    grid = new_grid
                    generation += 1
                stats.update(grid, generation)
                last_update_time = current_time
                should_redraw = True
            
            if should_redraw:
                print_grid_terminal(grid, generation, paused, history_pos, len(history)-1, stats)
            
            time.sleep(0.01)
                
    except KeyboardInterrupt:
        print("\nGame stopped by user (Ctrl+C)")

def run_gui_version():
    """Run the enhanced GUI version"""
    try:
        import tkinter as tk
        from tkinter import messagebox, filedialog, ttk
        try:
            from PIL import ImageTk
        except ImportError:
            ImageTk = None
    except ImportError:
        print("GUI not available - tkinter not installed")
        print("Returning to terminal version...")
        return run_terminal_version()
    
    class GameOfLifeGUI:
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("Conway's Game of Life - Enhanced Edition")
            self.root.geometry("1000x700")
            
            # Game state
            self.rows = 30
            self.cols = 40
            self.cell_size = 10
            self.grid = initialize_grid(self.rows, self.cols, 0.25)
            self.generation = 0
            self.paused = True
            self.history = [self.grid]
            self.history_pos = 0
            self.speed = 200
            self.stats = GameStats()
            self.stats.update(self.grid, self.generation)
            
            self.setup_ui()
            self.update_display()
            
        def setup_ui(self):
            # Control frame
            control_frame = tk.Frame(self.root)
            control_frame.pack(fill=tk.X, padx=5, pady=5)
            
            # Basic controls
            tk.Button(control_frame, text="Play/Pause", command=self.toggle_pause).pack(side=tk.LEFT, padx=2)
            tk.Button(control_frame, text="Step", command=self.step_forward).pack(side=tk.LEFT, padx=2)
            tk.Button(control_frame, text="Reset", command=self.reset_grid).pack(side=tk.LEFT, padx=2)
            tk.Button(control_frame, text="Clear", command=self.clear_grid).pack(side=tk.LEFT, padx=2)
            tk.Button(control_frame, text="Patterns", command=self.load_pattern_gui).pack(side=tk.LEFT, padx=2)
            
            # Export controls
            tk.Button(control_frame, text="Save", command=self.save_game).pack(side=tk.LEFT, padx=2)
            tk.Button(control_frame, text="Load", command=self.load_game).pack(side=tk.LEFT, padx=2)
            tk.Button(control_frame, text="Export PNG", command=self.export_image).pack(side=tk.LEFT, padx=2)
            
            # Speed control
            speed_frame = tk.Frame(control_frame)
            speed_frame.pack(side=tk.RIGHT)
            tk.Label(speed_frame, text="Speed:").pack(side=tk.LEFT)
            self.speed_var = tk.IntVar(value=self.speed)
            self.speed_scale = tk.Scale(speed_frame, from_=50, to=1000, orient=tk.HORIZONTAL, 
                                       variable=self.speed_var, length=100)
            self.speed_scale.pack(side=tk.LEFT)
            
            # Status frame
            status_frame = tk.Frame(self.root)
            status_frame.pack(fill=tk.X, padx=5)
            
            self.status_label = tk.Label(status_frame, text="Generation: 0 | PAUSED")
            self.status_label.pack()
            
            # Canvas
            self.canvas = tk.Canvas(self.root, bg='white', width=600, height=400)
            self.canvas.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
            self.canvas.bind('<Button-1>', self.on_canvas_click)
            
            # Keyboard bindings
            self.root.bind('<space>', lambda e: self.toggle_pause())
            self.root.bind('<Return>', lambda e: self.step_forward())
            self.root.focus_set()
            
        def clear_grid(self):
            self.grid = [[0] * self.cols for _ in range(self.rows)]
            self.generation = 0
            self.history = [self.grid]
            self.history_pos = 0
            self.paused = True
            self.stats = GameStats()
            self.stats.update(self.grid, self.generation)
            self.update_display()
            
        def load_pattern_gui(self):
            patterns = ['glider', 'blinker', 'block', 'beehive', 'toad', 'beacon', 'pulsar']
            
            dialog = tk.Toplevel(self.root)
            dialog.title("Select Pattern")
            dialog.geometry("300x400")
            
            tk.Label(dialog, text="Choose a pattern:", font=('Arial', 12)).pack(pady=10)
            
            selected_pattern = [None]
            
            for pattern_name in patterns:
                btn = tk.Button(dialog, text=pattern_name.replace('_', ' ').title(),
                               command=lambda p=pattern_name: self.select_pattern(p, selected_pattern, dialog))
                btn.pack(pady=2, fill=tk.X, padx=20)
            
            tk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=10)
            
            dialog.wait_window()
            
            if selected_pattern[0]:
                pattern = load_pattern(selected_pattern[0])
                if pattern:
                    start_row = (self.rows - len(pattern)) // 2
                    start_col = (self.cols - len(pattern[0])) // 2
                    self.grid = place_pattern(self.grid, pattern, start_row, start_col)
                    self.generation = 0
                    self.history = [self.grid]
                    self.history_pos = 0
                    self.paused = True
                    self.stats = GameStats()
                    self.stats.update(self.grid, self.generation)
                    self.update_display()
        
        def select_pattern(self, pattern_name, selected_pattern, dialog):
            selected_pattern[0] = pattern_name
            dialog.destroy()
        
        def save_game(self):
            filename = filedialog.asksaveasfilename(defaultextension=".json")
            if filename:
                success, message = save_state(self.grid, self.generation, filename)
                messagebox.showinfo("Save", message)
        
        def load_game(self):
            filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            if filename:
                success, loaded_grid, loaded_gen = load_state(filename)
                if success:
                    self.grid = loaded_grid
                    self.generation = loaded_gen
                    self.history = [self.grid]
                    self.history_pos = 0
                    self.paused = True
                    self.stats = GameStats()
                    self.stats.update(self.grid, self.generation)
                    self.update_display()
                    messagebox.showinfo("Load", "Game loaded successfully!")
        
        def export_image(self):
            filename = filedialog.asksaveasfilename(defaultextension=".png")
            if filename:
                success, message = export_as_image(self.grid, filename)
                messagebox.showinfo("Export", message)
        
        def on_canvas_click(self, event):
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            total_width = self.cols * self.cell_size
            total_height = self.rows * self.cell_size
            offset_x = (canvas_width - total_width) // 2
            offset_y = (canvas_height - total_height) // 2
            
            adjusted_x = event.x - offset_x
            adjusted_y = event.y - offset_y
            
            if adjusted_x >= 0 and adjusted_y >= 0:
                col = adjusted_x // self.cell_size
                row = adjusted_y // self.cell_size
                if 0 <= row < self.rows and 0 <= col < self.cols:
                    self.grid[row][col] = 1 - self.grid[row][col]
                    self.stats.update(self.grid, self.generation)
                    self.update_display()
        
        def toggle_pause(self):
            self.paused = not self.paused
            if not self.paused:
                self.auto_step()
            self.update_display()
        
        def step_forward(self):
            new_grid = next_generation(self.grid)
            self.history.append([row[:] for row in new_grid])
            if len(self.history) > 100:
                self.history.pop(0)
            else:
                self.history_pos += 1
            self.grid = new_grid
            self.generation += 1
            self.stats.update(self.grid, self.generation)
            self.update_display()
        
        def reset_grid(self):
            self.grid = initialize_grid(self.rows, self.cols, 0.25)
            self.generation = 0
            self.history = [self.grid]
            self.history_pos = 0
            self.paused = True
            self.stats = GameStats()
            self.stats.update(self.grid, self.generation)
            self.update_display()
        
        def update_display(self):
            self.canvas.delete("all")
            
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:
                max_cell_width = canvas_width // self.cols
                max_cell_height = canvas_height // self.rows
                self.cell_size = min(max_cell_width, max_cell_height, 20)
                
                total_width = self.cols * self.cell_size
                total_height = self.rows * self.cell_size
                
                offset_x = (canvas_width - total_width) // 2
                offset_y = (canvas_height - total_height) // 2
                
                for i in range(self.rows):
                    for j in range(self.cols):
                        x1 = offset_x + j * self.cell_size
                        y1 = offset_y + i * self.cell_size
                        x2 = x1 + self.cell_size
                        y2 = y1 + self.cell_size
                        
                        color = 'black' if self.grid[i][j] else 'white'
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')
            
            status = 'RUNNING' if not self.paused else 'PAUSED'
            live_cells = sum(sum(row) for row in self.grid)
            self.status_label.config(text=f"Generation: {self.generation} | {status} | Population: {live_cells}")
            
            if not self.paused:
                self.speed = self.speed_var.get()
                self.root.after(self.speed, self.auto_step)
        
        def auto_step(self):
            if not self.paused:
                self.step_forward()
        
        def run(self):
            self.root.mainloop()
    
    gui = GameOfLifeGUI()
    gui.run()

def initialize_3d_grid(x_size, y_size, z_size, density=0.1):
    """Initialize a 3D grid for 3D Game of Life"""
    try:
        import numpy as np
        return np.random.choice([0, 1], size=(x_size, y_size, z_size), p=[1-density, density])
    except ImportError:
        # Fallback without numpy
        return [[[1 if random.random() < density else 0 
                 for _ in range(z_size)] 
                for _ in range(y_size)] 
               for _ in range(x_size)]

def count_3d_neighbors(grid, x, y, z):
    """Count neighbors in 3D space"""
    try:
        import numpy as np
        if isinstance(grid, np.ndarray):
            X, Y, Z = grid.shape
            count = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    for dz in [-1, 0, 1]:
                        if dx == dy == dz == 0:
                            continue
                        nx, ny, nz = (x+dx) % X, (y+dy) % Y, (z+dz) % Z
                        count += grid[nx, ny, nz]
            return count
    except ImportError:
        pass
    
    # Fallback for regular lists
    X, Y, Z = len(grid), len(grid[0]), len(grid[0][0])
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                if dx == dy == dz == 0:
                    continue
                nx, ny, nz = (x+dx) % X, (y+dy) % Y, (z+dz) % Z
                count += grid[nx][ny][nz]
    return count

def next_3d_generation(grid):
    """3D Game of Life rules (simplified)"""
    try:
        import numpy as np
        if isinstance(grid, np.ndarray):
            X, Y, Z = grid.shape
            new_grid = np.zeros_like(grid)
            
            for x in range(X):
                for y in range(Y):
                    for z in range(Z):
                        neighbors = count_3d_neighbors(grid, x, y, z)
                        # 3D rules: survive with 4-6 neighbors, birth with 5 neighbors
                        if grid[x, y, z] == 1:
                            if 4 <= neighbors <= 6:
                                new_grid[x, y, z] = 1
                        else:
                            if neighbors == 5:
                                new_grid[x, y, z] = 1
            return new_grid
    except ImportError:
        pass
    
    # Fallback implementation
    X, Y, Z = len(grid), len(grid[0]), len(grid[0][0])
    new_grid = [[[0 for _ in range(Z)] for _ in range(Y)] for _ in range(X)]
    
    for x in range(X):
        for y in range(Y):
            for z in range(Z):
                neighbors = count_3d_neighbors(grid, x, y, z)
                if grid[x][y][z] == 1:
                    if 4 <= neighbors <= 6:
                        new_grid[x][y][z] = 1
                else:
                    if neighbors == 5:
                        new_grid[x][y][z] = 1
    return new_grid

def run_3d_demo():
    """Demo 3D Game of Life (requires matplotlib)"""
    try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        import numpy as np
        
        print("3D Game of Life Demo")
        print("Initializing 3D grid...")
        
        grid = initialize_3d_grid(15, 15, 15, 0.15)
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        for generation in range(10):
            ax.clear()
            ax.set_title(f'3D Game of Life - Generation {generation}')
            
            # Plot live cells
            if isinstance(grid, np.ndarray):
                live_cells = np.where(grid == 1)
                if len(live_cells[0]) > 0:
                    ax.scatter(live_cells[0], live_cells[1], live_cells[2], 
                             c='red', s=20, alpha=0.6)
            else:
                # Fallback for regular lists
                xs, ys, zs = [], [], []
                for x in range(len(grid)):
                    for y in range(len(grid[0])):
                        for z in range(len(grid[0][0])):
                            if grid[x][y][z]:
                                xs.append(x)
                                ys.append(y)
                                zs.append(z)
                if xs:
                    ax.scatter(xs, ys, zs, c='red', s=20, alpha=0.6)
            
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_xlim(0, 15)
            ax.set_ylim(0, 15)
            ax.set_zlim(0, 15)
            
            plt.pause(1)
            grid = next_3d_generation(grid)
            
            if isinstance(grid, np.ndarray):
                live_count = np.sum(grid)
            else:
                live_count = sum(sum(sum(plane) for plane in layer) for layer in grid)
            
            print(f"Generation {generation}: {live_count} live cells")
            
            if live_count == 0:
                print("Population extinct!")
                break
        
        plt.show()
        return True
    except ImportError as e:
        print(f"3D demo requires matplotlib and numpy: {e}")
        print("Install with: pip install matplotlib numpy")
        return False

def main():
    """Ultimate main function"""
    print("Conway's Game of Life - ULTIMATE EDITION")
    print("=" * 60)
    print("Features:")
    print("  • Pattern Previews & Enhanced Selection")
    print("  • GIF Animation Export & Live Recording")
    print("  • Advanced Analytics & Growth Tracking")
    print("  • Real-time Pattern Detection")
    print("  • Interactive Web Export")
    print("  • 3D Game of Life Demo")
    print("  • Enhanced Save/Load System")
    print("  • Professional GUI with Statistics")
    print("  • Speed Controls & History Navigation")
    print("=" * 60)
    print()
    print("Choose your adventure:")
    print("1. Terminal version (keyboard controls + analytics)")
    print("2. GUI version (mouse + keyboard, full features)")
    print("3. 3D Demo (experimental 3D Game of Life)")
    
    while True:
        choice = input("\nEnter choice (1, 2, or 3): ").strip()
        if choice == '1':
            run_terminal_version()
            break
        elif choice == '2':
            run_gui_version()
            break
        elif choice == '3':
            if not run_3d_demo():
                print("Falling back to 2D version...")
                run_gui_version()
            break
        else:
            print("Please enter 1, 2, or 3")

if __name__ == '__main__':
    main()