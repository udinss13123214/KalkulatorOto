# Kalkulator Otomatis ( For Education )

Cara kerja :
ketika file kalukalorotoql.exe dieksekusi maka akan ada 2 kotak yang akan muncul. 1 kotak akan sebagai menu dan 1 persegi panjang hitam transparan, Taruh persegi panjang transparan itu disoal
kemudian klick play untuk looping ( mendeteksi otomatis ) anda bisa klick tombol "cek" untuk mengecek tessaract-OCR nya dapat bekerja atau tidak.

Solusi ketika eror :
apabila anda klick cek tidak memperlihatkan bilangan ada 2 kemungkinan eror 
1.soal terlalu kecil 
2. anda belum ada tessaract-OCR 
( jika anda sudah mempunyai file Tessaract-OCR silahkan ganti code yang dipython bagian "pytesseract.pytesseract.tesseract_cmd = r"Direktori lengkap anda hingga tesseract.exe" dan hapus "import os" jika 
direktori Tessaract-OCR nya berbeda. Kalau berada disatu folder dengan file utama maka tidak ada yang harus diganti, apabila anda ingin menjalankan code melewati "python nama file" pada terminal pastikan anda sudah mempunyai library python. eror akan muncul didalam terminal/powershell, cukup klick pada function yang tidak bisa saja 1x dikarenakan kemungkinan eror akan muncul panjang )

Kelemahan :
1.hanya bisa mengerjakan matematika dasar ( 2+2= 4 | + x / - ) 
2.terkadang eror tidak mendeteksi terjadi ketika pada 6 soal dikerjakan 1x eror
3.kemungkinan eror ketika file .exe nya dikeluarkan dari folder dist/ 
( apabila tidak terbaca maka anda bisa ke solusi no 2 diatas )

anda bisa donwload lengkap sudah dengan tessarect-OCR library  python terpisah.
(https://www.mediafire.com/file/j6zxy6apl60rrqg/kalkulator+otomatis.zip/file)
