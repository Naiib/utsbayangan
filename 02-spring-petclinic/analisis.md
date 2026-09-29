# Analisis White-Box Testing: Spring PetClinic

## 1. Identitas proyek

| Komponen | Keterangan |
|---|---|
| Nama proyek | Spring PetClinic Sample Application |
| Repositori | https://github.com/spring-projects/spring-petclinic |
| File | `src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java` |
| Package | `org.springframework.samples.petclinic.owner` |
| Class | `OwnerController` |
| Method yang dianalisis | `processFindForm()` |
| Jenis pengujian | White-box / structural testing |
| Batasan | Analisis jalur method `processFindForm()`, bukan seluruh class |

Repositori resmi menjelaskan bahwa Spring PetClinic merupakan aplikasi contoh berbasis Spring Boot dan dapat dijalankan dengan Maven atau Gradle. Repositori juga menyebut kebutuhan Java 17 atau lebih baru. Karena cabang `main` dapat berubah, catat commit yang benar-benar digunakan saat melakukan checkout dan pengujian.

Sumber kode yang dianalisis:
https://github.com/spring-projects/spring-petclinic/blob/main/src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java

## 2. Gambaran fungsi

`OwnerController` menangani operasi terkait pemilik hewan (owner). Method `processFindForm()` memproses permintaan pencarian owner berdasarkan nama belakang. Method ini:
1. Mengambil `lastName` dari objek `Owner`.
2. Jika `lastName` bernilai `null`, mengubahnya menjadi string kosong agar pencarian dapat mencakup seluruh data.
3. Jika tidak `null`, menghapus spasi di awal dan akhir dengan `strip()`.
4. Memanggil `findPaginatedForOwnersLastName(page, lastName)` untuk memperoleh hasil.
5. Jika hasil kosong, menambahkan error pada field `lastName` dan kembali ke halaman pencarian.
6. Jika tepat satu owner ditemukan, mengarahkan pengguna ke halaman detail owner.
7. Jika lebih dari satu owner ditemukan, menyiapkan model pagination dan menampilkan daftar owner.

## 3. Pseudocode

```text
START
  lastName = owner.getLastName()

  IF lastName == null
      lastName = ""
  ELSE
      lastName = lastName.strip()
  ENDIF

  ownersResults = findPaginatedForOwnersLastName(page, lastName)

  IF ownersResults.isEmpty()
      result.rejectValue(...)
      RETURN "owners/findOwners"
  ENDIF

  IF ownersResults.getTotalElements() == 1
      owner = ownersResults.iterator().next()
      RETURN "redirect:/owners/" + owner.getId()
  ENDIF

  RETURN addPaginationModel(page, model, ownersResults)
END
```

## 4. Control Flow Graph (CFG)

```text
                       [Start]
                          |
             [ambil owner.getLastName()]
                          |
                  [lastName == null?]
                    /             \
                  Ya               Tidak
                  |                  |
          [lastName = ""]    [lastName.strip()]
                    \             /
                     \           /
               [panggil pencarian]
                          |
               [ownersResults.isEmpty?]
                    /             \
                  Ya               Tidak
                  |                  |
       [rejectValue(lastName)]  [totalElements == 1?]
                  |              /             \
       [return findOwners]     Ya               Tidak
                                |                  |
                         [ambil owner]    [addPaginationModel]
                                |                  |
                    [redirect detail]   [return ownersList]
                                |                  |
                              [End]              [End]
```

CFG ini hanya menggambarkan keputusan dan alur pada method yang dipilih. Pemanggilan repository dan helper diperlakukan sebagai satu node proses; isi internal helper tidak dihitung sebagai bagian dari CFG method ini.

## 5. Identifikasi keputusan

| ID | Kondisi | Jika True | Jika False |
|---|---|---|---|
| D1 | `lastName == null` | `lastName` diisi string kosong | `lastName` diproses dengan `strip()` |
| D2 | `ownersResults.isEmpty()` | Tambahkan error dan kembali ke form pencarian | Lanjut ke pemeriksaan jumlah hasil |
| D3 | `ownersResults.getTotalElements() == 1` | Ambil owner dan redirect ke halaman detail | Tampilkan daftar dengan pagination |

Ada tiga keputusan biner pada method. Setiap keputusan memiliki dua kemungkinan hasil yang harus dicakup untuk branch coverage.

## 6. Analisis path

| Path | Urutan keputusan | Alur | Hasil |
|---|---|---|---|
| P1 | D1=True, D2=True | Nama belakang null → pencarian luas → hasil kosong | Kembali ke `owners/findOwners` dengan error |
| P2 | D1=True, D2=False, D3=True | Nama belakang null → hasil ditemukan → tepat satu owner | Redirect ke detail owner |
| P3 | D1=True, D2=False, D3=False | Nama belakang null → hasil ditemukan → lebih dari satu owner | Menampilkan daftar owner |
| P4 | D1=False, D2=False, D3=False | Nama belakang tersedia → `strip()` → beberapa hasil | Menampilkan daftar owner |

P1 sampai P4 merupakan empat jalur basis yang dapat digunakan untuk menyusun pengujian. Secara kombinatorial, mungkin terdapat kombinasi kondisi lain, tetapi cabang `D3` hanya dievaluasi ketika `D2` bernilai false.

## 7. Cyclomatic Complexity

Cyclomatic complexity dapat dihitung dengan rumus:

`M = jumlah keputusan + 1`

Terdapat tiga keputusan pada method:
- `lastName == null`
- `ownersResults.isEmpty()`
- `ownersResults.getTotalElements() == 1`

Maka:

`M = 3 + 1 = 4`

