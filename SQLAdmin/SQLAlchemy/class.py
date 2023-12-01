# ============================================================================================================
# - python的类没有访问控制，所以一般要的话用_[name]表示protected,__[name]表示private，但是还是可以访问的到
#
# - Type Hints 是 Python 3.5 版本引入的一项功能，它允许开发者在函数声明、类声明等地方提供类型信息。
# 这样可以为代码添加一些静态类型检查，并提供更好的文档。
# Type Hints 并不会影响运行时的行为，但可以被一些工具（如类型检查器、IDE）用于静态分析。
#
# - class不需要声明定义成员变量，直接self.[变量]就可以，比如直接在__init__的时候声明和定义
# ============================================================================================================
class Animal:
    name: str = "None"  # :str是类型标注(Type Hints)

    # 这里用于定义成员变量的默认值，实际上__init__中的默认参数也有同样的效果self.name=name

    def __init__(self, name) -> None:  # 构造函数  ->用于返回类型标注
        self.name = name

    def Shout(self, name=name, voice="Undefined Shout"):  # 方法定义
        print(f"{voice}")

    def Self_Introduction(self):
        print("I am a animal")

    def Polymorphism(self) -> None:  # 多态
        print("Polymorphism Animal")


class Dog(Animal):  # 继承用()表示基类
    voice: str = "Woof"

    def __init__(self, name, voice="Woof") -> None:
        super().__init__(name)  # super()表示调用的父类的方法，这里调用父类的构造函数
        self.voice = voice

    def Shout(self):
        return super().Shout(super().name, self.voice)

    def Self_Introduction(self):
        print(f"I am a {super().name}")

    def __repr__(self) -> str:  # 重写内置函数__repr__方法，用于打印对象时显示的字符串
        return self.name

    def Polymorphism(self) -> None:  # 多态
        print("Polymorphism Dog")


animal = Animal("Animal_Name")  # 实例化类的对象
dog = Dog("Goofy")

print(f"animal name = {animal.name}")
animal.Shout()  # 调用类的方法
dog.Shout()
animal.Self_Introduction()
print(dog)

# 多态只需要函数名一样就行，好像
animal.Polymorphism()
dog.Polymorphism()


