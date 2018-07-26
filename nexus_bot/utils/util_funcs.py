
def convert_to_mb(file_size):
    size = float(file_size[:-2])
    metric = file_size[-2:]

    if metric == 'GB':
        size *= 1024
    elif metric == 'KB':
        size /= 1024

    return size
