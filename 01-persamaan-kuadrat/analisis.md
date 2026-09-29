# Analisis White-Box Testing: Program Persamaan Kuadrat

## 1. Tujuan dan ruang lingkup

Program menerima koefisien `a`, `b`, dan `c` dari persamaan `ax² + bx + c = 0`. Program menentukan apakah input bukan persamaan kuadrat, mempunyai dua akar real berbeda, mempunyai akar real kembar, atau mempunyai dua akar kompleks. Setelah menampilkan hasil, program meminta pengguna memilih apakah perhitungan diulang.

Analisis meliputi alur fungsi `solve_quadratic()` dan perulangan pada `main()`. Pengujian menggunakan unit test Python yang tersedia pada `test_quadratic.py`.

## 2. Dasar metode dari paper Annisa

Paper *Analysis of Statement Branch and Loop Coverage in Software Testing With Genetic Algorithm* oleh Rizal Broer Bahaweres, Khoirunnisya Zawawi, Dewi Khairani, dan Nashrul Hakiem membahas white-box testing dengan tiga ukuran utama: statement coverage, branch coverage, dan loop coverage. Paper menjelaskan statement coverage sebagai eksekusi setiap statement setidaknya sekali, sedangkan branch coverage mengharuskan setiap keputusan mempunyai hasil true dan false setidaknya sekali. Penelitian membandingkan pengujian manual, otomatis menggunakan CodeCover, dan CodeCover dengan Genetic Algorithm pada program klasifikasi segitiga.

Pada penelitian tersebut, GA digunakan untuk mencari target path. Parameter yang dilaporkan adalah `Pc = 0,5`, `Pm = 0,01`, `PopSize = 100`, dan `ChromLength = 13`. Angka hasil penelitian tidak dipindahkan ke program ini karena objek, struktur kode, dan lingkungan pengujiannya berbeda.

## 3. Struktur keputusan program

Fungsi `solve_quadratic(a, b, c)` mempunyai alur:
1. Periksa apakah `a == 0`. Jika benar, input bukan persamaan kuadrat.
2. Jika `a` tidak sama dengan nol, hitung diskriminan `D = b² - 4ac`.
3. Jika `D > 0`, hitung dua akar real berbeda.
4. Jika `D == 0`, hitung satu akar real kembar.
5. Selain kedua kondisi tersebut, diskriminan negatif sehingga akar berupa bilangan kompleks.

Fungsi `main()` menjalankan proses dalam `while True`. Setelah hasil ditampilkan, program membaca jawaban pengguna. Jika jawaban setelah diubah ke huruf kapital bukan `"Y"`, program menampilkan pesan selesai dan keluar dari perulangan. Jika `"Y"`, program kembali meminta koefisien.

## 4. Control Flow Graph (CFG)

CFG ringkas untuk `solve_quadratic()`:

```text
             [S]
              |
          [a == 0?]
           /      \
        Ya          Tidak
        |             |
 [return bukan]   [hitung D]
        |             |
       [E]         [D > 0?]
                    /    \
                  Ya      Tidak
                  |         |
             [akar real] [D == 0?]
                  |       /      \
                  |     Ya       Tidak
                  |     |          |
                  | [akar kembar] [akar kompleks]
                  |     |          |
                  +-----+----------+
                         |
                        [E]
```

CFG ringkas untuk `main()`:

```text
       [Mulai]
          |
     [while True]
          |
   [input a, b, c]
          |
   [solve_quadratic]
          |
 [pilih pesan sesuai jenis]
          |
    [input ulang]
          |
      [ulang != Y?]
        /       \
      Ya         Tidak
      |            |
 [selesai/break] [kembali ke while]
      |            |
     [Akhir] <-----+
```

Pada CFG `main()`, panah kembali menunjukkan pengulangan setelah jawaban `"Y"`. Kondisi `while True` merupakan loop dengan kondisi konstan; jalur keluar normal terjadi melalui `break`.

## 5. Analisis path

### 5.1 Path fungsi `solve_quadratic()`

| Path | Kondisi | Hasil |
|---|---|---|
| P1 | `a == 0` | Bukan persamaan kuadrat |
| P2 | `a != 0`, `D > 0` | Dua akar real berbeda |
| P3 | `a != 0`, `D <= 0`, `D == 0` | Akar real kembar |
| P4 | `a != 0`, `D < 0` | Dua akar kompleks |

P3 ditulis sebagai `D <= 0` sebelum pemeriksaan `D == 0` karena program sudah melewati cabang `D > 0`. P4 merupakan kondisi sisa, yaitu diskriminan negatif.

### 5.2 Path loop pada `main()`

- L1: satu iterasi, kemudian pengguna memasukkan selain `Y`; loop berhenti.
- L2: satu iterasi dengan jawaban `Y`, masuk iterasi kedua, kemudian pengguna memasukkan selain `Y`; loop berhenti.
- L3: beberapa iterasi dengan jawaban `Y`, lalu satu jawaban selain `Y`; loop berhenti.

Test otomatis yang disediakan menjalankan empat iterasi, dengan tiga jawaban `Y` dan satu jawaban `N`. Dengan demikian, alur pengulangan dan penghentian sama-sama dijalankan.

