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
            if any(keyword in code for keyword in ['=', 'def ', 'class ', 'import ', 'for ', 'while ', 'if ', 'try:', 'except']):
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
        self.clear_screen()
        self.print_header("Lesson 1: List Mutability and References", "第1课：列表可变性和引用")
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
        self.run_code_safely("x = [1, 2, 3]", "Create original list", "创建原始列表")
        self.run_code_safely("y = x", "Assign x to y - creates reference, not copy", "将x赋值给y - 创建引用，不是副本")
        self.run_code_safely("print(f'x: {x}, y: {y}')", "Both show same values", "两者显示相同的值")
        self.run_code_safely("print(f'Same object? {x is y}')", "Check if same object", "检查是否是同一个对象")
        self.run_code_safely("print(f'x id: {id(x)}, y id: {id(y)}')", "Memory addresses", "内存地址")
        self.print_bilingual("\nNow let's modify through y:", "\n现在让我们通过y进行修改：")
        self.run_code_safely("y[0] = 999", "Change first element through y", "通过y改变第一个元素")
        self.run_code_safely("print(f'x: {x}, y: {y}')", "Both lists changed!", "两个列表都改变了！")
        print(self.t("\n💡 KEY INSIGHT: x and y point to the same list in memory", "\n💡 关键洞察：x和y指向内存中的同一个列表"))
        self.print_separator()
        self.print_bilingual("How to create actual copies:", "如何创建真正的副本：")
        self.run_code_safely("original = [1, 2, 3]", "New original list", "新的原始列表")
        self.run_code_safely("copy1 = original.copy()", "Method 1: .copy()", "方法1：.copy()")
        self.run_code_safely("copy2 = original[:]", "Method 2: slice notation", "方法2：切片表示法")
        self.run_code_safely("copy3 = list(original)", "Method 3: list() constructor", "方法3：list()构造函数")
        self.run_code_safely("copy1[0] = 999", "Modify copy1", "修改copy1")
        self.run_code_safely("print(f'original: {original}')", "Original unchanged", "原始列表未改变")
        self.run_code_safely("print(f'copy1: {copy1}')", "Only copy1 changed", "只有copy1改变了")
        print(self.t("\n🎯 TAKEAWAY: Use .copy(), [:], or list() to create independent copies", "\n🎯 要点：使用.copy()、[:]或list()来创建独立的副本"))
        self.wait_for_user()

    def lesson_2_division_behavior(self):
        self.clear_screen()
        self.print_header("Lesson 2: Division Always Returns Float", "第2课：除法总是返回浮点数")
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
        self.run_code_safely("result1 = 4 / 2", "Even division", "整除")
        self.run_code_safely("type(result1)", "Type is float, not int", "类型是float，不是int")
        self.run_code_safely("result1", "Value is 2.0", "值是2.0")
        self.run_code_safely("result2 = 10 / 5", "Another even division", "另一个整除")
        self.run_code_safely("type(result2)", "Still float", "仍然是float")
        self.run_code_safely("result3 = 7 / 3", "Uneven division", "不整除")
        self.run_code_safely("type(result3)", "Also float", "也是float")
        self.print_bilingual("\n🔍 Compare with other operators:", "\n🔍 与其他运算符比较：")
        self.run_code_safely("type(4 + 2)", "Addition preserves int", "加法保持int")
        self.run_code_safely("type(4 * 2)", "Multiplication preserves int", "乘法保持int")
        self.run_code_safely("type(4 - 2)", "Subtraction preserves int", "减法保持int")
        self.run_code_safely("type(4 / 2)", "Division always gives float", "除法总是给出float")
        self.print_separator()
        self.print_bilingual("Alternatives for integer division:", "整数除法的替代方案：")
        self.run_code_safely("4 // 2", "Floor division", "地板除法")
        self.run_code_safely("type(4 // 2)", "Returns int", "返回int")
        self.run_code_safely("7 // 3", "Floor division truncates", "地板除法截断")
        self.run_code_safely("int(7 / 3)", "Convert float division to int", "将浮点除法转换为int")
        print(self.t("\n💡 WHY: Python prioritizes mathematical precision over type consistency", "\n💡 原因：Python优先考虑数学精度而不是类型一致性"))
        print(self.t("🎯 TAKEAWAY: Use // for integer division, / always gives float", "🎯 要点：使用//进行整数除法，/总是给出float"))
        self.wait_for_user()

    def lesson_3_variable_scope(self):
        self.clear_screen()
        self.print_header("Lesson 3: Variable Scope Issues", "第3课：变量作用域问题")
        self.print_bilingual(
            "MISCONCEPTION: Functions can modify global variables freely",
            "误解：函数可以自由修改全局变量"
        )
        self.print_bilingual(
            "REALITY: Assignment inside functions creates local variables",
            "实际：函数内的赋值会创建局部变量"
        )
        self.print_separator()
        self.print_bilingual("Problematic code:", "有问题的代码：")
        problematic_code = '''x = 10
def func():
    x += 1  # This will cause UnboundLocalError
    print(x)'''
        print(problematic_code)
        self.print_bilingual("Trying to run func()...", "尝试运行 func()...")
        try:
            x = 10
            def func():
                x += 1
                print(x)
            func()
        except Exception as e:
            error_msg = self.t("ERROR", "错误")
            print(f"{error_msg}: {type(e).__name__}: {e}")
        self.print_bilingual("\n🔍 Why this happens:", "\n🔍 为什么会这样：")
        print(self.t(
            "1. Python sees 'x += 1' as assignment\n"
            "2. Assignment makes x a local variable\n"
            "3. But x is read before it's assigned locally\n"
            "4. UnboundLocalError occurs",
            "1. Python 将 'x += 1' 视为赋值\n"
            "2. 赋值使 x 成为局部变量\n"
            "3. 但 x 在局部赋值前被读取\n"
            "4. 导致 UnboundLocalError"
        ))
        self.print_separator()
        self.print_bilingual("Solution 1: Use global keyword", "解决方案1：使用 global 关键字")
        code1 = '''x = 10
def func_global():
    global x
    x += 1
    print(f"Inside function: {x}")
func_global()
print(f"Outside function: {x}")'''
        self.run_code_safely(code1, "Use global to modify global variable", "使用 global 修改全局变量")
        self.print_separator()
        self.print_bilingual("Solution 2: Pass and return values", "解决方案2：传参并返回值")
        code2 = '''x = 10
def func_return(value):
    value += 1
    return value
x = func_return(x)
print(f"Result: {x}")'''
        self.run_code_safely(code2, "Pass and return avoids scope issues", "传参返回避免作用域问题")
        print(self.t("\n🎯 TAKEAWAY: Be explicit about scope - use global or pass/return patterns", "\n🎯 要点：明确作用域——使用 global 或传参/返回模式"))
        self.wait_for_user()

    def lesson_4_walrus_operator(self):
        self.clear_screen()
        self.print_header("Lesson 4: Walrus Operator (:=)", "第4课：海象运算符 (:=)")
        self.print_bilingual(
            "NEW FEATURE: Assignment expressions (Python 3.8+)",
            "新特性：赋值表达式（Python 3.8+）"
        )
        self.print_bilingual(
            "CONCEPT: Assign AND return value in one expression",
            "概念：在一个表达式中同时赋值并返回值"
        )
        self.print_separator()
        self.print_bilingual("Basic example:", "基本示例：")
        try:
            exec("x = 5\nif (x := 2) == 2:\n    print(f'x is now {x}')")
            print(self.t("(Code executed successfully)", "（代码执行成功）"))
        except SyntaxError:
            print(self.t("Walrus operator not supported in this Python version", "当前Python版本不支持海象运算符"))
            self.wait_for_user()
            return
        self.print_bilingual("\nStep by step breakdown:", "\n逐步解析：")
        self.run_code_safely("x = 5", "Initial value", "初始值")
        self.run_code_safely("print(f'Before: x = {x}')", "Check initial value", "检查初始值")
        print(self.t("\nExpression: if (x := 2) == 2:", "\n表达式：if (x := 2) == 2:"))
        print(self.t(
            "1. x := 2 assigns 2 to x\n"
            "2. x := 2 returns 2\n"
            "3. 2 == 2 evaluates to True\n"
            "4. x is permanently changed to 2",
            "1. x := 2 将 2 赋给 x\n"
            "2. x := 2 返回 2\n"
            "3. 2 == 2 为 True\n"
            "4. x 被永久改为 2"
        ))
        x = 5
        if (x := 2) == 2:
            print(f"Inside if: x = {x}")
        print(f"After if: x = {x}")
        self.print_separator()
        self.print_bilingual("Practical use cases:", "实用场景：")
        self.print_bilingual("\n1. Reading input until condition met:", "\n1. 读取输入直到满足条件：")
        print(self.t(
            "# Traditional way\n"
            "data = input(\"Enter data: \")\n"
            "while data != \"quit\":\n"
            "    print(f\"You entered: {data}\")\n"
            "    data = input(\"Enter data: \")\n"
            "\n# With walrus operator\n"
            "while (data := input(\"Enter data: \")) != \"quit\":\n"
            "    print(f\"You entered: {data}\")",
            "# 传统方式\n"
            "data = input(\"输入数据: \")\n"
            "while data != \"quit\":\n"
            "    print(f\"你输入了: {data}\")\n"
            "    data = input(\"输入数据: \")\n"
            "\n# 使用海象运算符\n"
            "while (data := input(\"输入数据: \")) != \"quit\":\n"
            "    print(f\"你输入了: {data}\")"
        ))
        self.print_bilingual("\n2. List comprehensions with complex conditions:", "\n2. 带复杂条件的列表推导式：")
        print(self.t(
            "# Traditional way\n"
            "results = []\n"
            "for x in range(10):\n"
            "    squared = x ** 2\n"
            "    if squared > 20:\n"
            "        results.append(squared)\n"
            "\n# With walrus operator\n"
            "results = [squared for x in range(10) if (squared := x ** 2) > 20]",
            "# 传统方式\n"
            "results = []\n"
            "for x in range(10):\n"
            "    squared = x ** 2\n"
            "    if squared > 20:\n"
            "        results.append(squared)\n"
            "\n# 使用海象运算符\n"
            "results = [squared for x in range(10) if (squared := x ** 2) > 20]"
        ))
        print(self.t("\n🎯 TAKEAWAY: Walrus operator creates permanent assignments within expressions", "\n🎯 要点：海象运算符在表达式内创建永久赋值"))
        self.wait_for_user()

    def lesson_5_slice_behavior(self):
        self.clear_screen()
        self.print_header("Lesson 5: List Slicing vs Direct Indexing", "第5课：列表切片 vs 直接索引")
        self.print_bilingual(
            "MISCONCEPTION: Out-of-bounds indices always cause errors",
            "误解：越界索引总会引发错误"
        )
        self.print_bilingual(
            "REALITY: Slicing is forgiving, direct indexing is strict",
            "实际：切片是宽容的，直接索引是严格的"
        )
        self.print_separator()
        self.print_bilingual("Demonstration with direct indexing:", "直接索引演示：")
        self.run_code_safely("a = [1, 2, 3]", "Create a 3-element list", "创建一个3元素列表")
        self.run_code_safely("len(a)", "Length is 3 (indices 0, 1, 2)", "长度为3（索引0,1,2）")
        self.run_code_safely("a[0]", "Valid index", "有效索引")
        self.run_code_safely("a[2]", "Valid index", "有效索引")
        self.print_bilingual("\nTrying invalid direct indices:", "\n尝试无效的直接索引：")
        self.run_code_safely("a[5]", "Index 5 doesn't exist", "索引5不存在")
        self.run_code_safely("a[-10]", "Index -10 doesn't exist", "索引-10不存在")
        self.print_separator()
        self.print_bilingual("Now let's try slicing with extreme indices:", "现在尝试极端切片索引：")
        self.run_code_safely("a[-100:100]", "Extreme slice indices", "极端切片索引")
        self.run_code_safely("a[10:20]", "Beyond list bounds", "超出列表边界")
        self.run_code_safely("a[-5:2]", "Start before beginning", "起始位置在开头之前")
        self.run_code_safely("a[1:100]", "End far beyond end", "结束位置远超末尾")
        print(self.t("\n🔍 What happens internally:", "\n🔍 内部发生了什么："))
        print(self.t(
            "1. Python clamps slice indices to valid ranges\n"
            "2. a[-100:100] becomes a[0:3]\n"
            "3. a[10:20] becomes a[3:3] (empty slice)\n"
            "4. No error is raised",
            "1. Python 将切片索引限制在有效范围内\n"
            "2. a[-100:100] 变成 a[0:3]\n"
            "3. a[10:20] 变成 a[3:3]（空切片）\n"
            "4. 不会报错"
        ))
        self.print_separator()
        self.print_bilingual("Why this design choice?", "为何这样设计？")
        print(self.t(
            "✓ Makes slicing more robust\n"
            "✓ Prevents crashes from conservative bounds\n"
            "✓ a[:] always returns full list regardless of size",
            "✓ 使切片更健壮\n"
            "✓ 避免因保守边界导致崩溃\n"
            "✓ a[:] 总是返回完整列表，无论大小"
        ))
        self.print_bilingual("\nComparison:", "\n对比：")
        self.run_code_safely("a[:]", "Full slice always works", "完整切片始终有效")
        self.run_code_safely("a[:1000]", "Conservative end index works", "保守的结束索引有效")
        self.run_code_safely("a[-1000:]", "Conservative start index works", "保守的起始索引有效")
        print(self.t("\n🎯 TAKEAWAY: Slicing is forgiving by design, indexing is strict", "\n🎯 要点：切片设计上是宽容的，索引是严格的"))
        self.wait_for_user()

    def lesson_6_set_concepts(self):
        self.clear_screen()
        self.print_header("Lesson 6: Set Behavior and Properties", "第6课：集合行为与特性")
        self.print_bilingual(
            "CONCEPTS: Set equality, identity, and hashability requirements",
            "概念：集合相等性、标识和可哈希性要求"
        )
        self.print_separator()
        self.print_bilingual("Set equality (contents matter, order doesn't):", "集合相等性（内容重要，顺序无关）：")
        self.run_code_safely("s1 = {1, 2, 3}", "First set", "第一个集合")
        self.run_code_safely("s2 = {3, 2, 1}", "Same elements, different order", "相同元素，不同顺序")
        self.run_code_safely("s1 == s2", "Equal contents", "内容相等")
        self.run_code_safely("s1 is s2", "Different objects", "不同对象")
        self.run_code_safely("id(s1) == id(s2)", "Different memory locations", "不同内存地址")
        self.print_bilingual("\nSets are unordered:", "\n集合是无序的：")
        self.run_code_safely("s3 = {5, 1, 3, 2, 4}", "Mixed order input", "混合顺序输入")
        self.run_code_safely("print(s3)", "Display order may vary", "显示顺序可能不同")
        self.print_separator()
        self.print_bilingual("Hashability requirements:", "可哈希性要求：")
        self.print_bilingual("\nValid set elements (hashable):", "\n有效的集合元素（可哈希）：")
        self.run_code_safely("valid_set = {1, 'hello', (1, 2), True}", "Numbers, strings, tuples", "数字、字符串、元组")
        self.print_bilingual("\nInvalid set elements (unhashable):", "\n无效的集合元素（不可哈希）：")
        self.run_code_safely("invalid_set = {[1, 2]}", "Lists are unhashable", "列表不可哈希")
        self.run_code_safely("invalid_set2 = {{1, 2}}", "Sets are unhashable", "集合不可哈希")
        self.run_code_safely("invalid_set3 = {{'key': 'value'}}", "Dicts are unhashable", "字典不可哈希")
        print(self.t("\n🔍 Why hashability matters:", "\n🔍 为何可哈希性重要："))
        print(self.t(
            "1. Sets use hash tables for fast lookup\n"
            "2. Only immutable objects can be hashed reliably\n"
            "3. Mutable objects could change, breaking the hash table",
            "1. 集合使用哈希表实现快速查找\n"
            "2. 只有不可变对象才能可靠哈希\n"
            "3. 可变对象可能变化，破坏哈希表"
        ))
        self.print_separator()
        self.print_bilingual("Workarounds for unhashable types:", "不可哈希类型的替代方案：")
        self.print_bilingual("\nInstead of sets of lists, use sets of tuples:", "\n不要用列表的集合，改用元组的集合：")
        self.run_code_safely("list_data = [[1, 2], [3, 4]]", "Lists we want to store", "要存储的列表")
        self.run_code_safely("tuple_set = {tuple(lst) for lst in list_data}", "Convert to tuples", "转换为元组")
        self.print_bilingual("\nInstead of sets of sets, use frozensets:", "\n不要用集合的集合，改用frozenset：")
        self.run_code_safely("set_data = [{1, 2}, {3, 4}]", "Sets we want to store", "要存储的集合")
        self.run_code_safely("frozenset_set = {frozenset(s) for s in set_data}", "Convert to frozensets", "转换为frozenset")
        print(self.t("\n🎯 TAKEAWAY: Sets require hashable elements; use tuples/frozensets for complex data", "\n🎯 要点：集合要求元素可哈希；对复杂数据使用元组/frozenset"))
        self.wait_for_user()

    def lesson_7_exception_handling(self):
        self.clear_screen()
        self.print_header("Lesson 7: Exception Handling Patterns", "第7课：异常处理模式")
        self.print_bilingual(
            "CONCEPTS: Catching exceptions and extracting useful information",
            "概念：捕获异常并提取有用信息"
        )
        self.print_separator()
        self.print_bilingual("Basic exception handling:", "基本异常处理：")
        code = '''try:
    result = 10 / 0
except Exception as e:
    print(f"Error type: {type(e)}")
    print(f"Error name: {type(e).__name__}")
    print(f"Error message: {e}")
    print(f"Error args: {e.args}")'''
        self.run_code_safely(code, "Catch and inspect exception", "捕获并检查异常")
        self.print_separator()
        self.print_bilingual("Different exception types:", "不同异常类型：")
        test_cases = [
            ("10 / 0", "Division by zero", "除零错误"),
            ("[1, 2, 3][10]", "Index out of range", "索引越界"),
            ("int('hello')", "Invalid conversion", "无效转换"),
            ("undefined_variable", "Undefined variable", "未定义变量"),
            ("{1, 2, 3}[0]", "Sets don't support indexing", "集合不支持索引")
        ]
        for code, en_desc, zh_desc in test_cases:
            desc = self.t(en_desc, zh_desc)
            print(f"\n🔍 {desc}")
            print(f"{self.t('Code', '代码')}: {code}")
            try:
                eval(code)
            except Exception as e:
                print(f"{self.t('Exception', '异常')}: {type(e).__name__}: {e}")
        self.print_separator()
        self.print_bilingual("Specific exception handling:", "具体异常处理：")
        code = '''def safe_divide(a, b):
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
print(safe_divide(10, "hello"))'''
        self.run_code_safely(code, "Handle specific exceptions", "处理特定异常")
        print(self.t("\n🎯 TAKEAWAY: Use specific exception types and extract useful error information", "\n🎯 要点：使用具体异常类型并提取有用的错误信息"))
        self.wait_for_user()

    def lesson_8_type_system(self):
        self.clear_screen()
        self.print_header("Lesson 8: Type System Understanding", "第8课：类型系统理解")
        self.print_bilingual(
            "CONCEPTS: Dynamic typing, type checking, and type behavior",
            "概念：动态类型、类型检查和类型行为"
        )
        self.print_separator()
        self.print_bilingual("Dynamic typing demonstration:", "动态类型演示：")
        self.run_code_safely("x = 42", "Start with integer", "从整数开始")
        self.run_code_safely("type(x)", "Check type", "检查类型")
        self.run_code_safely("x = 'hello'", "Change to string", "改为字符串")
        self.run_code_safely("type(x)", "Type changed", "类型已变")
        self.run_code_safely("x = [1, 2, 3]", "Change to list", "改为列表")
        self.run_code_safely("type(x)", "Type changed again", "类型再次改变")
        self.print_bilingual("\n🔍 Type checking methods:", "\n🔍 类型检查方法：")
        self.run_code_safely("isinstance(42, int)", "Check if 42 is int", "检查42是否为int")
        self.run_code_safely("isinstance(42, (int, float))", "Check multiple types", "检查多种类型")
        self.run_code_safely("isinstance('hello', str)", "Check string", "检查字符串")
        self.run_code_safely("type(42) == int", "Exact type comparison", "精确类型比较")
        self.print_separator()
        self.print_bilingual("Mutable vs Immutable types:", "可变 vs 不可变类型：")
        self.print_bilingual("\nImmutable types (cannot be changed in place):", "\n不可变类型（不能原地修改）：")
        examples = [
            ("x = 5; x += 1", "int - creates new object", "int - 创建新对象"),
            ("s = 'hello'; s += ' world'", "str - creates new object", "str - 创建新对象"),
            ("t = (1, 2); t += (3,)", "tuple - creates new object", "tuple - 创建新对象")
        ]
        for code, en_exp, zh_exp in examples:
            exp = self.t(en_exp, zh_exp)
            print(f"\n{exp}:")
            for part in code.split('; '):
                self.run_code_safely(part.strip(), "", "")
        self.print_bilingual("\nMutable types (can be changed in place):", "\n可变类型（可原地修改）：")
        mutable_examples = [
            ("lst = [1, 2]; lst.append(3)", "list - modifies in place", "list - 原地修改"),
            ("d = {'a': 1}; d['b'] = 2", "dict - modifies in place", "dict - 原地修改"),
            ("s = {1, 2}; s.add(3)", "set - modifies in place", "set - 原地修改")
        ]
        for code, en_exp, zh_exp in mutable_examples:
            exp = self.t(en_exp, zh_exp)
            print(f"\n{exp}:")
            self.run_code_safely(code, "", "")
        self.print_separator()
        self.print_bilingual("Type coercion and conversion:", "类型转换：")
        conversions = [
            ("int('42')", "String to int", "字符串转整数"),
            ("float('3.14')", "String to float", "字符串转浮点数"),
            ("str(42)", "Int to string", "整数转字符串"),
            ("list('hello')", "String to list", "字符串转列表"),
            ("tuple([1, 2, 3])", "List to tuple", "列表转元组"),
            ("set([1, 2, 2, 3])", "List to set (removes duplicates)", "列表转集合（去重）")
        ]
        for code, en_desc, zh_desc in conversions:
            self.run_code_safely(code, en_desc, zh_desc)
        print(self.t("\n🎯 TAKEAWAY: Understand mutability and use appropriate type checking methods", "\n🎯 要点：理解可变性并使用合适的类型检查方法"))
        self.wait_for_user()

    def interactive_quiz(self):
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
            },
            {
                "en_question": "What happens with this code?\na = [1, 2, 3]\nprint(a[-100:100])",
                "zh_question": "这段代码会发生什么？\na = [1, 2, 3]\nprint(a[-100:100])",
                "options": ["A) IndexError", "B) []", "C) [1, 2, 3]", "D) None"],
                "correct": "C",
                "en_explanation": "Slicing clamps indices to valid ranges, returning full list",
                "zh_explanation": "切片会将索引限制在有效范围内，返回完整列表"
            }
        ]
        score = 0
        for i, q in enumerate(questions, 1):
            print(self.t(f"\nQuestion {i}:", f"\n问题 {i}："))
            question = self.t(q["en_question"], q["zh_question"])
            print(question)
            print()
            for option in q["options"]:
                print(option)
            while True:
                answer = input(self.t("\nYour answer (A/B/C/D): ", "\n您的答案 (A/B/C/D): ")).upper().strip()
                if answer in ['A', 'B', 'C', 'D']:
                    break
                print(self.t("Please enter A, B, C, or D", "请输入A、B、C或D"))
            if answer == q["correct"]:
                print(self.t("✓ Correct!", "✓ 正确！"))
                score += 1
            else:
                print(self.t(f"✗ Incorrect. The answer is {q['correct']}", f"✗ 错误。答案是 {q['correct']}"))
            explanation = self.t(q["en_explanation"], q["zh_explanation"])
            print(f"{self.t('Explanation:', '解释：')} {explanation}")
            self.wait_for_user()
        final_score = self.t(f"\nFinal Score: {score}/{len(questions)}", f"\n最终得分：{score}/{len(questions)}")
        print(final_score)
        if score == len(questions):
            print(self.t("Perfect! You've mastered these concepts!", "完美！您已经掌握了这些概念！"))
        elif score >= len(questions) * 0.7:
            print(self.t("Great job! You understand most concepts well.", "做得很好！您很好地理解了大部分概念。"))
        else:
            print(self.t("Keep studying! Review the lessons and try again.", "继续学习！复习课程并再试一次。"))

    def language_selection(self):
        self.clear_screen()
        print("=" * 60)
        print(self.t("  Language Selection", "  语言选择"))
        print("=" * 60)
        print("1. English")
        print("2. 中文 (Chinese)")
        print("=" * 60)
        while True:
            choice = input(self.t("Choose language (1/2): ", "选择语言 (1/2): ")).strip()
            if choice == '1':
                self.language = 'en'
                break
            elif choice == '2':
                self.language = 'zh'
                break
            else:
                print(self.t("Please enter 1 or 2", "请输入1或2"))

    def main_menu(self):
        self.language_selection()
        while True:
            self.clear_screen()
            self.print_header("Python Concepts Trainer for Junior Developers", "面向初级开发者的Python概念训练器")
            prompt = self.t(
                "Choose a lesson to learn about common Python misconceptions:\n",
                "选择一个课程来学习常见的Python误解：\n"
            )
            print(prompt)
            if self.language == 'zh':
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
            progress = self.t(
                f"\nProgress: {self.current_lesson}/{self.total_lessons} lessons completed",
                f"\n进度：{self.current_lesson}/{self.total_lessons} 课程已完成"
            )
            print(progress)
            try:
                choice = input(self.t("\nEnter your choice (0-9, L): ", "\n输入您的选择 (0-9, L): ")).strip().upper()
                if choice == '0':
                    print(self.t("\nThanks for learning with Python Concepts Trainer!", "\n感谢使用Python概念训练器学习！"))
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
                    print(self.t("Invalid choice. Please enter a number from 0-9 or L.", "无效选择。请输入0-9的数字或L。"))
                    self.wait_for_user()
            except KeyboardInterrupt:
                print(self.t("\nExiting...", "\n正在退出..."))
                break
            except Exception as e:
                print(f"{self.t('An error occurred:', '发生错误：')} {e}")
                self.wait_for_user()

def main():
    trainer = PythonConceptsTrainer()
    trainer.main_menu()

if __name__ == "__main__":
    main()