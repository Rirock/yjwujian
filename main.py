import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# 游戏路径
path = r"D:\steam\steamapps\common\NARAKA BLADEPOINT\StartGame.exe"
path_audio = "NarakaBladepoint_Data\StreamingAssets\Audio\GeneratedSoundBanks\Windows"

# 角色列表
role_names_zh = ['宁红夜', '特木尔', '迦南', '季沧海', '胡桃', '天海', '妖刀姬', '崔三娘', '岳山', '无尘', '顾清寒', '武田', '殷紫萍', '沈妙', '胡为', '季莹莹', '悟空', '杨戬', '紫霞']
role_names = ['viper', 'temulch', 'matari', 'tarka', 'kurumi', 'tenkai', 'yotohime', 'valda', 'yueshan', 'wuchen', 'justinagu', 'takeda', 'zipingyin', 'feria', 'akos', 'zai', 'wukong', 'yangjian', 'zixia']


folder_zh = "Chinese(CN)"
folder_zh_backup = "Chinese(CN)_backup"
folder_jp = "Japanese(JP)"



class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.game_path = tk.StringVar()
        self.game_path.set(path)
        self.get_audio_path()
        
        self.checkbox_vars = []
        self.pack()
        self.createWidget()

    def createWidget(self):
        """布局"""
        self.label_title = tk.Label(self, text="汉语->日语")
        self.label_title.grid(row=0, column=0, columnspan=4)

        self.label01 = tk.Label(self, text="游戏文件路径")
        self.label01.grid(row=1, column=0)

        self.entry01 = tk.Entry(self, textvariable=self.game_path, width=50)
        self.entry01.grid(row=1, column=1)

        self.btn01 = tk.Button(self, text='选择', width=8,
                  command = self.pathCallBack)
        self.btn01.grid(row=1, column=2)


        self.label02 = tk.Label(self, text="选择到永劫无间游戏启动程序StartGame.exe的路径下")
        self.label02.grid(row=2, column=1)
        
        # 分隔布局容器
        checkbox_container = tk.Frame(self)
        checkbox_container.grid(row=3, column=0, columnspan=3)

        row_counter = 0
        col_counter = 0
        for role in role_names_zh:
            var = tk.IntVar()
            checkbox = tk.Checkbutton(checkbox_container, text=role, variable=var)
            checkbox.grid(row=row_counter, column=col_counter, sticky="w")
            self.checkbox_vars.append(var)

            col_counter += 1
            if col_counter == 4:
                col_counter = 0
                row_counter += 1

        row_counter += 1        
        self.select_all_var = tk.IntVar()
        select_all_checkbox = tk.Checkbutton(checkbox_container, text="全选", variable=self.select_all_var, command=self.toggle_select_all)
        select_all_checkbox.grid(row=row_counter, column=0, sticky="w")

        row_counter += 1
        self.label_suffix = tk.Label(self, text="Design by LJY.", font=('Times', 8,'italic') )
        self.label_suffix.grid(row=row_counter, column=0, columnspan=2, sticky=tk.SW)
        button = tk.Button(self, text="修改", width=8, command=self.replace_audio)
        button.grid(row=row_counter, column=0, columnspan=4)

        button = tk.Button(self, text="还原中文", width=8, command=self.restore_backup)
        button.grid(row=row_counter, column=2)


    def toggle_select_all(self):
        select_all_state = self.select_all_var.get()
        for var in self.checkbox_vars:
            var.set(select_all_state)

    def get_audio_path(self):
        game_path = self.game_path.get()
        self.audio_path = os.path.join(os.path.split(game_path)[0], path_audio)
    
    def replace_audio(self):
        self.update_path()
        selected_roles = [role_names_zh[i] for i, var in enumerate(self.checkbox_vars) if var.get() == 1]
        print("选中的角色：", selected_roles)

        # 获取角色编号
        list_replace = []
        for role_name in selected_roles:
            list_replace.append(role_names_zh.index(role_name))

        file_names = os.listdir(self.path_jp)

        # 替换为日语
        for i_replace in list_replace:
            role_name = role_names[i_replace]

            files_replace = [file_name for file_name in file_names if role_name in file_name]
            for file_replace in files_replace:
                shutil.copyfile(os.path.join(self.path_jp, file_replace), \
                                os.path.join(self.path_zh, file_replace))

        messagebox.showinfo(title='完成', message='游戏语音替换完成')
    
    def pathCallBack(self):
        # 选择游戏路径
        game_path1 = filedialog.askopenfilename()
        if(game_path1 != ''):
            self.game_path.set(game_path1)
        self.update_path()

    def update_path(self):
        self.get_audio_path()
        if not os.path.exists(self.audio_path):
            messagebox.showinfo(title='Error', message='游戏路径错误，请重新选择')

        # 更新备份
        self.path_zh = os.path.join(self.audio_path, folder_zh)
        self.path_zh_backup = os.path.join(self.audio_path, folder_zh_backup)
        self.path_jp = os.path.join(self.audio_path, folder_jp)
        self.update_backup()

    def update_backup(self):
        # 备份中文文件
        if not os.path.exists(self.path_zh_backup):
            shutil.copytree(self.path_zh, self.path_zh_backup)
        else:  # 更新备份
            new_files = os.listdir(self.path_zh)
            old_files = os.listdir(self.path_zh_backup)
            for new_file in new_files:
                if not new_file in old_files:
                    shutil.copyfile(os.path.join(self.path_zh, new_file), \
                                    os.path.join(self.path_zh_backup, new_file))
        
    def restore_backup(self):
        # 还原中文备份
        self.update_path()
        if os.path.exists(self.path_zh_backup):
            shutil.rmtree(self.path_zh)
            os.rename(self.path_zh_backup, self.path_zh)
        self.update_backup()
        messagebox.showinfo(title='完成', message='游戏语音已转换为中文')

if __name__ == "__main__":
    import ctypes
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        ctypes.windll.kernel32.CloseHandle(whnd)
    root = tk.Tk()
    root.title('永劫无间角色语音修改')
    root.geometry("650x320+200+200")
    app = Application(master=root)
    root.mainloop()


root.mainloop()
