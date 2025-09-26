import random
import os
import time
import sys
import json

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

def print_grid_terminal(grid, generation, paused, history_pos, max_history):
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
    print("Controls: [Space] Play/Pause | [→] Forward | [←] Backward | [R]eset | [P]attern | [S]ave | [L]oad | [E]xport | [G]UI | [Q]uit")

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

def run_terminal_version():
    """Run the terminal version with enhanced features"""
    rows, cols = 25, 50
    grid = initialize_grid(rows, cols, 0.25)
    generation = 0
    paused = False
    last_update_time = time.time()
    
    # History tracking
    history = [grid]  # Store generations for backward stepping
    history_pos = 0   # Current position in history
    
    print("Conway's Game of Life - Enhanced Terminal Version")
    print("Features: Patterns, Save/Load, Export, History Navigation")
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    print_grid_terminal(grid, generation, paused, history_pos, len(history)-1)
    
    try:
        while True:
            current_time = time.time()
            key = get_key()
            should_redraw = False
            
            if key == 'space': 
                paused = not paused
                should_redraw = True
            elif key == 'right':  # Forward step
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
                should_redraw = True
            elif key == 'left':  # Backward step
                if history_pos > 0:
                    history_pos -= 1
                    grid = [row[:] for row in history[history_pos]]
                    generation = history_pos
                    should_redraw = True
            elif key == 'r': 
                grid = initialize_grid(rows, cols, 0.25)
                generation = 0
                history = [grid]
                history_pos = 0
                should_redraw = True
            elif key == 'p':  # Pattern placement
                pattern_name = show_pattern_menu()
                if pattern_name:
                    pattern = load_pattern(pattern_name)
                    if pattern:
                        # Place pattern in center
                        start_row = (rows - len(pattern)) // 2
                        start_col = (cols - len(pattern[0])) // 2
                        grid = place_pattern(grid, pattern, start_row, start_col)
                        generation = 0
                        history = [grid]
                        history_pos = 0
                        should_redraw = True
                        print(f"\n{pattern_name.replace('_', ' ').title()} placed!")
                        time.sleep(1)
            elif key == 's':  # Save state
                success, message = save_state(grid, generation)
                print(f"\n{message}")
                time.sleep(2)
                should_redraw = True
            elif key == 'l':  # Load state
                success, loaded_grid, loaded_gen = load_state()
                if success:
                    grid = loaded_grid
                    generation = loaded_gen
                    history = [grid]
                    history_pos = 0
                    print("\nGame loaded successfully!")
                else:
                    print("\nNo save file found!")
                time.sleep(2)
                should_redraw = True
            elif key == 'e':  # Export image
                success, message = export_as_image(grid, f"generation_{generation}.png")
                print(f"\n{message}")
                time.sleep(2)
                should_redraw = True
            elif key == 'g':
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
                last_update_time = current_time
                should_redraw = True
            
            if should_redraw:
                print_grid_terminal(grid, generation, paused, history_pos, len(history)-1)
            
            time.sleep(0.01)
                
    except KeyboardInterrupt:
        print("\nGame stopped by user (Ctrl+C)")

