#!/bin/bash
#SBATCH --job-name=mpi_matrix_lab       
#SBATCH --output=matrix_report.txt 
#SBATCH --error=matrix_errors.err 
#SBATCH --partition=batch             
#SBATCH --nodes=1                       
#SBATCH --ntasks-per-node=8             
#SBATCH --time=00:20:00                 

module purge
module load intel/icc18
module load intel/mpi4

mkdir -p input output
> results.txt
echo "N Procs Time_s" >> results.txt

SIZES="200 400 800 1200 1600 2000"
PROCS="1 2 4 8"

for N in $SIZES; do
    echo "Generating N=$N..."
    python3 -c "
import random
n = $N
with open('input/matrix_a.txt', 'w') as f:
    f.write(str(n) + '\n')
    for _ in range(n):
        f.write(' '.join(str(random.uniform(-10, 10)) for _ in range(n)) + '\n')
with open('input/matrix_b.txt', 'w') as f:
    f.write(str(n) + '\n')
    for _ in range(n):
        f.write(' '.join(str(random.uniform(-10, 10)) for _ in range(n)) + '\n')
" 2>/dev/null

    for P in $PROCS; do
        if [ ! -f "input/matrix_a.txt" ]; then continue; fi
        echo "Running N=$N, Procs=$P..."
        
        mpirun -np $P -bootstrap slurm ./main_mpi_app
        
        if [ -f "output/info.txt" ]; then
            TIME=$(grep "Execution time:" output/info.txt | awk '{print $3}')
            echo "$N $P $TIME" >> results.txt
            echo "  -> Time: $TIME s"
            rm -f output/info.txt
        else
            echo "$N $P FAIL" >> results.txt
            echo "  -> Failed"
        fi
    done
done
echo "Done!"
