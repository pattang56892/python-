import random
import os
import time
import sys
import json
from collections import deque

# Optional: numpy support
try:
    import numpy as np
except ImportError:
    np = None

# ========================
# Core Game of Life Logic
# ========================

def initialize_grid(rows, cols, density=0.2):
    """Initialize a random grid with given density"""
    return [[1 if random.random() < density else 0 
             for _ in range(cols)] for _ in range(rows)]

def count_neighbors(grid, row, col):
    """Count live neighbors for a cell at (row, col) with toroidal wrapping"""
    rows, cols = len(grid), len(grid[0])
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr = (row + dr) % rows
            nc = (col + dc) % cols
            count += grid[nr][nc]
    return count

def next_generation(grid):
    """Compute the next generation based on Conway's rules"""
    rows, cols = len(grid), len(grid[0])
    new_grid = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            neighbors = count_neighbors(grid, i, j)
            current_state = grid[i][j]
            if current_state == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[i][j] = 0
                else:
                    new_grid[i][j] = 1
            else:
                if neighbors == 3:
                    new_grid[i][j] = 1
    return new_grid

# ========================
# Pattern Support
# ========================

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

def place_pattern(grid, pattern, start_row, start_col):
    """Place a pattern on the grid at specified position with wrapping"""
    if not pattern:
        return grid
    rows, cols = len(grid), len(grid[0])
    pattern_rows, pattern_cols = len(pattern), len(pattern[0])
    new_grid = [row[:] for row in grid]
    for i in range(pattern_rows):
        for j in range(pattern_cols):
            new_row = (start_row + i) % rows
            new_col = (start_col + j) % cols
            new_grid[new_row][new_col] = pattern[i][j]
    return new_grid

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
    """Check if pattern exists anywhere in grid (non-wrapping)"""
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

# ========================
# Utilities & I/O
# ========================

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
    """Export history as animated GIF (last 50 frames)"""
    try:
        from PIL import Image, ImageDraw
        if not grid_history:
            return False, "No history to export"
        frames = []
        for grid in grid_history[-50:]:
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

def create_pattern_preview(pattern, size=80):
    """Generate a small preview image of a pattern (for GUI)"""
    try:
        from PIL import Image, ImageDraw, ImageTk
        if not pattern:
            return None
        rows, cols = len(pattern), len(pattern[0])
        if rows == 0 or cols == 0:
            return None
        cell_size = max(1, min(size // max(rows, cols), 8))
        img_width = cols * cell_size + 10
        img_height = rows * cell_size + 10
        img = Image.new('RGB', (img_width, img_height), 'white')
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, img_width-1, img_height-1], outline='gray')
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

# ========================
# Statistics
# ========================

class GameStats:
    """Advanced statistics tracking for Game of Life"""
    def __init__(self):
        self.population_history = deque(maxlen=1000)
        self.generation = 0
        self.max_population = 0
        self.min_population = float('inf')
        self.stable_count = 0
        self.last_population = 0

    def update(self, grid, gen):
        live_cells = sum(sum(row) for row in grid)
        self.population_history.append((gen, live_cells))
        self.generation = gen
        self.max_population = max(self.max_population, live_cells)
        if live_cells > 0:
            self.min_population = min(self.min_population, live_cells)
        if live_cells == self.last_population:
            self.stable_count += 1
        else:
            self.stable_count = 0
        self.last_population = live_cells

    def get_growth_rate(self, window=10):
        if len(self.population_history) < 2:
            return 0
        recent = list(self.population_history)[-window:]
        if len(recent) < 2:
            return 0
        total_change = recent[-1][1] - recent[0][1]
        time_span = recent[-1][0] - recent[0][0]
        return total_change / time_span if time_span > 0 else 0

    def get_current_population(self):
        return self.population_history[-1][1] if self.population_history else 0

    def is_stable(self, threshold=5):
        return self.stable_count >= threshold

    def is_extinct(self):
        return self.get_current_population() == 0

    def get_summary(self):
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
    if len(stats.population_history) > 1:
        recent_pops = [p[1] for p in list(stats.population_history)[-10:]]
        print(f"Recent Population Trend: {' → '.join(map(str, recent_pops))}")
    if len(stats.population_history) > 5:
        populations = [p[1] for p in stats.population_history]
        avg_population = sum(populations) / len(populations)
        print(f"Average Population: {avg_population:.1f}")
        if len(populations) > 1:
            changes = [abs(populations[i] - populations[i-1]) for i in range(1, len(populations))]
            avg_change = sum(changes) / len(changes) if changes else 0
            print(f"Average Change per Generation: {avg_change:.2f}")
    if grid is not None:
        print("\n" + "-"*30)
        print("PATTERN ANALYSIS")
        print("-"*30)
        patterns = find_patterns_in_grid(grid)
        if patterns:
            print(f"Detected Patterns: {', '.join(patterns).title()}")
        else:
            print("No common patterns detected")
    print("="*50)
    print("Analytics displayed - returning to game...")
    time.sleep(3)

