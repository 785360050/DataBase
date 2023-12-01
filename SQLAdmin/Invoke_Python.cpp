#include <iostream>
#include <fstream>

#include <python3.10/Python.h>

int main(int argc, char const *argv[])
{
    Py_Initialize(); // 初始化 Python 解释器

    /// ============================================================================================================
    /// 		直接执行 Python 代码
    /// ============================================================================================================
    PyRun_SimpleString("print('Executeing Python code directly')");

    /// ============================================================================================================
    /// 		执行 Python 文件
    /// ============================================================================================================
    FILE *file_descriptor = fopen("Show.py", "r");
    if (!file_descriptor)
    {
        std::cout<<strerror(errno)<<std::endl;
        return EXIT_FAILURE;
    }

    int result = PyRun_SimpleFile(file_descriptor, "Show.py");

    if (!result)   // 检查执行结果
        PyErr_Print(); // 打印错误信息

    Py_Finalize(); // 关闭 Python 解释器
    return EXIT_SUCCESS;
}
