import random
import os
import time
import sys

def initialize_grid(rows, cols, density=0.2):
    """Initialize a random grid with given density"""
    return [[1 if random.random() < density else 0 
             for _ in range(cols)] for _ in range(rows)]

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
    print("Controls: [Space] Play/Pause | [→] Forward | [←] Backward | [R]eset | [G]UI | [Q]uit")

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

def run_terminal_version():
    """Run the terminal version with history support"""
    rows, cols = 25, 50
    grid = initialize_grid(rows, cols, 0.25)
    generation = 0
    paused = False
    last_update_time = time.time()
    
    # History tracking
    history = [grid]  # Store generations for backward stepping
    history_pos = 0   # Current position in history
    
    print("Conway's Game of Life - Terminal Version")
    print("Controls: [P] = Pause/Resume | [F] = Forward | [B] = Backward | [R] = Reset | [G] = GUI | [Q] = Quit")
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
                    # Move forward in history
                    history_pos += 1
                    grid = [row[:] for row in history[history_pos]]
                    generation = history_pos
                else:
                    # Generate new generation
                    new_grid = next_generation(grid)
                    history.append([row[:] for row in new_grid])
                    # Limit history to prevent memory issues
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
    """Run the GUI version with resizable window"""
    try:
        import tkinter as tk
        from tkinter import messagebox, simpledialog
    except ImportError:
        print("GUI not available - tkinter not installed")
        print("Returning to terminal version...")
        return run_terminal_version()
    
    class GameOfLifeGUI:
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("Conway's Game of Life - GUI Version")
            self.root.geometry("800x600")
            
            # Game state
            self.rows = 40
            self.cols = 60
            self.cell_size = 8
            self.grid = initialize_grid(self.rows, self.cols, 0.25)
            self.generation = 0
            self.paused = True
            self.history = [self.grid]
            self.history_pos = 0
            
            self.setup_ui()
            self.update_display()
            
        def setup_ui(self):
            # Control frame
            control_frame = tk.Frame(self.root)
            control_frame.pack(pady=5)
            
            tk.Button(control_frame, text="Play/Pause (Space)", command=self.toggle_pause).pack(side=tk.LEFT, padx=2)
            tk.Button(control_frame, text="Forward (→)", command=self.step_forward).pack(side=tk.LEFT, padx=2)
            tk.Button(control_frame, text="Backward (←)", command=self.step_backward).pack(side=tk.LEFT, padx=2)
            tk.Button(control_frame, text="Reset (R)", command=self.reset_grid).pack(side=tk.LEFT, padx=2)
            tk.Button(control_frame, text="Resize (G)", command=self.resize_grid).pack(side=tk.LEFT, padx=2)
            tk.Button(control_frame, text="Terminal (T)", command=self.switch_to_terminal).pack(side=tk.LEFT, padx=2)
            
            # Status frame
            self.status_frame = tk.Frame(self.root)
            self.status_frame.pack(pady=2)
            self.status_label = tk.Label(self.status_frame, text="Generation: 0 | PAUSED")
            self.status_label.pack()
            
            # Keyboard shortcuts info
            info_label = tk.Label(self.status_frame, text="Keyboard: [Space] Play/Pause | [→] Forward | [←] Backward | [R]eset | [G]rid Size | [T]erminal", 
                                font=('Arial', 8), fg='gray')
            info_label.pack()
            
            # Canvas for the grid
            self.canvas = tk.Canvas(self.root, bg='white', width=800, height=500)
            self.canvas.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
            self.canvas.bind('<Button-1>', self.on_canvas_click)
            
            # Enable keyboard focus and bind keys
            self.root.focus_set()
            self.root.bind('<KeyPress>', self.on_key_press)
            self.root.bind('<Left>', self.on_arrow_key)
            self.root.bind('<Right>', self.on_arrow_key)
            self.canvas.bind('<Button-1>', self.focus_canvas)  # Focus when clicked
            
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
            
            # Update status
            status = 'RUNNING' if not self.paused else 'PAUSED'
            history_info = f" | History: {self.history_pos}/{len(self.history)-1}"
            self.status_label.config(text=f"Generation: {self.generation} | {status}{history_info}")
            
            if not self.paused:
                self.root.after(200, self.auto_step)
            
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
                self.history_pos += 1  # Always increment
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
            dialog.geometry("300x300")
            dialog.transient(self.root)
            dialog.grab_set()
            dialog.resizable(False, False)
            
            # Center the dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (300 // 2)
            y = (dialog.winfo_screenheight() // 2) - (200 // 2)
            dialog.geometry(f"300x300+{x}+{y}")
            
            # Variables to store results
            self.new_rows = None
            self.new_cols = None
            
            # Create input fields with proper alignment
            tk.Label(dialog, text="Enter new grid dimensions:", font=('Arial', 10, 'bold')).pack(pady=(15, 20))
            
            # Main frame for inputs
            input_frame = tk.Frame(dialog)
            input_frame.pack(pady=10)
            
            # Rows input with fixed width labels
            rows_frame = tk.Frame(input_frame)
            rows_frame.pack(pady=8)
            rows_label = tk.Label(rows_frame, text="Rows:", width=8, anchor='e', font=('Arial', 9))
            rows_label.pack(side=tk.LEFT, padx=(0, 10))
            rows_entry = tk.Entry(rows_frame, width=12, font=('Arial', 9), justify='center')
            rows_entry.pack(side=tk.LEFT)
            rows_entry.insert(0, str(self.rows))
            rows_entry.select_range(0, tk.END)
            
            # Columns input with same fixed width
            cols_frame = tk.Frame(input_frame)
            cols_frame.pack(pady=8)
            cols_label = tk.Label(cols_frame, text="Columns:", width=8, anchor='e', font=('Arial', 9))
            cols_label.pack(side=tk.LEFT, padx=(0, 10))
            cols_entry = tk.Entry(cols_frame, width=12, font=('Arial', 9), justify='center')
            cols_entry.pack(side=tk.LEFT)
            cols_entry.insert(0, str(self.cols))
            
            def apply_resize():
                try:
                    rows_val = int(rows_entry.get())
                    cols_val = int(cols_entry.get())
                    if 10 <= rows_val <= 200 and 10 <= cols_val <= 200:
                        self.new_rows = rows_val
                        self.new_cols = cols_val
                        dialog.destroy()
                    else:
                        tk.messagebox.showerror("Invalid Input", "Please enter values between 10 and 200")
                except ValueError:
                    tk.messagebox.showerror("Invalid Input", "Please enter valid numbers")
            
            def cancel_resize():
                dialog.destroy()
            
            # Button frame with better spacing
            button_frame = tk.Frame(dialog)
            button_frame.pack(pady=(30, 20))
            
            ok_button = tk.Button(button_frame, text="OK", command=apply_resize, width=8, font=('Arial', 9))
            ok_button.pack(side=tk.LEFT, padx=8)
            
            cancel_button = tk.Button(button_frame, text="Cancel", command=cancel_resize, width=8, font=('Arial', 9))
            cancel_button.pack(side=tk.LEFT, padx=8)
            
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
    print("Conway's Game of Life")
    print("Choose interface:")
    print("1. Terminal version (keyboard controls)")
    print("2. GUI version (resizable window, mouse interaction)")
    
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