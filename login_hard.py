# sophisticated login system

import getpass
import time
import sys
from typing import Dict, Optional

class LoginSystem:
    """A secure and user-friendly login system."""
    
    def __init__(self, max_attempts: int = 3):
        self.max_attempts = max_attempts
        # In production, this would come from a secure database
        self.users: Dict[str, str] = {
            'xq': '888888',
            'admin': 'admin123',
            'user1': 'password1'
        }
    
    def get_secure_input(self, prompt: str, hide_input: bool = False) -> str:
        """Get user input with optional password masking."""
        if hide_input:
            return getpass.getpass(prompt)
        return input(prompt).strip()
    
    def validate_credentials(self, username: str, password: str) -> bool:
        """Validate user credentials."""
        return username in self.users and self.users[username] == password
    
    def display_welcome_message(self) -> None:
        """Display a welcome message."""
        print("=" * 50)
        print("🔐 欢迎使用登录系统 | Welcome to Login System")
        print("=" * 50)
        print(f"您有 {self.max_attempts} 次登录机会")
        print()
    
    def display_login_success(self, username: str) -> None:
        """Display success message with animation."""
        print("\n✅ 登录验证中", end="")
        for _ in range(3):
            print(".", end="", flush=True)
            time.sleep(0.5)
        print(f"\n🎉 欢迎回来, {username}! 登录成功!")
        print("正在进入系统...")
        time.sleep(1)
        print("✨ 系统加载完成!")
    
    def display_failed_attempt(self, attempts_left: int) -> None:
        """Display failed attempt message."""
        if attempts_left > 0:
            print(f"❌ 用户名或密码不正确!")
            print(f"⚠️  您还有 {attempts_left} 次尝试机会")
            if attempts_left == 1:
                print("⚡ 最后一次机会，请仔细输入!")
            print("-" * 30)
        else:
            print("\n🚫 对不起，您已用完所有登录机会!")
            print("🔒 系统已锁定，请联系管理员或稍后再试")
    
    def get_user_choice(self) -> bool:
        """Ask user if they want to try again after failed attempts."""
        while True:
            choice = input("\n是否要重新开始? (y/n): ").strip().lower()
            if choice in ['y', 'yes', '是']:
                return True
            elif choice in ['n', 'no', '否']:
                return False
            else:
                print("请输入 'y' 或 'n'")
    
    def login(self) -> bool:
        """Main login process."""
        attempts = 0
        
        while attempts < self.max_attempts:
            try:
                print(f"\n📝 登录尝试 {attempts + 1}/{self.max_attempts}")
                
                # Get username
                username = self.get_secure_input("请输入用户名: ")
                if not username:
                    print("⚠️  用户名不能为空!")
                    attempts += 1
                    continue
                
                # Get password (hidden input)
                password = self.get_secure_input("请输入密码: ", hide_input=True)
                if not password:
                    print("⚠️  密码不能为空!")
                    attempts += 1
                    continue
                
                # Validate credentials
                if self.validate_credentials(username, password):
                    self.display_login_success(username)
                    return True
                else:
                    attempts += 1
                    attempts_left = self.max_attempts - attempts
                    self.display_failed_attempt(attempts_left)
                    
            except KeyboardInterrupt:
                print("\n\n👋 用户取消登录，再见!")
                return False
            except Exception as e:
                print(f"\n❌ 系统错误: {e}")
                return False
        
        return False
    
    def run(self) -> None:
        """Run the complete login system."""
        while True:
            self.display_welcome_message()
            
            if self.login():
                print("\n🎯 登录流程完成!")
                break
            else:
                if not self.get_user_choice():
                    print("\n👋 感谢使用，再见!")
                    break
                print("\n🔄 重新开始登录流程...\n")

def main():
    """Main function to run the login system."""
    try:
        login_system = LoginSystem(max_attempts=3)
        login_system.run()
    except Exception as e:
        print(f"系统启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()