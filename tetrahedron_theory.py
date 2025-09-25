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
    
    # Calculate height using the relationship with the third side and angles
    height = c * math.sin(alpha_rad)
    volume = (1/3) * base_area * height
    
    return round(volume, 2)

def explain_calculation_detailed(a, b, c, alpha, beta, gamma):
    """
    Provide a detailed explanation of the calculation with the given values
    """
    print("\n=== DETAILED CALCULATION EXPLANATION ===\n")
    
    print(f"Given:")
    print(f"  Edge lengths: A={a}, B={b}, C={c}")
    print(f"  Angles: α={alpha}°, β={beta}°, γ={gamma}°")
    print()
    
    print("ASSUMPTION MADE BY THE CODE:")
    print("- Edges A and B form the base of a triangle")
    print("- Angle γ (gamma) is the angle BETWEEN edges A and B")
    print("- Edge C is connected to the apex of the tetrahedron")
    print("- Angle α (alpha) is used to calculate the height from edge C")
    print()
    
    # Step 1: Calculate base area
    gamma_rad = math.radians(gamma)
    base_area = 0.5 * a * b * math.sin(gamma_rad)
    
    print("STEP 1: Calculate base triangle area")
    print(f"  Formula: Area = (1/2) × A × B × sin(γ)")
    print(f"  Area = (1/2) × {a} × {b} × sin({gamma}°)")
    print(f"  sin({gamma}°) = {math.sin(gamma_rad):.6f}")
    print(f"  Area = {base_area:.6f} square units")
    print()
    
    # Step 2: Calculate height
    alpha_rad = math.radians(alpha)
    height = c * math.sin(alpha_rad)
    
    print("STEP 2: Calculate height")
    print(f"  Formula: Height = C × sin(α)")
    print(f"  Height = {c} × sin({alpha}°)")
    print(f"  sin({alpha}°) = {math.sin(alpha_rad):.6f}")
    print(f"  Height = {height:.6f} units")
    print()
    
    # Step 3: Calculate volume
    volume = (1/3) * base_area * height
    
    print("STEP 3: Calculate tetrahedron volume")
    print(f"  Formula: Volume = (1/3) × Base Area × Height")
    print(f"  Volume = (1/3) × {base_area:.6f} × {height:.6f}")
    print(f"  Volume = {volume:.6f} cubic units")
    print()
    
    print(f"ROUNDED RESULT: Volume = {round(volume, 2)} cubic units")
    print()

def show_visual_explanation(a, b, c, alpha, beta, gamma):
    """
    Show a text-based visualization of what we assumed
    """
    print("\n=== VISUAL REPRESENTATION OF OUR ASSUMPTION ===")
    print()
    print("We assumed the tetrahedron looks something like this:")
    print()
    print("       D (apex)")
    print("       /|\\")
    print("      / | \\")
    print(f"  C={c} /  |h \\")
    print("    /   |   \\")
    print("   /    |    \\")
    print(f"  A={a}-----+-----B={b}")
    print(f"       γ={gamma}°")
    print()
    print("Where:")
    print(f"- A and B are edges of length {a} and {b}")
    print(f"- γ ({gamma}°) is the angle between A and B")
    print(f"- h is the height calculated using C={c} and α={alpha}°")
    
    gamma_rad = math.radians(gamma)
    base_area = 0.5 * a * b * math.sin(gamma_rad)
    alpha_rad = math.radians(alpha)
    height = c * math.sin(alpha_rad)
    volume = (1/3) * base_area * height
    
    print(f"- The base triangle has area = (1/2) × {a} × {b} × sin({gamma}°) = {base_area:.3f}")
    print(f"- The height h = {c} × sin({alpha}°) = {height:.3f}")
    print(f"- Volume = (1/3) × {base_area:.3f} × {height:.3f} = {volume:.3f}")

