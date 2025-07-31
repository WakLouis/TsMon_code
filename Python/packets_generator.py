import pandas as pd
import numpy as np


def convert_flow_to_packet(input_file, output_file):
    # 读取输入文件
    try:
        df = pd.read_csv(input_file, sep=',', header=None)
    except:
        # 如果读取失败，尝试其他格式
        try:
            df = pd.read_excel(input_file)
        except:
            print("无法读取输入文件，请检查文件格式")
            return

    # 设置列名
    if len(df.columns) == 13:
        df.columns = ['src_ip', 'src_port', 'dst_ip', 'dst_port', 'protocol',
                      'duration', 'total_bytes', 'num_packets', 'timestamp', 'label', '', '', '']
    else:
        print(f"输入文件格式不正确，列数应为10，实际为{len(df.columns)}")
        return

    # 找到最小时间戳
    min_timestamp = df['timestamp'].min()

    # 创建输出数据框
    output_rows = []

    # 为五元组分配唯一ID
    flow_ids = {}
    current_id = 1

    # 处理每一行数据流
    for _, row in df.iterrows():
        print(_)
        # print(row)
        # flag = 0
        # for i in row:
        #     if i is None:
        #         flag = 1
        #         break
        #
        # if flag == 1:
        #     continue


        # 创建五元组键
        five_tuple = (row['src_ip'], row['src_port'], row['dst_ip'], row['dst_port'], row['protocol'])

        # 如果这个五元组是新的，分配一个ID
        if five_tuple not in flow_ids:
            flow_ids[five_tuple] = current_id
            current_id += 1

        key = flow_ids[five_tuple]
        try:
            num_packets = int(row['num_packets'])
            total_bytes = int(row['total_bytes'])
            duration = float(row['duration'])
            label = int(row['label'])
        except:
            print(key)
            print(row)
            print()
            continue

        # 计算每个包的字节数（均匀分配）
        bytes_per_packet = total_bytes // num_packets
        remaining_bytes = total_bytes % num_packets

        # 计算基础时间戳（以纳秒为单位，从1秒开始）
        base_timestamp = (float(row['timestamp']) - min_timestamp) * 1_000_000_000

        # 如果只有一个包
        if num_packets == 1:
            output_rows.append([key, total_bytes, int(base_timestamp), label])
        else:
            # 计算包之间的时间间隔（纳秒）
            time_interval = (duration * 1_000_000_000) / (num_packets - 1)

            # 添加所有包
            for i in range(num_packets):
                # 计算当前包的时间戳
                current_timestamp = base_timestamp + (i * time_interval)

                # 计算当前包的字节数（最后一个包可能会多一些字节）
                pkt_bytes = bytes_per_packet + (1 if i < remaining_bytes else 0)

                # 添加数据行
                output_rows.append([key, pkt_bytes, int(current_timestamp), label])

    # 创建输出数据框
    output_df = pd.DataFrame(output_rows, columns=['key', 'pkt_bytes', 'timeStamp', 'label'])
    output_df['timeStamp'] = output_df['timeStamp'].astype(str)

    # 保存到CSV文件
    output_df.to_csv(output_file, index=False)
    print(f"转换完成，结果已保存到 {output_file}")


# 使用示例
if __name__ == "__main__":
    input_file = "filtered_2.csv"  # 输入文件名
    output_file = "NB15_2.csv"  # 输出文件名
    convert_flow_to_packet(input_file, output_file)