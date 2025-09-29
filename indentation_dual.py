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
    
    # Initialize execution log for Chinese translation
    execution_log = []
    
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
            execution_log.append(f"用户输入的变量x值：{x}")
            break
        except ValueError:
            print("❌ Oops! Please enter a whole number (e.g., 5, -3, 0).")
    
    print(f"\n✅ Great! Your variable 'x' is now set to: {x}")
    execution_log.append(f"✅ 很好！变量'x'现在设置为：{x}")
    print(f"\n📋 Here's the ACTUAL CODE we're about to execute:")
    execution_log.append("📋 我们即将执行的实际代码：")
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
        execution_log.append(f"✅ 是的！{x} 大于 2 → 运行'if'代码块：")
        print("   📤 EXECUTING: print('Bigger than 2')")
        execution_log.append("   📤 执行：print('Bigger than 2')")
        print("   📤 EXECUTING: print('Still bigger')")
        execution_log.append("   📤 执行：print('Still bigger')")
        print("   💡 Notice: Both indented lines inside the 'if' block run because the condition is True")
        execution_log.append("   💡 注意：'if'块内的两行缩进代码都会运行，因为条件为真")
    else:
        print(f"\n❌ NO! {x} is NOT greater than 2 → Skipping the 'if' block:")
        execution_log.append(f"❌ 不！{x} 不大于 2 → 跳过'if'代码块：")
        print("   ⏭️  SKIPPED: print('Bigger than 2') (won't execute)")
        execution_log.append("   ⏭️  跳过：print('Bigger than 2')（不会执行）")
        print("   ⏭️  SKIPPED: print('Still bigger') (won't execute)")
        execution_log.append("   ⏭️  跳过：print('Still bigger')（不会执行）")
        print("   💡 Notice: The indented lines inside the 'if' block are ignored because the condition is False")
        execution_log.append("   💡 注意：'if'块内的缩进行被忽略，因为条件为假")
    
    print("\n📤 ALWAYS EXECUTING: print('Done with 2') (this line is NOT indented under the 'if')")
    execution_log.append("📤 总是执行：print('Done with 2')（这行代码不在'if'语句的缩进内）")
    
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
                execution_log.append(f"用户选择的循环次数：{loop_range}")
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
        execution_log.append(f"🔢 第{i+1}次迭代 (i = {i})")
        print(f"{'='*40}")
        print(f"📤 EXECUTING: print(f'Current number: {i}')")
        execution_log.append(f"📤 执行：print(f'Current number: {i}')")
        
        # Show conditional check in loop
        print(f"\n🔍 Now checking the NESTED condition: Is {i} > 2?")
        execution_log.append(f"🔍 现在检查嵌套条件：{i} > 2 吗？")
        if i > 2:
            print(f"✅ YES! {i} > 2 → Running the nested 'if' block:")
            execution_log.append(f"✅ 是的！{i} > 2 → 运行嵌套的'if'代码块：")
            print(f"   📤 EXECUTING: print('Bigger than 2')")
            execution_log.append("   📤 执行：print('Bigger than 2')")
        else:
            print(f"❌ NO! {i} ≤ 2 → Skipping the nested 'if' block:")
            execution_log.append(f"❌ 不！{i} ≤ 2 → 跳过嵌套的'if'代码块：")
            print(f"   ⏭️  SKIPPED: print('Bigger than 2') (won't execute)")
            execution_log.append("   ⏭️  跳过：print('Bigger than 2')（不会执行）")
        
        print(f"\n📤 EXECUTING: print(f'Done with i = {i}') (always runs - it's indented under the loop, not the nested 'if')")
        execution_log.append(f"📤 执行：print(f'Done with i = {i}')（总是运行——它缩进在循环下，而不是嵌套的'if'下）")
        
        # Pause between iterations (except last)
        if i < loop_range - 1:
            input("   ⏸️  Press Enter for the next iteration...")
    
    print(f"\n🎉 ALL {loop_range} ITERATIONS COMPLETED!")
    execution_log.append(f"🎉 所有{loop_range}次迭代完成！")
    print("📤 EXECUTING: print('All Done') (final line - not indented under anything)")
    execution_log.append("📤 执行：print('All Done')（最后一行——不在任何缩进下）")
    
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
        execution_log.append("🏆 完美！您已掌握了Python控制流程！")
    elif quiz_score >= 2:
        print("👍 Great job! You're almost there!")
        execution_log.append("👍 做得很好！您快要掌握了！")
    else:
        print("📖 Keep practicing—you'll get it soon!")
        execution_log.append("📖 继续练习——您很快就会掌握的！")
    
    # Generate Chinese summary file
    generate_chinese_summary(execution_log, x, loop_range, quiz_score)


