import compileall
import os
import shutil

# main.cpython-37.pyc　-> main.pyc
replace_str='cpython-37.pyc'

def move_pyc(path, file_path):
    for file in os.listdir(file_path):
        son_file_path = os.path.join(file_path, file)
        new_file_path = os.path.join(path, file.replace(f'{replace_str}', 'pyc'))
        shutil.move(son_file_path, new_file_path)


def remove_py(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if file.endswith('.py'):
            os.remove(file_path)
        elif file == '__pycache__':
            move_pyc(path, file_path)
            shutil.rmtree(file_path)
        elif os.path.isdir(file_path):
            remove_py(file_path)


if __name__ == '__main__':
    dir_name = input(r'输入要处理的目录:')
    path = os.path.join(os.getcwd(), dir_name)
    compileall.compile_dir(path)
    remove_py(path)
