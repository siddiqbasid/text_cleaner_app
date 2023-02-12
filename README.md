# text_cleaner_app

API ini secara umum berfungsi untuk melakukan cleansing data teks dengan 3 pilihan input output data:
1. Input Text : User menginputkan teks secara manual dan memilih opsi cleansing data. Jika dijalankan, aplikasi akan mengeluarkan output teks hasil cleansing data.
2. Input Text from CSV : User mengupload file CSV atau memilih teks dari file CSV yang telah disediakan dan memilih opsi cleansing data. Jika dijalankan, aplikasi akan mengeluarkan output teks hasil cleansing data.
3. Input Multiple Text from CSV : User mengupload file CSV atau memilih teks dari file CSV yang telah disediakan lalu aplikasi secara otomatis akan mengeluarkan output teks hasil cleansing data. Selain itu aplikasi juga menampilkan barchart 5 kata yang sering muncul dan menampilkan wordcloud.

Data cleansing yang dapat dilakukan oleh aplikasi ini adalah:
1. Remove Emoji : Menghapus emoji baik yang berformat unicode maupun UTF-8
2. Lowercase : Membuat semua huruf menjadi huruf kecil (lowercase)
3. Three or More : Menormalkan kata yang melakukan penulisan huruf yang sama secara berurutan. Misalnya : siaaaap --> siap
4. Stemming : Mencari kata dasar dari tiap kata dengan menghilangkan imbuhan yang melekat pada kata tersebut. Misalnya : mencintai --> cinta
5. Tokenization : Membagi teks yang panjang menjadi kata per kata
6. Normalization (Kamus Alay) : memperbaiki kata slang menjadi kata baku sesuai data yang ada pada "Kamus Alay". Misalnya : bakalan --> akan; aj --> saja
7. Remove Number : Menghapus angka
8. Remove Punctuation : Menghapus tanda baca dan white space
9. Stopwords : Menghapus kata umum yang biasanya muncul dalam jumlah besar dan dianggap tidak memiliki makna. Misalnya : aku, dan, kamu

Fitur tambahan dari API ini adalah melakukan update database Kamus Alay dan Stopwords. Data barchart dan wordcloud dapat digunakan sebagai bahan pertimbangan dalam melakukan update database Kamus Alay dan Stopwords.                        