def generate_chinese_summary(execution_log, user_x, user_loop_range, quiz_score):
    """
    Generate a comprehensive Chinese summary of the tutorial execution
    """
    import datetime
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"Python控制流程学习记录_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    chinese_content = f"""
================================================================================
🐍 Python 控制流程互动学习记录
================================================================================
学习时间：{timestamp}
学习者输入：x = {user_x}, 循环次数 = {user_loop_range}
测验得分：{quiz_score}/3

📋 完整程序代码：
--------------------------------------------------------------------------------
def main():
    # 初始化变量 x，值为 5
    x = 5
    
    # 检查 x 是否大于 2
    if x > 2:
        print('Bigger than 2')
        print('Still bigger')
    
    # 打印一个语句，表示我们已完成条件检查
    print('Done with 2')
    
    # 循环遍历从 0 到 4 的数字
    for i in range(5):
        print(f'Current number: {{i}}')
        
        # 检查当前数字是否大于 2
        if i > 2:
            print('Bigger than 2')
        
        # 打印一个语句，表示当前迭代已完成
        print(f'Done with i = {{i}}')
    
    # 循环完成后打印最终消息
    print('All Done')

================================================================================
📚 学习要点总结
================================================================================

1. 变量和赋值
   • 变量存储值（例如：x = {user_x}）
   • Python从上到下逐行执行代码

2. 条件语句（if语句）
   • 'if'语句仅在条件为True时运行代码
   • 缩进定义了哪些代码属于'if'块
   • 在您的例子中：{user_x} > 2 = {'True' if user_x > 2 else 'False'}
   
3. 循环（for循环）
   • 'for'循环为序列中的每个项目重复代码
   • range(n)生成从0到n-1的数字
   • range({user_loop_range})产生：{list(range(user_loop_range))}
   
4. 嵌套结构
   • 循环内部可以包含if语句
   • 缩进级别显示代码的归属关系
   • 更深的缩进 = 更内层的代码块

5. 程序执行流程
   • 代码从上到下执行
   • 条件语句可能跳过某些代码
   • 循环会重复执行内部代码

================================================================================
📝 您的学习过程记录
================================================================================
"""

    # Add execution log
    for i, log_entry in enumerate(execution_log, 1):
        chinese_content += f"{i:2d}. {log_entry}\n"

    chinese_content += f"""

================================================================================
🧠 测验结果分析
================================================================================
您的得分：{quiz_score}/3

问题1：range(4)产生什么？
正确答案：0,1,2,3
解释：range()函数生成从0开始到n-1结束的数字序列

问题2：如果x = 1，'x > 2'是True还是False？
正确答案：False
解释：1不大于2，所以条件为False

问题3：在for循环中，内部代码运行一次还是多次？
正确答案：多次
解释：循环为序列中的每个元素运行一次内部代码

================================================================================
💡 进一步学习建议
================================================================================

如果您想继续学习Python：

1. 练习更多条件语句：
   • 尝试elif（else if）
   • 学习逻辑运算符（and, or, not）
   • 练习嵌套if语句

2. 探索更多循环类型：
   • while循环
   • 循环中的break和continue
   • 列表推导式

3. 学习更多数据类型：
   • 字符串操作
   • 列表和字典
   • 函数定义

4. 实践项目想法：
   • 制作一个简单的计算器
   • 创建一个数字猜测游戏
   • 编写一个待办事项列表程序

================================================================================
🎉 恭喜完成Python控制流程学习！
================================================================================

记住：编程是一项需要练习的技能。继续编写代码，尝试新的挑战，
您会发现自己的技能在不断提高！

学习愉快！🐍✨
"""

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(chinese_content)
        
        print(f"\n📄 Chinese learning summary saved as: {filename}")
        print("   Perfect for Chinese-speaking students to review!")
        
    except Exception as e:
        print(f"❌ Could not save Chinese summary: {e}")
        print("But don't worry - you completed the tutorial successfully!")


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