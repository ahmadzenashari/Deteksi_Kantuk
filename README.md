# Mikro-Sleep
<div align="center">
  <img src="assets/COVER NEW.png" alt="COVER PROJECT" width="500">
</div>

<div align="center">

### DI SUSUN OLEH
| No | Nama | NRP |
| :-: | :-------------------------: | :----------: |
| **1** | Arfin Nurur Robbi | 2122600002 |
| **2** | Nataratungga Xina Tannisa | 2122600006 |
| **3** | Ahmad Zen Ashari | 2122600009 |
| **4** | Thofail Syakirudin | 2122600037 |
| **5** | Muhammad Iqbal Hanafi | 2122600043 |

### DOSEN PENGAMPU
Akhmad Hendriawan, S.T., M.T.

NIP: 197501272002121003

### LINK PRESENTASI (PPT)
[🔗 Buka Presentasi (Canva)](https://www.canva.com/design/DAG4SUS50Nc/X9_LE9DxaSkAgMKRbhSYXQ/edit?utm_content=DAG4SUS50Nc&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
**LINK You Tube (Demonstrasi)**
https://youtu.be/_K0K-iuGGx8?si=IBIX1jOYdsZZlV8Z

</div>

# KATA PENGANTAR
Proyek ini dibuat sebagai bentuk implementasi teknologi Computer Vision untuk mendeteksi tingkat kantuk seseorang secara real-time menggunakan kamera. Sistem ini dikembangkan dengan bantuan MediaPipe Face Mesh untuk melacak pergerakan area mata dan menghitung Eye Aspect Ratio (EAR) sebagai indikator utama apakah mata terbuka atau tertutup.

Melalui metode ini, sistem mampu mengenali kondisi kantuk berdasarkan durasi mata tertutup dan memberikan peringatan berupa suara serta notifikasi agar pengguna tetap waspada. Proyek ini diharapkan dapat membantu meningkatkan keselamatan kerja maupun berkendara, terutama bagi pengguna yang membutuhkan fokus tinggi dalam jangka waktu lama.

Pengembangan dilakukan menggunakan Python dengan dukungan pustaka seperti mediapipe, opencv, tkinter, dan pygame, serta dilengkapi antarmuka sederhana agar mudah digunakan oleh pengguna umum maupun pengembang.

Kami berharap proyek ini dapat menjadi kontribusi kecil dalam bidang keamanan berbasis visi komputer, sekaligus membuka peluang penelitian lanjutan untuk sistem deteksi kelelahan yang lebih cerdas dan akurat.

# TUJUAN
| No    | Tujuan                                                                                                           |
| ----- | ---------------------------------------------------------------------------------------------------------------- |
| **1** | Mendeteksi tanda-tanda kantuk secara real-time menggunakan kamera.                                               |
| **2** | Memberikan peringatan (visual + suara + notifikasi) saat mata tertutup melebihi ambang waktu.                    |
| **3** | Menyimpan jumlah kejadian kantuk untuk analisis dan evaluasi.                                                    |
| **4** | Menyediakan antarmuka (GUI) untuk konfigurasi ambang waktu, nada peringatan, dan resolusi kamera bagi developer. |

# METODE YANG DIGUNAKAN
MediaPipe Face Mesh adalah model deteksi wajah berbasis machine learning yang mampu memetakan 468 titik (landmark) pada wajah manusia secara 3D dan real-time.
Model ini menggunakan Deep Neural Network (DNN) untuk mengenali fitur wajah seperti mata, hidung, dan mulut dari citra kamera.

Dalam proyek Deteksi Kantuk, sistem memanfaatkan titik-titik di sekitar mata untuk menghitung Eye Aspect Ratio (EAR) — yaitu rasio antara tinggi dan lebar mata.
Jika mata mulai menutup, nilai EAR akan menurun — kondisi ini diidentifikasi sebagai tanda kantuk atau kelelahan.

# MENGAPA VIOLA–JONES (HAARCASCADE) TIDAK DIGUNAKAN
Metode Viola–Jones (Haarcascade) memang populer untuk deteksi wajah dasar, tetapi kurang sesuai untuk deteksi kantuk berbasis gerakan mata, karena:

**1.** Hanya mendeteksi area mata secara bounding box, bukan titik (landmark).

**2.** Tidak sensitif terhadap perubahan kecil, seperti kelopak mata yang menutup sebagian.

**3.** Rentan terhadap pencahayaan, posisi, dan sudut wajah.

**4.** Tidak bisa mendeteksi kondisi mata tertutup atau terbuka secara akurat.

# ALGORITMA SISTEM
<div align="center">
  <img src="assets/ALGORITMA.png" alt="DIAGRAM ALGORITMA" width="400">
</div>

# KONSEP SISTEM

Konsep sistem yang dikembangkan terdiri dari dua bagian utama:
### 1️⃣ Deteksi Mata dan Wajah
- Sistem menggunakan **MediaPipe Face Mesh** untuk mendeteksi wajah dan posisi mata secara **real-time**.  
- MediaPipe memetakan **468 titik landmark wajah**, dan sistem mengambil area mata untuk menghitung **Eye Aspect Ratio (EAR)**.  
- Nilai EAR ini menjadi dasar untuk mengetahui apakah mata dalam kondisi terbuka atau tertutup.
### 2️⃣ Penentuan Parameter Mengantuk
- Nilai **EAR** dibandingkan dengan ambang batas tertentu (contoh: **0.22**).  
- Jika **mata tertutup selama lebih dari 3 detik**, sistem akan mendeteksi kondisi **mengantuk**.  
- Ketika kondisi tersebut terdeteksi, sistem akan menampilkan **notifikasi peringatan** dan mengaktifkan **alarm suara** untuk memperingatkan pengguna.

# UML USE CASE 
<div align="center">
 <img src="assets/UML Project Deteksi Ngantuk.png" alt="UML" width="400">
</div>

Ketika aplikasi dijalankan, system akan menampilkan gui pengaturan
- System akan menampilkan gui untuk mode user.
- Jika pengguna mengubah mode user ke mode developer, system akan menampilkan gui untuk memasukkan pasword.
- Pengguna memasukkan password, system akan memverifikasi password.
- Jika salah akan menampilkan “password salah”, jika benar maka system akan mengubah tampilan gui pengaturan developer.

Dalam mode developer
- Pengguna bisa mengatur pengaturan seperti resolusi kamera, nada dering, waktu kantuk dan batas kedipan kantuk.
- Jika pengguna menekan tombol start, maka system akan menyimpan pengaturan yang telah ditetapkan kemudian akan mengakses kamera.
- System akan menampilkan kamera untuk mendeteksi kantuk.
- System akan mendeteksi kantuk berdasarkan mata pengguna, jika mata tertutup selama beberapa detik akan dideteksi kantuk dan akan membunyikan alarm sementara.
- Jika system mendeteksi kantuk lagi dan melebihi batas kantuk, system akan membunyikan alarm untuk istirahat.

Dalam mode user
- Jika pengguna menekan tombol start, maka system akan menetapkan pengaturan secar default kemudian akan mengakses kamera.
- System akan menampilkan kamera untuk mendeteksi kantuk.
- System akan mendeteksi kantuk berdasarkan mata pengguna, jika mata tertutup selama beberapa detik akan dideteksi kantuk dan akan membunyikan alarm sementara.
- Jika system mendeteksi kantuk lagi dan melebihi batas kantuk, system akan membunyikan alarm untuk istirahat.

# KELEBIHAN MEDIAPIPE
  - Real-time dan Ringan
  - Akurasi Tinggi
  - Tidak Membutuhkan Perangkat Khusus
  - Open Source dan Mudah Diintegrasikan
# KEKURANGAN MEDIAPIPE
  - Sensitif Terhadap Pencahayaan
  - Kinerja Turun Saat wajah Tidak Menghadap Kamera
  - Tidak Mendeteksi Tanda Lain dari Ngantuk
