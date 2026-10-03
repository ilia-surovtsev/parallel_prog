import os
import matplotlib.pyplot as plt
import numpy as np

txt_path = "lab1/output/experiments.txt"

if not os.path.exists(txt_path):
    print(f"Ошибка: Файл {txt_path} не найден! Сначала запустите experiments.py.")
    exit(1)

with open(txt_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

sizes = []
times = []

for line in lines[2:]:  
    parts = line.strip().split(" | ")
    if len(parts) >= 2:
        sizes.append(int(parts[0]))
        times.append(float(parts[1]))

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(sizes, times, 'o-', color='steelblue', linewidth=2, markersize=8, label='Эксперимент')

sizes_arr = np.array(sizes)
times_arr = np.array(times)

theoretical = times_arr[0] * (sizes_arr / sizes_arr[0]) ** 3
ax.plot(sizes, theoretical, '--', color='red', alpha=0.6, label='Теоретическая O(N³)')

ax.set_xlabel('Размер матрицы N', fontsize=12)
ax.set_ylabel('Время (сек)', fontsize=12)
ax.set_title('Зависимость времени умножения матриц от размера N', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend()

plt.tight_layout()
output_path = 'lab1/output/graph.png'
plt.savefig(output_path, dpi=150)
plt.close()

print(f"График сохранён в {output_path}")
