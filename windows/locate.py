#Code by Sergio00166

from concurrent.futures import ProcessPoolExecutor, as_completed
from os import scandir, sep, cpu_count
from os.path import isdir, join, normpath, basename, isabs, relpath
import re
from time import perf_counter
from colors import color
from syntax import parse_basic_syntax
from functools import partial


def fast_scandir(path):
    dirs = []
    files = []
    with scandir(path) as it:
        for entry in it:
            if entry.is_dir(follow_symlinks=False):
                dirs.append(entry.path)
            files.append(entry.path)
    return dirs, files

def parallel_walk(root, executors):
    all_files = []
    current_dirs = [root]
    level = 0
    
    with ProcessPoolExecutor(max_workers=executors) as pool:
        while current_dirs:
            futures = {}
            batch_size = max(1, len(current_dirs) // (executors * 2))
            
            for i in range(0, len(current_dirs), batch_size):
                batch = current_dirs[i:i + batch_size]
                future = pool.submit(process_batch, batch)
                futures[future] = batch
            
            current_dirs = []
            for future in as_completed(futures):
                batch_result = future.result()
                all_files.extend(batch_result['files'])
                current_dirs.extend(batch_result['dirs'])
                level += 1
                
    return all_files


def process_batch(dirs):
    result = {'files': [], 'dirs': []}
    for d in dirs:
        try:
            dirs, files = fast_scandir(d)
            result['files'].extend(files)
            result['dirs'].extend(dirs)
        except Exception:
            continue
    return result


def locate(pattern, root, recursive=True, executors=None):
    executors = executors or cpu_count()
    root = normpath(root)
    all_files = [root] if isdir(root) else []
    
    if recursive:
        all_files = parallel_walk(root, executors)
    
    return filter_files(all_files, pattern, executors)


def filter_files(files, pattern, executors):
    regex = re.compile(pattern)
    chunk_size = max(1000, len(files) // (executors * 10))
    matches = []
    
    with ProcessPoolExecutor(max_workers=executors) as pool:
        futures = [pool.submit(match_chunk, chunk, regex) 
                 for chunk in chunks(files, chunk_size)]
        
        for future in as_completed(futures):
            matches.extend(future.result())
    
    return matches


def match_chunk(chunk, regex):
    return [f for f in chunk if regex.search(basename(f))]


def chunks(lst, n):
    for i in range(0, len(lst), n): yield lst[i:i + n]


def main(arg, arg1, directory):
    try:
        start_time = perf_counter()
        buff2, buff = parse_basic_syntax(arg1, directory, "in")
        root = normpath(join(directory, buff[0]))
        
        results = []
        for pattern in buff2:
            t1 = perf_counter()
            found = locate(pattern, root, recursive=(arg != "locatenr"))
            dt = perf_counter() - t1
            results.append((pattern, found, dt))
        
        print_results(results, root, perf_counter() - start_time)
        
    except Exception as e:
        print(color(f"\nERROR: {str(e)}\n", "R"))


def print_results(results, root, total_time):
    reset = color()
    col_g,col_m = color("", "Gnr"),color("", "Mnr")
    col_y,col_b = color("", "Ynr"),color("", "Bnr")
    col_r,col_c = color("", "Rnr"), color("", "Cnr")
    print("")
    for pattern, found, dt in results:
        print(f"{col_g}┌─[ {col_m}{pattern}{col_g} ]\n│{reset}")
        for path in found: print(f"{col_g}│  {col_b}{path}{reset}")
    print(f"{col_g}│\n└─ {len(found)} results {col_y}({dt:.3f}s){reset}\n")

