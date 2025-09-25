def interactive_control_flow_demo():
    """
    Interactive Python Control Flow Learning Tool
    
    This program demonstrates:
    1. Variable assignment
    2. Conditional statements (if)
    3. For loops with range()
    4. Print formatting
    5. Program flow and execution order
    """
    
    print("=" * 70)
    print("🐍 PYTHON CONTROL FLOW INTERACTIVE DEMO 🐍")
    print("=" * 70)
    print("\nWelcome! This tutorial will teach you Python's core control structures—step by step.")
    print("You'll interact with code, see real-time results, and test your knowledge with a quiz!\n")
    
    print("📋 THE BIG PICTURE: Here's the COMPLETE program we'll explore together:")
    print("┌" + "─" * 68 + "┐")
    print("│ def main():                                                  │")
    print("│     # Initialize a variable x with value 5                   │")
    print("│     x = 5                                                    │")
    print("│                                                              │")
    print("│     # Check if x is greater than 2                          │")
    print("│     if x > 2:                                                │")
    print("│         print('Bigger than 2')                              │")
    print("│         print('Still bigger')                               │")
    print("│                                                              │")
    print("│     # Print a statement indicating we are done checking     │")
    print("│     print('Done with 2')                                    │")
    print("│                                                              │")
    print("│     # Loop through numbers from 0 to 4                      │")
    print("│     for i in range(5):                                       │")
    print("│         print(f'Current number: {i}')                       │")
    print("│                                                              │")
    print("│         # Check if the current number is greater than 2     │")
    print("│         if i > 2:                                            │")
    print("│             print('Bigger than 2')                          │")
    print("│                                                              │")
    print("│         # Print a statement for current iteration           │")
    print("│         print(f'Done with i = {i}')                         │")
    print("│                                                              │")
    print("│     # Print a final message after the loop completes        │")
    print("│     print('All Done')                                        │")
    print("└" + "─" * 68 + "┘")
    
    print("\n🎯 WHAT THIS PROGRAM DEMONSTRATES:")
    print("• Variables & assignment (x = 5)")
    print("• If statements (conditionals that may or may not run)")
    print("• For loops (code that repeats multiple times)")
    print("• How indentation controls which code belongs together")
    print("• Program flow (top-to-bottom execution order)")
    
    print("\n💡 We'll break this down into TWO main parts:")
    print("   Part 1: Variables + Conditionals (the first 'if' statement)")
    print("   Part 2: Loops + Nested Conditionals (the 'for' loop with an 'if' inside)")
    
    input("\n⏸️  Ready to dive in? Press Enter to start with Part 1...")
    print("\n" + "=" * 70)
    
    # Part 1: Variables & Conditionals
    print("\n📝 PART 1: VARIABLES AND CONDITIONAL LOGIC")
    print("-" * 50)
    print("Let's start by assigning a value to a variable and testing a condition.")
    
    # Get user input for variable x
    while True:
        try:
            x = int(input("\n🔢 Enter ANY integer (positive, negative, or zero) for variable 'x': "))
            break
        except ValueError:
            print("❌ Oops! Please enter a whole number (e.g., 5, -3, 0).")
    
    print(f"\n✅ Great! Your variable 'x' is now set to: {x}")
    print(f"\n📋 Here's the ACTUAL CODE we're about to execute:")
    print("┌────────────────────────────────────────┐")
    print(f"│ x = {x}                               │")
    print("│                                        │")
    print("│ if x > 2:                              │")
    print("│     print('Bigger than 2')             │")
    print("│     print('Still bigger')              │")
    print("│                                        │")
    print("│ print('Done with 2')                   │")
    print("└────────────────────────────────────────┘")
    
    print(f"\n🔍 Now we'll check: Is {x} greater than 2? This is called a 'conditional statement'.")
    print("💡 Watch which parts of the code above actually execute!")
    
    # Demonstrate conditional logic
    if x > 2:
        print(f"\n✅ YES! {x} is greater than 2 → Running the 'if' block:")
        print("   📤 EXECUTING: print('Bigger than 2')")
        print("   📤 EXECUTING: print('Still bigger')")
        print("   💡 Notice: Both indented lines inside the 'if' block run because the condition is True")
    else:
        print(f"\n❌ NO! {x} is NOT greater than 2 → Skipping the 'if' block:")
        print("   ⏭️  SKIPPED: print('Bigger than 2') (won't execute)")
        print("   ⏭️  SKIPPED: print('Still bigger') (won't execute)")
        print("   💡 Notice: The indented lines inside the 'if' block are ignored because the condition is False")
    
    print("\n📤 ALWAYS EXECUTING: print('Done with 2') (this line is NOT indented under the 'if')")
    
    input("\n⏸️  Press Enter to move to Part 2 (loops)...")
    
    # Part 2: For Loops
    print("\n🔄 PART 2: FOR LOOPS WITH RANGE()")
    print("-" * 50)
    print("Next, we'll use a 'for loop' to repeat code for a set of numbers.")
    print("You'll choose how many numbers to loop through (1-10).")
    
    # Get user input for loop range
    while True:
        try:
            loop_range = int(input("\n🔢 How many numbers should we loop through? (1-10): "))
            if 1 <= loop_range <= 10:
                break
            else:
                print("❌ Please pick a number BETWEEN 1 and 10!")
        except ValueError:
            print("❌ Invalid! Enter a whole number (e.g., 3, 7).")
    
    print(f"\n📋 Here's the ACTUAL LOOP CODE we're about to execute:")
    print("┌─────────────────────────────────────────────┐")
    print(f"│ for i in range({loop_range}):                        │")
    print("│     print(f'Current number: {i}')           │")
    print("│                                             │")
    print("│     if i > 2:                               │")
    print("│         print('Bigger than 2')              │")
    print("│                                             │")
    print("│     print(f'Done with i = {i}')             │")
    print("└─────────────────────────────────────────────┘")
    
    print(f"\n🔄 Loop setup: for i in range({loop_range})")
    print(f"   → This will generate numbers: {list(range(loop_range))} (from 0 to {loop_range-1})")
    print("   → Each iteration runs ALL the indented code inside the loop")
    print("   💡 Notice the indentation levels - they show which code belongs where!")
    
    input("\n⏸️  Press Enter to start the loop demonstration...")
    
    for i in range(loop_range):
        print(f"\n{'='*40}")
        print(f"🔢 ITERATION #{i+1} (i = {i})")
        print(f"{'='*40}")
        print(f"📤 EXECUTING: print(f'Current number: {i}')")
        
        # Show conditional check in loop
        print(f"\n🔍 Now checking the NESTED condition: Is {i} > 2?")
        if i > 2:
            print(f"✅ YES! {i} > 2 → Running the nested 'if' block:")
            print(f"   📤 EXECUTING: print('Bigger than 2')")
        else:
            print(f"❌ NO! {i} ≤ 2 → Skipping the nested 'if' block:")
            print(f"   ⏭️  SKIPPED: print('Bigger than 2') (won't execute)")
        
        print(f"\n📤 EXECUTING: print(f'Done with i = {i}') (always runs - it's indented under the loop, not the nested 'if')")
        
        # Pause between iterations (except last)
        if i < loop_range - 1:
            input("   ⏸️  Press Enter for the next iteration...")
    
    print(f"\n🎉 ALL {loop_range} ITERATIONS COMPLETED!")
    print("📤 EXECUTING: print('All Done') (final line - not indented under anything)")
    
    # Summary Section
    print("\n" + "=" * 70)
    print("📚 WHAT YOU LEARNED:")
    print("=" * 70)
    print("1. ✅ Variables store values (e.g., x = your_number)")
    print("2. ✅ 'if' statements run code ONLY if a condition is True")
    print("3. ✅ 'for' loops repeat code for each item in a sequence (e.g., range())")
    print("4. ✅ range(n) generates numbers from 0 to n-1 (e.g., range(3) = [0,1,2])")
    print("5. ✅ Indentation defines code blocks (same indent = same block)")
    print("6. ✅ Code executes top-to-bottom, line by line")
    
    # Interactive Quiz
    print("\n🧠 QUICK QUIZ: Test your knowledge!")
    print("-" * 25)
    
    quiz_score = 0
    
    # Question 1
    q1_answer = input("Q1: What does range(4) produce? (Enter as: 0,1,2,3): ")
    if q1_answer.strip() == "0,1,2,3":
        print("✅ Correct! range(4) gives [0,1,2,3].")
        quiz_score += 1
    else:
        print("❌ Incorrect. range(4) produces: 0, 1, 2, 3.")
    
    # Question 2
    q2_answer = input("Q2: If x = 1, will 'x > 2' be True or False? ").strip().lower()
    if q2_answer == "false":
        print("✅ Correct! 1 is not greater than 2.")
        quiz_score += 1
    else:
        print("❌ Incorrect. 1 > 2 is False.")
    
    # Question 3
    q3_answer = input("Q3: In a for loop, does the code inside run once or multiple times? ").strip().lower()
    if "multiple" in q3_answer:
        print("✅ Correct! Loops run code once per iteration.")
        quiz_score += 1
    else:
        print("❌ Incorrect. Loop code runs multiple times (once per item in the sequence).")
    
    print(f"\n🎯 Quiz Score: {quiz_score}/3")
    if quiz_score == 3:
        print("🏆 Perfect! You mastered Python control flow!")
    elif quiz_score >= 2:
        print("👍 Great job! You're almost there!")
    else:
        print("📖 Keep practicing—you'll get it soon!")