# ========================
# Terminal UI
# ========================

def print_grid_terminal(grid, generation, paused, history_pos, max_history, stats=None):
    """Print the grid in terminal"""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    for row in grid:
        print(' '.join(['■' if cell else '.' for cell in row]))
    status = 'PAUSED' if paused else 'RUNNING'
    history_info = f" | History: {history_pos}/{max_history}" if max_history > 0 else ""
    print(f"\nGeneration: {generation} | {status}{history_info}")
    if stats:
        summary = stats.get_summary()
        print(f"Population: {summary['current_population']} | Growth Rate: {summary['growth_rate']:.2f} | Status: {summary['status']}")
        patterns = find_patterns_in_grid(grid)
        if patterns:
            print(f"Patterns Detected: {', '.join(patterns).title()}")
    print("Controls: [Space] Play/Pause | [→] Forward | [←] Backward | [R]eset | [P]attern | [S]ave | [L]oad")
    print("Advanced: [E]xport PNG | [G]IF Export | [W]eb Export | [A]nalytics | [GUI] Switch | [Q]uit")

def get_key():
    """Get single keypress without Enter - cross-platform"""
    try:
        import msvcrt
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\x03':
                raise KeyboardInterrupt
            elif key == b'\xe0':
                key2 = msvcrt.getch()
                if key2 == b'M':
                    return 'right'
                elif key2 == b'K':
                    return 'left'
                return None
            elif key == b' ':
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
                    if key == '\x1b':
                        key += sys.stdin.read(2)
                        if key == '\x1b[C':
                            return 'right'
                        elif key == '\x1b[D':
                            return 'left'
                        return None
                    elif key == ' ':
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

def run_terminal_version():
    """Run the enhanced terminal version"""
    rows, cols = 25, 50
    grid = initialize_grid(rows, cols, 0.25)
    generation = 0
    paused = False
    last_update_time = time.time()
    history = [grid]
    history_pos = 0
    stats = GameStats()
    stats.update(grid, generation)
    print("Conway's Game of Life - ULTIMATE Terminal Edition")
    print("🚀 Features: Patterns • Analytics • GIF Export • Web Export • Pattern Detection")
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
            elif key == 'g':
                if len(history) > 1:
                    success, message = export_gif(history, f"simulation_{generation}.gif")
                    print(f"\n{message}")
                else:
                    print("\nNeed more history for GIF export!")
                time.sleep(2)
                should_redraw = True
            elif key == 'w':
                success, message = export_web(grid, f"gameoflife_{generation}.html")
                print(f"\n{message}")
                time.sleep(2)
                should_redraw = True
            elif key == 'a':
                show_analytics(stats, grid)
                should_redraw = True
            elif key.startswith('gui') or key == 'u':
                return run_gui_version()
            elif key == 'q': 
                print("\nGoodbye!")
                return
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

# ========================
# GUI Version
# ========================

