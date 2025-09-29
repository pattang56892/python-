#!/usr/bin/env python3
"""
Python Concepts Trainer for Junior Developers (Bilingual: English/Chinese)
面向初级开发者的Python概念训练器（双语：英文/中文）
An interactive educational tool to teach common Python misconceptions
用于教授常见Python误解的互动教育工具
"""

import sys
import traceback
from typing import Any

class PythonConceptsTrainer:
    def __init__(self):
        self.current_lesson = 0
        self.total_lessons = 8
        self.language = 'en'  # Default to English
        
    def set_language(self, lang):
        """Set the display language"""
        self.language = lang
    
    def t(self, en_text, zh_text):
        """Translation helper - returns text based on current language"""
        return zh_text if self.language == 'zh' else en_text
    
    def print_bilingual(self, en_text, zh_text):
        """Print text in both languages"""
        if self.language == 'zh':
            print(f"{zh_text}")
            print(f"({en_text})")
        else:
            print(f"{en_text}")
            print(f"({zh_text})")
    
    def clear_screen(self):
        """Clear the console screen"""
        print("\n" * 50)
    
    def print_header(self, en_title, zh_title):
        """Print a formatted bilingual header"""
        print("=" * 80)
        if self.language == 'zh':
            print(f"  {zh_title}")
            print(f"  {en_title}")
        else:
            print(f"  {en_title}")
            print(f"  {zh_title}")
        print("=" * 80)
    
    def print_separator(self):
        """Print a separator line"""
        print("-" * 80)
    
    def wait_for_user(self):
        """Wait for user input to continue"""
        prompt = self.t("Press Enter to continue...", "按回车键继续...")
        input(f"\n{prompt}")
    
    def run_code_safely(self, code: str, en_desc: str = "", zh_desc: str = ""):
        """Execute code safely and show results"""
        desc = self.t(en_desc, zh_desc) if zh_desc else en_desc
        print(f"\n🔍 {desc}")
        print(f"{self.t('Code', '代码')}: {code}")
        print(f"{self.t('Result', '结果')}:", end=" ")
        
        try:
            # Use eval for expressions, exec for statements
            if any(keyword in code for keyword in ['=', 'def ', 'class ', 'import ', 'for ', 'while ', 'if ']):
                # Create a local namespace for exec
                local_vars = {}
                exec(code, globals(), local_vars)
                if local_vars:
                    for var, value in local_vars.items():
                        if not var.startswith('_'):
                            print(f"{var} = {repr(value)}")
                else:
                    print(self.t("(Code executed)", "（代码已执行）"))
            else:
                result = eval(code)
                print(repr(result))
        except Exception as e:
            error_msg = self.t("ERROR", "错误")
            print(f"{error_msg}: {type(e).__name__}: {e}")
    
    def lesson_1_list_mutability(self):
        """Lesson 1: List Mutability and References"""
        self.clear_screen()
        self.print_header("Lesson 1: List Mutability and References", 
                         "第1课：列表可变性和引用")
        
        self.print_bilingual(
            "MISCONCEPTION: When you assign y = x, you get separate lists",
            "误解：当你赋值 y = x 时，你得到了两个独立的列表"
        )
        self.print_bilingual(
            "REALITY: You get two references to the same list object",
            "实际：你得到了两个指向同一个列表对象的引用"
        )
        
        self.print_separator()
        self.print_bilingual("Let's demonstrate:", "让我们演示一下：")
        
        # Demonstration
        self.run_code_safely("x = [1, 2, 3]", 
                           "Create original list", "创建原始列表")
        self.run_code_safely("y = x", 
                           "Assign x to y - creates reference, not copy", 
                           "将x赋值给y - 创建引用，不是副本")
        self.run_code_safely("print(f'x: {x}, y: {y}')", 
                           "Both show same values", "两者显示相同的值")
        self.run_code_safely("print(f'Same object? {x is y}')", 
                           "Check if same object", "检查是否是同一个对象")
        self.run_code_safely("print(f'x id: {id(x)}, y id: {id(y)}')", 
                           "Memory addresses", "内存地址")
        
        self.print_bilingual("\nNow let's modify through y:", "\n现在让我们通过y进行修改：")
        self.run_code_safely("y[0] = 999", 
                           "Change first element through y", "通过y改变第一个元素")
        self.run_code_safely("print(f'x: {x}, y: {y}')", 
                           "Both lists changed!", "两个列表都改变了！")
        
        insight = self.t(
            "\n💡 KEY INSIGHT: x and y point to the same list in memory",
            "\n💡 关键洞察：x和y指向内存中的同一个列表"
        )
        print(insight)
        
        self.print_separator()
        self.print_bilingual("How to create actual copies:", "如何创建真正的副本：")
        
        self.run_code_safely("original = [1, 2, 3]", 
                           "New original list", "新的原始列表")
        self.run_code_safely("copy1 = original.copy()", 
                           "Method 1: .copy()", "方法1：.copy()")
        self.run_code_safely("copy2 = original[:]", 
                           "Method 2: slice notation", "方法2：切片表示法")
        self.run_code_safely("copy3 = list(original)", 
                           "Method 3: list() constructor", "方法3：list()构造函数")
        
        self.run_code_safely("copy1[0] = 999", 
                           "Modify copy1", "修改copy1")
        self.run_code_safely("print(f'original: {original}')", 
                           "Original unchanged", "原始列表未改变")
        self.run_code_safely("print(f'copy1: {copy1}')", 
                           "Only copy1 changed", "只有copy1改变了")
        
        takeaway = self.t(
            "\n🎯 TAKEAWAY: Use .copy(), [:], or list() to create independent copies",
            "\n🎯 要点：使用.copy()、[:]或list()来创建独立的副本"
        )
        print(takeaway)
        self.wait_for_user()
    
    def lesson_2_division_behavior(self):
        """Lesson 2: Division Always Returns Float"""
        self.clear_screen()
        self.print_header("Lesson 2: Division Always Returns Float", 
                         "第2课：除法总是返回浮点数")
        
        self.print_bilingual(
            "MISCONCEPTION: 4 / 2 should return 2 (integer)",
            "误解：4 / 2 应该返回 2（整数）"
        )
        self.print_bilingual(
            "REALITY: Division operator / always returns float in Python",
            "实际：在Python中，除法运算符/总是返回浮点数"
        )
        
        self.print_separator()
        self.print_bilingual("Demonstration:", "演示：")
        
        self.run_code_safely("result1 = 4 / 2", 
                           "Even division", "整除")
        self.run_code_safely("type(result1)", 
                           "Type is float, not int", "类型是float，不是int")
        self.run_code_safely("result1", 
                           "Value is 2.0", "值是2.0")
        
        self.run_code_safely("result2 = 10 / 5", 
                           "Another even division", "另一个整除")
        self.run_code_safely("type(result2)", 
                           "Still float", "仍然是float")
        
        self.run_code_safely("result3 = 7 / 3", 
                           "Uneven division", "不整除")
        self.run_code_safely("type(result3)", 
                           "Also float", "也是float")
        
        self.print_bilingual("\n🔍 Compare with other operators:", "\n🔍 与其他运算符比较：")
        self.run_code_safely("type(4 + 2)", 
                           "Addition preserves int", "加法保持int")
        self.run_code_safely("type(4 * 2)", 
                           "Multiplication preserves int", "乘法保持int")
        self.run_code_safely("type(4 - 2)", 
                           "Subtraction preserves int", "减法保持int")
        self.run_code_safely("type(4 / 2)", 
                           "Division always gives float", "除法总是给出float")
        
        self.print_separator()
        self.print_bilingual("Alternatives for integer division:", "整数除法的替代方案：")
        
        self.run_code_safely("4 // 2", 
                           "Floor division", "地板除法")
        self.run_code_safely("type(4 // 2)", 
                           "Returns int", "返回int")
        self.run_code_safely("7 // 3", 
                           "Floor division truncates", "地板除法截断")
        self.run_code_safely("int(7 / 3)", 
                           "Convert float division to int", "将浮点除法转换为int")
        
        why_msg = self.t(
            "\n💡 WHY: Python prioritizes mathematical precision over type consistency",
            "\n💡 原因：Python优先考虑数学精度而不是类型一致性"
        )
        takeaway = self.t(
            "🎯 TAKEAWAY: Use // for integer division, / always gives float",
            "🎯 要点：使用//进行整数除法，/总是给出float"
        )
        print(why_msg)
        print(takeaway)
        self.wait_for_user()
    
    def language_selection(self):
        """Language selection menu"""
        self.clear_screen()
        print("=" * 60)
        print("  Language Selection / 语言选择")
        print("=" * 60)
        print("1. English")
        print("2. 中文 (Chinese)")
        print("=" * 60)
        
        while True:
            choice = input("Choose language / 选择语言 (1/2): ").strip()
            if choice == '1':
                self.language = 'en'
                break
            elif choice == '2':
                self.language = 'zh'
                break
            else:
                print("Please enter 1 or 2 / 请输入1或2")
    
    def main_menu(self):
        """Display main menu and handle navigation"""
        # First, let user choose language
        self.language_selection()
        
        while True:
            self.clear_screen()
            if self.language == 'zh':
                self.print_header("Python Concepts Trainer for Junior Developers", 
                                 "面向初级开发者的Python概念训练器")
                
                print("选择一个课程来学习常见的Python误解：\n")
                
                lessons = [
                    "1. 列表可变性和引用 (List Mutability and References)",
                    "2. 除法总是返回浮点数 (Division Always Returns Float)", 
                    "3. 变量作用域（全局vs局部） (Variable Scope - Global vs Local)",
                    "4. 海象运算符（赋值表达式） (Walrus Operator - Assignment Expressions)",
                    "5. 列表切片vs直接索引 (List Slicing vs Direct Indexing)",
                    "6. 集合相等性和可哈希性 (Set Equality and Hashability)",
                    "7. 异常处理模式 (Exception Handling Patterns)",
                    "8. 类型系统基础 (Type System Fundamentals)",
                    "9. 互动测验 (Interactive Quiz)",
                    "L. 切换语言 (Switch Language)",
                    "0. 退出 (Exit)"
                ]
            else:
                self.print_header("Python Concepts Trainer for Junior Developers", 
                                 "面向初级开发者的Python概念训练器")
                
                print("Choose a lesson to learn about common Python misconceptions:\n")
                
                lessons = [
                    "1. List Mutability and References (列表可变性和引用)",
                    "2. Division Always Returns Float (除法总是返回浮点数)", 
                    "3. Variable Scope (Global vs Local) (变量作用域：全局vs局部)",
                    "4. Walrus Operator (Assignment Expressions) (海象运算符：赋值表达式)",
                    "5. List Slicing vs Direct Indexing (列表切片vs直接索引)",
                    "6. Set Equality and Hashability (集合相等性和可哈希性)",
                    "7. Exception Handling Patterns (异常处理模式)",
                    "8. Type System Fundamentals (类型系统基础)",
                    "9. Interactive Quiz (互动测验)",
                    "L. Switch Language (切换语言)",
                    "0. Exit (退出)"
                ]
            
            for lesson in lessons:
                print(lesson)
            
            progress_text = self.t(
                f"\nProgress: {self.current_lesson}/{self.total_lessons} lessons completed",
                f"\n进度：{self.current_lesson}/{self.total_lessons} 课程已完成"
            )
            print(progress_text)
            
            try:
                prompt = self.t("Enter your choice (0-9, L):", "输入您的选择 (0-9, L):")
                choice = input(f"\n{prompt} ").strip().upper()
                
                if choice == '0':
                    exit_msg = self.t(
                        "Thanks for learning with Python Concepts Trainer!",
                        "感谢使用Python概念训练器学习！"
                    )
                    print(f"\n{exit_msg}")
                    break
                elif choice == 'L':
                    self.language_selection()
                    continue
                elif choice == '1':
                    self.lesson_1_list_mutability()
                    self.current_lesson = max(self.current_lesson, 1)
                elif choice == '2':
                    self.lesson_2_division_behavior()
                    self.current_lesson = max(self.current_lesson, 2)
                # Add other lesson calls here...
                elif choice == '9':
                    self.interactive_quiz()
                else:
                    error_msg = self.t(
                        "Invalid choice. Please enter a number from 0-9 or L.",
                        "无效选择。请输入0-9的数字或L。"
                    )
                    print(error_msg)
                    self.wait_for_user()
                    
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                error_msg = self.t("An error occurred:", "发生错误：")
                print(f"{error_msg} {e}")
                self.wait_for_user()

    def interactive_quiz(self):
        """Interactive quiz to test understanding"""
        self.clear_screen()
        self.print_header("Interactive Quiz", "互动测验")
        
        questions = [
            {
                "en_question": "What does this code print?\nx = [1, 2]\ny = x\ny.append(3)\nprint(len(x))",
                "zh_question": "这段代码输出什么？\nx = [1, 2]\ny = x\ny.append(3)\nprint(len(x))",
                "options": ["A) 2", "B) 3", "C) Error", "D) 1"],
                "correct": "B",
                "en_explanation": "y is a reference to x, so both see the appended element",
                "zh_explanation": "y是x的引用，所以两者都能看到追加的元素"
            },
            {
                "en_question": "What type does this expression return?\ntype(10 / 5)",
                "zh_question": "这个表达式返回什么类型？\ntype(10 / 5)",
                "options": ["A) int", "B) float", "C) str", "D) bool"],
                "correct": "B",
                "en_explanation": "Division operator / always returns float in Python",
                "zh_explanation": "除法运算符/在Python中总是返回float"
            }
        ]
        
        score = 0
        for i, q in enumerate(questions, 1):
            question_text = self.t(f"\nQuestion {i}:", f"\n问题 {i}：")
            print(question_text)
            
            question = self.t(q["en_question"], q["zh_question"])
            print(question)
            print()
            for option in q["options"]:
                print(option)
            
            while True:
                prompt = self.t("Your answer (A/B/C/D):", "您的答案 (A/B/C/D):")
                answer = input(f"\n{prompt} ").upper().strip()
                if answer in ['A', 'B', 'C', 'D']:
                    break
                error_msg = self.t("Please enter A, B, C, or D", "请输入A、B、C或D")
                print(error_msg)
            
            if answer == q["correct"]:
                correct_msg = self.t("✓ Correct!", "✓ 正确！")
                print(correct_msg)
                score += 1
            else:
                incorrect_msg = self.t(
                    f"✗ Incorrect. The answer is {q['correct']}",
                    f"✗ 错误。答案是 {q['correct']}"
                )
                print(incorrect_msg)
            
            explanation = self.t(q["en_explanation"], q["zh_explanation"])
            exp_label = self.t("Explanation:", "解释：")
            print(f"{exp_label} {explanation}")
            self.wait_for_user()
        
        final_score = self.t(f"\nFinal Score: {score}/{len(questions)}", 
                           f"\n最终得分：{score}/{len(questions)}")
        print(final_score)
        
        if score == len(questions):
            perfect_msg = self.t("Perfect! You've mastered these concepts!", 
                               "完美！您已经掌握了这些概念！")
            print(perfect_msg)
        elif score >= len(questions) * 0.7:
            good_msg = self.t("Great job! You understand most concepts well.", 
                            "做得很好！您很好地理解了大部分概念。")
            print(good_msg)
        else:
            study_msg = self.t("Keep studying! Review the lessons and try again.", 
                             "继续学习！复习课程并再试一次。")
            print(study_msg)
        
    def clear_screen(self):
        """Clear the console screen"""
        print("\n" * 50)
    
    def print_header(self, title: str):
        """Print a formatted header"""
        print("=" * 60)
        print(f"  {title}")
        print("=" * 60)
    
    def print_separator(self):
        """Print a separator line"""
        print("-" * 60)
    
    def wait_for_user(self):
        """Wait for user input to continue"""
        input("\nPress Enter to continue...")
    
    def run_code_safely(self, code: str, description: str = ""):
        """Execute code safely and show results"""
        print(f"\n🔍 {description}")
        print(f"Code: {code}")
        print("Result:", end=" ")
        
        try:
            # Use eval for expressions, exec for statements
            if any(keyword in code for keyword in ['=', 'def ', 'class ', 'import ', 'for ', 'while ', 'if ']):
                # Create a local namespace for exec
                local_vars = {}
                exec(code, globals(), local_vars)
                if local_vars:
                    for var, value in local_vars.items():
                        if not var.startswith('_'):
                            print(f"{var} = {repr(value)}")
                else:
                    print("(Code executed)")
            else:
                result = eval(code)
                print(repr(result))
        except Exception as e:
            print(f"ERROR: {type(e).__name__}: {e}")
    
    def lesson_1_list_mutability(self):
        """Lesson 1: List Mutability and References"""
        self.clear_screen()
        self.print_header("Lesson 1: List Mutability and References")
        
        print("MISCONCEPTION: When you assign y = x, you get separate lists")
        print("REALITY: You get two references to the same list object")
        
        self.print_separator()
        print("\nLet's demonstrate:")
        
        # Demonstration
        self.run_code_safely("x = [1, 2, 3]", "Create original list")
        self.run_code_safely("y = x", "Assign x to y - creates reference, not copy")
        self.run_code_safely("print(f'x: {x}, y: {y}')", "Both show same values")
        self.run_code_safely("print(f'Same object? {x is y}')", "Check if same object")
        self.run_code_safely("print(f'x id: {id(x)}, y id: {id(y)}')", "Memory addresses")
        
        print("\nNow let's modify through y:")
        self.run_code_safely("y[0] = 999", "Change first element through y")
        self.run_code_safely("print(f'x: {x}, y: {y}')", "Both lists changed!")
        
        print("\n💡 KEY INSIGHT: x and y point to the same list in memory")
        
        self.print_separator()
        print("\nHow to create actual copies:")
        
        self.run_code_safely("original = [1, 2, 3]", "New original list")
        self.run_code_safely("copy1 = original.copy()", "Method 1: .copy()")
        self.run_code_safely("copy2 = original[:]", "Method 2: slice notation")
        self.run_code_safely("copy3 = list(original)", "Method 3: list() constructor")
        
        self.run_code_safely("copy1[0] = 999", "Modify copy1")
        self.run_code_safely("print(f'original: {original}')", "Original unchanged")
        self.run_code_safely("print(f'copy1: {copy1}')", "Only copy1 changed")
        
        print("\n🎯 TAKEAWAY: Use .copy(), [:], or list() to create independent copies")
        self.wait_for_user()
    
    def lesson_2_division_behavior(self):
        """Lesson 2: Division Always Returns Float"""
        self.clear_screen()
        self.print_header("Lesson 2: Division Always Returns Float")
        
        print("MISCONCEPTION: 4 / 2 should return 2 (integer)")
        print("REALITY: Division operator / always returns float in Python")
        
        self.print_separator()
        print("\nDemonstration:")
        
        self.run_code_safely("result1 = 4 / 2", "Even division")
        self.run_code_safely("type(result1)", "Type is float, not int")
        self.run_code_safely("result1", "Value is 2.0")
        
        self.run_code_safely("result2 = 10 / 5", "Another even division")
        self.run_code_safely("type(result2)", "Still float")
        
        self.run_code_safely("result3 = 7 / 3", "Uneven division")
        self.run_code_safely("type(result3)", "Also float")
        
        print("\n🔍 Compare with other operators:")
        self.run_code_safely("type(4 + 2)", "Addition preserves int")
        self.run_code_safely("type(4 * 2)", "Multiplication preserves int")
        self.run_code_safely("type(4 - 2)", "Subtraction preserves int")
        self.run_code_safely("type(4 / 2)", "Division always gives float")
        
        self.print_separator()
        print("\nAlternatives for integer division:")
        
        self.run_code_safely("4 // 2", "Floor division")
        self.run_code_safely("type(4 // 2)", "Returns int")
        self.run_code_safely("7 // 3", "Floor division truncates")
        self.run_code_safely("int(7 / 3)", "Convert float division to int")
        
        print("\n💡 WHY: Python prioritizes mathematical precision over type consistency")
        print("🎯 TAKEAWAY: Use // for integer division, / always gives float")
        self.wait_for_user()
    
    def lesson_3_variable_scope(self):
        """Lesson 3: Variable Scope and Global vs Local"""
        self.clear_screen()
        self.print_header("Lesson 3: Variable Scope Issues")
        
        print("MISCONCEPTION: Functions can modify global variables freely")
        print("REALITY: Assignment inside functions creates local variables")
        
        self.print_separator()
        print("\nProblematic code:")
        
        problematic_code = '''
x = 10
def func():
    x += 1  # This will cause UnboundLocalError
    print(x)
'''
        print(problematic_code)
        print("Trying to run func()...")
        
        try:
            x = 10
            def func():
                x += 1
                print(x)
            func()
        except Exception as e:
            print(f"ERROR: {type(e).__name__}: {e}")
        
        print("\n🔍 Why this happens:")
        print("1. Python sees 'x += 1' as assignment")
        print("2. Assignment makes x a local variable")
        print("3. But x is read before it's assigned locally")
        print("4. UnboundLocalError occurs")
        
        self.print_separator()
        print("\nSolution 1: Use global keyword")
        
        solution1_code = '''
x = 10
def func_global():
    global x
    x += 1
    print(f"Inside function: {x}")

func_global()
print(f"Outside function: {x}")
'''
        
        exec(solution1_code)
        
        self.print_separator()
        print("\nSolution 2: Pass and return values")
        
        solution2_code = '''
x = 10
def func_return(value):
    value += 1
    return value

x = func_return(x)
print(f"Result: {x}")
'''
        
        exec(solution2_code)
        
        print("\n🎯 TAKEAWAY: Be explicit about scope - use global or pass/return patterns")
        self.wait_for_user()
    
    def lesson_4_walrus_operator(self):
        """Lesson 4: Walrus Operator (Assignment Expressions)"""
        self.clear_screen()
        self.print_header("Lesson 4: Walrus Operator (:=)")
        
        print("NEW FEATURE: Assignment expressions (Python 3.8+)")
        print("CONCEPT: Assign AND return value in one expression")
        
        self.print_separator()
        print("\nBasic example:")
        
        # Check if walrus operator is supported
        try:
            exec("x = 5\nif (x := 2) == 2:\n    print(f'x is now {x}')")
            print("Code executed successfully")
        except SyntaxError:
            print("Walrus operator not supported in this Python version")
            return
        
        print("\nStep by step breakdown:")
        self.run_code_safely("x = 5", "Initial value")
        self.run_code_safely("print(f'Before: x = {x}')", "Check initial value")
        
        # Simulate the walrus operator effect
        print("\nExpression: if (x := 2) == 2:")
        print("1. x := 2 assigns 2 to x")
        print("2. x := 2 returns 2")
        print("3. 2 == 2 evaluates to True")
        print("4. x is permanently changed to 2")
        
        x = 5
        if (x := 2) == 2:
            print(f"Inside if: x = {x}")
        print(f"After if: x = {x}")
        
        self.print_separator()
        print("\nPractical use cases:")
        
        print("\n1. Reading input until condition met:")
        practical_code1 = '''
# Traditional way
data = input("Enter data: ")
while data != "quit":
    print(f"You entered: {data}")
    data = input("Enter data: ")

# With walrus operator
while (data := input("Enter data: ")) != "quit":
    print(f"You entered: {data}")
'''
        print(practical_code1)
        
        print("\n2. List comprehensions with complex conditions:")
        practical_code2 = '''
# Traditional way
results = []
for x in range(10):
    squared = x ** 2
    if squared > 20:
        results.append(squared)

# With walrus operator
results = [squared for x in range(10) if (squared := x ** 2) > 20]
'''
        print(practical_code2)
        
        print("\n🎯 TAKEAWAY: Walrus operator creates permanent assignments within expressions")
        self.wait_for_user()
    
    def lesson_5_slice_behavior(self):
        """Lesson 5: Forgiving Slice Behavior"""
        self.clear_screen()
        self.print_header("Lesson 5: List Slicing vs Direct Indexing")
        
        print("MISCONCEPTION: Out-of-bounds indices always cause errors")
        print("REALITY: Slicing is forgiving, direct indexing is strict")
        
        self.print_separator()
        print("\nDemonstration with direct indexing:")
        
        self.run_code_safely("a = [1, 2, 3]", "Create a 3-element list")
        self.run_code_safely("len(a)", "Length is 3 (indices 0, 1, 2)")
        self.run_code_safely("a[0]", "Valid index")
        self.run_code_safely("a[2]", "Valid index")
        
        print("\nTrying invalid direct indices:")
        self.run_code_safely("a[5]", "Index 5 doesn't exist")
        self.run_code_safely("a[-10]", "Index -10 doesn't exist")
        
        self.print_separator()
        print("\nNow let's try slicing with extreme indices:")
        
        self.run_code_safely("a[-100:100]", "Extreme slice indices")
        self.run_code_safely("a[10:20]", "Beyond list bounds")
        self.run_code_safely("a[-5:2]", "Start before beginning")
        self.run_code_safely("a[1:100]", "End far beyond end")
        
        print("\n🔍 What happens internally:")
        print("1. Python clamps slice indices to valid ranges")
        print("2. a[-100:100] becomes a[0:3]")
        print("3. a[10:20] becomes a[3:3] (empty slice)")
        print("4. No error is raised")
        
        self.print_separator()
        print("\nWhy this design choice?")
        print("✓ Makes slicing more robust")
        print("✓ Prevents crashes from conservative bounds")
        print("✓ a[:] always returns full list regardless of size")
        
        print("\nComparison:")
        self.run_code_safely("a[:]", "Full slice always works")
        self.run_code_safely("a[:1000]", "Conservative end index works")
        self.run_code_safely("a[-1000:]", "Conservative start index works")
        
        print("\n🎯 TAKEAWAY: Slicing is forgiving by design, indexing is strict")
        self.wait_for_user()
    
    def lesson_6_set_concepts(self):
        """Lesson 6: Set Equality and Hashability"""
        self.clear_screen()
        self.print_header("Lesson 6: Set Behavior and Properties")
        
        print("CONCEPTS: Set equality, identity, and hashability requirements")
        
        self.print_separator()
        print("\nSet equality (contents matter, order doesn't):")
        
        self.run_code_safely("s1 = {1, 2, 3}", "First set")
        self.run_code_safely("s2 = {3, 2, 1}", "Same elements, different order")
        self.run_code_safely("s1 == s2", "Equal contents")
        self.run_code_safely("s1 is s2", "Different objects")
        self.run_code_safely("id(s1) == id(s2)", "Different memory locations")
        
        print("\nSets are unordered:")
        self.run_code_safely("s3 = {5, 1, 3, 2, 4}", "Mixed order input")
        self.run_code_safely("print(s3)", "Display order may vary")
        
        self.print_separator()
        print("\nHashability requirements:")
        
        print("\nValid set elements (hashable):")
        self.run_code_safely("valid_set = {1, 'hello', (1, 2), True}", "Numbers, strings, tuples")
        
        print("\nInvalid set elements (unhashable):")
        self.run_code_safely("invalid_set = {[1, 2]}", "Lists are unhashable")
        self.run_code_safely("invalid_set2 = {{1, 2}}", "Sets are unhashable")
        self.run_code_safely("invalid_set3 = {{'key': 'value'}}", "Dicts are unhashable")
        
        print("\n🔍 Why hashability matters:")
        print("1. Sets use hash tables for fast lookup")
        print("2. Only immutable objects can be hashed reliably")
        print("3. Mutable objects could change, breaking the hash table")
        
        self.print_separator()
        print("\nWorkarounds for unhashable types:")
        
        print("\nInstead of sets of lists, use sets of tuples:")
        self.run_code_safely("list_data = [[1, 2], [3, 4]]", "Lists we want to store")
        self.run_code_safely("tuple_set = {tuple(lst) for lst in list_data}", "Convert to tuples")
        
        print("\nInstead of sets of sets, use frozensets:")
        self.run_code_safely("set_data = [{1, 2}, {3, 4}]", "Sets we want to store")
        self.run_code_safely("frozenset_set = {frozenset(s) for s in set_data}", "Convert to frozensets")
        
        print("\n🎯 TAKEAWAY: Sets require hashable elements; use tuples/frozensets for complex data")
        self.wait_for_user()
    
    def lesson_7_exception_handling(self):
        """Lesson 7: Exception Handling and Introspection"""
        self.clear_screen()
        self.print_header("Lesson 7: Exception Handling Patterns")
        
        print("CONCEPTS: Catching exceptions and extracting useful information")
        
        self.print_separator()
        print("\nBasic exception handling:")
        
        exception_demo = '''
try:
    result = 10 / 0
except Exception as e:
    print(f"Error type: {type(e)}")
    print(f"Error name: {type(e).__name__}")
    print(f"Error message: {e}")
    print(f"Error args: {e.args}")
'''
        
        print(exception_demo)
        print("Output:")
        exec(exception_demo)
        
        self.print_separator()
        print("\nDifferent exception types:")
        
        exceptions_to_test = [
            ("10 / 0", "Division by zero"),
            ("[1, 2, 3][10]", "Index out of range"),
            ("int('hello')", "Invalid conversion"),
            ("undefined_variable", "Undefined variable"),
            ("{1, 2, 3}[0]", "Sets don't support indexing")
        ]
        
        for code, description in exceptions_to_test:
            print(f"\n🔍 Testing: {description}")
            print(f"Code: {code}")
            try:
                eval(code)
            except Exception as e:
                print(f"Exception: {type(e).__name__}: {e}")
        
        self.print_separator()
        print("\nSpecific exception handling:")
        
        specific_handling = '''
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Cannot divide by zero"
    except TypeError as e:
        return f"Type error: {e}"
    except Exception as e:
        return f"Unexpected error: {type(e).__name__}: {e}"

print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide(10, "hello"))
'''
        
        exec(specific_handling)
        
        print("\n🎯 TAKEAWAY: Use specific exception types and extract useful error information")
        self.wait_for_user()
    
    def lesson_8_type_system(self):
        """Lesson 8: Python Type System Fundamentals"""
        self.clear_screen()
        self.print_header("Lesson 8: Type System Understanding")
        
        print("CONCEPTS: Dynamic typing, type checking, and type behavior")
        
        self.print_separator()
        print("\nDynamic typing demonstration:")
        
        self.run_code_safely("x = 42", "Start with integer")
        self.run_code_safely("type(x)", "Check type")
        self.run_code_safely("x = 'hello'", "Change to string")
        self.run_code_safely("type(x)", "Type changed")
        self.run_code_safely("x = [1, 2, 3]", "Change to list")
        self.run_code_safely("type(x)", "Type changed again")
        
        print("\n🔍 Type checking methods:")
        self.run_code_safely("isinstance(42, int)", "Check if 42 is int")
        self.run_code_safely("isinstance(42, (int, float))", "Check multiple types")
        self.run_code_safely("isinstance('hello', str)", "Check string")
        self.run_code_safely("type(42) == int", "Exact type comparison")
        
        self.print_separator()
        print("\nMutable vs Immutable types:")
        
        print("\nImmutable types (cannot be changed in place):")
        immutable_examples = [
            ("x = 5; x += 1", "int - creates new object"),
            ("s = 'hello'; s += ' world'", "str - creates new object"),
            ("t = (1, 2); t += (3,)", "tuple - creates new object")
        ]
        
        for code, explanation in immutable_examples:
            print(f"\n{explanation}:")
            parts = code.split('; ')
            for part in parts:
                self.run_code_safely(part.strip(), "")
        
        print("\nMutable types (can be changed in place):")
        mutable_examples = [
            ("lst = [1, 2]; lst.append(3)", "list - modifies in place"),
            ("d = {'a': 1}; d['b'] = 2", "dict - modifies in place"),
            ("s = {1, 2}; s.add(3)", "set - modifies in place")
        ]
        
        for code, explanation in mutable_examples:
            print(f"\n{explanation}:")
            self.run_code_safely(code, "")
        
        self.print_separator()
        print("\nType coercion and conversion:")
        
        self.run_code_safely("int('42')", "String to int")
        self.run_code_safely("float('3.14')", "String to float")
        self.run_code_safely("str(42)", "Int to string")
        self.run_code_safely("list('hello')", "String to list")
        self.run_code_safely("tuple([1, 2, 3])", "List to tuple")
        self.run_code_safely("set([1, 2, 2, 3])", "List to set (removes duplicates)")
        
        print("\n🎯 TAKEAWAY: Understand mutability and use appropriate type checking methods")
        self.wait_for_user()
    
    def interactive_quiz(self):
        """Interactive quiz to test understanding"""
        self.clear_screen()
        self.print_header("Interactive Quiz")
        
        questions = [
            {
                "question": "What does this code print?\nx = [1, 2]\ny = x\ny.append(3)\nprint(len(x))",
                "options": ["A) 2", "B) 3", "C) Error", "D) 1"],
                "correct": "B",
                "explanation": "y is a reference to x, so both see the appended element"
            },
            {
                "question": "What type does this expression return?\ntype(10 / 5)",
                "options": ["A) int", "B) float", "C) str", "D) bool"],
                "correct": "B",
                "explanation": "Division operator / always returns float in Python"
            },
            {
                "question": "What happens with this code?\na = [1, 2, 3]\nprint(a[-100:100])",
                "options": ["A) IndexError", "B) []", "C) [1, 2, 3]", "D) None"],
                "correct": "C",
                "explanation": "Slicing clamps indices to valid ranges, returning full list"
            }
        ]
        
        score = 0
        for i, q in enumerate(questions, 1):
            print(f"\nQuestion {i}:")
            print(q["question"])
            print()
            for option in q["options"]:
                print(option)
            
            while True:
                answer = input("\nYour answer (A/B/C/D): ").upper().strip()
                if answer in ['A', 'B', 'C', 'D']:
                    break
                print("Please enter A, B, C, or D")
            
            if answer == q["correct"]:
                print("✓ Correct!")
                score += 1
            else:
                print(f"✗ Incorrect. The answer is {q['correct']}")
            
            print(f"Explanation: {q['explanation']}")
            self.wait_for_user()
        
        print(f"\nFinal Score: {score}/{len(questions)}")
        if score == len(questions):
            print("Perfect! You've mastered these concepts!")
        elif score >= len(questions) * 0.7:
            print("Great job! You understand most concepts well.")
        else:
            print("Keep studying! Review the lessons and try again.")
    
    def main_menu(self):
        """Display main menu and handle navigation"""
        while True:
            self.clear_screen()
            self.print_header("Python Concepts Trainer for Junior Developers")
            
            print("Choose a lesson to learn about common Python misconceptions:\n")
            
            lessons = [
                "1. List Mutability and References",
                "2. Division Always Returns Float", 
                "3. Variable Scope (Global vs Local)",
                "4. Walrus Operator (Assignment Expressions)",
                "5. List Slicing vs Direct Indexing",
                "6. Set Equality and Hashability",
                "7. Exception Handling Patterns",
                "8. Type System Fundamentals",
                "9. Interactive Quiz",
                "0. Exit"
            ]
            
            for lesson in lessons:
                print(lesson)
            
            print(f"\nProgress: {self.current_lesson}/{self.total_lessons} lessons completed")
            
            try:
                choice = input("\nEnter your choice (0-9): ").strip()
                
                if choice == '0':
                    print("\nThanks for learning with Python Concepts Trainer!")
                    break
                elif choice == '1':
                    self.lesson_1_list_mutability()
                    self.current_lesson = max(self.current_lesson, 1)
                elif choice == '2':
                    self.lesson_2_division_behavior()
                    self.current_lesson = max(self.current_lesson, 2)
                elif choice == '3':
                    self.lesson_3_variable_scope()
                    self.current_lesson = max(self.current_lesson, 3)
                elif choice == '4':
                    self.lesson_4_walrus_operator()
                    self.current_lesson = max(self.current_lesson, 4)
                elif choice == '5':
                    self.lesson_5_slice_behavior()
                    self.current_lesson = max(self.current_lesson, 5)
                elif choice == '6':
                    self.lesson_6_set_concepts()
                    self.current_lesson = max(self.current_lesson, 6)
                elif choice == '7':
                    self.lesson_7_exception_handling()
                    self.current_lesson = max(self.current_lesson, 7)
                elif choice == '8':
                    self.lesson_8_type_system()
                    self.current_lesson = max(self.current_lesson, 8)
                elif choice == '9':
                    self.interactive_quiz()
                else:
                    print("Invalid choice. Please enter a number from 0-9.")
                    self.wait_for_user()
                    
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                self.wait_for_user()

def main():
    """Main entry point"""
    trainer = PythonConceptsTrainer()
    trainer.main_menu()

if __name__ == "__main__":
    main()