import os
import argparse

# DVD标准物理容量字节（刻录标准）
DVD_CAP = {
    "dvd5": 4699979776,  # 单层4.7G
    "dvd9": 8543666176   # 双层8.5G
}

def fill_iso_to_dvd_size(input_iso: str, output_iso: str, target_bytes: int):
    # 获取原文件大小
    src_size = os.path.getsize(input_iso)
    if src_size > target_bytes:
        print(f"错误：原ISO {src_size/1024/1024/1024:.2f}GB 超过目标碟片 {target_bytes/1024/1024/1024:.2f}GB，无法填充！")
        return False
    if src_size == target_bytes:
        print("文件已等于DVD标准容量，无需处理")
        # 复制原文件
        with open(input_iso, "rb") as f_in, open(output_iso, "wb") as f_out:
            f_out.write(f_in.read())
        return True

    # 计算需要填充的空白字节
    pad_len = target_bytes - src_size
    print(f"原大小：{src_size/1024/1024/1024:.2f}GB，填充 {pad_len/1024/1024:.2f}GB 空白至标准碟片容量")

    # 读写+填充
    chunk_size = 1024 * 1024 * 10  # 10MB分块读写，防止大文件占满内存
    with open(input_iso, "rb") as f_in, open(output_iso, "wb") as f_out:
        # 复制原ISO全部内容
        while chunk := f_in.read(chunk_size):
            f_out.write(chunk)
        # 写入全0填充
        remaining = pad_len
        while remaining > 0:
            write_size = min(chunk_size, remaining)
            f_out.write(b"\x00" * write_size)
            remaining -= write_size
    print(f"完成！输出文件：{output_iso}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ISO仅填充空白到DVD5/DVD9容量，不裁剪文件")
    parser.add_argument("-i", "--input", required=True, help="输入原始ISO路径")
    parser.add_argument("-o", "--output", required=True, help="填充后输出ISO路径")
    parser.add_argument("-d", "--dvd", choices=["dvd5", "dvd9"], default="dvd5", help="dvd5单层 / dvd9双层")
    args = parser.parse_args()

    fill_iso_to_dvd_size(args.input, args.output, DVD_CAP[args.dvd])