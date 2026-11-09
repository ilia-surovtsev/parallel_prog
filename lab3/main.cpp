#include <mpi.h>
#include <iostream>
#include <vector>
#include <fstream>
#include <chrono>
#include <iomanip>

using namespace std;

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int num_procs, my_rank;
    MPI_Comm_size(MPI_COMM_WORLD, &num_procs);
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);

    int m = 0;
    vector<double> A_global;
    vector<double> B_global;
    vector<double> C_global;

    auto start_time = chrono::high_resolution_clock::now();

    if (my_rank == 0) {
        ifstream file1("input/matrix_a.txt");
        if (!file1.is_open()) {
            cerr << "Error: input/matrix_a.txt not found!" << endl;
            MPI_Abort(MPI_COMM_WORLD, 1);
            return 1;
        }
        file1 >> m;
        A_global.resize(m * m);
        for (int i = 0; i < m * m; i++) file1 >> A_global[i];
        file1.close();

        ifstream file2("input/matrix_b.txt");
        if (!file2.is_open()) {
            cerr << "Error: input/matrix_b.txt not found!" << endl;
            MPI_Abort(MPI_COMM_WORLD, 1);
            return 1;
        }
        int n_check;
        file2 >> n_check;
        if (m != n_check) {
            cerr << "Error: Matrix dimensions must agree!" << endl;
            MPI_Abort(MPI_COMM_WORLD, 1);
            return 1;
        }
        B_global.resize(m * m);
        for (int i = 0; i < m * m; i++) file2 >> B_global[i];
        file2.close();

        cout << "Matrix size: " << m << "x" << m << " | Processes: " << num_procs << endl;
    }

    MPI_Bcast(&m, 1, MPI_INT, 0, MPI_COMM_WORLD);

    vector<int> send_counts(num_procs), displs(num_procs);
    int rows_per_proc = m / num_procs;
    int remaining_rows = m % num_procs;

    int current_displ = 0;
    for (int i = 0; i < num_procs; i++) {
        int rows = rows_per_proc + (i < remaining_rows ? 1 : 0);
        send_counts[i] = rows * m;
        displs[i] = current_displ;
        current_displ += send_counts[i];
    }

    int my_rows = send_counts[my_rank] / m;
    vector<double> A_local(send_counts[my_rank]);
    vector<double> C_local(send_counts[my_rank], 0.0);

    if (my_rank != 0) {
        B_global.resize(m * m);
    }

    MPI_Scatterv(A_global.data(), send_counts.data(), displs.data(), MPI_DOUBLE,
        A_local.data(), send_counts[my_rank], MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(B_global.data(), m * m, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    MPI_Barrier(MPI_COMM_WORLD);
    auto calc_start = chrono::high_resolution_clock::now();

    for (int i = 0; i < my_rows; i++) {
        for (int k = 0; k < m; k++) {
            double temp = A_local[i * m + k];
            for (int j = 0; j < m; j++) {
                C_local[i * m + j] += temp * B_global[k * m + j];
            }
        }
    }

    auto calc_end = chrono::high_resolution_clock::now();
    MPI_Barrier(MPI_COMM_WORLD);

    if (my_rank == 0) C_global.resize(m * m);

    MPI_Gatherv(C_local.data(), send_counts[my_rank], MPI_DOUBLE,
        C_global.data(), send_counts.data(), displs.data(), MPI_DOUBLE, 0, MPI_COMM_WORLD);

    if (my_rank == 0) {
        double time_sec = chrono::duration<double>(calc_end - calc_start).count();
        double total_time_sec = chrono::duration<double>(chrono::high_resolution_clock::now() - start_time).count();

        cout << "Computation completed." << endl;
        cout << "Calc time: " << time_sec << " sec (Total time: " << total_time_sec << " sec)" << endl;

        int total_elements = 3 * m * m;
        long long total_flops = 2LL * m * m * m;

        ofstream out("output/result.txt");
        if (out.is_open()) {
            out << m << endl;
            out << setprecision(15);
            for (int i = 0; i < m; i++) {
                for (int j = 0; j < m; j++) {
                    out << C_global[i * m + j] << " ";
                }
                out << endl;
            }
            out.close();
        }

        ofstream info("output/info.txt");
        if (info.is_open()) {
            info << "=== MPI Matrix Multiplication Info ===" << endl;
            info << "Matrix size: " << m << "x" << m << endl;
            info << "Processes: " << num_procs << endl;
            info << "Execution time: " << time_sec << " sec" << endl;
            info << "Task volume (Data): " << total_elements << " elements" << endl;
            info << "Task volume (Ops): " << total_flops << " FLOP" << endl;
            info.close();
        }
    }

    MPI_Finalize();
}
