import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def chat(question):
    
   client = OpenAI(
      api_key=os.getenv("openai_key"), 
   )
   system_message = "You are a research assistant that can help user to do their research writing. Please follow and help the user needs."
   messages = [{"role": "system", "content": system_message}]
   messages.append({"role": "user", "content": question})
   completion = client.chat.completions.create(
      model="gpt-4o-2024-08-06",
      seed=42,
      messages=messages,
      max_tokens=16384
   )
   response_content = completion.choices[0].message.content
   prompt_tokens = completion.usage.prompt_tokens
   completion_tokens = completion.usage.completion_tokens
   total_tokens = completion.usage.total_tokens
   print("Token usage report:")
   print(f"\t- Prompt tokens: {prompt_tokens}")
   print(f"\t- Completion tokens: {completion_tokens}")
   print(f"\t- Total tokens: {total_tokens}")
   print("Pricing:")
   input_cost = (int(prompt_tokens) * 0.00250) / 1000
   output_cost = (int(completion_tokens) * 0.01000) / 1000
   total_cost = input_cost + output_cost
   print(f"\t- Input tokens cost: ${input_cost:.5f}")
   print(f"\t- Output tokens cost: ${output_cost:.5f}")
   print(f"\t- Total cost: ${total_cost:.5f}")
   return response_content

def prompt_template():
   template = """
<paper>
# Does Embedding Dimension Matter on Information Retrieval? Optimizing Lightweight Retrieval-Augmented Generation for Health Chatbots in Ampalu and Apar Villages with Minimal Computational Resources

## Introduction
1. **Background and Motivation**
   - Overview of the significance of health chatbots in rural healthcare settings.
   - Introduction to Ampalu and Apar Villages and their healthcare challenges.
   - Challenges with minimal computational resources.
   - Introduction to Retrieval-Augmented Generation (RAG) models.
   - Importance of Retrieval-Augmented Generation (RAG).

2. **Research Question**
   - Why the embedding dimension might impact the performance of information retrieval?
   - Does embedding dimension affect the performance of RAG models in low-resource environments?

3. **Objectives**
   - To explore the effect of embedding dimensions on RAG for health chatbots.
   - To optimize RAG for health chatbots in Ampalu and Apar with constraints.
   - To evaluate the impact of embedding dimensions on performance.

## Related Works
1. **Overview of Health Chatbots and Their Applications**
   - Overview of existing health chatbot implementations.
   - Key features and benefits.
   - Case studies in similar resource-constrained settings.

2. **Embedding Dimensions and Their Importance**
   - Explanation of embedding dimensions in natural language processing.
   - Previous studies on embedding dimensions affecting model performance.

3. **Retrieval-Augmented Generation (RAG)**
   - Explanation of RAG and its benefits in NLP tasks.
   - Description of RAG mechanisms.
   - Recent advancements in RAG-based systems.

4. **Challenges with Computational Resources**
   - Discussion on constraints in deploying AI in rural settings.
   - Strategies for efficiency improvement in low-resource areas.

5. **Applications in Rural Healthcare**
   - Review of chatbots in rural and underserved areas.
   - Specific challenges in deploying technology in Ampalu and Apar.

## Methodology
1. **Study Design**
   - Description of the experimental framework and study context.

2. **System Architecture**
   - Description of chatbot architecture using RAG.
   - Discussion of selected embedding models and techniques.

3. **Embedding Dimension Analysis**
   - Selection of different embedding dimensions for experimentation.
   - Outline of criteria for selecting optimal embedding size.

4. **Data Collection and Preprocessing**
   - Sources of health-related data for Ampalu and Apar villages.
   - Preprocessing steps and data augmentation techniques.

5. **Evaluation Metrics**
   - Definition of metrics used to evaluate chatbot performance.
   - Justification for each metric in the context of the study.


## Experiments
1. **Experimental Setup**
   - Description of environment and tools used (Including Hardware and software environment).
   - Configurations for different embedding dimensions.

2. **Procedure**
   - Step-by-step explanation of the experimental process.
   - Variability in embedding dimensions and conditions tested.
   - Comparison across different embedding dimensions.

3. **Benchmarks**
   - Baseline models for comparison.
   - Justification of chosen benchmarks.
   - Controlling external variables for a fair assessment.

## Results and Discussion
1. **Performance Analysis**
   - Quantitative results for different embedding dimensions.
   - Impact on retrieval and generation quality.
   - Analysis of performance differences across configurations.

2. **Resource Utilization**
   - Analysis of computational efficiency and resource usage.
   - Trade-offs between performance and resource demands.

3. **Implications for Health Chatbots**
   - Discuss how embedding dimension influences chatbot efficacy.
   - Implications for health communication in rural settings.

4. **Comparative Analysis**
   - Comparison with existing models and solutions.
   - Advantages and identification of potential study limitations of the proposed approach.
   - Challenges encountered during implementation.

5. **Recommendations for Future Research**
   - Suggestions for further exploration in embedding dimension optimization.
   - Suggestions for further exploration in low compute resource application.


## Conclusion
1. **Summary of Findings**
   - Recap the significant outcomes of the study.
   - Highlight key insights on embedding dimensions and performance.

2. **Contribution to Field**
   - Highlight the study's contribution to chatbot optimization and rural healthcare.

3. **Practical Implications**
   - Discuss how the findings can improve chatbot deployment in Ampalu and Apar.

4. **Final Thoughts**
   - Concluding remarks on the study's impact and future potential.
   - Suggestions for further studies on embedding dimensions for low compute resource.

</paper>
Based on the paper outline above that are enclosed using xml tag, help me create some query to search for related works, other works than can be my references.

   """
   return template


def read_md_file(file_path):
   with open(file_path, 'r') as file:
      return file.read()

