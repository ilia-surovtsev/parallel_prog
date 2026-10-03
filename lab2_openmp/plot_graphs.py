import os
import matplotlib.pyplot as plt
import numpy as np

txt_path = "output/experiments.txt"

if not os.path.exists(txt_path):
    print(f"Ошибка: Файл {txt_path} не найден!")
    exit(1)

with open(txt_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

data = {}
for line in lines[2:]:
    parts = line.strip().split(" | ")
    if len(parts) == 5:
        size = int(parts[0])
        t = int(parts[1])
        time_sec = float(parts[2])
        speedup = float(parts[3])
        
        if size not in data:
            data[size] = {"threads": [], "times": [], "speedups": []}
        data[size]["threads"].append(t)
        data[size]["times"].append(time_sec)
        data[size]["speedups"].append(speedup)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

for size in sorted(data.keys()):
    threads = data[size]["threads"]
    times = data[size]["times"]
    speedups = data[size]["speedups"]
    
    ax1.plot(threads, times, 'o-', linewidth=1.5, markersize=5, label=f'{size}x{size}')
    ax2.plot(threads, speedups, 'o-', linewidth=1.5, markersize=5, label=f'{size}x{size}')

ax1.set_yscale('log')
ax1.set_xlabel('Число потоков', fontsize=11)
ax1.set_ylabel('Время (сек)', fontsize=11)
ax1.set_title('Время выполнения от числа потоков', fontsize=12)
ax1.grid(True, which="both", linestyle='--', alpha=0.5)
ax1.legend()

max_threads = max(threads) if threads else 8
ideal_threads = np.array([1, max_threads])
ax2.plot(ideal_threads, ideal_threads, '--', color='gray', alpha=0.7, label='Идеальное')

ax2.set_xlim(0, max_threads + 1)
ax2.set_ylim(0, max_threads + 1)
ax2.set_xlabel('Число потоков', fontsize=11)
ax2.set_ylabel('Ускорение (раз)', fontsize=11)
ax2.set_title('Ускорение OpenMP', fontsize=12)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend()

plt.tight_layout()
output_path = 'output/graphs.png'
plt.savefig(output_path, dpi=150)
plt.close()

print(f"Парные графики успешно сохранены в {output_path}")