Nilai 4 menunjukkan empat jalur basis untuk rancangan pengujian method ini. Perhitungan ini tidak mencakup keputusan di dalam method helper `findPaginatedForOwnersLastName()` atau `addPaginationModel()`.

## 8. Rancangan test case

Untuk pengujian unit, hasil `Page<Owner>` dapat dibuat menggunakan mock. Tabel berikut merupakan rancangan input dan hasil yang diharapkan, bukan klaim bahwa test sudah dijalankan pada repositori.

| TC | `lastName` | Hasil pencarian | Jalur | Hasil yang diharapkan |
|---|---|---|---|---|
| TC01 | `null` | Kosong | P1 | `result.rejectValue("lastName", ...)` dipanggil; view `owners/findOwners` |
| TC02 | `null` | Tepat 1 owner, ID 7 | P2 | Redirect `redirect:/owners/7` |
| TC03 | `null` | 3 owner | P3 | Memanggil helper pagination; hasil `owners/ownersList` |
| TC04 | `" Smith "` | 3 owner | P4 | Pencarian menggunakan `"Smith"`; hasil `owners/ownersList` |

### Detail verifikasi per test case

- **TC01:** Pastikan hasil `Page` kosong, error ditambahkan pada field `lastName`, dan method mengembalikan nama view pencarian.
- **TC02:** Pastikan `iterator().next()` menghasilkan owner dengan ID 7 dan method mengembalikan URL redirect yang sesuai.
- **TC03:** Pastikan daftar hasil lebih dari satu sehingga method mengembalikan view daftar melalui `addPaginationModel()`.
- **TC04:** Selain memeriksa view daftar, verifikasi bahwa repository dipanggil dengan nama belakang yang sudah dibersihkan dari spasi.

## 9. Statement Coverage (SC)

Statement coverage mengukur statement yang dijalankan setidaknya sekali. Dalam ruang lingkup method `processFindForm()`, rancangan TC01–TC04 melewati:
- pengambilan nama belakang;
- cabang `null` dan cabang `strip()`;
- pemanggilan pencarian;
- penanganan hasil kosong;
- penanganan satu hasil;
- penanganan banyak hasil.

Secara rancangan, seluruh statement utama method memiliki kasus uji. Persentase aktual harus dikonfirmasi dengan menjalankan test pada versi kode yang dipilih dan membaca laporan alat coverage.

## 10. Branch Coverage (BC)

| Keputusan | True dicakup oleh | False dicakup oleh |
|---|---|---|
| D1: `lastName == null` | TC01, TC02, TC03 | TC04 |
| D2: `ownersResults.isEmpty()` | TC01 | TC02, TC03, TC04 |
| D3: `totalElements == 1` | TC02 | TC03, TC04 |

Dengan empat test case tersebut, setiap keputusan dirancang memiliki hasil true dan false. Ini memenuhi rancangan branch coverage untuk tiga keputusan pada method, tetapi persentase coverage aktual tetap harus diambil dari alat.

## 11. Loop Coverage (LC)

Tidak terdapat perulangan eksplisit (`for`, `while`, atau `do-while`) di dalam `processFindForm()`. Karena itu, loop coverage tidak menjadi kriteria yang relevan untuk method ini. Perulangan yang mungkin terjadi di dalam implementasi `Page`, repository, atau framework berada di luar ruang lingkup CFG method yang dianalisis.

## 12. Cara menjalankan proyek dan mengumpulkan bukti

1. Clone repositori resmi:
   ```bash
   git clone https://github.com/spring-projects/spring-petclinic.git
   cd spring-petclinic
   ```
2. Catat commit yang digunakan:
   ```bash
   git rev-parse HEAD
   ```
3. Jalankan test yang tersedia:
   ```bash
   ./mvnw test
   ```
   Pada Windows, gunakan `mvnw.cmd test`.
4. Untuk mengukur coverage, gunakan konfigurasi JaCoCo yang tersedia atau tambahkan konfigurasi/plugin JaCoCo pada checkout kerja. Pastikan laporan mencakup class `OwnerController` dan method `processFindForm()`.
5. Simpan laporan hasil test dan coverage sebagai bukti. Jika menulis test baru, letakkan pada struktur `src/test/java` yang sesuai dan gunakan versi dependensi dari checkout yang dipakai.

Catatan: file analisis ini tidak mengklaim telah menjalankan seluruh Spring PetClinic atau mengukur coverage aktual. Pengujian terintegrasi perlu dilakukan di lingkungan Java/Maven dengan dependensi proyek.

## 13. Kesimpulan

Method `processFindForm()` mempunyai tiga keputusan utama dan cyclomatic complexity 4. Empat test case disusun untuk mencakup hasil pencarian kosong, tepat satu hasil, banyak hasil, serta input nama belakang yang perlu dibersihkan. Karena tidak ada loop eksplisit pada method ini, loop coverage tidak diterapkan pada ruang lingkup tersebut.

Analisis ini menunjukkan bagaimana CFG dapat digunakan untuk menentukan jalur basis dan menyusun test case. Coverage membantu menunjukkan bagian kode yang telah dieksekusi, tetapi tidak dengan sendirinya membuktikan bahwa seluruh perilaku program bebas dari kesalahan.

## Source code objek analisis

File `OwnerController.java` disertakan dalam folder ini sebagai salinan file dari repository publik Spring PetClinic. Analisis difokuskan pada method `processFindForm()`; class lengkap disertakan agar konteks package dan method dapat diperiksa.

Sumber asli: https://github.com/spring-projects/spring-petclinic/blob/main/src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java

Lisensi sumber: Apache License 2.0. File ini merupakan bagian dari project Spring PetClinic dan hak cipta tetap pada pemilik aslinya.