def run_gui_version():
    """Run the ULTIMATE enhanced GUI version"""
    try:
        import tkinter as tk
        from tkinter import messagebox, filedialog
    except ImportError:
        print("GUI not available - tkinter not installed")
        print("Returning to terminal version...")
        return run_terminal_version()

    class UltimateGameOfLifeGUI:
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("Conway's Game of Life - ULTIMATE Edition")
            self.root.geometry("1200x800")
            self.rows = 40
            self.cols = 60
            self.cell_size = 8
            self.grid = initialize_grid(self.rows, self.cols, 0.25)
            self.generation = 0
            self.paused = True
            self.history = [self.grid]
            self.history_pos = 0
            self.speed = 200
            self.stats = GameStats()
            self.stats.update(self.grid, self.generation)
            self.recording = False
            self.recorded_frames = []
            self.setup_ui()
            self.update_display()

        def setup_ui(self):
            top_frame = tk.Frame(self.root)
            top_frame.pack(fill=tk.X, padx=5, pady=5)
            control_frame1 = tk.Frame(top_frame)
            control_frame1.pack(side=tk.LEFT, fill=tk.X, expand=True)
            stats_frame = tk.Frame(top_frame)
            stats_frame.pack(side=tk.RIGHT, padx=10)

            basic_controls = tk.LabelFrame(control_frame1, text="Basic Controls", font=('Arial', 9, 'bold'))
            basic_controls.pack(side=tk.LEFT, padx=5, pady=2)
            tk.Button(basic_controls, text="▶️ Play/Pause", command=self.toggle_pause, bg='#4CAF50', fg='white').pack(side=tk.LEFT, padx=2)
            tk.Button(basic_controls, text="⏭️ Step", command=self.step_forward, bg='#2196F3', fg='white').pack(side=tk.LEFT, padx=2)
            tk.Button(basic_controls, text="⏮️ Back", command=self.step_backward, bg='#FF9800', fg='white').pack(side=tk.LEFT, padx=2)
            tk.Button(basic_controls, text="🔄 Reset", command=self.reset_grid, bg='#F44336', fg='white').pack(side=tk.LEFT, padx=2)
            tk.Button(basic_controls, text="🗑️ Clear", command=self.clear_grid, bg='#9E9E9E', fg='white').pack(side=tk.LEFT, padx=2)
            speed_subframe = tk.Frame(basic_controls)
            speed_subframe.pack(side=tk.LEFT, padx=5)
            tk.Label(speed_subframe, text="Speed:", font=('Arial', 8)).pack(side=tk.LEFT)
            self.speed_var = tk.IntVar(value=self.speed)
            self.speed_scale = tk.Scale(speed_subframe, from_=50, to=1000, orient=tk.HORIZONTAL, 
                                       variable=self.speed_var, length=80, command=self.update_speed)
            self.speed_scale.pack(side=tk.LEFT)

            advanced_controls = tk.LabelFrame(control_frame1, text="Advanced Features", font=('Arial', 9, 'bold'))
            advanced_controls.pack(side=tk.LEFT, padx=5, pady=2)
            tk.Button(advanced_controls, text="🎭 Patterns", command=self.load_pattern_gui, bg='#9C27B0', fg='white').pack(side=tk.LEFT, padx=2)
            tk.Button(advanced_controls, text="💾 Save", command=self.save_game, bg='#607D8B', fg='white').pack(side=tk.LEFT, padx=2)
            tk.Button(advanced_controls, text="📁 Load", command=self.load_game, bg='#795548', fg='white').pack(side=tk.LEFT, padx=2)

            export_controls = tk.LabelFrame(control_frame1, text="Export Options", font=('Arial', 9, 'bold'))
            export_controls.pack(side=tk.LEFT, padx=5, pady=2)
            tk.Button(export_controls, text="📷 PNG", command=self.export_image, bg='#00BCD4', fg='white').pack(side=tk.LEFT, padx=2)
            tk.Button(export_controls, text="🎬 GIF", command=self.export_gif_gui, bg='#E91E63', fg='white').pack(side=tk.LEFT, padx=2)
            tk.Button(export_controls, text="🌐 Web", command=self.export_web_gui, bg='#3F51B5', fg='white').pack(side=tk.LEFT, padx=2)
            record_frame = tk.Frame(export_controls)
            record_frame.pack(side=tk.LEFT, padx=5)
            self.record_button = tk.Button(record_frame, text="🔴 Record", command=self.toggle_recording, bg='#F44336', fg='white')
            self.record_button.pack()

            stats_label = tk.Label(stats_frame, text="📊 Live Statistics", font=('Arial', 10, 'bold'))
            stats_label.pack()
            self.stats_text = tk.Text(stats_frame, width=25, height=8, font=('Courier', 8), state=tk.DISABLED)
            self.stats_text.pack(fill=tk.BOTH, expand=True)
            self.pattern_frame = tk.LabelFrame(stats_frame, text="🔍 Detected Patterns", font=('Arial', 9, 'bold'))
            self.pattern_frame.pack(fill=tk.X, pady=5)
            self.pattern_label = tk.Label(self.pattern_frame, text="None detected", font=('Arial', 8), wraplength=200)
            self.pattern_label.pack()

            status_frame = tk.Frame(self.root)
            status_frame.pack(fill=tk.X, padx=5)
            self.status_label = tk.Label(status_frame, text="Generation: 0 | PAUSED", font=('Arial', 12, 'bold'))
            self.status_label.pack()
            self.pop_label = tk.Label(status_frame, text="Population: 0 | Growth Rate: 0.00", font=('Arial', 10))
            self.pop_label.pack()
            help_text = ("🎮 Controls: [Space] Play/Pause | [→←] Step | [R]eset | [C]lear | [P]attern | Click/Drag to draw")
            help_label = tk.Label(status_frame, text=help_text, font=('Arial', 8), fg='gray')
            help_label.pack()

            self.canvas = tk.Canvas(self.root, bg='white', width=800, height=500)
            self.canvas.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
            self.canvas.bind('<Button-1>', self.on_canvas_click)
            self.canvas.bind('<B1-Motion>', self.on_canvas_drag)
            self.root.focus_set()
            self.root.bind('<KeyPress>', self.on_key_press)
            self.root.bind('<Left>', self.on_arrow_key)
            self.root.bind('<Right>', self.on_arrow_key)

        def update_speed(self, value):
            self.speed = int(value)

        def clear_grid(self):
            self.grid = [[0] * self.cols for _ in range(self.rows)]
            self.generation = 0
            self.history = [[row[:] for row in self.grid]]
            self.history_pos = 0
            self.paused = True
            self.stats = GameStats()
            self.stats.update(self.grid, self.generation)
            self.update_display()

        def get_grid_stats(self):
            live_cells = sum(sum(row) for row in self.grid)
            total_cells = self.rows * self.cols
            population_percent = (live_cells / total_cells) * 100 if total_cells > 0 else 0
            return live_cells, population_percent

        def toggle_recording(self):
            self.recording = not self.recording
            if self.recording:
                self.recorded_frames = []
                self.record_button.config(text="⏹️ Stop", bg='#4CAF50')
            else:
                self.record_button.config(text="🔴 Record", bg='#F44336')
                if self.recorded_frames:
                    self.export_recorded_gif()

        def export_recorded_gif(self):
            if not self.recorded_frames:
                messagebox.showwarning("No Recording", "No frames recorded!")
                return
            filename = filedialog.asksaveasfilename(
                defaultextension=".gif",
                filetypes=[("GIF files", "*.gif"), ("All files", "*.*")],
                title="Save Recorded Animation"
            )
            if filename:
                success, message = export_gif(self.recorded_frames, filename, cell_size=15, duration=150)
                if success:
                    messagebox.showinfo("Export Successful", message)
                else:
                    messagebox.showerror("Export Failed", message)

        def load_pattern_gui(self):
            patterns = ['glider', 'blinker', 'block', 'beehive', 'loaf', 'boat', 'tub', 
                       'beacon', 'toad', 'pulsar', 'gosper_gun', 'penta_decathlon', 'lightweight_spaceship']
            dialog = tk.Toplevel(self.root)
            dialog.title("🎭 Select Pattern")
            dialog.geometry("500x600")
            dialog.transient(self.root)
            dialog.grab_set()
            main_frame = tk.Frame(dialog)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            canvas_frame = tk.Canvas(main_frame)
            scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas_frame.yview)
            scrollable_frame = tk.Frame(canvas_frame)
            scrollable_frame.bind("<Configure>", lambda e: canvas_frame.configure(scrollregion=canvas_frame.bbox("all")))
            canvas_frame.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas_frame.configure(yscrollcommand=scrollbar.set)
            tk.Label(scrollable_frame, text="Choose a pattern:", font=('Arial', 14, 'bold')).pack(pady=10)
            selected_pattern = [None]
            for i, pattern_name in enumerate(patterns):
                frame = tk.Frame(scrollable_frame, relief=tk.RAISED, borderwidth=1)
                frame.pack(fill=tk.X, padx=5, pady=3)
                preview_frame = tk.Frame(frame)
                preview_frame.pack(side=tk.LEFT, padx=10, pady=5)
                pattern = load_pattern(pattern_name)
                try:
                    from PIL import ImageTk
                    if ImageTk and pattern:
                        preview_img = create_pattern_preview(pattern, size=60)
                        if preview_img:
                            preview_label = tk.Label(preview_frame, image=preview_img)
                            preview_label.image = preview_img
                            preview_label.pack()
                        else:
                            tk.Label(preview_frame, text="[Preview]", width=8, height=3, bg='lightgray').pack()
                    else:
                        tk.Label(preview_frame, text="[Preview]", width=8, height=3, bg='lightgray').pack()
                except:
                    tk.Label(preview_frame, text="[Preview]", width=8, height=3, bg='lightgray').pack()
                info_frame = tk.Frame(frame)
                info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=5)
                name_label = tk.Label(info_frame, text=pattern_name.replace('_', ' ').title(), font=('Arial', 12, 'bold'))
                name_label.pack(anchor=tk.W)
                descriptions = {
                    'glider': 'Travels diagonally across the grid',
                    'blinker': 'Oscillates between horizontal and vertical',
                    'block': 'Static 2x2 square (still life)',
                    'beehive': 'Static hexagonal shape (still life)',
                    'loaf': 'Static asymmetric shape (still life)',
                    'boat': 'Small static shape (still life)',
                    'tub': 'Small circular static shape (still life)',
                    'beacon': 'Oscillates with 2-generation period',
                    'toad': 'Oscillates with 2-generation period',
                    'pulsar': 'Large oscillator with 3-generation period',
                    'gosper_gun': 'Generates gliders indefinitely',
                    'penta_decathlon': 'Oscillates with 15-generation period',
                    'lightweight_spaceship': 'Travels horizontally across grid'
                }
                desc_label = tk.Label(info_frame, text=descriptions.get(pattern_name, 'Classic Game of Life pattern'), 
                                    font=('Arial', 9), wraplength=300, justify=tk.LEFT)
                desc_label.pack(anchor=tk.W)
                select_btn = tk.Button(info_frame, text="Select", 
                                     command=lambda p=pattern_name: self.select_pattern(p, selected_pattern, dialog),
                                     bg='#4CAF50', fg='white')
                select_btn.pack(anchor=tk.E, pady=2)
            canvas_frame.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            tk.Button(dialog, text="Cancel", command=dialog.destroy, bg='#F44336', fg='white').pack(pady=10)
            dialog.wait_window()
            if selected_pattern[0]:
                pattern = load_pattern(selected_pattern[0])
                if pattern:
                    start_row = (self.rows - len(pattern)) // 2
                    start_col = (self.cols - len(pattern[0])) // 2
                    self.grid = place_pattern(self.grid, pattern, start_row, start_col)
                    self.generation = 0
                    self.history = [[row[:] for row in self.grid]]
                    self.history_pos = 0
                    self.paused = True
                    self.stats = GameStats()
                    self.stats.update(self.grid, self.generation)
                    self.update_display()
                    messagebox.showinfo("Pattern Loaded", 
                                      f"🎭 {selected_pattern[0].replace('_', ' ').title()} loaded successfully!")

        def select_pattern(self, pattern_name, selected_pattern, dialog):
            selected_pattern[0] = pattern_name
            dialog.destroy()

        def save_game(self):
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Save Game State"
            )
            if filename:
                success, message = save_state(self.grid, self.generation, filename)
                if success:
                    messagebox.showinfo("💾 Save Successful", message)
                else:
                    messagebox.showerror("Save Failed", message)

        def load_game(self):
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Load Game State"
            )
            if filename:
                success, loaded_grid, loaded_gen = load_state(filename)
                if success:
                    self.grid = loaded_grid
                    self.rows = len(loaded_grid)
                    self.cols = len(loaded_grid[0]) if loaded_grid else 0
                    self.generation = loaded_gen
                    self.history = [[row[:] for row in self.grid]]
                    self.history_pos = 0
                    self.paused = True
                    self.stats = GameStats()
                    self.stats.update(self.grid, self.generation)
                    self.update_display()
                    messagebox.showinfo("📁 Load Successful", "Game state loaded successfully!")
                else:
                    messagebox.showerror("Load Failed", "Failed to load game state!")

        def export_image(self):
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                title="Export as Image"
            )
            if filename:
                success, message = export_as_image(self.grid, filename, cell_size=20)
                if success:
                    messagebox.showinfo("📷 Export Successful", message)
                else:
                    messagebox.showerror("Export Failed", message)

        def export_gif_gui(self):
            if len(self.history) < 2:
                messagebox.showwarning("Insufficient History", "Need at least 2 generations for GIF export!")
                return
            filename = filedialog.asksaveasfilename(
                defaultextension=".gif",
                filetypes=[("GIF files", "*.gif"), ("All files", "*.*")],
                title="Export Animation as GIF"
            )
            if filename:
                success, message = export_gif(self.history, filename, cell_size=15, duration=200)
                if success:
                    messagebox.showinfo("🎬 Export Successful", message)
                else:
                    messagebox.showerror("Export Failed", message)

        def export_web_gui(self):
            filename = filedialog.asksaveasfilename(
                defaultextension=".html",
                filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
                title="Export as Interactive Web Page"
            )
            if filename:
                success, message = export_web(self.grid, filename)
                if success:
                    messagebox.showinfo("🌐 Export Successful", message)
                else:
                    messagebox.showerror("Export Failed", message)

        def on_arrow_key(self, event):
            if event.keysym == 'Left':
                self.step_backward()
            elif event.keysym == 'Right':
                self.step_forward()

        def on_key_press(self, event):
            key = event.char.lower()
            if key == ' ':
                self.toggle_pause()
            elif key == 'r':
                self.reset_grid()
            elif key == 'c':
                self.clear_grid()
            elif key == 'p':
                self.load_pattern_gui()
            elif key == 's':
                self.save_game()
            elif key == 'l':
                self.load_game()
            elif key == 'e':
                self.export_image()
            elif key == 'g':
                self.export_gif_gui()
            elif key == 'w':
                self.export_web_gui()
            elif key == 't':
                self.switch_to_terminal()
            elif key == 'q':
                self.on_closing()

        def update_display(self):
            self.canvas.delete("all")
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            if canvas_width > 1 and canvas_height > 1:
                max_cell_width = canvas_width // self.cols
                max_cell_height = canvas_height // self.rows
                self.cell_size = min(max_cell_width, max_cell_height)
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
            self.update_statistics()
            self.update_pattern_detection()
            if self.recording:
                self.recorded_frames.append([row[:] for row in self.grid])
            status = 'RUNNING' if not self.paused else 'PAUSED'
            history_info = f" | History: {self.history_pos}/{len(self.history)-1}"
            self.status_label.config(text=f"Generation: {self.generation} | {status}{history_info}")
            live_cells, population_percent = self.get_grid_stats()
            growth_rate = self.stats.get_growth_rate()
            self.pop_label.config(text=f"Population: {live_cells} ({population_percent:.1f}%) | Growth Rate: {growth_rate:.2f}")
            if not self.paused:
                self.root.after(self.speed, self.auto_step)

        def update_statistics(self):
            self.stats_text.config(state=tk.NORMAL)
            self.stats_text.delete(1.0, tk.END)
            summary = self.stats.get_summary()
            stats_info = f"""Generation: {summary['generation']}
Current Pop: {summary['current_population']}
Max Pop: {summary['max_population']}
Min Pop: {summary['min_population']}
Growth Rate: {summary['growth_rate']:.3f}
Status: {summary['status']}
"""
            if summary['stable_count'] > 0:
                stats_info += f"Stable: {summary['stable_count']} gens\n"
            if len(self.stats.population_history) > 1:
                recent = [p[1] for p in list(self.stats.population_history)[-5:]]
                stats_info += f"Trend: {' → '.join(map(str, recent))}\n"
            self.stats_text.insert(tk.END, stats_info)
            self.stats_text.config(state=tk.DISABLED)

        def update_pattern_detection(self):
            patterns = find_patterns_in_grid(self.grid)
            if patterns:
                pattern_text = f"🔍 Found: {', '.join(p.title() for p in patterns[:3])}"
                if len(patterns) > 3:
                    pattern_text += f" (+{len(patterns)-3} more)"
                self.pattern_label.config(text=pattern_text, fg='green')
            else:
                self.pattern_label.config(text="No common patterns detected", fg='gray')

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

        def on_canvas_drag(self, event):
            self.on_canvas_click(event)

        def toggle_pause(self):
            self.paused = not self.paused
            if not self.paused:
                self.auto_step()
            self.update_display()

        def step_forward(self):
            if self.history_pos < len(self.history) - 1:
                self.history_pos += 1
                self.grid = [row[:] for row in self.history[self.history_pos]]
                self.generation = self.history_pos
            else:
                new_grid = next_generation(self.grid)
                self.history.append([row[:] for row in new_grid])
                if len(self.history) > 1000:
                    self.history.pop(0)
                else:
                    self.history_pos += 1
                self.grid = new_grid
                self.generation += 1
            self.stats.update(self.grid, self.generation)
            self.update_display()

        def step_backward(self):
            if self.history_pos > 0:
                self.history_pos -= 1
                self.grid = [row[:] for row in self.history[self.history_pos]]
                self.generation = self.history_pos
                self.stats.update(self.grid, self.generation)
                self.update_display()

        def reset_grid(self):
            self.grid = initialize_grid(self.rows, self.cols, 0.25)
            self.generation = 0
            self.history = [[row[:] for row in self.grid]]
            self.history_pos = 0
            self.paused = True
            self.stats = GameStats()
            self.stats.update(self.grid, self.generation)
            self.update_display()

        def switch_to_terminal(self):
            self.root.destroy()
            run_terminal_version()

        def auto_step(self):
            if not self.paused:
                self.step_forward()

        def run(self):
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.mainloop()

        def on_closing(self):
            self.root.destroy()

    gui = UltimateGameOfLifeGUI()
    gui.run()

