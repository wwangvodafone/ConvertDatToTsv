import os
import argparse
import shutil


def read_rulesim():
    rulesim_file = "./conf/rule.frm"
    with open(rulesim_file, "r", encoding='utf-8') as f:
        lines = f.readlines()
    line_arr = [line for line in lines if line[0] != '#' if line[0] != '@']
    colspecs = [(line.split()[1], line.split()[2]) for line in line_arr]

    return colspecs

def process_datData(path, file, result_folder, colspecs):
    file_main = file[:-4]
    file_converted = file_main + ('.tsv')
    encoding = 'cp932'
    file_converted = os.path.join(result_folder, file_converted)
    with open(file_converted, mode="a", encoding='cp932') as fw:
        with open(path, mode="r", encoding="cp932") as f:
            for line in f:
                line = line.rstrip('\r\n')
                line = line.replace('\t', ' ')
                line = line.encode(encoding)
                line_arr = [line[int(start):int(start)+int(length)].decode(encoding)+'\t' for start,length in colspecs]
                fw.write(''.join(line_arr).rstrip('\t'))
                fw.write('\n')

    return file_converted


def start_process_local_nocompress(source_folder, dest_folder, path_converted):
    result_folder = path_converted
    file_count = 1
    colspecs = read_rulesim()
    file_list = [name for name in os.listdir(source_folder) if name.endswith('.dat')]
    for idx, filename in enumerate(file_list):
        file_full_path = os.path.join(source_folder, filename)
        if filename.endswith('dat'):
            converted_file = process_datData(file_full_path, filename, result_folder, colspecs)
            file_count += 1
            converted_basename = os.path.basename(converted_file)
            converted_file_path = os.path.join(dest_folder, converted_basename)
            shutil.move(converted_file, converted_file_path)

def get_args():
    parser = argparse.ArgumentParser(description='This is a tool for feature processing.')
    parser.add_argument("--path_tmp", type=str, help="temp folder", required=True)
    parser.add_argument("--source_folder", type=str, help="dat files folder", default=None)
    parser.add_argument("--dest_folder", type=str, help="tsv files folder", default=None)

    return parser.parse_args()


def main(run_py_file):
    args = get_args()
    path_tmp = args.path_tmp
    source_folder = args.source_folder
    dest_folder = args.dest_folder
    path_converted = os.path.join(path_tmp, "converted")
    os.makedirs(path_converted, exist_ok=True)

    assert os.path.exists(path_tmp)

    start_process_local_nocompress(source_folder, dest_folder, path_converted)

