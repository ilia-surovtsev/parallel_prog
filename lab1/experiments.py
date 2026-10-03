import os
import subprocess
import time
import csv
import glob
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from generate_matrix import generate_and_save_matrices
from verify import verify_results

SIZES = [200, 400, 800, 1200, 1600, 2000]
CPP_SOURCE = "src/main.cpp"
CPP_BINARY = "main_app.exe"

def parse_info_txt(info_path="output/info.txt"):
    time_sec, volume_elements = 0.0, 0
    if os.path.exists(info_path):
        with open(info_path, "r", encoding="utf-8") as f:
            for line in f:
                if "Execution time:" in line:
                    time_sec = float(line.split(": ")[1].split()[0])
                elif "Task volume (Data):" in line:
                    volume_elements = int(line.split(": ")[1].split()[0])
    return time_sec, volume_elements


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
    print(f"Найдено окружение сборки: {vc_bat}")
    print("Компиляция C++ кода с оптимизацией /O2 во временном окружении...")
    
    compile_cmd = f'"{vc_bat}" amd64 && cl.exe /EHsc /O2 /fp:precise "{CPP_SOURCE}" /Fe:"{CPP_BINARY}"'
    result = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Ошибка компиляции:")
        print(result.stderr)
        return
        
    print("Компиляция успешно завершена! Создан файл lab1/main_app.exe")
    if os.path.exists("main.obj"): os.remove("main.obj")

    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    results = []
    print(f"\n{'Размер':<8} | {'Время (сек)':<12} | {'Объём задачи':<15} | {'Макс. Ошибка':<15} | {'Статус':<8}")
    print("-" * 75)

    for size in SIZES:
        generate_and_save_matrices(size, base_path="input")
        
        binary_path = os.path.abspath(CPP_BINARY)
        subprocess.run([binary_path], cwd=".", check=True, capture_output=True)
        
        is_valid, max_error = verify_results(input_dir="input", output_dir="output")
        time_sec, vol_elem = parse_info_txt()
        status = "PASS" if is_valid else "FAIL"
        
        print(f"{size:<8} | {time_sec:<12.4f} | {size ** 3:<15} | {max_error:<15.2e} | {status:<8}")

        results.append({
            "Size": size, "Execution_Time_Sec": time_sec,
            "Volume_FLOP": size ** 3, "Max_Error": max_error, "Verified": status
        })
        
    with open("output/experiments.txt", "w", encoding="utf-8") as f:
        f.write("Размер | Время (сек) | Объём задачи (N³) | Макс. Ошибка | Верификация\n")
        f.write("-" * 75 + "\n")
        for r in results:
            f.write(f"{r['Size']} | {r['Execution_Time_Sec']:.4f} | {r['Volume_FLOP']} | {r['Max_Error']:.2e} | {r['Verified']}\n")
        
    print("\nВсе эксперименты успешно завершены!")

if __name__ == "__main__":
    main()
