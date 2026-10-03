import os
import subprocess
import re
import glob
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from generate_matrix import generate_and_save_matrices
from verify import verify_results

SIZES = [200, 400, 800, 1200, 1600, 2000]
THREADS = [1, 2, 4, 8]

CPP_SOURCE = "src/main.cpp"
CPP_BINARY = "main_app.exe"

def parse_info_txt(info_path="output/info.txt"):
    time_sec = 0.0
    if os.path.exists(info_path):
        with open(info_path, "r", encoding="utf-8") as f:
            for line in f:
                if "Execution time:" in line:
                    time_sec = float(line.split(": ")[1].split()[0])
    return time_sec

def main():
    print("Автоматический поиск окружения MSVC...")
    vcvars_search = "C:/Program Files/Microsoft Visual Studio/**/vcvars64.bat"
    found_vcvars = glob.glob(vcvars_search, recursive=True)
    if not found_vcvars:
        vcvars_search_alt = "C:/Program Files/Microsoft Visual Studio/**/vcvarsall.bat"
        found_vcvars = glob.glob(vcvars_search_alt, recursive=True)
        
    if not found_vcvars:
        print("Ошибка: Компоненты сборки Visual Studio не найдены.")
        return

    vc_bat = os.path.abspath(found_vcvars[0])
    print("Компиляция C++ кода с поддержкой OpenMP (/openmp)...")
    
    compile_cmd = f'"{vc_bat}" amd64 && cl.exe /EHsc /O2 /openmp /fp:precise "{CPP_SOURCE}" /Fe:"{CPP_BINARY}"'
    result = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("Ошибка компиляции:", result.stderr)
        return
        
    if os.path.exists("main.obj"): os.remove("main.obj")

    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    output_log_path = "output/experiments.txt"
    with open(output_log_path, "w", encoding="utf-8") as f:
        f.write("Размер | Потоки | Время (сек) | Ускорение | Эффективность\n")
        f.write("-" * 70 + "\n")

    print(f"\n{'Размер':<8} | {'Потоки':<6} | {'Время (сек)':<12} | {'Ускорение':<10} | {'Эффективность':<12} | {'Статус':<8}")
    print("-" * 75)

    for size in SIZES:
        generate_and_save_matrices(size, base_path="input")
        t1_time = 1.0 
        
        for t in THREADS:
            binary_path = os.path.abspath(CPP_BINARY)
            subprocess.run([binary_path, str(size), str(t)], cwd=".", check=True, capture_output=True)
            
            time_sec = parse_info_txt()
            if t == 1:
                t1_time = time_sec if time_sec > 0 else 1.0

            speedup = t1_time / time_sec if time_sec > 0 else 1.0
            efficiency = (speedup / t) * 100.0
            
            is_valid, max_error = verify_results(input_dir="input", output_dir="output")
            status = "PASS" if is_valid else "FAIL"
            
            print(f"{size:<8} | {t:<6} | {time_sec:<12.4f} | {speedup:<10.2f} | {efficiency:.1f}% | {status:<8}")
            
            with open(output_log_path, "a", encoding="utf-8") as f:
                f.write(f"{size} | {t} | {time_sec:.4f} | {speedup:.2f} | {efficiency:.1f}%\n")
        print("-" * 75)
        
    print("\nВсе эксперименты успешно завершены!")

if __name__ == "__main__":
    main()
