import numpy as np
from fractions import Fraction

def solve_matrix_obe_with_multipliers(matrix):
    """
    Menyelesaikan sistem persamaan linier menggunakan metode OBE dengan langkah-langkah
    ditampilkan dalam format pecahan beserta operasi yang dilakukan.
    
    Parameter:
    matrix : np.ndarray
        Matriks augmented berukuran n x (n+1).
    
    Return:
    steps : list
        Langkah-langkah dalam format string beserta solusi akhir.
    """
    # Konversi elemen matriks ke Fraction untuk menghindari kesalahan tipe
    mat = np.array([[Fraction(val).limit_denominator() for val in row] for row in matrix])
    rows, cols = mat.shape
    step = 0
    steps = []  # Array untuk menyimpan langkah-langkah
    
    # Fungsi untuk menambahkan langkah ke dalam daftar
    def add_step(matrix, operation=None):
        nonlocal step
        step += 1
        text = f"Langkah {step}:\n"
        if operation:
            text += f"Operasi: {operation}\n"
        text += "\n".join(["  " + "  ".join(f"{Fraction(val).limit_denominator()}" for val in row) for row in matrix])
        text += "\n"
        steps.append(text)
    
    # Tambahkan matriks awal
    add_step(mat, operation="Matriks awal")
    
    # Forward elimination
    for i in range(rows):
        # Ambil pivot
        pivot = mat[i, i]
        if pivot == 0:
            # Tukar baris jika pivot nol
            for j in range(i + 1, rows):
                if mat[j, i] != 0:
                    mat[[i, j]] = mat[[j, i]]  # Tukar baris
                    add_step(mat, operation=f"Tukar R{i+1} ↔ R{j+1}")
                    pivot = mat[i, i]
                    break
        
        if pivot == 0:
            steps.append(f"Pivot di baris {i+1} adalah nol, sistem tidak dapat diselesaikan.")
            return steps
        
        # Normalisasi pivot
        multiplier = Fraction(1, pivot).limit_denominator()
        mat[i] = [val * multiplier for val in mat[i]]  # Normalisasi baris
        add_step(mat, operation=f"R{i+1} × {multiplier}")
        
        # Nolkan elemen di bawah pivot
        for j in range(i + 1, rows):
            multiplier = mat[j, i]
            mat[j] = [val - multiplier * pivot_val for val, pivot_val in zip(mat[j], mat[i])]
            add_step(mat, operation=f"R{j+1} - ({multiplier}) × R{i+1}")
    
    # Backward substitution
    for i in range(rows - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            multiplier = mat[j, i]
            mat[j] = [val - multiplier * pivot_val for val, pivot_val in zip(mat[j], mat[i])]
            add_step(mat, operation=f"R{j+1} - ({multiplier}) × R{i+1}")
    
    # Solusi adalah kolom terakhir
    solusi = mat[:, -1]
    solusi_fraction = [Fraction(val).limit_denominator() for val in solusi]
    solution_text = "Hasil Akhir :\n" + "\n".join([f"x{i+1} = {sol}" for i, sol in enumerate(solusi_fraction)])
    steps.append(solution_text)
    return steps