def show_potential_issues():
    """
    Explain why this might not be correct
    """
    print("\n=== POTENTIAL ISSUES WITH THIS APPROACH ===")
    print()
    print("1. UNCLEAR RELATIONSHIPS:")
    print("   - We don't know which edges are connected to which vertices")
    print("   - We don't know which angles correspond to which edges")
    print()
    print("2. MULTIPLE INTERPRETATIONS:")
    print("   - The 3 edges could be any 3 of the 6 edges of a tetrahedron")
    print("   - The 3 angles could be face angles, dihedral angles, or other angles")
    print()
    print("3. MATHEMATICAL CONSTRAINTS:")
    print("   - Not all combinations of edges and angles form valid tetrahedra")
    print("   - The calculation assumes a specific geometric configuration")
    print()
    print("To get the CORRECT answer, we need to know:")
    print("- Exactly which edges these lengths represent")
    print("- Exactly what type of angles these are")
    print("- How they're positioned relative to each other")

def explain_what_volume_means(volume):
    """
    Explain what the volume result actually means
    """
    print(f"\n=== WHAT DOES 'Volume: {volume}' MEAN? ===")
    print()
    print(f"The 'Volume: {volume}' means the calculated volume of the tetrahedron is {volume} cubic units.")
    print()
    print("Units: The volume is in whatever units your edge lengths were measured in.")
    print("Since you input edge lengths as numbers without specifying units,")
    print("the volume is in cubic units (could be cm³, m³, inches³, etc.).")
    print()
    print("Important note: This calculation assumes a specific geometric interpretation")
    print("of how your edges and angles relate to form the tetrahedron.")
    print("The actual volume formula for a tetrahedron can be quite complex")
    print("depending on exactly which edges and angles you're given.")

def main():
    try:
        while True:
            print("\n" + "="*60)
            print("TETRAHEDRON VOLUME CALCULATOR")
            print("="*60)
            print("This calculator uses a specific geometric assumption:")
            print("• Edges A and B form a triangle base with angle γ between them")
            print("• Edge C connects to the apex, with angle α determining height")
            print()
            print("INPUT FORMAT:")
            print("Line 1: Three edge lengths (A B C) - space separated numbers")
            print("Line 2: Three angles in degrees (α β γ) - space separated numbers")
            print()
            print("Example:")
            print("3 4 5")
            print("30 60 90")
            print()
            print("Press Ctrl+C or Ctrl+D to exit")
            print("-"*60)
            
            # Read edge lengths
            print("Enter three edge lengths (A B C): ", end="")
            line1 = input().strip()
            if not line1:
                break
            a, b, c = map(float, line1.split())
            
            # Read angles
            print("Enter three angles in degrees (α β γ): ", end="")
            line2 = input().strip()
            alpha, beta, gamma = map(float, line2.split())
            
            # Calculate volume
            volume = calculate_tetrahedron_volume(a, b, c, alpha, beta, gamma)
            
            # Output the result
            print(f"\nCalculated volume: {volume:.2f} cubic units")
            
            # Ask if user wants explanation
            print("\nWould you like to see how this was calculated? (y/n): ", end="")
            try:
                choice = input().strip().lower()
                if choice == 'y' or choice == 'yes':
                    explain_calculation_detailed(a, b, c, alpha, beta, gamma)
                    show_visual_explanation(a, b, c, alpha, beta, gamma)
                    explain_what_volume_means(volume)
                    show_potential_issues()
            except (EOFError, KeyboardInterrupt):
                pass
                
    except (EOFError, KeyboardInterrupt):
        print("\n\nGoodbye! Thanks for using the Tetrahedron Volume Calculator.")

if __name__ == "__main__":
    # Run the main program
    main()
    
    # Keep the test example for reference
    print("\n" + "="*50)
    print("TEST EXAMPLE (for reference):")
    print("="*50)
    test_volume = calculate_tetrahedron_volume(3, 4, 5, 30, 60, 90)
    print("Input: 3 4 5")
    print("Input: 30 60 90")
    print(f"Volume: {test_volume}")
    
    # Show explanation for test case
    explain_what_volume_means(test_volume)