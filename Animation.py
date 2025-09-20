import tkinter as tk
from tkinter import Canvas
import math
import time

# Constants
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

class Heart:
    def __init__(self):
        self.points = []
        self.colors = ['red', 'pink', 'crimson', 'hotpink', 'deeppink']
        self.generate_heart_points()
    
    def generate_heart_points(self):
        """Generate points for heart shape using parametric equations"""
        self.points = []
        for i in range(0, 360, 2):  # Generate points every 2 degrees
            t = math.radians(i)
            # Heart parametric equations
            x = 16 * (math.sin(t) ** 3)
            y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
            
            # Scale and center the heart
            x = x * 8 + CANVAS_WIDTH // 2
            y = -y * 8 + CANVAS_HEIGHT // 2  # Flip Y axis
            
            self.points.append((x, y))
    
    def render(self, canvas, frame):
        """Render the heart with animation effects"""
        canvas.delete('heart')  # Remove previous heart drawings
        
        # Create pulsing effect
        pulse = math.sin(frame * 0.1) * 0.2 + 1.0
        
        # Draw heart outline
        if len(self.points) > 2:
            scaled_points = []
            center_x, center_y = CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2
            
            for x, y in self.points:
                # Apply pulse effect
                new_x = center_x + (x - center_x) * pulse
                new_y = center_y + (y - center_y) * pulse
                scaled_points.extend([new_x, new_y])
            
            # Draw filled heart
            canvas.create_polygon(
                scaled_points, 
                fill=self.colors[frame % len(self.colors)], 
                outline='darkred', 
                width=2,
                tags='heart'
            )
        
        # Add sparkle effects
        self.add_sparkles(canvas, frame)
    
    def add_sparkles(self, canvas, frame):
        """Add sparkle effects around the heart"""
        import random
        canvas.delete('sparkle')
        
        for i in range(10):
            angle = (frame * 2 + i * 36) % 360
            distance = 150 + math.sin(frame * 0.05 + i) * 50
            
            x = CANVAS_WIDTH // 2 + math.cos(math.radians(angle)) * distance
            y = CANVAS_HEIGHT // 2 + math.sin(math.radians(angle)) * distance
            
            size = 3 + math.sin(frame * 0.1 + i) * 2
            canvas.create_oval(
                x - size, y - size, x + size, y + size,
                fill='gold', outline='yellow',
                tags='sparkle'
            )

def draw(main: tk.Tk, render_canvas: Canvas, render_heart: Heart, render_frame: int):
    """Main drawing function called every frame"""
    # Clear canvas
    render_canvas.delete('all')
    
    # Render heart with current frame
    render_heart.render(render_canvas, render_frame)
    
    # Schedule next frame
    main.after(50, draw, main, render_canvas, render_heart, render_frame + 1)

def main():
    """Main function to set up and run the application"""
    # Create main window
    root = tk.Tk()
    root.title('爱心代码')  # Love Heart Code
    root.geometry(f"{CANVAS_WIDTH}x{CANVAS_HEIGHT}")
    root.configure(bg='black')
    
    # Create canvas
    canvas = Canvas(
        root, 
        bg='black', 
        height=CANVAS_HEIGHT, 
        width=CANVAS_WIDTH,
        highlightthickness=0
    )
    canvas.pack(expand=True, fill='both')
    
    # Create heart object
    heart = Heart()
    
    # Start animation
    draw(root, canvas, heart, 0)
    
    # Start main loop
    root.mainloop()

if __name__ == '__main__':
    main()