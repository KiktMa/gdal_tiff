import re

def remove_usemtl_lines(input_path, output_path):
    with open(input_path, 'r') as infile:
        lines = infile.readlines()

    # 使用正则表达式删除包含'usemtl'的行
    lines_without_usemtl = [line for line in lines if not re.match(r'usemtl', line)]

    with open(output_path, 'w') as outfile:
        outfile.writelines(lines_without_usemtl)

if __name__ == "__main__":
    input_file_path = r"C:\Users\mj\Desktop\Merged mesh.obj"
    output_file_path = r"C:\Users\mj\Desktop\mesh.obj"

    remove_usemtl_lines(input_file_path, output_file_path)