# ========================
# 3D Game of Life (Experimental)
# ========================

def initialize_3d_grid(x_size, y_size, z_size, density=0.1):
    """Initialize a 3D grid for 3D Game of Life"""
    try:
        import numpy as np
        return np.random.choice([0, 1], size=(x_size, y_size, z_size), p=[1-density, density])
    except ImportError:
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
                        if grid[x, y, z] == 1:
                            if 4 <= neighbors <= 6:
                                new_grid[x, y, z] = 1
                        else:
                            if neighbors == 5:
                                new_grid[x, y, z] = 1
            return new_grid
    except ImportError:
        pass
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
        print("🌌 3D Game of Life Demo")
        print("Initializing 3D grid...")
        grid = initialize_3d_grid(20, 20, 20, 0.15)
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        for generation in range(10):
            ax.clear()
            ax.set_title(f'3D Game of Life - Generation {generation}')
            if isinstance(grid, np.ndarray):
                live_cells = np.where(grid == 1)
                if len(live_cells[0]) > 0:
                    ax.scatter(live_cells[0], live_cells[1], live_cells[2], 
                             c='red', s=20, alpha=0.6)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_xlim(0, 20)
            ax.set_ylim(0, 20)
            ax.set_zlim(0, 20)
            plt.pause(1)
            grid = next_3d_generation(grid)
            live_count = np.sum(grid) if isinstance(grid, np.ndarray) else sum(sum(sum(plane) for plane in layer) for layer in grid)
            print(f"Generation {generation}: {live_count} live cells")
            if live_count == 0:
                print("Population extinct!")
                break
        plt.show()
        return True
    except ImportError as e:
        print(f"3D demo requires matplotlib and numpy: {e}")
        return False

# ========================
# Main Entry Point
# ========================

def main():
    """Ultimate main function"""
    print("🚀 Conway's Game of Life - ULTIMATE EDITION")
    print("=" * 60)
    print("✨ INCREDIBLE New Features:")
    print("  🎭 Pattern Previews & Enhanced Selection")
    print("  🎬 GIF Animation Export & Live Recording")
    print("  📊 Advanced Analytics & Growth Tracking")
    print("  🔍 Real-time Pattern Detection")
    print("  🌐 Interactive Web Export")
    print("  🌌 3D Game of Life Demo")
    print("  💾 Enhanced Save/Load System")
    print("  🎮 Professional GUI with Statistics")
    print("  ⚡ Speed Controls & History Navigation")
    print("=" * 60)
    print()
    print("Choose your adventure:")
    print("1. 🖥️  Terminal version (keyboard controls + analytics)")
    print("2. 🎮 GUI version (mouse + keyboard, full features)")
    print("3. 🌌 3D Demo (experimental 3D Game of Life)")
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