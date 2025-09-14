i = 1

while i <= 3:
    user_name = input('请输入用户名: ')
    pwd = input('请输入密码: ')
    
    if user_name == 'xq' and pwd == '888888':
        print('正在登录中!')
        break  # Exit the loop on successful login
    else:
        if i < 3:  # Still have attempts left
            print(f'用户名或密码不正确。你还有{3-i}次机会。')
        i += 1

# Check if all attempts were exhausted
if i > 3:
    print('对不起，三次均输入错误!')