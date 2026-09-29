# Tugas Mandiri: Analisis White-Box Testing

Repository ini disusun untuk tugas mandiri analisis dan pengujian perangkat lunak menggunakan pendekatan *white-box testing*.

## Identitas

- Nama: Muhammad Naqib Muhtadi
- NIM: **Isi NIM sebelum dikumpulkan**
- Program studi: Teknik Informatika
- Institusi: UIN Syarif Hidayatullah Jakarta

## Ruang Lingkup

Tugas ini mencakup dua objek:

1. **Program persamaan kuadrat** yang dibuat menggunakan Python. Analisis mencakup alur program, *control flow graph* (CFG), path, cyclomatic complexity, statement coverage, branch coverage, dan loop coverage.
2. **Spring PetClinic**, proyek open-source Spring. Analisis dibatasi pada method `processFindForm()` dalam class `OwnerController`, package `org.springframework.samples.petclinic.owner`.

## Struktur Repository

```text
analisis-white-box-testing/
├── README.md
├── .gitignore
├── 01-persamaan-kuadrat/
│   ├── quadratic.py
│   ├── test_quadratic.py
│   └── analisis.md
├── 02-spring-petclinic/
│   └── analisis.md
└── docs/
    └── Laporan_Final_Analisis_White_Box_Testing.docx
```

## 1. Menjalankan Program Persamaan Kuadrat

Persyaratan: Python 3.

Dari root repository, jalankan:

```bash
cd 01-persamaan-kuadrat
python quadratic.py
```

Program meminta koefisien `a`, `b`, dan `c` dari persamaan `ax² + bx + c = 0`. Setelah menampilkan hasil, program menawarkan penghitungan ulang.

## 2. Menjalankan Unit Test

Dari direktori `01-persamaan-kuadrat`:

```bash
python -m unittest -v
```

Test mencakup input yang bukan persamaan kuadrat, dua akar real berbeda, akar real kembar, akar kompleks, serta pengulangan input dan penghentian program.

## 3. Mengukur Coverage Program Python

Instal `coverage.py`:

```bash
python -m pip install coverage
```

Jalankan unit test dengan pengukuran branch:

```bash
coverage run --branch -m unittest
```

Untuk turut mengukur jalur eksekusi antarmuka program (`main()`), jalankan program secara langsung dengan input uji. Contoh di bawah menguji kasus `a = 0`, lalu menghentikan program:

```bash
printf '0\n2\n1\nN\n' | coverage run --branch --append quadratic.py
coverage report -m
```

Pada Windows PowerShell, input interaktif dapat dimasukkan langsung saat program dijalankan. Hasil coverage dapat berbeda jika hanya unit test yang dijalankan atau jika cakupan file test ikut dihitung. Perhatikan baris `quadratic.py` saat melaporkan coverage program.

## 4. Objek Open-Source Spring

- Repository: [spring-projects/spring-petclinic](https://github.com/spring-projects/spring-petclinic)
- Source file: [OwnerController.java](https://github.com/spring-projects/spring-petclinic/blob/main/src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java)
- Package: `org.springframework.samples.petclinic.owner`
- Class: `OwnerController`
- Method: `processFindForm()`

Analisis Spring berisi identifikasi keputusan, CFG, path, cyclomatic complexity, dan rancangan test case. **Pengujian aktual serta pengukuran coverage Spring belum dilakukan dalam paket ini.** Karena itu, rancangan test case tidak dinyatakan sebagai hasil eksekusi atau persentase coverage.

Untuk menguji versi proyek yang digunakan, clone repository resmi dan catat commit-nya:

```bash
git clone https://github.com/spring-projects/spring-petclinic.git
cd spring-petclinic
git rev-parse HEAD
./mvnw test
```

Pada Windows, gunakan `mvnw.cmd test`. Pengukuran coverage method perlu dilakukan dengan konfigurasi JaCoCo yang sesuai dan dilaporkan berdasarkan hasil aktual.

## Referensi

Bahaweres, R. B., Zawawi, K., Khairani, D., & Hakiem, N. (2017). *Analysis of Statement Branch and Loop Coverage in Software Testing With Genetic Algorithm*. EECSI 2017.

Spring PetClinic: https://github.com/spring-projects/spring-petclinic
