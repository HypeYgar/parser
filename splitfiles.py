import os

def split_file(num_files):
    with open("kaif.txt", 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines_per_file = len(lines) // num_files
    remainder = len(lines) % num_files
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for i in range(num_files):
        output_subdir = os.path.join(output_dir, f'для_машины_{i+1}')
        if not os.path.exists(output_subdir):
            os.makedirs(output_subdir)
        start = i * lines_per_file + min(i, remainder)
        end = start + lines_per_file + (1 if i < remainder else 0)
        with open(os.path.join(output_subdir, 'kaif.txt'), 'w') as f:
            f.writelines(lines[start:end])

if __name__ == "__main__":
    num_files = int(input("Сколько машин?: "))
    split_file(num_files)
