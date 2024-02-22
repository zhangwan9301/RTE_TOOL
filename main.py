import os
import glob
import generate
if __name__ == '__main__':
    '''
    1.创建txt文件
    2.填写示例   类型 + 名称 + 元素个数
        uint16* GcAPC_FLBSWRippleCurrentArray_mA    10
        uint16  GbAPC_FLWindowCurrentNumCnt_n   1
        uint8   GbAPC_FLCurrentNumClearCnt_flg  1
    '''
    # 获取当前文件夹路径
    folder_path = os.getcwd()
    # 使用glob模块匹配所有txt文件
    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
    # 提取文件名（去掉后缀）
    file_names = [os.path.splitext(os.path.basename(file))[0] for file in txt_files]
    # 打印文件名
    for name in file_names:
        generate.generate_Module(name)
        print(f'{name} generate ok!\n')
    input("按下回车键退出...")
    
    
