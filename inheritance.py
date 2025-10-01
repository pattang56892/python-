#!/usr/bin/env python3
"""
Interactive Python Inheritance Learning System
Tests understanding of: Class inheritance, attribute lookup, MRO, shadowing
"""

import os
import sys
from typing import Dict, List, Tuple

# ============ TRANSLATIONS ============
TRANSLATIONS = {
    'en': {
        'title': '=== Python Inheritance & Attribute Lookup Quiz ===',
        'select_lang': 'Select Language / 选择语言:',
        'lang_en': '1) English',
        'lang_zh': '2) 简体中文 (Simplified Chinese)',
        'invalid': 'Invalid choice. Please try again.',
        'main_menu': '\n=== Main Menu ===',
        'menu_learn': '1) Learning Mode - Understand the Concept',
        'menu_quiz': '2) Quiz Mode - Test Your Knowledge',
        'menu_exit': '3) Exit',
        'press_enter': '\nPress Enter to continue...',
        'learning_title': '\n=== Learning Mode: Class Inheritance & Attribute Lookup ===',
        'concept_intro': '\nConcept: Python Attribute Lookup & Method Resolution Order (MRO)',
        'concept_explain': '''
When you access an attribute (like b.x), Python searches in this order:
1. Instance's own attributes (__dict__)
2. Class's attributes
3. Parent class's attributes (following MRO)
4. Raise AttributeError if not found

Key Points:
• Child class attributes SHADOW parent class attributes
• del ClassName.attr removes the attribute from that class
• Deleting child's attribute REVEALS parent's attribute
• Parent's attribute is NEVER modified when child creates its own
        ''',
        'walkthrough_title': '\n--- Step-by-Step Walkthrough ---',
        'initial_state': '\nInitial State:',
        'step': 'Step',
        'code': 'Code',
        'state': 'State',
        'output': 'Output',
        'explanation': 'Explanation',
        'quiz_title': '\n=== Quiz Mode ===',
        'question': 'Question',
        'your_answer': 'Your answer (A/B/C/D): ',
        'correct': '✓ Correct!',
        'incorrect': '✗ Incorrect.',
        'correct_answer': 'The correct answer is',
        'score': 'Your Score',
        'try_again': 'Would you like to try again? (y/n): ',
        'q1_question': '''
class A:
    x = 1

class B(A):
    pass

b = B()
print(b.x)      # First print
B.x = 2
print(b.x)      # Second print
del B.x
print(b.x)      # Third print

What will be printed?
        ''',
        'q1_a': 'A) 1 2 1',
        'q1_b': 'B) 1 2 2',
        'q1_c': 'C) 1 1 1',
        'q1_d': 'D) Error',
        'q1_answer': 'A',
        'q1_explain': '''
Explanation:
1st print: b.x looks up B → A, finds A.x = 1
2nd print: B.x = 2 creates new attribute in B, shadows A.x
3rd print: del B.x removes B's attribute, reveals A.x = 1 again
        ''',
        'q2_question': '''
class Parent:
    value = 10

class Child(Parent):
    pass

c = Child()
Child.value = 20
print(c.value)
print(Parent.value)

What will be printed?
        ''',
        'q2_a': 'A) 20 20',
        'q2_b': 'B) 20 10',
        'q2_c': 'C) 10 10',
        'q2_d': 'D) 10 20',
        'q2_answer': 'B',
        'q2_explain': '''
Explanation:
Child.value = 20 creates new attribute in Child (shadows Parent.value)
c.value finds Child.value = 20
Parent.value remains unchanged = 10
        ''',
        'q3_question': '''
class A:
    x = 1

class B(A):
    x = 2

b = B()
print(b.x)
del B.x
print(b.x)

What will be printed?
        ''',
        'q3_a': 'A) 2 1',
        'q3_b': 'B) 2 2',
        'q3_c': 'C) 1 1',
        'q3_d': 'D) 2 Error',
        'q3_answer': 'A',
        'q3_explain': '''
Explanation:
1st print: b.x finds B.x = 2
2nd print: After del B.x, lookup continues to A, finds A.x = 1
        ''',
    },
    'zh': {
        'title': '=== Python 继承与属性查找测验 ===',
        'select_lang': 'Select Language / 选择语言:',
        'lang_en': '1) English',
        'lang_zh': '2) 简体中文 (Simplified Chinese)',
        'invalid': '无效选择。请重试。',
        'main_menu': '\n=== 主菜单 ===',
        'menu_learn': '1) 学习模式 - 理解概念',
        'menu_quiz': '2) 测验模式 - 测试你的知识',
        'menu_exit': '3) 退出',
        'press_enter': '\n按回车键继续...',
        'learning_title': '\n=== 学习模式：类继承与属性查找 ===',
        'concept_intro': '\n概念：Python 属性查找与方法解析顺序 (MRO)',
        'concept_explain': '''
当你访问一个属性（如 b.x）时，Python 按以下顺序搜索：
1. 实例自己的属性 (__dict__)
2. 类的属性
3. 父类的属性（遵循 MRO）
4. 如果未找到则抛出 AttributeError

关键点：
• 子类属性会遮蔽（shadow）父类属性
• del ClassName.attr 从该类中删除属性
• 删除子类属性会显露父类的属性
• 当子类创建自己的属性时，父类的属性永远不会被修改
        ''',
        'walkthrough_title': '\n--- 逐步演示 ---',
        'initial_state': '\n初始状态：',
        'step': '步骤',
        'code': '代码',
        'state': '状态',
        'output': '输出',
        'explanation': '解释',
        'quiz_title': '\n=== 测验模式 ===',
        'question': '问题',
        'your_answer': '你的答案 (A/B/C/D): ',
        'correct': '✓ 正确！',
        'incorrect': '✗ 不正确。',
        'correct_answer': '正确答案是',
        'score': '你的分数',
        'try_again': '想再试一次吗？(y/n): ',
        'q1_question': '''
class A:
    x = 1

class B(A):
    pass

b = B()
print(b.x)      # 第一次打印
B.x = 2
print(b.x)      # 第二次打印
del B.x
print(b.x)      # 第三次打印

会打印什么？
        ''',
        'q1_a': 'A) 1 2 1',
        'q1_b': 'B) 1 2 2',
        'q1_c': 'C) 1 1 1',
        'q1_d': 'D) 报错',
        'q1_answer': 'A',
        'q1_explain': '''
解释：
第1次打印：b.x 查找 B → A，找到 A.x = 1
第2次打印：B.x = 2 在 B 中创建新属性，遮蔽 A.x
第3次打印：del B.x 删除 B 的属性，再次显露 A.x = 1
        ''',
        'q2_question': '''
class Parent:
    value = 10

class Child(Parent):
    pass

c = Child()
Child.value = 20
print(c.value)
print(Parent.value)

会打印什么？
        ''',
        'q2_a': 'A) 20 20',
        'q2_b': 'B) 20 10',
        'q2_c': 'C) 10 10',
        'q2_d': 'D) 10 20',
        'q2_answer': 'B',
        'q2_explain': '''
解释：
Child.value = 20 在 Child 中创建新属性（遮蔽 Parent.value）
c.value 找到 Child.value = 20
Parent.value 保持不变 = 10
        ''',
        'q3_question': '''
class A:
    x = 1

class B(A):
    x = 2

b = B()
print(b.x)
del B.x
print(b.x)

会打印什么？
        ''',
        'q3_a': 'A) 2 1',
        'q3_b': 'B) 2 2',
        'q3_c': 'C) 1 1',
        'q3_d': 'D) 2 报错',
        'q3_answer': 'A',
        'q3_explain': '''
解释：
第1次打印：b.x 找到 B.x = 2
第2次打印：del B.x 后，查找继续到 A，找到 A.x = 1
        ''',
    }
}


