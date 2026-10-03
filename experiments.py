import os
import subprocess
import re
from generate_matrix import generate_and_save_matrices
from verify import verify_results

EXE_PATH = "lab1/main_app.exe"
sizes = [200, 400, 800, 1200, 1600, 2000]

print()
print("=" * 75)
print("ЭКСПЕРИМЕНТЫ: последовательное умножение матриц")
print("=" * 75)
print()
print(f"{'Размер':<8} | {'Время (сек)':<12} | {'Объём задачи':<15} | {'Верификация':<12}")
print("-" * 75)

results = []
os.makedirs("lab1/input", exist_ok=True)
os.makedirs("lab1/output", exist_ok=True)

for size in sizes:
    generate_and_save_matrices(size)

    result = subprocess.run(
        [os.path.abspath(EXE_PATH)],
        cwd="lab1",
        capture_output=True,
        text=True
    )

    match = re.search(r"[Tt]ime:\s*([\d.eE+-]+)", result.stdout)
    elapsed = float(match.group(1)) if match else 0.0
    operations = size ** 3

    is_valid = verify_results(input_dir="lab1/input", output_dir="lab1/output")
    status = "PASS" if is_valid else "FAIL"

    print(f"{size:<8} | {elapsed:<12.4f} | {operations:<15} | {status:<12}")
    
    results.append({
        "Size": size,
        "Execution_Time_Sec": elapsed,
        "Volume_FLOP": operations,
        "Verified": status
    })

print("-" * 75)

with open("lab1/output/experiments.txt", "w", encoding="utf-8") as f:
    f.write("Размер | Время (сек) | Объём задачи (N³) | Верификация\n")
    f.write("-" * 65 + "\n")
    for r in results:
        f.write(f"{r['Size']} | {r['Execution_Time_Sec']:.4f} | {r['Volume_FLOP']} | {r['Verified']}\n")

print()
print("Результаты успешно сохранены в: lab1/output/experiments.txt")
print("Все эксперименты успешно завершены!")