def run_gui_version():
    """Run the enhanced GUI version"""
    try:
        import tkinter as tk
        from tkinter import messagebox, simpledialog, filedialog, ttk
    except ImportError:
        print("GUI not available - tkinter not installed")
        print("Returning to terminal version...")
        return run_terminal_version()
    
    class GameOfLifeGUI:
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("Conway's Game of Life - Enhanced GUI")
            self.root.geometry("1000x700")
            
            # Game state
            self.rows = 40
            self.cols = 60
            self.cell_size = 8
            self.grid = initialize_grid(self.rows, self.cols, 0.25)
            self.generation = 0
            self.paused = True
            self.history = [self.grid]
            self.history_pos = 0
            self.speed = 200  # milliseconds
            
            self.setup_ui()
            self.update_display()
            
        def setup_ui(self):
            # Main control frame
            main_control_frame = tk.Frame(self.root)
            main_control_frame.pack(pady=5)
            
            # First row of controls
            control_frame1 = tk.Frame(main_control_frame)
            control_frame1.pack(pady=2)
            
            tk.Button(control_frame1, text="Play/Pause", command=self.toggle_pause).pack(side=tk.LEFT, padx=2)
            tk.Button(control_frame1, text="Step →", command=self.step_forward).pack(side=tk.LEFT, padx=2)
            tk.Button(control_frame1, text="← Step", command=self.step_backward).pack(side=tk.LEFT, padx=2)
            tk.Button(control_frame1, text="Reset", command=self.reset_grid).pack(side=tk.LEFT, padx=2)
            tk.Button(control_frame1, text="Clear", command=self.clear_grid).pack(side=tk.LEFT, padx=2)
            
            # Speed control
            speed_frame = tk.Frame(control_frame1)
            speed_frame.pack(side=tk.LEFT, padx=10)
            tk.Label(speed_frame, text="Speed:").pack(side=tk.LEFT)
            self.speed_var = tk.IntVar(value=self.speed)
            self.speed_scale = tk.Scale(speed_frame, from_=50, to=1000, orient=tk.HORIZONTAL, 
                                       variable=self.speed_var, length=100, command=self.update_speed)
            self.speed_scale.pack(side=tk.LEFT)
            
            # Second row of controls
            control_frame2 = tk.Frame(main_control_frame)
            control_frame2.pack(pady=2)
            
            tk.Button(control_frame2, text="Load Pattern", command=self.load_pattern_gui).pack(side=tk.LEFT, padx=2)
            tk.Button(control_frame2, text="Save Game", command=self.save_game).pack(side=tk.LEFT, padx=2)
            tk.Button(control_frame2, text="Load Game", command=self.load_game).pack(side=tk.LEFT, padx=2)
            tk.Button(control_frame2, text="Export PNG", command=self.export_image).pack(side=tk.LEFT, padx=2)
            tk.Button(control_frame2, text="Resize Grid", command=self.resize_grid).pack(side=tk.LEFT, padx=2)
            tk.Button(control_frame2, text="Terminal", command=self.switch_to_terminal).pack(side=tk.LEFT, padx=2)
            
            # Status frame
            self.status_frame = tk.Frame(self.root)
            self.status_frame.pack(pady=2)
            self.status_label = tk.Label(self.status_frame, text="Generation: 0 | PAUSED", font=('Arial', 10, 'bold'))
            self.status_label.pack()
            
            # Statistics frame
            self.stats_frame = tk.Frame(self.root)
            self.stats_frame.pack(pady=2)
            self.stats_label = tk.Label(self.stats_frame, text="Live Cells: 0 | Population: 0%", font=('Arial', 9))
            self.stats_label.pack()
            
            # Help frame
            help_text = ("Keyboard: [Space] Play/Pause | [→←] Step | [R]eset | [C]lear | [P]attern | [S]ave | [L]oad | [E]xport | Click cells to toggle")
            help_label = tk.Label(self.root, text=help_text, font=('Arial', 8), fg='gray')
            help_label.pack()
            
            # Canvas for the grid
            self.canvas = tk.Canvas(self.root, bg='white', width=800, height=500)
            self.canvas.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
            self.canvas.bind('<Button-1>', self.on_canvas_click)
            self.canvas.bind('<B1-Motion>', self.on_canvas_drag)
            
            # Enable keyboard focus and bind keys
            self.root.focus_set()
            self.root.bind('<KeyPress>', self.on_key_press)
            self.root.bind('<Left>', self.on_arrow_key)
            self.root.bind('<Right>', self.on_arrow_key)
            self.canvas.bind('<Button-1>', self.focus_canvas)
            
        def update_speed(self, value):
            """Update simulation speed"""
            self.speed = int(value)
        
        def clear_grid(self):
            """Clear all cells"""
            self.grid = [[0] * self.cols for _ in range(self.rows)]
            self.generation = 0
            self.history = [[row[:] for row in self.grid]]
            self.history_pos = 0
            self.paused = True
            self.update_display()
        
        def get_grid_stats(self):
            """Calculate grid statistics"""
            live_cells = sum(sum(row) for row in self.grid)
            total_cells = self.rows * self.cols
            population_percent = (live_cells / total_cells) * 100 if total_cells > 0 else 0
            return live_cells, population_percent
        
        def load_pattern_gui(self):
            """Show pattern selection dialog"""
            patterns = ['glider', 'blinker', 'block', 'beehive', 'loaf', 'boat', 'tub', 
                       'beacon', 'toad', 'pulsar', 'gosper_gun', 'penta_decathlon', 'lightweight_spaceship']
            
            # Create pattern selection dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("Select Pattern")
            dialog.geometry("300x400")
            dialog.transient(self.root)
            dialog.grab_set()
            
            tk.Label(dialog, text="Choose a pattern:", font=('Arial', 12, 'bold')).pack(pady=10)
            
            # Listbox for patterns
            listbox_frame = tk.Frame(dialog)
            listbox_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
            
            scrollbar = tk.Scrollbar(listbox_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, font=('Arial', 10))
            listbox.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
            scrollbar.config(command=listbox.yview)
            
            for pattern in patterns:
                listbox.insert(tk.END, pattern.replace('_', ' ').title())
            
            selected_pattern = [None]
            
            def on_select():
                selection = listbox.curselection()
                if selection:
                    selected_pattern[0] = patterns[selection[0]]
                    dialog.destroy()
            
            def on_cancel():
                dialog.destroy()
            
            button_frame = tk.Frame(dialog)
            button_frame.pack(pady=10)
            
            tk.Button(button_frame, text="Load Pattern", command=on_select).pack(side=tk.LEFT, padx=5)
            tk.Button(button_frame, text="Cancel", command=on_cancel).pack(side=tk.LEFT, padx=5)
            
            # Double-click to select
            listbox.bind('<Double-Button-1>', lambda e: on_select())
            
            dialog.wait_window()
            
            if selected_pattern[0]:
                pattern = load_pattern(selected_pattern[0])
                if pattern:
                    # Place pattern in center
                    start_row = (self.rows - len(pattern)) // 2
                    start_col = (self.cols - len(pattern[0])) // 2
                    self.grid = place_pattern(self.grid, pattern, start_row, start_col)
                    self.generation = 0
                    self.history = [[row[:] for row in self.grid]]
                    self.history_pos = 0
                    self.paused = True
                    self.update_display()
                    messagebox.showinfo("Pattern Loaded", f"{selected_pattern[0].replace('_', ' ').title()} loaded successfully!")
        
        def save_game(self):
            """Save current game state"""
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Save Game State"
            )
            if filename:
                success, message = save_state(self.grid, self.generation, filename)
                if success:
                    messagebox.showinfo("Save Successful", message)
                else:
                    messagebox.showerror("Save Failed", message)
        
        def load_game(self):
            """Load game state from file"""
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
                    self.update_display()
                    messagebox.showinfo("Load Successful", "Game state loaded successfully!")
                else:
                    messagebox.showerror("Load Failed", "Failed to load game state!")
        
        def export_image(self):
            """Export current grid as PNG image"""
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                title="Export as Image"
            )
            if filename:
                # Use larger cell size for export
                success, message = export_as_image(self.grid, filename, cell_size=20)
                if success:
                    messagebox.showinfo("Export Successful", message)
                else:
                    messagebox.showerror("Export Failed", message)
        
        def focus_canvas(self, event):
            """Set focus to canvas when clicked"""
            self.on_canvas_click(event)
            self.root.focus_set()
        
        def on_arrow_key(self, event):
            """Handle arrow key presses"""
            if event.keysym == 'Left':
                self.step_backward()
            elif event.keysym == 'Right':
                self.step_forward()
        
        def on_key_press(self, event):
            """Handle keyboard shortcuts"""
            key = event.char.lower()
            if key == ' ':  # Space bar
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
                self.resize_grid()
            elif key == 't':
                self.switch_to_terminal()
            elif key == 'q':
                self.on_closing()
            
        def update_display(self):
            self.canvas.delete("all")
            
            # Get canvas dimensions
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:
                # Calculate square cell size that fits both dimensions
                max_cell_width = canvas_width // self.cols
                max_cell_height = canvas_height // self.rows
                self.cell_size = min(max_cell_width, max_cell_height)
                
                # Calculate total grid size
                total_width = self.cols * self.cell_size
                total_height = self.rows * self.cell_size
                
                # Center the grid
                offset_x = (canvas_width - total_width) // 2
                offset_y = (canvas_height - total_height) // 2
                
                # Draw grid with centering
                for i in range(self.rows):
                    for j in range(self.cols):
                        x1 = offset_x + j * self.cell_size
                        y1 = offset_y + i * self.cell_size
                        x2 = x1 + self.cell_size
                        y2 = y1 + self.cell_size
                        
                        color = 'black' if self.grid[i][j] else 'white'
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')
            
            # Update status and statistics
            status = 'RUNNING' if not self.paused else 'PAUSED'
            history_info = f" | History: {self.history_pos}/{len(self.history)-1}"
            self.status_label.config(text=f"Generation: {self.generation} | {status}{history_info}")
            
            live_cells, population_percent = self.get_grid_stats()
            self.stats_label.config(text=f"Live Cells: {live_cells} | Population: {population_percent:.1f}%")
            
            if not self.paused:
                self.root.after(self.speed, self.auto_step)
            
        def on_canvas_click(self, event):
            """Toggle cell state on click"""
            # Get canvas dimensions and centering offset
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            total_width = self.cols * self.cell_size
            total_height = self.rows * self.cell_size
            offset_x = (canvas_width - total_width) // 2
            offset_y = (canvas_height - total_height) // 2
            
            # Adjust click coordinates for centering
            adjusted_x = event.x - offset_x
            adjusted_y = event.y - offset_y
            
            if adjusted_x >= 0 and adjusted_y >= 0:
                col = adjusted_x // self.cell_size
                row = adjusted_y // self.cell_size
                if 0 <= row < self.rows and 0 <= col < self.cols:
                    self.grid[row][col] = 1 - self.grid[row][col]
                    self.update_display()
        
        def on_canvas_drag(self, event):
            """Handle mouse drag for drawing"""
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
            self.update_display()
        
        def step_backward(self):
            if self.history_pos > 0:
                self.history_pos -= 1
                self.grid = [row[:] for row in self.history[self.history_pos]]
                self.generation = self.history_pos
                self.update_display()
        
        def reset_grid(self):
            self.grid = initialize_grid(self.rows, self.cols, 0.25)
            self.generation = 0
            self.history = [[row[:] for row in self.grid]]
            self.history_pos = 0
            self.paused = True
            self.update_display()
        
        def resize_grid(self):
            # Custom dialog that accepts Enter key
            dialog = tk.Toplevel(self.root)
            dialog.title("Resize Grid")
            dialog.geometry("350x400")
            dialog.transient(self.root)
            dialog.grab_set()
            dialog.resizable(False, False)
            
            # Center the dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (350 // 2)
            y = (dialog.winfo_screenheight() // 2) - (400 // 2)
            dialog.geometry(f"350x400+{x}+{y}")
            
            # Variables to store results
            self.new_rows = None
            self.new_cols = None
            
            # Create input fields with proper alignment
            tk.Label(dialog, text="Enter new grid dimensions:", font=('Arial', 12, 'bold')).pack(pady=(20, 25))
            
            # Main frame for inputs
            input_frame = tk.Frame(dialog)
            input_frame.pack(pady=15)
            
            # Rows input with fixed width labels
            rows_frame = tk.Frame(input_frame)
            rows_frame.pack(pady=10)
            rows_label = tk.Label(rows_frame, text="Rows:", width=10, anchor='e', font=('Arial', 10))
            rows_label.pack(side=tk.LEFT, padx=(0, 15))
            rows_entry = tk.Entry(rows_frame, width=15, font=('Arial', 10), justify='center')
            rows_entry.pack(side=tk.LEFT)
            rows_entry.insert(0, str(self.rows))
            rows_entry.select_range(0, tk.END)
            
            # Columns input with same fixed width
            cols_frame = tk.Frame(input_frame)
            cols_frame.pack(pady=10)
            cols_label = tk.Label(cols_frame, text="Columns:", width=10, anchor='e', font=('Arial', 10))
            cols_label.pack(side=tk.LEFT, padx=(0, 15))
            cols_entry = tk.Entry(cols_frame, width=15, font=('Arial', 10), justify='center')
            cols_entry.pack(side=tk.LEFT)
            cols_entry.insert(0, str(self.cols))
            
            # Info label
            tk.Label(dialog, text="Range: 10-200 for both dimensions", font=('Arial', 8), fg='gray').pack(pady=(10, 0))
            
            def apply_resize():
                try:
                    rows_val = int(rows_entry.get())
                    cols_val = int(cols_entry.get())
                    if 10 <= rows_val <= 200 and 10 <= cols_val <= 200:
                        self.new_rows = rows_val
                        self.new_cols = cols_val
                        dialog.destroy()
                    else:
                        messagebox.showerror("Invalid Input", "Please enter values between 10 and 200")
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter valid numbers")
            
            def cancel_resize():
                dialog.destroy()
            
            # Button frame with better spacing
            button_frame = tk.Frame(dialog)
            button_frame.pack(pady=(25, 20))
            
            ok_button = tk.Button(button_frame, text="Apply", command=apply_resize, width=10, font=('Arial', 10))
            ok_button.pack(side=tk.LEFT, padx=10)
            
            cancel_button = tk.Button(button_frame, text="Cancel", command=cancel_resize, width=10, font=('Arial', 10))
            cancel_button.pack(side=tk.LEFT, padx=10)
            
            # Bind Enter key to apply_resize
            dialog.bind('<Return>', lambda event: apply_resize())
            dialog.bind('<Escape>', lambda event: cancel_resize())
            
            # Focus on the first entry field
            rows_entry.focus_set()
            
            # Wait for dialog to close
            dialog.wait_window()
            
            # Apply changes if values were set
            if self.new_rows and self.new_cols:
                self.rows = self.new_rows
                self.cols = self.new_cols
                self.reset_grid()
        
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
    
    # Run GUI
    gui = GameOfLifeGUI()
    gui.run()

def main():
    """Main function - choose between terminal and GUI"""
    print("Conway's Game of Life - Enhanced Edition")
    print("=" * 45)
    print("✨ New Features:")
    print("  • 13 Classic Patterns (Glider, Gosper Gun, Pulsar, etc.)")
    print("  • Save/Load Game States (JSON format)")
    print("  • Export Generations as PNG Images")
    print("  • Adjustable Speed Control")
    print("  • Grid Statistics & Population Tracking")
    print("  • Enhanced Keyboard Controls")
    print("  • Mouse Drawing in GUI Mode")
    print()
    print("Choose interface:")
    print("1. Terminal version (keyboard controls)")
    print("2. GUI version (mouse + keyboard, resizable)")
    
    while True:
        choice = input("\nEnter choice (1 or 2): ").strip()
        if choice == '1':
            run_terminal_version()
            break
        elif choice == '2':
            run_gui_version()
            break
        else:
            print("Please enter 1 or 2")

if __name__ == '__main__':
    main()