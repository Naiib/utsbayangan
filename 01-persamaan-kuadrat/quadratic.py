"""Program sederhana untuk menentukan akar persamaan kuadrat.

Persamaan yang diselesaikan berbentuk ax^2 + bx + c = 0.
"""

import math


def solve_quadratic(a: float, b: float, c: float):
    """Mengembalikan jenis dan akar persamaan kuadrat."""
    if a == 0:
        return "bukan_persamaan_kuadrat", None

    discriminant = b**2 - 4 * a * c

    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return "dua_akar_real", (x1, x2)
    elif discriminant == 0:
        x = -b / (2 * a)
        return "akar_real_kembar", (x,)
    else:
        real = -b / (2 * a)
        imag = math.sqrt(-discriminant) / abs(2 * a)
        return "dua_akar_kompleks", (complex(real, imag), complex(real, -imag))


def main():
    """Antarmuka input-output yang mengulang sampai pengguna berhenti."""
    while True:
        print("\n=== PROGRAM PERSAMAAN KUADRAT ===")
        a = float(input("Masukkan nilai a: "))
        b = float(input("Masukkan nilai b: "))
        c = float(input("Masukkan nilai c: "))

        jenis, akar = solve_quadratic(a, b, c)

        if jenis == "bukan_persamaan_kuadrat":
            print("Bukan persamaan kuadrat karena a = 0")
        elif jenis == "dua_akar_real":
            print("Diskriminan: lebih besar dari 0")
            print("Persamaan memiliki dua akar real")
            print("x1 =", akar[0])
            print("x2 =", akar[1])
        elif jenis == "akar_real_kembar":
            print("Diskriminan: 0")
            print("Persamaan memiliki akar real kembar")
            print("x =", akar[0])
        else:
            print("Diskriminan: kurang dari 0")
            print("Persamaan memiliki dua akar kompleks")
            print("x1 =", akar[0])
            print("x2 =", akar[1])

        ulang = input("\nHitung lagi? (Y/N): ").upper()
        if ulang != "Y":
            print("Program selesai.")
            break


if __name__ == "__main__":
    main()
