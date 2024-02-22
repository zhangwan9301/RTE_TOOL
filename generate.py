import os
import shutil

def generate_rte_Module(module_name):
    '''
    自动生成TRE接口
    module_name：模块名称，用"_"来对名称分段
    input_file：入口文件名称
    '''
    input_file = module_name + '.txt'
    with open(input_file, 'r') as file:
        lines = file.readlines()
    header_file = 'RTE_' + module_name.title() + '.h'
    source_file = 'RTE_' + module_name.title() + '.c'
    MODULE_NAME = module_name.upper()
    Module_Name = ''.join(word.capitalize() for word in module_name.split('_'))
    with open(header_file, 'w') as header:
        header.write(f'#ifndef __RTE_{MODULE_NAME}_H\n')
        header.write(f'#define __RTE_{MODULE_NAME}_H\n\n')
        with open(source_file, 'w') as source:
            
            # 声明头文件
            header.write(f'#include "Platform_info.h"\n')
            header.write(f'#include "Platform_Types.h"\n')
            header.write(f'#include "string.h"\n\n\n\n')
            
            source.write(f'#include "{header_file}"\n\n\n\n')
            # 变量定义
            for line in lines:
                line = line.strip()
                if line:
                    parts = line.split()
                    var_type = parts[0]
                    var_name = parts[1]
                    if len(parts) == 3 and var_type[-1] == "*":
                        var_len  = parts[2]
                        source.write(f'{var_type} {var_name}[{var_len}] = {{0}};\n')
                    elif len(parts) == 2 or len(parts) == 3:
                        source.write(f'{var_type} {var_name} = 0;\n')
            source.write('\n\n\n\n\n\n')

            # 变量声明
            for line in lines:
                line = line.strip()
                if line:
                    parts = line.split()
                    var_type = parts[0]
                    var_name = parts[1]
                    if len(parts) == 3 and var_type[-1] == "*":
                        var_len  = parts[2]
                        header.write(f'extern {var_type} {var_name}[{var_len}];\n')
                    elif len(parts) == 2 or len(parts) == 3:
                        header.write(f'extern {var_type} {var_name};\n')
            header.write('\n\n\n\n\n\n')
            # 变量方法
            for line in lines:
                line = line.strip()
                if line:
                    parts = line.split()
                    var_type = parts[0]
                    var_name = parts[1]
                    if len(parts) == 3 and var_type[-1] == "*":
                        # Generate set function declaration
                        set_func_name = ''.join(word.capitalize() for word in var_name.split('_'))
                        header.write(f'extern void RTE_{Module_Name}_Set_{set_func_name}({var_type} buff, uint8 len);\n')
                        # Generate get function declaration
                        get_func_name = ''.join(word.capitalize() for word in var_name.split('_'))
                        header.write(f'extern void RTE_{Module_Name}_Get_{get_func_name}({var_type} buff, uint8 len);\n\n')

                        unit_type = var_type.rstrip("*")
                        # Generate set function definition
                        source.write(f'void RTE_{Module_Name}_Set_{set_func_name}({var_type} buff, uint8 len)\n')
                        source.write('{\n')
                        source.write(f'    memcpy({var_name}, buff, sizeof({var_name}) < len*sizeof({unit_type}) ? sizeof({var_name}) : len*sizeof({unit_type}));\n')
                        source.write('}\n\n')
                        # Generate get function definition
                        source.write(f'void RTE_{Module_Name}_Get_{get_func_name}({var_type} buff, uint8 len)\n')
                        source.write('{\n')
                        source.write(f'    memcpy(buff, {var_name}, sizeof({var_name}) < len*sizeof({unit_type}) ? sizeof({var_name}) : len*sizeof({unit_type}));\n')
                        source.write(f'    return;\n')
                        source.write('}\n\n')    
                    
                    elif len(parts) == 2 or len(parts) == 3:
                        
                        # Generate set function declaration
                        set_func_name = ''.join(word.capitalize() for word in var_name.split('_'))
                        header.write(f'extern void RTE_{Module_Name}_Set_{set_func_name}({var_type} value);\n')
                        # Generate get function declaration
                        get_func_name = ''.join(word.capitalize() for word in var_name.split('_'))
                        header.write(f'extern {var_type} RTE_{Module_Name}_Get_{get_func_name}(void);\n\n')
                        # Generate set function definition
                        source.write(f'void RTE_{Module_Name}_Set_{set_func_name}({var_type} value)\n')
                        source.write('{\n')
                        source.write(f'    {var_name} = value;\n')
                        source.write('}\n\n')
                        # Generate get function definition
                        source.write(f'{var_type} RTE_{Module_Name}_Get_{get_func_name}(void)\n')
                        source.write('{\n')
                        source.write(f'    return {var_name};\n')
                        source.write('}\n\n')
        header.write('\n\n\n#endif')

def generate_plugin_Module(module_name):
    header_file = 'Plugin_' + module_name.title() + '.h'
    source_file = 'Plugin_' + module_name.title() + '.c'
    MODULE_NAME = module_name.upper()
    Module_Name = ''.join(word.capitalize() for word in module_name.split('_'))
    with open(header_file, 'w') as header:
        header.write(f'#ifndef __PLUGIN_{MODULE_NAME}_H\n')
        header.write(f'#define __PLUGIN_{MODULE_NAME}_H\n\n')
        header.write(f'#include "Platform_info.h"\n')
        header.write(f'#include "Platform_Types.h"\n')
        header.write(f'#include "string.h"\n')
        header.write(f'#include "stdio.h"\n')
        header.write(f'#include "RTE_{module_name}.h"\n\n\n\n')
        header.write(f'extern void Plugin_{Module_Name}_Init(void);\n\n\n')
        header.write('\n\n\n#endif')
    with open(source_file, 'w') as source:
        source.write(f'#include "Plugin_{module_name}.h"\n\n\n\n')
        source.write(f'void Plugin_{Module_Name}_Init(void)\n')
        source.write('{\n')
        source.write(f'    return;\n')
        source.write('}\n\n')

def generate_Module(obj_name):
    obj_name = obj_name.title()
    # 检查文件夹是否存在
    if os.path.exists(obj_name):
        # 如果文件夹已存在，则删除文件夹及其内容
        shutil.rmtree(obj_name)
    # 创建文件夹
    os.makedirs(obj_name, exist_ok=True)
    generate_rte_Module(obj_name)
    generate_plugin_Module(obj_name)
    # 获取当前目录下的所有文件
    files = os.listdir()
    # 遍历所有文件
    for file in files:
        # 检查文件扩展名是否为 .c 或 .h
        if file.endswith(".c") or file.endswith(".h"):
            # 移动文件到 abc 文件夹
            shutil.move(file, os.path.join(obj_name, file))