def simple_demo():
    """
    Run the original code for comparison
    """
    print("\n" + "="*60)
    print("🔄 ORIGINAL CODE OUTPUT:")
    print("="*60)
    
    # Initialize a variable x with value 5
    x = 5
    print(f"Variable x = {x}")
    
    # Check if x is greater than 2
    if x > 2:
        print('Bigger than 2')
        print('Still bigger')
    
    # Print a statement indicating we are done checking the condition
    print('Done with 2')
    
    # Loop through numbers from 0 to 4
    for i in range(5):
        print(f'\nCurrent number: {i}')
        
        # Check if the current number is greater than 2
        if i > 2:
            print('Bigger than 2')
        
        # Print a statement indicating we are done with the current iteration
        print(f'Done with i = {i}')
    
    # Print a final message after the loop completes
    print('\nAll Done')


def main():
    """
    Main function to run the interactive learning tool
    """
    print("Welcome to the Python Control Flow Learning Experience!")
    print("\nChoose your learning mode:")
    print("1. 🎓 Interactive Tutorial (Step-by-step with quizzes)")
    print("2. 🏃 Quick Demo (See the original code run)")
    print("3. ❌ Exit")
    
    while True:
        choice = input("\nEnter your choice (1, 2, or 3): ").strip()
        
        if choice == '1':
            interactive_control_flow_demo()
            break
        elif choice == '2':
            simple_demo()
            break
        elif choice == '3':
            print("👋 Thanks for learning with Python! Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
    
    print("\n🎉 Thanks for exploring Python control flow!")
    print("💡 Remember: Practice is key to mastering programming!")


if __name__ == "__main__":
    main()