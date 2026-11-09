import os
import matplotlib.pyplot as plt

txt_path = "results.txt"

if not os.path.exists(txt_path):
    print(f"Error: {txt_path} not found!")
    exit(1)

data_raw = []
with open(txt_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines[1:]:  
    parts = line.strip().split()
    if len(parts) == 3:
        try:
            n_val = int(parts[0])
            p_val = int(parts[1])
            t_val = float(parts[2])
            data_raw.append((n_val, p_val, t_val))
        except ValueError:
            continue

os.makedirs("output", exist_ok=True)

sizes = sorted(list(set([x[0] for x in data_raw])))
cores = sorted(list(set([x[1] for x in data_raw])))

time_vs_size = {c: [] for c in cores}
for c in cores:
    for s in sizes:
        t = [x[2] for x in data_raw if x[0] == s and x[1] == c]
        if t:
            time_vs_size[c].append(t[0] * 1000)

plt.figure(figsize=(10, 5))
for c in cores:
    if len(time_vs_size[c]) == len(sizes):
        plt.plot(sizes, time_vs_size[c], 'o-', label=f'{c} MPI-ядер')

plt.yscale('log')
plt.xlabel('Размер матрицы (N x N)')
plt.ylabel('Время расчета (мс)')
plt.title('Зависимость времени расчета от размера матрицы')
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig('output/time_graph.png', dpi=150)
plt.close()

plt.figure(figsize=(10, 5))
plt.plot([1, max(cores)], [1, max(cores)], '--', color='gray', label='Идеальное ускорение')

target_sizes = [800, 1600, 2000]
for s in target_sizes:
    t1_list = [x[2] for x in data_raw if x[0] == s and x[1] == 1]
    if not t1_list:
        continue
    t1 = t1_list[0]
    
    speedups = []
    available_cores = []
    for c in cores:
        tc_list = [x[2] for x in data_raw if x[0] == s and x[1] == c]
        if tc_list:
            speedups.append(t1 / tc_list[0])
            available_cores.append(c)
            
    if speedups:
        plt.plot(available_cores, speedups, 's-', label=f'Матрица {s}x{s}')

plt.xlabel('Количество MPI-ядер')
plt.ylabel('Ускорение S = T(1)/T(p)')
plt.title('Ускорение алгоритма (Speedup) в зависимости от количества MPI-ядер')
plt.grid(True, ls="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig('output/speedup_graph.png', dpi=150)
plt.close()

print("Graphs successfully created from file and saved to output/ folder!")