class InheritanceQuiz:
    def __init__(self):
        self.lang = 'en'
        self.t = TRANSLATIONS['en']
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_text(self, key: str) -> str:
        """Get translated text"""
        return self.t.get(key, key)
    
    def select_language(self):
        """Language selection menu"""
        self.clear_screen()
        print(self.get_text('title'))
        print(self.get_text('select_lang'))
        print(self.get_text('lang_en'))
        print(self.get_text('lang_zh'))
        
        while True:
            choice = input('\n> ').strip()
            if choice == '1':
                self.lang = 'en'
                self.t = TRANSLATIONS['en']
                break
            elif choice == '2':
                self.lang = 'zh'
                self.t = TRANSLATIONS['zh']
                break
            else:
                print(self.get_text('invalid'))
    
    def show_main_menu(self) -> str:
        """Display main menu and get choice"""
        self.clear_screen()
        print(self.get_text('title'))
        print(self.get_text('main_menu'))
        print(self.get_text('menu_learn'))
        print(self.get_text('menu_quiz'))
        print(self.get_text('menu_exit'))
        
        return input('\n> ').strip()
    
    def learning_mode(self):
        """Interactive learning mode with step-by-step explanation"""
        self.clear_screen()
        print(self.get_text('learning_title'))
        print(self.get_text('concept_intro'))
        print(self.get_text('concept_explain'))
        
        input(self.get_text('press_enter'))
        
        # Step-by-step walkthrough
        print(self.get_text('walkthrough_title'))
        
        steps = [
            {
                'code': 'class A:\n    x = 1',
                'state': 'A.x = 1',
                'output': '',
                'explain': 'Define class A with class variable x = 1' if self.lang == 'en' 
                          else '定义类 A，类变量 x = 1'
            },
            {
                'code': 'class B(A):\n    pass',
                'state': 'B inherits from A\nB has no own attributes' if self.lang == 'en'
                        else 'B 继承自 A\nB 没有自己的属性',
                'output': '',
                'explain': 'B inherits from A, has no attributes of its own' if self.lang == 'en'
                          else 'B 继承自 A，没有自己的属性'
            },
            {
                'code': 'b = B()\nprint(b.x)',
                'state': 'b.x lookup: B → A\nFinds A.x = 1' if self.lang == 'en'
                        else 'b.x 查找：B → A\n找到 A.x = 1',
                'output': '1',
                'explain': 'b.x searches B (not found) → A (found x=1)' if self.lang == 'en'
                          else 'b.x 在 B 中搜索（未找到）→ A（找到 x=1）'
            },
            {
                'code': 'B.x = 2\nprint(b.x)',
                'state': 'A.x = 1 (unchanged)\nB.x = 2 (new!)' if self.lang == 'en'
                        else 'A.x = 1（未变）\nB.x = 2（新！）',
                'output': '2',
                'explain': 'B.x = 2 creates NEW attribute in B, shadows A.x' if self.lang == 'en'
                          else 'B.x = 2 在 B 中创建新属性，遮蔽 A.x'
            },
            {
                'code': 'del B.x\nprint(b.x)',
                'state': 'A.x = 1 (still there)\nB.x (deleted)' if self.lang == 'en'
                        else 'A.x = 1（仍然存在）\nB.x（已删除）',
                'output': '1',
                'explain': 'del B.x removes B\'s attribute, reveals A.x again' if self.lang == 'en'
                          else 'del B.x 删除 B 的属性，再次显露 A.x'
            }
        ]
        
        for i, step in enumerate(steps, 1):
            print(f"\n{self.get_text('step')} {i}:")
            print(f"{self.get_text('code')}: {step['code']}")
            print(f"{self.get_text('state')}: {step['state']}")
            if step['output']:
                print(f"{self.get_text('output')}: {step['output']}")
            print(f"{self.get_text('explanation')}: {step['explain']}")
            input(self.get_text('press_enter'))
        
    def quiz_mode(self):
        """Quiz mode with multiple questions"""
        questions = [
            {
                'question': 'q1_question',
                'options': ['q1_a', 'q1_b', 'q1_c', 'q1_d'],
                'answer': 'q1_answer',
                'explain': 'q1_explain'
            },
            {
                'question': 'q2_question',
                'options': ['q2_a', 'q2_b', 'q2_c', 'q2_d'],
                'answer': 'q2_answer',
                'explain': 'q2_explain'
            },
            {
                'question': 'q3_question',
                'options': ['q3_a', 'q3_b', 'q3_c', 'q3_d'],
                'answer': 'q3_answer',
                'explain': 'q3_explain'
            }
        ]
        
        score = 0
        total = len(questions)
        
        self.clear_screen()
        print(self.get_text('quiz_title'))
        
        for i, q in enumerate(questions, 1):
            print(f"\n{self.get_text('question')} {i}/{total}:")
            print(self.get_text(q['question']))
            for opt in q['options']:
                print(self.get_text(opt))
            
            while True:
                answer = input(self.get_text('your_answer')).strip().upper()
                if answer in ['A', 'B', 'C', 'D']:
                    break
                print(self.get_text('invalid'))
            
            correct_answer = self.get_text(q['answer'])
            if answer == correct_answer:
                print(self.get_text('correct'))
                score += 1
            else:
                print(f"{self.get_text('incorrect')} {self.get_text('correct_answer')}: {correct_answer}")
            
            print(self.get_text(q['explain']))
            input(self.get_text('press_enter'))
        
        # Show final score
        print(f"\n{self.get_text('score')}: {score}/{total} ({score*100//total}%)")
        
        # Ask to retry
        retry = input(self.get_text('try_again')).strip().lower()
        if retry == 'y':
            self.quiz_mode()
    
    def run(self):
        """Main program loop"""
        self.select_language()
        
        while True:
            choice = self.show_main_menu()
            
            if choice == '1':
                self.learning_mode()
            elif choice == '2':
                self.quiz_mode()
            elif choice == '3':
                print('\nGoodbye! 再见！')
                break
            else:
                print(self.get_text('invalid'))
                input(self.get_text('press_enter'))


if __name__ == '__main__':
    quiz = InheritanceQuiz()
    quiz.run()