## 6. Cyclomatic Complexity

Untuk fungsi `solve_quadratic()`, terdapat tiga keputusan:
- `a == 0`
- `discriminant > 0`
- `discriminant == 0`

Dengan rumus sederhana `M = jumlah keputusan + 1`, diperoleh:

`M = 3 + 1 = 4`

Artinya terdapat empat jalur basis yang dapat digunakan sebagai dasar rancangan pengujian, sesuai empat hasil klasifikasi pada tabel path.

Untuk `main()`, jika kondisi loop konstan `while True` ikut dihitung sebagai satu keputusan dan kondisi `if ulang != "Y"` dihitung sebagai keputusan lain, terdapat dua node keputusan sehingga `M = 2 + 1 = 3`. Perhitungan ini mengikuti CFG sumber, bukan hasil optimasi bytecode.

## 7. Test case

| TC | a | b | c | D | Hasil yang diharapkan | Path |
|---|---:|---:|---:|---:|---|---|
| TC01 | 0 | 2 | 1 | Tidak dihitung | Bukan persamaan kuadrat | P1 |
| TC02 | 1 | 0 | -4 | 16 | Akar 2 dan -2 | P2 |
| TC03 | 1 | -2 | 1 | 0 | Akar kembar 1 | P3 |
| TC04 | 1 | 2 | 5 | -16 | Akar kompleks -1 + 2j dan -1 - 2j | P4 |

Test loop tambahan dilakukan melalui urutan input pada `test_multiple_iterations_and_stop`: TC01, TC02, TC03, dan TC04 dijalankan dalam satu sesi. Jawaban `Y` diberikan setelah tiga kasus pertama, lalu `N` setelah kasus keempat.

## 8. Statement Coverage (SC)

Statement coverage mengukur banyaknya statement yang dieksekusi dibandingkan seluruh statement yang menjadi ruang lingkup pengukuran.

`SC = (statement yang dieksekusi / total statement) × 100%`

Empat test case fungsi mengaktifkan masing-masing cabang return. Pengujian antarmuka juga melewati pembacaan input, pemanggilan fungsi, penampilan keluaran, pembacaan pilihan ulang, serta `break`. Secara rancangan, seluruh statement yang relevan telah mempunyai test case.

Persentase aktual tetap perlu dibuktikan menggunakan alat coverage pada lingkungan eksekusi. Perhitungan rancangan ini bukan laporan hasil alat.

## 9. Branch Coverage (BC)

Branch coverage mengharuskan kedua hasil setiap keputusan dijalankan.

| Keputusan | Cabang True | Cabang False | Test case yang meliputi |
|---|---|---|---|
| `a == 0` | TC01 | TC02, TC03, TC04 | TC01–TC04 |
| `D > 0` | TC02 | TC03, TC04 | TC02–TC04 |
| `D == 0` | TC03 | TC04 | TC03–TC04 |
| `ulang != "Y"` | N menghentikan loop | Y melanjutkan loop | Test interaktif |

Untuk loop, `ulang != "Y"` bernilai false ketika pengguna menjawab `Y`, sehingga program melanjutkan iterasi; kondisi bernilai true ketika pengguna menjawab `N`, sehingga program berhenti.

## 10. Loop Coverage (LC)

Loop utama adalah `while True` yang dihentikan dengan `break`. Pengujian loop perlu mencakup:
1. Satu iterasi lalu berhenti.
2. Lebih dari satu iterasi, kemudian berhenti.
3. Jalur melanjutkan loop (`Y`) dan jalur keluar (`N`).

Test `test_multiple_iterations_and_stop` menjalankan empat iterasi dalam satu sesi dan mencakup jalur lanjut serta berhenti. Ini merupakan rancangan uji loop untuk perilaku program. Persentase LC yang dilaporkan alat dapat berbeda menurut definisi instrumen dan cara alat menangani `while True` serta `break`.

## 11. Hasil pengujian yang disiapkan

File `test_quadratic.py` berisi lima pengujian:
- empat pengujian hasil matematis;
- satu pengujian interaksi yang menguji pengulangan beberapa kali dan penghentian.

Jalankan dari direktori ini:

```bash
python -m unittest -v
```

Untuk mengukur coverage dengan `coverage.py`, instal alat lalu jalankan:

```bash
python -m pip install coverage
coverage run --branch -m unittest
coverage report -m
```

Simpan keluaran terminal sebagai bukti pengujian apabila diminta dosen.

## 12. Kesimpulan

Program persamaan kuadrat memiliki empat jalur hasil utama pada fungsi penyelesaian: input bukan kuadrat, dua akar real berbeda, akar real kembar, dan akar kompleks. Cyclomatic complexity fungsi tersebut adalah 4 berdasarkan tiga keputusan. Test case disusun untuk melewati seluruh hasil tersebut, sedangkan pengujian interaktif menguji perilaku loop untuk melanjutkan dan berhenti.

Coverage adalah ukuran bagian kode yang telah dieksekusi, bukan bukti bahwa program bebas dari seluruh kesalahan. Pengujian tetap perlu memperhatikan ketepatan hasil, nilai batas, dan input yang tidak valid.
