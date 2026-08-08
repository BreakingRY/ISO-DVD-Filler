import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

# DVD标准容量字节
DVD_CAP = {
    "DVD5 (单层 4.7G)": 4699979776,
    "DVD9 (双层 8.5G)": 8543666176
}

def format_size(byte_num):
    """字节转GB显示"""
    gb = byte_num / 1024 / 1024 / 1024
    return f"{gb:.2f} GB"

class IsoFillGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ISO镜像DVD容量填充工具")
        self.root.geometry("580x420")
        self.root.resizable(False, False)

        # 变量存储
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.dvd_type = tk.StringVar(value=list(DVD_CAP.keys())[0])
        self.status_text = tk.StringVar(value="就绪，请选择ISO文件")

        self.build_ui()

    def build_ui(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. 输入ISO文件选择
        frame_in = ttk.Frame(main_frame)
        frame_in.pack(fill=tk.X, pady=6)
        ttk.Label(frame_in, text="源ISO文件:    ").pack(side=tk.LEFT)
        ttk.Entry(frame_in, textvariable=self.input_path, width=40).pack(side=tk.LEFT, padx=8)
        ttk.Button(frame_in, text="浏览", command=self.select_input).pack(side=tk.LEFT)

        # 2. 输出保存路径
        frame_out = ttk.Frame(main_frame)
        frame_out.pack(fill=tk.X, pady=6)
        ttk.Label(frame_out, text="输出ISO文件: ").pack(side=tk.LEFT)
        ttk.Entry(frame_out, textvariable=self.output_path, width=40).pack(side=tk.LEFT, padx=8)
        ttk.Button(frame_out, text="另存为", command=self.select_output).pack(side=tk.LEFT)

        # 3. DVD规格选择
        frame_dvd = ttk.Frame(main_frame)
        frame_dvd.pack(fill=tk.X, pady=12)
        ttk.Label(frame_dvd, text="碟片规格:      ").pack(side=tk.LEFT)
        combo = ttk.Combobox(frame_dvd, textvariable=self.dvd_type, state="readonly")
        combo["values"] = list(DVD_CAP.keys())
        combo.pack(side=tk.LEFT, padx=8)
        combo.bind("<<ComboboxSelected>>", self.update_size_info)

        # 容量信息展示卡片
        info_frame = ttk.LabelFrame(main_frame, text="容量信息", padding=12)
        info_frame.pack(fill=tk.X, pady=10)
        self.info_label = ttk.Label(info_frame, text="未选择ISO，无容量数据")
        self.info_label.pack()

        # 进度与状态
        ttk.Label(main_frame, textvariable=self.status_text, foreground="#2255bb").pack(pady=10)
        self.progress = ttk.Progressbar(main_frame, length=500, mode="determinate")
        self.progress.pack()

        # 操作按钮（只剩开始填充和清空全部）
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        self.run_btn = ttk.Button(btn_frame, text="开始填充", command=self.start_fill_task)
        self.run_btn.grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="清空全部", command=self.clear_all).grid(row=0, column=1, padx=10)

    def select_input(self):
        path = filedialog.askopenfilename(filetypes=[("ISO镜像", "*.iso"), ("全部文件", "*.*")])
        if path:
            self.input_path.set(path)
            self.update_size_info()

    def select_output(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".iso",
            filetypes=[("ISO镜像", "*.iso")]
        )
        if path:
            self.output_path.set(path)

    def update_size_info(self, event=None):
        in_path = self.input_path.get()
        dvd_name = self.dvd_type.get()
        target_bytes = DVD_CAP[dvd_name]

        if not os.path.exists(in_path):
            self.info_label.config(text="请先选择有效的ISO源文件", foreground="#333333")
            return
        src_size = os.path.getsize(in_path)
        src_gb = format_size(src_size)
        target_gb = format_size(target_bytes)

        if src_size > target_bytes:
            tip = f"警告：源ISO {src_gb} 超过碟片上限 {target_gb}，无法填充！"
            self.info_label.config(text=tip, foreground="#dd2222")
        elif src_size == target_bytes:
            tip = f"源ISO {src_gb} = 碟片容量 {target_gb}，无需填充"
            self.info_label.config(text=tip, foreground="#227722")
        else:
            pad_need = target_bytes - src_size
            pad_gb = format_size(pad_need)
            tip = f"源文件：{src_gb} | 目标碟片：{target_gb} | 需要填充空白：{pad_gb}"
            self.info_label.config(text=tip, foreground="#2255bb")

    def clear_all(self):
        self.input_path.set("")
        self.output_path.set("")
        self.dvd_type.set(list(DVD_CAP.keys())[0])
        self.info_label.config(text="未选择ISO，无容量数据", foreground="#333333")
        self.status_text.set("就绪，请选择ISO文件")
        self.progress["value"] = 0

    def fill_iso_logic(self):
        """填充核心逻辑"""
        in_path = self.input_path.get()
        out_path = self.output_path.get()
        dvd_name = self.dvd_type.get()
        target_bytes = DVD_CAP[dvd_name]
        chunk_size = 10 * 1024 * 1024

        src_size = os.path.getsize(in_path)
        if src_size > target_bytes:
            self.root.after(0, lambda: messagebox.showerror("错误", "源ISO大于碟片容量，禁止填充"))
            self.root.after(0, lambda: self.status_text.set("填充失败：文件超限"))
            self.run_btn.config(state="normal")
            return

        if src_size == target_bytes:
            self.status_text.set("正在复制原文件...")
            with open(in_path, "rb") as fi, open(out_path, "wb") as fo:
                fo.write(fi.read())
            self.root.after(0, lambda: messagebox.showinfo("完成", "文件容量匹配，已复制完成"))
            self.root.after(0, lambda: self.status_text.set("操作完成"))
            self.run_btn.config(state="normal")
            return

        pad_len = target_bytes - src_size
        total_work = src_size + pad_len
        written = 0

        self.status_text.set("正在复制原ISO数据...")
        with open(in_path, "rb") as fi, open(out_path, "wb") as fo:
            while chunk := fi.read(chunk_size):
                fo.write(chunk)
                written += len(chunk)
                percent = int((written / total_work) * 100)
                self.root.after(0, lambda p=percent: self.progress.config(value=p))

            self.status_text.set("正在填充空白数据...")
            remaining = pad_len
            while remaining > 0:
                write_len = min(chunk_size, remaining)
                fo.write(b"\x00" * write_len)
                written += write_len
                percent = int((written / total_work) * 100)
                self.root.after(0, lambda p=percent: self.progress.config(value=p))
                remaining -= write_len

        self.root.after(0, lambda: messagebox.showinfo("填充完成", f"ISO已填充至{dvd_name}标准容量！"))
        self.root.after(0, lambda: self.status_text.set("填充任务全部完成"))
        self.run_btn.config(state="normal")

    def start_fill_task(self):
        in_path = self.input_path.get()
        out_path = self.output_path.get()
        if not in_path or not os.path.exists(in_path):
            messagebox.showwarning("提示", "请选择有效的源ISO文件")
            return
        if not out_path:
            messagebox.showwarning("提示", "请设置输出保存路径")
            return

        self.run_btn.config(state="disabled")
        self.status_text.set("开始处理，请勿关闭窗口...")
        work_thread = threading.Thread(target=self.fill_iso_logic, daemon=True)
        work_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = IsoFillGUI(root)
    root.mainloop()