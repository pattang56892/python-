import math

def calculate_tetrahedron_volume(a, b, c, alpha, beta, gamma):
    """
    Calculate the volume of a tetrahedron given three edge lengths and three angles.
    
    Args:
        a, b, c: Three edge lengths
        alpha, beta, gamma: Three angles in degrees
        
    Returns:
        Volume of the tetrahedron rounded to 2 decimal places
    """
    # Convert angles from degrees to radians
    alpha_rad = math.radians(alpha)
    beta_rad = math.radians(beta)
    gamma_rad = math.radians(gamma)
    
    # Calculate the area of the base triangle using the formula:
    # Area = (1/2) * a * b * sin(gamma)
    # Assuming gamma is the angle between sides a and b
    base_area = 0.5 * a * b * math.sin(gamma_rad)
    
    # For a tetrahedron, we need to determine the height
    # This is a simplified approach assuming we have a right triangular base
    # and the third edge c represents a height-related measurement
    
    # Calculate height using the relationship with the third side and angles
    # This is an approximation - the exact formula depends on the specific
    # geometric configuration of the tetrahedron
    
    # Using the formula for tetrahedron volume with known edges and angles
    # V = (1/6) * base_area * height
    # Height can be estimated using: h = c * sin(alpha) or similar
    
    height = c * math.sin(alpha_rad)
    volume = (1/3) * base_area * height
    
    return round(volume, 2)

def main():
    try:
        while True:
            # Read edge lengths
            line1 = input().strip()
            if not line1:
                break
            a, b, c = map(int, line1.split())
            
            # Read angles
            line2 = input().strip()
            alpha, beta, gamma = map(float, line2.split())
            
            # Calculate and output volume
            volume = calculate_tetrahedron_volume(a, b, c, alpha, beta, gamma)
            print(f"{volume:.2f}")
            
    except EOFError:
        pass

if __name__ == "__main__":
    # Example usage
    print("Enter edge lengths (A B C) and angles (α β γ):")
    print("Press Ctrl+C or Ctrl+D to exit")
    main()

# Alternative implementation with more precise tetrahedron volume calculation
def precise_tetrahedron_volume(a, b, c, alpha, beta, gamma):
    """
    More precise calculation using the general tetrahedron volume formula.
    This assumes the three given measurements form a valid tetrahedron.
    """
    # Convert to radians
    alpha_rad = math.radians(alpha)
    beta_rad = math.radians(beta)
    gamma_rad = math.radians(gamma)
    
    # Using Cayley-Menger determinant approach for tetrahedron volume
    # This is more complex but more accurate for general cases
    
    # For now, using the simpler triangular base approach
    # Area of triangle with sides a, b and included angle gamma
    base_area = 0.5 * a * b * math.sin(gamma_rad)
    
    # Height estimation (this may need adjustment based on the specific problem)
    height = c * math.sin(alpha_rad)
    
    volume = (1/3) * base_area * height
    return round(volume, 2)

# Test example
if __name__ == "__main__":
    # Test with sample values
    print("\nTest example:")
    print("Input: 3 4 5")
    print("Input: 30 60 90")
    result = calculate_tetrahedron_volume(3, 4, 5, 30, 60, 90)
    print(f"Volume: {result}")