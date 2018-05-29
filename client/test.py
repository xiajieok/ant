user_status = False  # 用户登录了就把这个改成True


def login(func):
    def inner():
        _username = "alex"  # 假装这是DB里存的用户信息
        _password = "abc!23"  # 假装这是DB里存的用户信息
        global user_status

        if user_status == False:
            username = input("user:")
            password = input("pasword:")

            if username == _username and password == _password:
                print("welcome login....")
                user_status = True
            else:
                print("wrong username or password!")
        if user_status == True:
            func()

    return inner


def home():
    print("---首页----")


@login
def america():
    # login() #执行前加上验证
    print("----欧美专区----")


def japan():
    print("----日韩专区----")


def henan():
    # login() #执行前加上验证
    print("----河南专区----")
america()