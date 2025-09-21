import numpy as np
import matplotlib.pyplot as plt
import time

def create_spiral_matrix(n):
    """
    Creates an n×n matrix filled with numbers 1 to n² in a clockwise spiral pattern.
    
    Args:
        n (int): Size of the square matrix
        
    Returns:
        numpy.ndarray: n×n matrix with spiral pattern
    """
    if n <= 0:
        return np.array([])
    
    # Initialize matrix with zeros
    matrix = np.zeros((n, n), dtype=int)
    
    # Starting position and direction
    row, col = 0, 0
    direction = 0  # 0:right, 1:down, 2:left, 3:up
    
    # Direction vectors: [right, down, left, up]
    dr = [0, 1, 0, -1]  # row changes
    dc = [1, 0, -1, 0]  # column changes
    
    for i in range(1, n * n + 1):
        matrix[row][col] = i
        
        # Calculate next position
        next_row = row + dr[direction]
        next_col = col + dc[direction]
        
        # Check if we need to turn (hit boundary or filled cell)
        if (next_row < 0 or next_row >= n or 
            next_col < 0 or next_col >= n or 
            matrix[next_row][next_col] != 0):
            
            # Turn clockwise
            direction = (direction + 1) % 4
            next_row = row + dr[direction]
            next_col = col + dc[direction]
        
        row, col = next_row, next_col
    
    return matrix

def print_matrix(matrix, title="Matrix"):
    """Pretty print the matrix with proper formatting."""
    print(f"\n{title}:")
    print("-" * (len(title) + 1))
    
    if matrix.size == 0:
        print("Empty matrix")
        return
    
    # Calculate width needed for largest number
    max_val = np.max(matrix)
    width = len(str(max_val)) + 1
    
    for row in matrix:
        print(" ".join(f"{val:>{width}}" for val in row))

def visualize_matrix(matrix, title="Spiral Matrix Visualization"):
    """Create a visual representation of the spiral matrix."""
    if matrix.size == 0:
        print("Cannot visualize empty matrix")
        return
    
    plt.figure(figsize=(8, 8))
    
    # Create colormap
    plt.imshow(matrix, cmap='viridis', interpolation='nearest')
    
    # Add numbers to each cell
    n = matrix.shape[0]
    for i in range(n):
        for j in range(n):
            plt.text(j, i, str(matrix[i, j]), 
                    ha='center', va='center', 
                    color='white', fontweight='bold')
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.colorbar(label='Value')
    plt.xticks(range(n))
    plt.yticks(range(n))
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def validate_spiral(matrix):
    """
    Validate that the matrix contains a proper spiral pattern.
    
    Returns:
        bool: True if valid spiral, False otherwise
    """
    if matrix.size == 0:
        return True
    
    n = matrix.shape[0]
    expected_values = set(range(1, n * n + 1))
    actual_values = set(matrix.flatten())
    
    # Check if all numbers from 1 to n² are present exactly once
    if expected_values != actual_values:
        print(f"❌ Invalid values. Expected: {len(expected_values)} unique values from 1 to {n*n}")
        print(f"   Got: {len(actual_values)} unique values")
        return False
    
    print(f"✅ All values from 1 to {n*n} are present exactly once")
    return True

def performance_test():
    """Test performance for different matrix sizes."""
    print("\n" + "="*50)
    print("PERFORMANCE TEST")
    print("="*50)
    
    sizes = [5, 10, 20, 50, 100]
    times = []
    
    for size in sizes:
        start_time = time.time()
        matrix = create_spiral_matrix(size)
        end_time = time.time()
        
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        times.append(execution_time)
        
        print(f"Size {size:>3}×{size:<3}: {execution_time:>8.3f} ms")
    
    return sizes, times

def run_tests():
    """Run comprehensive tests of the spiral matrix function."""
    print("="*60)
    print("SPIRAL MATRIX GENERATOR - TEST SUITE")
    print("="*60)
    
    # Test cases
    test_cases = [
        {"n": 1, "description": "Single element matrix"},
        {"n": 2, "description": "2×2 matrix"},
        {"n": 3, "description": "3×3 matrix"},
        {"n": 4, "description": "4×4 matrix"},
        {"n": 5, "description": "5×5 matrix"},
        {"n": 0, "description": "Edge case: n=0"},
    ]
    
    for i, test in enumerate(test_cases, 1):
        n = test["n"]
        desc = test["description"]
        
        print(f"\nTest {i}: {desc} (n={n})")
        print("-" * 40)
        
        try:
            matrix = create_spiral_matrix(n)
            print_matrix(matrix, f"{n}×{n} Spiral Matrix")
            
            if n > 0:
                is_valid = validate_spiral(matrix)
                if is_valid:
                    print("✅ Test PASSED")
                else:
                    print("❌ Test FAILED")
            else:
                print("✅ Empty matrix test PASSED")
                
        except Exception as e:
            print(f"❌ Test FAILED with error: {e}")
    
    # Performance test
    performance_test()
    
    # Interactive visualization
    print(f"\n{'='*50}")
    print("VISUALIZATION")
    print("="*50)
    
    try:
        # Create a 6×6 matrix for visualization
        demo_matrix = create_spiral_matrix(6)
        print_matrix(demo_matrix, "6×6 Demo Matrix")
        
        # Uncomment the next line to show matplotlib visualization
        # visualize_matrix(demo_matrix, "6×6 Spiral Matrix")
        
    except ImportError:
        print("Matplotlib not available for visualization")

def interactive_mode():
    """Interactive mode for custom testing."""
    print(f"\n{'='*50}")
    print("INTERACTIVE MODE")
    print("="*50)
    
    while True:
        try:
            user_input = input("\nEnter matrix size (or 'q' to quit): ").strip()
            
            if user_input.lower() in ['q', 'quit', 'exit']:
                break
                
            n = int(user_input)
            
            if n < 0:
                print("Please enter a non-negative integer.")
                continue
            
            if n > 20:
                confirm = input(f"Large matrix ({n}×{n}) may take time. Continue? (y/n): ")
                if confirm.lower() not in ['y', 'yes']:
                    continue
            
            print(f"\nGenerating {n}×{n} spiral matrix...")
            start_time = time.time()
            matrix = create_spiral_matrix(n)
            end_time = time.time()
            
            print_matrix(matrix)
            validate_spiral(matrix)
            
            execution_time = (end_time - start_time) * 1000
            print(f"⏱️  Execution time: {execution_time:.3f} ms")
            
            if n <= 10:
                show_viz = input("Show visualization? (y/n): ").strip().lower()
                if show_viz in ['y', 'yes']:
                    try:
                        visualize_matrix(matrix)
                    except:
                        print("Visualization not available")
                        
        except ValueError:
            print("Please enter a valid integer.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    # Run automated tests
    run_tests()
    
    # Run interactive mode
    interactive_mode()
    
    print("\n🎉 All tests completed!")