if __name__ == "__main__":

   # literature_type = "mixture-of-expert"
   # file_name = "From Sparse to Soft Mixtures of Experts"
   doc = read_md_file('paper/references/A Deep Look into neural ranking models for information retrieval.md')
   # prompt = prompt_template()
   prompt = """
I have an interview, help me extract information about this company. I will give you some data.

<data_1>

Home
›
About Us
About Us
Aksoro is an Entrepreneur Education Platform.
Founded in 2019, Aksoro has launched tens of books and classes that become national best sellers in Indonesia, with more than 25.000 entrepreneurs joining the Aksoro ecosystem.


Bring Impact
From The Best In Country














Our mission is to bridge
THE GAP.

Our mission is to bridge the knowledge & network gap among small & medium businesses in Indonesia. 


Opening access to tried and tested methods in business.


Opening access to networks that can help them grow & scale faster.


More than 50 mentors and speakers share their knowledge and experience on our platform.

Super Impact
From Our Superteam






Discuss with our friendly team
Get in touch with us
Jl. Pasir No.35, Patuk, Banyuraden, Gamping, Sleman, Yogyakarta

Mon to Fri: 08:30 – 17:30

0821-3153-3535

care@aksoro.co.id

Name

Email

Message




PT. Aksara Juara Nusantara

Aksoro Business School adalah platform edukasi bisnis yang memfasilitasi para pengusaha untuk bertemu dan belajar langsung dari orang-orang hebat yang menjadi guru impian mereka.

Programs
Workshop for Business Owner

Workshop for Team

Business Coaching

Superteam Picnic

Community Development

Books
Semua bisa diatur

Scale Up Jilid 1

Branding 360

Premium Ebook

Company
About us

Blog

Why Aksoro

Collaborate

Career

© 2024 Aksoro Juara Nusantara. All Rights Reserved
</data_1>
<data_2>

Strategi Ampuh Jadi Nomor 1 di Pasar Lewat Branding dan Marketing Tepat Sasaran: Budget Irit, Cuan Sebukit
Strategi Ampuh Jadi Nomor 1 di Pasar Lewat Branding dan Marketing Tepat Sasaran: Budget Irit, Cuan Sebukit
12-13 Oktober 2024
08.00 – selesai WIB
Jakarta
Learn More: Strategi Ampuh Jadi Nomor 1 di Pasar Lewat Branding dan Marketing Tepat Sasaran: Budget Irit, Cuan Sebukit
Kesempatan Langka!  Belajar Culture Terbaik Langsung dari XL Axiata dan Bluebird!
Kesempatan Langka!
Belajar Culture Terbaik Langsung dari XL Axiata dan Bluebird!
Solusi untuk para owner dan HR bisa belajar cara implementasi culture agar bisnis terus tumbuh dan sustain!
Learn More: Kesempatan Langka!
Belajar Culture Terbaik Langsung dari XL Axiata dan Bluebird!
FORMULA JITU BIKIN BISNIS PLAN YANG MATANG BUAT 3 TAHUN KE DEPAN
FORMULA JITU BIKIN BISNIS PLAN YANG MATANG BUAT 3 TAHUN KE DEPAN
Premium Online Workshop
CEO MASTERPLAN
How to Transform Your Vision into Strategic Action

16-17 Oktober 2024
13.00 – 17.30 WIB
Learn More: FORMULA JITU BIKIN BISNIS PLAN YANG MATANG BUAT 3 TAHUN KE DEPAN
HOW TO BOOST YOUR EXPONENTIAL BUSINESS GROWTH
HOW TO BOOST YOUR EXPONENTIAL BUSINESS GROWTH
Premium Workshop AKSORO x IGNASIUS JONAN : 4 Strategi Proven Gedein Bisnis Yang Udah Gede
Learn More: HOW TO BOOST YOUR EXPONENTIAL BUSINESS GROWTH

PT. Aksara Juara Nusantara

Aksoro Business School adalah platform edukasi bisnis yang memfasilitasi para pengusaha untuk bertemu dan belajar langsung dari orang-orang hebat yang menjadi guru impian mereka.

Programs
Workshop for Business Owner

Workshop for Team

Business Coaching

Superteam Picnic

Community Development

Books
Semua bisa diatur

Scale Up Jilid 1

Branding 360

Premium Ebook

Company
About us

Blog

Why Aksoro

Collaborate

Career

© 2024 Aksoro Juara Nusantara. All Rights Reserved

</data_2>

<data_3>


BUKAN PLATFORM EDUKASI BISNIS TERBESAR DI INDONESIA
Tapi paling bagus reviewnya, paling banyak rekomendasinya, dan paling banyak jumlah pesertanya dalam setahun terakhir!


Learn More
Our Programs



Rating Tertinggi di Edukasi Bisnis

Andika Fahrurozi
5 months ago
Workshopnya lebih dari ekspektasi, next ajak tim leader untuk asah skillset dengan Aksoro 🔥🔥🔥🙏

Armand Ramadhan
5 months ago
It was super fun yet the most insightful program i’ve ever joined so far. At first I thought it was going to be “oh thats kind of program.” Turns out it was different!!! It was all worth. Thank You Aksoro for the great and unforgettable experience 😍

Mianty Henna
5 months ago
2 hari bersama Aksoro benar-benar luar biasa. Pengalaman, pelajaran, pengetahuan yang diperoleh sangat banyak. Bagaimana bekerja sama dan memahami orang lain. Problem solving dari yang tidak mungkin menjadi mungkin. Aksoro keren. 😍😍

Yin Sachrulli
5 months ago
Joining the Scale Up 2.0 with Mr. Ignasius Jonan as the main speaker was a very great experience. I learn a lot from the master of transformation himself. Good stuff!

Nur Liviana
5 months ago
Alhamdulillah 2 hari mengikuti kelas KPI masterclass Aksoro sangat-sangat bermanfaat bangettttt dapet ilmu baru dan terbantu bangettttt ❤️❤️❤️ Pak Himawan menjawab pertanyaan dari peserta sangat detailllll, sukak dehhh❤️ Ini sudah ke 2 kalinya aku ikut kls pelatihan dari Aksoro, next ikut scale up 2.0 nich

Masayu Yulinvinanda
5 months ago
Luar biasa acara HRD Masterclass pembicaranya bukan cuma teori tapi beneran praktek. Daging banget! Recommended buat ikutan HRD Masterclass 😍😍

Dave Dabito
5 months ago
The Great Sales Formula : The best training for growing your skill and competency

5,0

Based on 1073 reviews


Aksoro Adalah Kumpulan Kekuatan

Kami Mengumpulkan Orang-orang Hebat
untuk Mengajarkan Anda Cara Main di Level Berikutnya!

ANDI AISYAH ALQUMAIRAH

Corporate Culture Identity & Employer Branding XL Axiata

STEPHANIE REGINA

Founder and CEO of Haloka Grup Indonesia
Salah satu branding expert terbaik di Indonesia.

DWIWAHYU HARYO SURYO

Chief Supply Chain Officer & BoD Mie Gacoan.

KOKO HADIONO

25++ Years Experience in FnB Industry Former Top Management Global Brand Fast Food

ALDILA SEPTIADI

Digital Group Head of Marketing Strategy & Technology PT Erajaya Swasembada Tbk

ASMARANDHANY

Certified Leadership & Team Development Coach, 12+ Years

MUHAMMAD ISMAIL

CEO of Zahir Internasional

BUDI ISMAN

Ex-Direksi at Coca Cola Amatil & Sari Husada (SGM), Founder @Biznis.id, Guru Bisnis, dan Angel Investor
Super Impact!

Signature Programs
Workshop dan Bootcamp yang dirancang untuk bikin bisnis lari kencang.

Kelas Owner Bisnis
View More
Bertemu dan belajar dari orang-orang hebat yang bisnisnya juga hebat. Kuasai ilmu dan kebijaksanaan bisnis yang terbukti ngefek abis.

Strategi Ampuh Jadi Nomor 1 di Pasar Lewat Branding dan Marketing Tepat Sasaran: Budget Irit, Cuan Sebukit
HOW TO BOOST YOUR EXPONENTIAL BUSINESS GROWTH
FORMULA JITU BIKIN BISNIS PLAN YANG MATANG BUAT 3 TAHUN KE DEPAN

Kelas Superteam
View More
Bikin tim makin pinter, bisnis jadi banter. Lompatan omset terjadi saat kita punya tim yang bisa diandalkan!

Kesempatan Langka!  Belajar Culture Terbaik Langsung dari XL Axiata dan Bluebird!

Super Impact!

Literally Bukan Buku Biasa

“We make difficult things simple. Buku-buku dengan konsep before-after. Membuat hal sulit jadi sederhana dan mudah diikuti. Berorientasi pada efek kenaikan omset. ”


Buku Scale Up
Buku panduan wajib untuk yang mau mulai bisnis. Mulai dari 0 sampai tembus omset 400 jt/bulan. Dipandu dari memilih produk, cara menjual, cara meningkatkan kapasitas, sampai caranya bertahan dan terus berkembang.
Learn More: Buku Scale Up

Branding 360˚ Workbook
Buku panduan membangun branding untuk scale up bisnis, dengan 3 langkah mudah yang holistik dan sistematis.
Learn More: Branding 360˚ Workbook

Semua Bisa Diatur
Paket belajar lengkap bagi owner bisnis untuk mengelola timnya menjadi superteam. Superteam yang dapat diandalkan untuk menumbuhkan perusahaan. Superteam yang happy, produktif dan militan dalam bekerja.
Learn More: Semua Bisa Diatur

Selami perkataan tulus para alumni
DAMPAK YANG LUAR BIASA BAGI MEREKA

Selami perkataan tulus para alumni
KAMI BERBAHAGIA DENGAN PERTUMBUHAN BISNIS MEREKA
Join the Growth Club

Pintu untuk bertemu dengan ribuan pebisnis hebat
Networking dan bertukar nilai, dengan ribuan pebisnis hebat di komunitas alumni kami. Sebuah komunitas yang saling mengangkat ke atas

Learn More


Buka peluang bisnis baru lewat business matching & elite gathering.


Tingkatkan omset & profit dengan info trend bisnis terupdate dari alumni hebat.


Buka koneksi dengan alumni pilihan lewat Meetup offline.

Kami membantu ratusan perusahaan memaksimalkan peluang dan potensialnya




























As Featured In






Masih bingung mau join kelas yang mana? ngobrol dengan kami
Learn More

PT. Aksara Juara Nusantara

Aksoro Business School adalah platform edukasi bisnis yang memfasilitasi para pengusaha untuk bertemu dan belajar langsung dari orang-orang hebat yang menjadi guru impian mereka.

Programs
Workshop for Business Owner

Workshop for Team

Business Coaching

Superteam Picnic

Community Development

Books
Semua bisa diatur

Scale Up Jilid 1

Branding 360

Premium Ebook

Company
About us

Blog

Why Aksoro

Collaborate

Career

© 2024 Aksoro Juara Nusantara. All Rights Reserved

</data_3>

<data_4>
Buku Scale Up

Rahasia Tembus 400 Juta Sebulan
Cek Daftar Isi
Anda ingin jadi pengusaha, tapi:
😥 Masih takut mulai karena minim ilmu dan gak ada pengalaman
😥 Gak tau mau bikin produk apa
😥 Bingung nanti cara jualinnya gimana
😥 Modal juga masih terbatas

Nah, itu tandanya kamu harus membaca buku ini.

Ibaratnya google maps, buku ini akan menuntun kamu dalam memulai bisnis. Dari meriset produk sampai caranya mencapai level keluar zona UMKM.

Anda sangat beruntung dapat informasi buku ini
Buku Scale Up ini berat. Ini buku praktek, bukan buku motivasi.
Untuk mendapatkan manfaat dan dampak nyata, Anda harus baca perlahan isi bukunya, bahkan mungkin di tengah-tengah Anda harus BERHENTI membaca buku ini.

Spesifikasi Buku:
Softcover, berwarna
11 Bab, 376 halaman

Mindset
Bagaimana menata mindset untuk Scale Up

Riset
Bagaimana caranya riset, mencari produk, dan memilih bisnis

Talent
Bagaimana menarik talenta terbaik supaya mau kerja dengan Anda

Orang yang tepat
Bagaimana menempatkan orang yang tepat di posisi yang tepat

Tim Solid
Bagaimana mengelola tim supaya solid, produktif, dan agresif dalam memajukan perusahaan

Winning formula
Bagaimana caranya mendapatkan WINNING FORMULA untuk bisnis Anda

image 8662
Rahasia Scale Up Bisnis Kami Bongkar Habis
Perbedaan besar yang akan Anda rasakan ketika memiliki buku ini adalah ciri khasnya yang menonjolkan detail dalam setiap penjelasan.


How this book can help
Penjelasannya Detail
Menjelaskan caranya mencari ide bisnis hingga bisa scale up

Bahasa yang Mudah Dipahami
Menggunakan bahasa Indonesia yang mudah dipahami dan dibuat sesimpel mungkin.

Step by Step
Buku ini tidak mengajarkan hal-hal mudah untuk mendapatkan hasil instant.

Bisnis Bertahan Lama
Buku ini menjelaskan langkah-langkah untuk menjadikan bisnis Anda meningkat permanen.

Keluar dari Zona UMKM
Siapapun yang 100% fokus dan bisa menyelesaikan semua check listnya. Pasti bisa merasakan progress kemajuan.




Siapa yang harus segera miliki, baca dan praktik buku Ini secepatnya?
🔥 Pebisnis dan Wirausaha: yang ingin membangun bisnis mulai dari mencari produk yang tepat dan cara agar keluar dari zona UMKM

🔥 Pemilik Usaha Kecil Menengah: yang ingin memperkuat bisnis mereka untuk meningkatkan visibilitas dan kepercayaan customer.

🔥 Pemilik Bisnis Online: yang ingin memahami bagaimana agar bisnis tetap bertahan dan mendapat respon positif pasar.

🔥 Mahasiswa dan Pelajar: yang sedang mempelajari bisnis, pemasaran, atau komunikasi dan ingin memulai membangun bisnis

🔥 Marketing Professionals: yang ingin mendalami lagi dan mengembangkan bisnisnya agar terus naik level

🔥 Anda: yang ingin dituntun dalam membangun bisnis dari dasar hingga menjadi sebuah bisnis besar.

Lihat Reviewnya
4 MANFAAT ANDA MEMBACA BUKU SCALE UP

Pebisnis Sukses
Sukses Menjadi Pebisnis yang Diinginkan Banyak Orang


Tau Caranya
Menemukan FAKTOR X keberhasilan dalam Scale Up bisnis.


Bisnis Terukur
Sanggup menilai apakah bisnis yang Anda lakukan sudah berjalan dengan benar.


Membuka Peluang
Mengidentifikasi peluang baru dan mengembangkan inovasi bisnis

SIAPA ORANG GILA YANG RELA MEMBONGKAR ISI DAPURNYA?

ALFAN ROBBANI

Man behind 10 fast growing brand

Man behind 10 fast growing brand, CEO Muda penyelamat hutang perusahaan milyaran, berhasil survive & berkembang.


AFRIG WASISO

Founder & CEO Aksoro Group

“Scale Up Mastermind”. Peraih HP Indigo Innovation Award 2019 se-Asia Pasifik. Sulap 9 UMKM menjadi market leader.

Buku ini ditulis oleh 2 CEO muda dengan pengalaman lebih dari 13 tahun di dunia bisnis. Mereka berdua berhasil membangun dan membesarkan belasan bisnis sendiri dan juga partner-partnernya. Menggunakan formula proven yang sudah mereka tulis semuanya di buku ini.

🔥 13 tahun pengalaman dalam analisis dan strategi bisnis.
🔥 Membantu lebih dari 9 UKM Indonesia untuk menjadi pemimpin industri (market leader) di bidangnya.
🔥 Menjadi CEO termuda dan mampu melunasi hutang perusahaan milliaran, dll

Ya, Saya Mau Bukunya!
Our Customer
Testimonial
image 8674
image 8675
image 8676
image 8677
REKAP SEMUA BONUS YANG ANDA DAPATKAN
✅ Ebook Premium “How To Start A Business” 👉 Senilai Rp200.000
✅ Ebook Premium “5 Level Leadership” 👉 Senilai Rp170.000
✅ Ebook Premium “31 Cara Berbeda Menulis Headline Yang Memikat” 👉 Senilai Rp150.000
✅ Ebook Premium “Rahasia Hiring : Daftar Pertanyaan Untuk Mengetahui Karakter Seseorang” 👉 Senilai Rp130.000
✅ Ebook Premium “Mindset Is Everything” 👉 Senilai Rp130.000
✅ Ebook Premium “Marketing Otak Kiri dan Otak Kanan” 👉 Senilai Rp150.000
✅ 12 Video Ekslusif Aksoro Tentang Dunia Bisnis 👉 Senilai Rp1.250.000

TOTAL NILAI BONUS Rp. 2.180.000
Dapatkan Semua Bonus di Atas dan Keuntungan Lainnya.,

PROMO TERBATAS DISKON 50%
Bonus Yang Anda Dapatkan
Kenapa jika Anda miliki bukunya hari ini akan terasa begitu menguntungkan dibandingkan nanti atau lain kali?

Semakin cepat Anda miliki bukunya, semakin cepat Anda amalkan isinya dan semakin cepat pula Anda petik hasilnya.

Apalagi hari ini masih ada promo, kapan lagi bisa dapat buku hebat dengan harga hemat.

00 : 00 : 00 : 00
Learn More`
Nikmati Harga Promo
KHUSUS UNTUK ANDA

Harga Diskon Spesial untuk hari ini + 7 Bonus Premium
Rp. 314rb
628.000
Softcover, 11 Bab, 379 halaman

Buku pelengkap: Standard Kemampuan Khusus Scale Up

Golden Invitation: Join komunitas pengusaha yang dikelola oleh Aksoro

Bonus senilai Rp2,180,000 (jika transaksi sekarang)

Ya, Saya Mau Bukunya!
Terima kasih sudah memesan Buku Scale Up
Semoga ilmu di buku ini bermanfaat dan dapat membantu bisnis Anda scale up.
Kami tunggu review, feedback dan testimoni Anda setelah baca dan praktek ya 😉

Apabila ada pertanyaan lanjutan, silahkan hubungi

Customer Care Aksoro
© Copyright 2024 Aksoro – All Rights Reserved
</data_4>


<data_5>

Strategi Ampuh Jadi Nomor 1 di Pasar Lewat Branding dan Marketing Tepat Sasaran: Budget Irit, Cuan Sebukit
12-13 Oktober 2024
08.00 – selesai WIB
Jakarta

Inilah Saatnya Bisnis Anda jadi Market Leader yang paham banget target market, kreatif, bertanggung jawab, dan berdampak!
Gak semua Business Owner tahu caranya bikin strategi marketing yang efektif dan branding yang kuat. Jadi, di workshop ini Anda akan diajarin:

✅ Strategi branding dan marketing yang terarah dan sesuai dengan bisnis Anda
✅ Nentuin Brand Purpose dan Brand Vision agar value bisnismu tersampaikan dan mencapai customer loyalty bahkan customer advocate
✅ Cara manfaatin algoritme media sosial untuk strategi marketing yang tepat sasaran
✅ Trik endorse anti boncos
✅Keluar dan terhindar dari persaingan harga yang gak sehat

“Focus on long-term success, but be willing to make short-term adjustments to get there.” – Simon Sinek


20 : 15 : 6 : 37
Alasan kenapa Marketing Mastermind sangat ideal untuk Anda:
Anda adalah Founder, CEO, atau Marketer yang punya tanggung jawab besar dalam pengembangan bisnis.
Sudah tahu branding dan marketing tapi masih belum bisa bedain dan mengimplementasikan dengan benar.
Merasa stuck bikin strategi, kehabisan ide marketing, dan kurang motivasi
Ingin menguasai pasar dan lebih unggul dari kompetitor.
Mendambakan punya networking berkualitas yang mungkin bisa jadi partner, mentor, bahkan customer Anda.
Impact setelah ikut Marketing Mastermind :
Paham sampai ke “dagingnya” branding dan marketing serta tahu pengimplementasiannya.
Lebih sat set merancang strategi marketing lebih terarah agar bisnis lebih efisien.
Percaya diri bikin marketing plan melalui materi yang diberikan dan menjelaskannya ke tim.
Melakukan cek kesehatan brand melalui BLUEPRINT yang diberikan untuk lebih memahami persepsi customer.
Ketemu orang baru yang bisa kasih manfaat buat bisnismu, entah jadi mentor, partner, atau bahkan customer!

Introduction to Business Model Canvas
Gimana membuat strategi pemasaran jadi lebih terarah agar target tercapai lebih mudah

Building Unique Selling Point
Strategi bikin produk atau layanan Anda jadi lebih menonjol, mudah dipahami, dan lebih menarik bagi customer

The Power of Community Collaboration
Teknik menjangkau dan meningkatkan reputasi brand di mata pelanggan dengan lebih personal dan relevan

Beating Social Media Algorithm
Cara cerdas menunggangi algoritma untuk kepentingan strategi marketing kita

Rumus Endorse Anti Boncos
Tracking keberhasilan dan optimalisasi endorsement agar budget tidak terbuang sia-sia

Emotional Buying Decision
Trik mempengaruhi alam bawah sadar konsumen agar segera close the deal

Brand Purpose Activation
Cara nentuin alasan utama mengapa brand kita ada agar kita beda gak sekedar beda

Crystal Clear Brand Vision Formula
Teknik membuat gambaran jangka panjang tentang brand kita akan seperti apa di masa depan

Positioning Hacks Formula
Breakdown cara mengubah dan menanamkan persepsi tentang produk atau jasa kita di kepala pelanggan

Business Appearance Consistency
Langkah membuat dan menjaga konsistensi branding (visual, voice, dan messages) di semua channel distribusi

Brand Audit Recipe
Rumus ngecek kesesuaian antara branding yang kita rancang dengan persepsi konsumen dan gimana mengatasinya

Serap Ilmu Mereka!
SPECIAL SPEAKER

ADYTHIA PRATAMA

Guerilla Marketing Strategist, IPO Consultant
Salah seorang pelopor strategi Guerilla Marketing di Indonesia dengan pengalaman lebih dari 10 tahun.
Guerilla Marketing Strategist, IPO Consultant
ADYTHIA PRATAMA
Founder & CEO PT Braja Biru Abadi ini merupakan salah seorang pelopor Guerilla Marketing di Indonesia.

Lewat strategi marketing ini beliau berhasil memenangkan penghargaan sebagai “Fastest Growing Aesthetic Clinic in Indonesia” pada tahun 2020.

Strategi marketing andalannya terkenal karena efisiensi penggunaan budget minimal namun hasilnya super maksimal.


STEPHANIE REGINA

Founder and CEO of Haloka Grup Indonesia
Salah satu branding expert terbaik di Indonesia.
Founder and CEO of Haloka Grup Indonesia
STEPHANIE REGINA
Founder & CEO Haloka Group Indonesia ini, lewat bisnisnya telah membantu mengembangkan ratusan ribu personal branding dan lebih dari 50 brand perusahaan seperti Danone, HMNS, dan Tokopedia membangun persepsi positif brand di pasar.

Beliau adalah seorang pakar branding yang juga pernah berkarir di Unilever sebagai seorang Brand manager.

Mengenal dunia marketing dan branding selama lebih dari 10 tahun, menjadikan beliau salah satu influencer bisnis dengan lebih dari 100K followers di Tiktok dan 40K followers di Instagram.

Early Bird
hanya 6,6jt

Rp11,5JT

Workshop offline praktek seru 2 hari full lengkap dengan modul materi, tools dan simulasi

Quality networking dan download ilmu langsung dari mentor-mentor hebat

Akses networking dan join komunitas dari berbagai industri

Premium seminar kit dan sertifikat

BLUEPRINT siap pakai untuk cek kesehatan brand

WORKSHEET untuk memilih strategi marketing yang tepat supaya ga salah nembak!

Gratis 2x lunch dan coffee break

All time sharing access dengan tim Aksoro

Daftar via Whatsapp
Kami membantu ratusan perusahaan memaksimalkan peluang dan potensialnya




























Rating Tertinggi di Edukasi Bisnis

Andika Fahrurozi
5 months ago
Workshopnya lebih dari ekspektasi, next ajak tim leader untuk asah skillset dengan Aksoro 🔥🔥🔥🙏

Armand Ramadhan
5 months ago
It was super fun yet the most insightful program i’ve ever joined so far. At first I thought it was going to be “oh thats kind of program.” Turns out it was different!!! It was all worth. Thank You Aksoro for the great and unforgettable experience 😍

Mianty Henna
5 months ago
2 hari bersama Aksoro benar-benar luar biasa. Pengalaman, pelajaran, pengetahuan yang diperoleh sangat banyak. Bagaimana bekerja sama dan memahami orang lain. Problem solving dari yang tidak mungkin menjadi mungkin. Aksoro keren. 😍😍

Yin Sachrulli
5 months ago
Joining the Scale Up 2.0 with Mr. Ignasius Jonan as the main speaker was a very great experience. I learn a lot from the master of transformation himself. Good stuff!

Nur Liviana
5 months ago
Alhamdulillah 2 hari mengikuti kelas KPI masterclass Aksoro sangat-sangat bermanfaat bangettttt dapet ilmu baru dan terbantu bangettttt ❤️❤️❤️ Pak Himawan menjawab pertanyaan dari peserta sangat detailllll, sukak dehhh❤️ Ini sudah ke 2 kalinya aku ikut kls pelatihan dari Aksoro, next ikut scale up 2.0 nich

Masayu Yulinvinanda
5 months ago
Luar biasa acara HRD Masterclass pembicaranya bukan cuma teori tapi beneran praktek. Daging banget! Recommended buat ikutan HRD Masterclass 😍😍

Dave Dabito
5 months ago
The Great Sales Formula : The best training for growing your skill and competency

5,0

Based on 1073 reviews


© Copyright 2024 Aksoro – All Rights Reserved
</data_5>

<data_6>

Kesempatan Langka!
Belajar Culture Terbaik Langsung dari XL Axiata dan Bluebird!
Solusi untuk para owner dan HR bisa belajar cara implementasi culture agar bisnis terus tumbuh dan sustain!

Mengapa Kita Harus Serius Menggarap Culture?​


80% masalah owner bisnis adalah masalah tim :

😡 Tim yang kurang produktif
😡 Tim yang sulit diatur
😡 Tim yang gak betahan, susah bertahan
😡 Tim yang kurang solid, banyak konflik
😡 Tim yang gak semangat belajar, gak suka training, gak lapar perbaikan
😡 Tim yang gak bisa berpikir dan bertindak seperti yang kita mau​

Maka, semua itu jawabannya CULTURE!

2 : 23 : 6 : 3
Belajar dari yang Terbaik
Kenapa Saya Perlu Belajar dari XL Axiata dan Bluebird?
XL Axiata adalah salah satu contoh perusahaan yang berhasil besar, dan makin besar karena culturenya yang sangat baik.
XL Axiata meraih segudang penghargaan nasional dan international salah satunya dari HR Asia award sebagai “Best Companies to Work for in Asia” selama 2 tahun berturut turut sejak 2023.


————————————————————————————————————-

Bluebird dinobatkan sebagai Asia’s Outstanding Company 2021 karena unggul dalam manajemen tim. 
Implementasi culture yang diterapkan oleh Bluebird bisa dirasakan hingga ke seluruh karyawan Blue Bird Group baik di lapangan (pengemudi) maupun di office..
Culture Bluebird yang selalu menjadikan prioritas utama dalam hal kualitas layanan hingga berhasil memborong 5 penghargaan WOW Service Excellent Award.
Belajar culture dengan metode yang powerfull! Kunjungan langsung, melihat dan merasakan bagaimana proses implementasi dan internalisasi culture dari perusahaan TOP Nasional yang bisnisnya sudah terbukti tumbuh besar dan sustain.

 

Case Study yang akan dibahas : 

Bedah purpose, vision, dan strategy perusahaan
Culture di perusahaan dan gambaran proses penyusunannya
Apa saja core values dan key behavior perusahaan
Bagaimana menyelaraskan employee value dengan value perusahaan hingga ke customer
Kumpulan program implementasi culture dan cara eksekusinya agar berhasil
CX Promise dan CX Commitment : Bagaimana culture bisa berimpact hingga ke customer experience
Keseruan Company Culture Bootcamp Batch Sebelumnya
image 9321
image 9322
image 9323
image 9324

ANDI AISYAH ALQUMAIRAH

Corporate Culture Identity & Employer Branding XL Axiata
Corporate Culture Identity & Employer Branding XL Axiata
ANDI AISYAH ALQUMAIRAH
Seorang profesional yang berdedikasi di bidang pemberdayaan dan pengembangan sumber daya manusia. Selama lebih dari 5 tahun, Kak Aisyah telah sukses menjalankan berbagai inisiatif yang berfokus pada peningkatan kapasitas individu.

Memulai kariernya sebagai pemimpin proyek pemberdayaan di berbagai komunitas, Kak Aisyah telah mengembangkan wawasannya hingga ke dunia korporasi. Kini, ia menjabati posisi Corporate Culture Identity di PT. XL Axiata Tbk.

Berkat keterampilan Kak Aisyah dalam mengembangkan SDM, perusahaan tersebut berhasil menyabet beragam prestasi. Di antaranya, “Best Companies to Work in Asia” dari HR Asia Award pada tahun 2023 dan 2024, dan “Diversity, Equity, and Inclusion Awards” di tahun 2024.

Kata Mereka yang Ikut di Batch Sebelumnya
image 9327
image 9328
image 9329
image 9330
Early Bird
hanya 4,8jt

6,8jt

Kesempatan langka bisa kunjungan privat ke XL Axiata dan Bluebird

Rasakan experience seru office tour dan sharing session materi culture untuk akselarasi pertumbuhan bisnis

Kapan lagi bisa tanya jawab case by case langsung dengan pemateri dari 2 big company ini

Full insight dan dapatkan banyak inspirasi untuk Anda terapkan di perusahaan

Akses networking dan join komunitas dari berbagai industri

Lunch and coffee break

Seminar kit dan sertifikat

Include tranportasi selama acara kunjungan

Pulang-pulang gak sabar pengen langsung action!

Daftar via Whatsapp
Kami membantu ratusan perusahaan memaksimalkan peluang dan potensialnya




























Rating Tertinggi di Edukasi Bisnis

Andika Fahrurozi
5 months ago
Workshopnya lebih dari ekspektasi, next ajak tim leader untuk asah skillset dengan Aksoro 🔥🔥🔥🙏

Armand Ramadhan
5 months ago
It was super fun yet the most insightful program i’ve ever joined so far. At first I thought it was going to be “oh thats kind of program.” Turns out it was different!!! It was all worth. Thank You Aksoro for the great and unforgettable experience 😍

Mianty Henna
5 months ago
2 hari bersama Aksoro benar-benar luar biasa. Pengalaman, pelajaran, pengetahuan yang diperoleh sangat banyak. Bagaimana bekerja sama dan memahami orang lain. Problem solving dari yang tidak mungkin menjadi mungkin. Aksoro keren. 😍😍

Yin Sachrulli
5 months ago
Joining the Scale Up 2.0 with Mr. Ignasius Jonan as the main speaker was a very great experience. I learn a lot from the master of transformation himself. Good stuff!

Nur Liviana
5 months ago
Alhamdulillah 2 hari mengikuti kelas KPI masterclass Aksoro sangat-sangat bermanfaat bangettttt dapet ilmu baru dan terbantu bangettttt ❤️❤️❤️ Pak Himawan menjawab pertanyaan dari peserta sangat detailllll, sukak dehhh❤️ Ini sudah ke 2 kalinya aku ikut kls pelatihan dari Aksoro, next ikut scale up 2.0 nich

Masayu Yulinvinanda
5 months ago
Luar biasa acara HRD Masterclass pembicaranya bukan cuma teori tapi beneran praktek. Daging banget! Recommended buat ikutan HRD Masterclass 😍😍

Dave Dabito
5 months ago
The Great Sales Formula : The best training for growing your skill and competency

5,0

Based on 1073 reviews


Frequently Asked Questions
Apa Bedanya Event Ini dengan yang Lain?
(1) Bukan hanya teori di kelas namun benar benar belajar dari lapangan. (2) Tergabung dalam sebuah komunitas yang bisa saling sharing terkait dengan penerapan culture
Apa Kerugian Jika Saya Tidak Ikut?
(1) Culture itu adalah hal fundamental. Its about time. Kalau mau diundur terus ya harus siap dengan konsekuensi masalah tim yang berulang. (2) Kesempatan visit ke 2 perusahaan terbaik, ga akan ada kesempatan ke-2.
© Copyright 2024 Aksoro – All Rights Reserved
</data_6>

<data_7>

FORMULA JITU BIKIN BISNIS PLAN YANG MATANG BUAT 3 TAHUN KE DEPAN
Premium Online Workshop
CEO MASTERPLAN
How to Transform Your Vision into Strategic Action

16-17 Oktober 2024
13.00 – 17.30 WIB

IDEALNYA, SEORANG PEBISNIS HARUS…
Punya rencana bisnis jangka panjang sampai 25 tahun ke depan. Sayangnya, belum banyak pebisnis yang BISA begitu. 

Bahkan yang sadar bahwa TUGAS UTAMA sebagai pucuk pimpinan bisnis adalah BIKIN STRATEGI, pun masih sedikit.

Memang, yang namanya bikin strategic planning gak gampang. Jangankan 25 tahun…3 tahun ke depan pun kita masih sering ngawang.

Udah bikinnya susah, implementasinya lebih ruwet lagi!

Join Now
“If You Fail to Plan, You Plan to Fail”
(Benjamin Franklin)

LOKASI
Online Via Zoom


WAKTU
16-17 Oktober 2024 13.00 – 17.30 WIB

25 : 4 : 5 : 48
Join Now
Beberapa tantangan ketika kita merumuskan strategi/bisnis plan tahunan:

Perubahan pasar yang cepat
Kompetisi yang makin ketat
Keterbatasan sumberdaya, dan
Ketidak-selarasan antara visi owner, strategi bisnis, dengan kegiatan tim sehari-hari.
Ujung-ujungnya pertumbuhan bisnis Anda terhambat, jalannya semakin lambat dan berat. 

Sebelum terlambat, itulah mengapa workshop CEO Masterplan ini sangat cocok untuk pebisnis seperti kita, yang ingin bisa merumuskan VISI dengan jelas, menjadi STRATEGIC & ACTION PLAN yang bisa dijalankan oleh seluruh tim di perusahaan.


Premium Workshop Online ini membantu Anda untuk:

Lepas dari kesulitan membuat dan menyesuaikan strategi tahunan perusahaan dengan perubahan pasar yang cepat.
Memudahkan implementasi strategi sampai ke level tim
 







 


Vision Clearing Formula
Cara seorang CEO/Founder/Owner merumuskan visi dengan jelas menjadi strategi yang matang.

360° Market Analysis
Membaca kebutuhan pasar saat ini termasuk menganalisis kompetitor dan kondisi global.

See the Future
Praktek merancang business plan yang sustainable dan memberikan lompatan pertumbuhan pada perusahaan.

One Heart Formula
Langkah demi langkah menyelaraskan strategi besaran perusahaan menjadi strategi tiap divisi dan action list individu.

Forming Resilient Team.
Bagaimana menjadikan tim kita sekumpulan orang-orang yang fleksibel dan adaptif sama perubahan.

Elevating Ownership & Milestone
Cara menempatkan orang yang tepat untuk eksekusi strategi, sekaligus merumuskan deadline dan target pencapaian kecil.

CEO Mentality Monster
Rahasia membangun mental tangguh dan respon tepat-cepat ketika strategi tidak berjalan sesuai rencana.

Belajar formula rahasia dan langkah-langkah membuatnya dari:
SPECIAL SPEAKER

BUDI ISMAN

Ex-Direksi at Coca Cola Amatil & Sari Husada (SGM), Founder @Biznis.id, Guru Bisnis, dan Angel Investor
Ex-Direksi at Coca Cola Amatil & Sari Husada (SGM), Founder @Biznis.id, Guru Bisnis, dan Angel Investor
BUDI ISMAN
Beliau adalah ex CEO dan Direktur 2 perusahaan consumer goods multinasional yang memiliki rekam jejak luar biasa.

Beliau juga seorang Founder dan CEO Biznis.id, sebuah platform belajar bisnis yang ditujukan untuk pengembangan UMKM. Beliau sudah melatih, membimbing, dan mengembangkan ribuan entrepreneurs Indonesia di lebih dari 50 kota.

Saat ini, Pak Budi banyak menghabiskan waktunya menjadi pengusaha, angel investor dan advisor di beberapa perusahaan rintisan tanah air.


MUHAMMAD ISMAIL

CEO of Zahir Internasional
CEO of Zahir Internasional
MUHAMMAD ISMAIL
Beliau adalah seorang pengusaha dan juga CEO PT Zahir Internasional, selama hampir 10 tahun.

Sebagai seorang CEO, beliau memiliki pengalaman yang komplit dalam berbagai business process seperti marketing, sales, dan business development.

Pengalaman dan expertise beliau dalam membuat business plan yang strategis dan berdampak pada growth perusahaan terbukti membawa Zahir terus berkembang dan menjadi salah satu perusahaan teknologi asli Indonesia yang mendunia dengan lebih dari 110.000 pengguna di 4 negara.

Early Bird
Rp1,499k/pax

6Juta

Framework and business plan templates for CEO

Feedback dan review tugas/praktek peserta langsung dari pemateri (Terbatas)

E-certificate

GRATIS softcopy alat praktek + materi komplit

GRATIS rekaman live e-course

BONUS Focus Group Discussion after event

Tanya via Whatsapp
Segera Daftar, Seat TERBATAS!
Isi Form Pendaftaran Dibawah:
Nama Lengkap
No. WhatsApp Anda
Email Anda
Nama Bisnis Anda

Metode Pembayaran:

 Bank Transfer

credit_card Credit Card
RINCIAN PESANAN:
CEO Masterplan (x1)
Rp6.000.000
Rp 1.499.000
Kode Unik
Rp85
Total
Rp1.499.085
Kami membantu ratusan perusahaan memaksimalkan peluang dan potensialnya




























Rating Tertinggi di Edukasi Bisnis

Andika Fahrurozi
5 months ago
Workshopnya lebih dari ekspektasi, next ajak tim leader untuk asah skillset dengan Aksoro 🔥🔥🔥🙏

Armand Ramadhan
5 months ago
It was super fun yet the most insightful program i’ve ever joined so far. At first I thought it was going to be “oh thats kind of program.” Turns out it was different!!! It was all worth. Thank You Aksoro for the great and unforgettable experience 😍

Mianty Henna
5 months ago
2 hari bersama Aksoro benar-benar luar biasa. Pengalaman, pelajaran, pengetahuan yang diperoleh sangat banyak. Bagaimana bekerja sama dan memahami orang lain. Problem solving dari yang tidak mungkin menjadi mungkin. Aksoro keren. 😍😍

Yin Sachrulli
5 months ago
Joining the Scale Up 2.0 with Mr. Ignasius Jonan as the main speaker was a very great experience. I learn a lot from the master of transformation himself. Good stuff!

Nur Liviana
5 months ago
Alhamdulillah 2 hari mengikuti kelas KPI masterclass Aksoro sangat-sangat bermanfaat bangettttt dapet ilmu baru dan terbantu bangettttt ❤️❤️❤️ Pak Himawan menjawab pertanyaan dari peserta sangat detailllll, sukak dehhh❤️ Ini sudah ke 2 kalinya aku ikut kls pelatihan dari Aksoro, next ikut scale up 2.0 nich

Masayu Yulinvinanda
5 months ago
Luar biasa acara HRD Masterclass pembicaranya bukan cuma teori tapi beneran praktek. Daging banget! Recommended buat ikutan HRD Masterclass 😍😍

Dave Dabito
5 months ago
The Great Sales Formula : The best training for growing your skill and competency

5,0

Based on 1073 reviews


Frequently Asked Questions
Kapan & Dimana Acara Ini Berlangsung?
Online Course ini akan diadakan online via Zoom. Pada tanggal 16-17 Oktober 2024
Acara Ini Cocok Untuk Siapa?
Sesuai yang kami infokan, Jika Anda Bisnis Owner/ CEO/Founder/Direkturs, Anda sangat cocok mengikuti acara ini
© Copyright 2024 Aksoro – All Rights Reserved
</data_7>

<data_8>

HOW TO BOOST YOUR EXPONENTIAL BUSINESS GROWTH
Premium Workshop AKSORO x IGNASIUS JONAN : 4 Strategi Proven Gedein Bisnis Yang Udah Gede
thumb-scu2.0-1
Selami perkataan tulus para alumni
DAMPAK YANG LUAR BIASA BAGI MEREKA
Halo CEO/Founder dan Bisnis Owners!
Apakah Anda merasakan hal yang sama seperti saya?

Alhamdulillah omset termasuk bagus.
Tapi udah lama ini gak naik-naik. Mentok.
Angkanya segitu-gitu aja. Stabil.
Padahal kalau liat pangsa pasar, harusnya masih sangat bisa berkembang.
Penasaran!
Pengen naikin lagi. Tumbuhin lagi. Gedein lagi.
Tapi udah coba berbagai cara, masih gagal-gagal juga.
Belum lagi, tim saya udah mulai kehilangan gairah.
Kayak udah puas, udah nyaman sama kondisi sekarang.
Nge-push nya semakin susah.
Semangatnya. Ngototnya. Gak kayak dulu lagi.

Anda sedang di posisi ini juga? Kalau iya, saya tau kita harus kemana…

LOKASI
Jakarta


WAKTU
Sabtu & Minggu, 5 – 6 Oktober 2024

Workshop Premium SCALE UP 2.0 Batch #4
Ignasius Jonan X Aksoro
13 : 23 : 5 : 33
Saya Daftar Sekarang
IGNASIUS JONAN x AKSORO Proudly Present
Premium Workshop SCALE UP 2.0 Batch #4
Dari Workshop Scale Up 2.0, Anda Mendapatkan:

Caranya menggerakkan tim agar mau berubah dan terus bertumbuh
Memaksimalkan potensi tim agar mampu mencapai target yang tinggi
Strategi memajukan bisnis yang low budget high impact
Cara ber-networking yang efektif untuk ekspansi bisnis
Networking yang luas dan berkualitas dengan ratusan pebisnis dari seluruh Indonesia

How to be an Ultimate Leader Ala Pak Jonan
180 Minutes

Bagaimana menjadi seorang leader yang mampu membawa perbaikan bisnis jangka pendek dan panjang. | Bagaimana memastikan perbaikan terus dilakukan bahkan ketika kita sudah tidak aktif di perusahaan. | Excellence Execution: Bagaimana meningkatkan kualitas eksekusi tim, mulai dari yang level atas sampai office boy.

How to Unleash Your Team's High Potential
180 Minutes

Metode memaksimalkan potensi tim yang biasa-biasa saja, agar mampu mencapai target setinggi-tingginya. | Menemukan hot button tim internal supaya selalu lapar dengan pencapaian-pencapaian baru.

How to recruit the Game Changer for Scale Up
120 Minutes

360° Recruitment Process : Teknik menemukan, mendekati, dan memenangkan game changer untuk join ke perusahaan Anda. | Formula Interview Anti Ketipu: Bagaimana menilai seorang kandidat benar-benar bagus atau tidak dalam waktu 30 menit saja.

How to Master Guerilla Networking Strategy
120 Minutes

Cara menemukan, memperkenalkan diri, dan berteman dengan orang yang bisa membuat bisnis kita naik kelas. | Cara close the deal dan menjaga hubungan jangka panjang dengan orang-orang hebat.

Sekilas
Keseruan Peserta Scale Up 2.0 Batch Sebelumnya
image 9207
image 8997
image 9205
image 9206
image 8992
Apa kata mereka tentang event ini
300+ Founders & CEO

CUSTOMER PUAS

Tkyu aksoro training nya keren2 terutama waktu mengundang pa I. Jonan banyak dapat ilmu dari beliau dan narasumber launya yg ga kalah keren… lanjut😊 …

Setiyadi Nuryatin

・

Joining the Scale Up 2.0 with Mr. Ignasius Jonan as the main speaker was a very great experience. I learn a lot from the master of transformation himself. Good stuff!

Yin Sachrulli

・

Terima Kasih Aksoro telah menghadirkan Pa Jonan (Sosok yang sangat menginspirasi ) di Scale Up 2.0 Terima Kasih juga mas Afrig motivasinya "Ya Allah ini hasil karyaku, kupersembahkan kepada-Mu"

Udin Itqan

・

2500+

Participants

48hrs

Activity

460+

Company Joined

5.0

Google Reviews

Owner Bisnis Beralih ke Aksoro
Aksoro berkomitmen 100% menghadirkan mentor dan pembicara yang “super qualified”. Para mentor di Aksoro terjamin memenuhi kriteria “been there done that” dan jago mengajar.

Our Speakers
Para Maestro Yang Akan Sharing

IGNASIUS JONAN

CEO PT KAI 2009 – 2014
Salah seorang tokoh transformasi bisnis terbaik dengan prestasi mendunia yang dimiliki Indonesia.
CEO PT KAI 2009 – 2014
IGNASIUS JONAN
CEO PT KAI (2009 – 2014)
Menteri Perhubungan & ESDM 2014-2019
Tokoh Reformasi KAI
The Best CEO (2014)
People of The Year (2013)
Marketeers of The Year (2013)
Best of the Best CEO BUMN (2013)
Di Workshop SCALE UP 2.0 Pak Jonan bukan cuma talkshow, tapi mengisi materi tentang ULTIMATE LEADERSHIP. Sesinya panjang. Anda bisa berdiskusi langsung dengan beliau.

Maksimalkan kesempatan langka yang mahal ini! Karena memang sesusah itu untuk ketemu Pak Jonan. Jangan sampai, justru kompetitor Anda yang ikutan, bisnis Anda pasti kebalap.


NATALI ARDIANTO

CO-FOUNDER LIFEPACK.ID & TIKET.COM
Sosok pioneer dengan pengalaman lebih dari 20 tahun yang sangat dihormati di industri startup teknologi Indonesia.
CO-FOUNDER LIFEPACK.ID & TIKET.COM
NATALI ARDIANTO
Seorang serial entrepreneur dan leader yang sangat dihormati di industri startup Indonesia. Pada tahun 2015, beliau mendapatkan penghargaan sebagai The Most Intelligent CIO pada iCIO Awards, dan Best CIO by SWA and PricewaterhouseCooper.

Sesepuh industri start up nasional ini sudah berkecimpung sejak tahun 2008. Beliau terbiasa memegang project bernilai miliaran US Dollar. Berhasil mengembangkan 2 start up yang kemudian sukses dijual dengan nilai yang sangat tinggi. Sejak 2012 beliau menjadi angel investor pada lebih dari 14 perusahaan. Dan sekarang sedang sibuk-sibuknya menjadi CEO di Lifepack.id.


ADYTHIA PRATAMA

Guerilla Marketing Strategist, IPO Consultant
Salah seorang pelopor strategi Guerilla Marketing di Indonesia dengan pengalaman lebih dari 10 tahun.
Guerilla Marketing Strategist, IPO Consultant
ADYTHIA PRATAMA
Founder & CEO PT Braja Biru Abadi ini merupakan salah seorang pelopor Guerilla Marketing di Indonesia.

Lewat strategi marketing ini beliau berhasil memenangkan penghargaan sebagai “Fastest Growing Aesthetic Clinic in Indonesia” pada tahun 2020.

Strategi marketing andalannya terkenal karena efisiensi penggunaan budget minimal namun hasilnya super maksimal.

image 9003
image 9002
image 8999
image 9000

Exclusive Online Zoom Live Streaming
3,3jt

Rp3,8juta

Live conference selama 2 hari

E – sertifikat

Akses rekaman seumur hidup

Saya Daftar Online!
Premium Offline JAKARTA
10,8jt

Rp12juta

Workshop yang seru & insightful 2 hari full

Modul pembelajaran, lengkap dengan tools, template, sesi simulasi dan juga praktek

Kesempatan langka bisa upgrade ilmu bisis dari 4 mentor sekaligus

Lunch dan coffeebreak selama 2 hari

Sertifikat & premium merchandise

Soft materi dan rekaman workshop yang bisa diakses lagi kapan aja

MC yang kece, lengkap dengan games yang seru

Dokumentasi foto dan video selama acara

WA grup untuk networking sesama peserta dan komunitas Aksoro

Saya Daftar Offline!
Kami membantu ratusan perusahaan memaksimalkan peluang dan potensialnya




























Rating Tertinggi di Edukasi Bisnis

Andika Fahrurozi
5 months ago
Workshopnya lebih dari ekspektasi, next ajak tim leader untuk asah skillset dengan Aksoro 🔥🔥🔥🙏

Armand Ramadhan
5 months ago
It was super fun yet the most insightful program i’ve ever joined so far. At first I thought it was going to be “oh thats kind of program.” Turns out it was different!!! It was all worth. Thank You Aksoro for the great and unforgettable experience 😍

Mianty Henna
5 months ago
2 hari bersama Aksoro benar-benar luar biasa. Pengalaman, pelajaran, pengetahuan yang diperoleh sangat banyak. Bagaimana bekerja sama dan memahami orang lain. Problem solving dari yang tidak mungkin menjadi mungkin. Aksoro keren. 😍😍

Yin Sachrulli
5 months ago
Joining the Scale Up 2.0 with Mr. Ignasius Jonan as the main speaker was a very great experience. I learn a lot from the master of transformation himself. Good stuff!

Nur Liviana
5 months ago
Alhamdulillah 2 hari mengikuti kelas KPI masterclass Aksoro sangat-sangat bermanfaat bangettttt dapet ilmu baru dan terbantu bangettttt ❤️❤️❤️ Pak Himawan menjawab pertanyaan dari peserta sangat detailllll, sukak dehhh❤️ Ini sudah ke 2 kalinya aku ikut kls pelatihan dari Aksoro, next ikut scale up 2.0 nich

Masayu Yulinvinanda
5 months ago
Luar biasa acara HRD Masterclass pembicaranya bukan cuma teori tapi beneran praktek. Daging banget! Recommended buat ikutan HRD Masterclass 😍😍

Dave Dabito
5 months ago
The Great Sales Formula : The best training for growing your skill and competency

5,0

Based on 1073 reviews


Frequently Asked Questions
Kapan & Dimana Workshop Berlangsung?
Workshop Scale Up 2.0 Batch #4 akan diadakan di Jakarta. Pada tanggal 5-6 Oktober 2024, jam 08.00 WIB – selesai.
Apakah Investasi Tersebut Sudah Termasuk Penginapan?
Belum. Namun kami dapat membantu Anda mencarikan penginapan yang cocok selama workshop berlangsung.
Apakah Ada Harga Korporat?
Anda bisa menghubungi tim Aksoro untuk informasi lebih lanjut: Mbak Etha 0821-3153-3535
© Copyright 2024 Aksoro – All Rights Reserved
</data_8>
"""

   result = chat(prompt)
   # print(result)
   with open("paper/aksoro.txt", "w") as text_file:
      text_file.write(result)