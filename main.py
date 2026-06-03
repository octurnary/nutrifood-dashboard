import os

import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import ttest_ind


NUMERIC_COLUMNS = ['kalori', 'protein', 'karbo', 'lemak', 'harga']

CATEGORY_RULES = {
    'Karbohidrat': ['beras', 'nasi', 'kentang', 'roti', 'mie', 'jagung'],
    'Protein': ['ikan', 'ayam', 'daging', 'tahu', 'tempe', 'telur', 'susu', 'udang'],
    'Sayur': [
        'brokoli',
        'wortel',
        'bayam',
        'kangkung',
        'sawi',
        'mentimun',
        'kol',
        'selada',
        'tomat',
        'cabai',
    ],
    'Buah': ['pepaya', 'melon', 'apel', 'pisang', 'jeruk', 'mangga', 'semangka'],
    'Minuman': ['teh', 'kopi', 'jus'],
}

BUSINESS_QUESTIONS = [
    'Bagaimana distribusi kategori bahan pangan dalam dataset?',
    'Bahan pangan apa saja yang memiliki protein tertinggi per 100 gram?',
    'Bahan pangan apa saja yang memiliki harga paling rendah?',
    'Bahan pangan apa saja yang memiliki kalori tertinggi?',
    'Bahan pangan apa saja yang memiliki skor_kesehatan tertinggi?',
    (
        'Apakah rata-rata skor_kesehatan makanan murah berbeda '
        'dengan makanan mahal?'
    ),
]

DATA_DICTIONARY = {
    'nama_makanan': 'Nama bahan pangan',
    'kategori': 'Kategori makanan',
    'kalori': 'Jumlah kalori per 100g',
    'protein': 'Jumlah protein per 100g',
    'lemak': 'Jumlah lemak per 100g',
    'karbo': 'Jumlah karbohidrat per 100g',
    'harga': 'Harga makanan per kilogram',
    'skor_kesehatan': 'Skor kesehatan hasil feature engineering',
}


def print_section(title):
    print(f'\n=== {title} ===')


def print_interpretation(text):
    print('\nInterpretasi:')
    print(text)


def kategori_makanan(nama):
    nama = str(nama).lower()

    for kategori, keywords in CATEGORY_RULES.items():
        if any(keyword in nama for keyword in keywords):
            return kategori

    return 'Lainnya'


def plot_barh(data, x, y, title, xlabel, ylabel):
    ax = data.plot(kind='barh', x=x, y=y, figsize=(8, 5), legend=False)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    plt.show()


print_section('CEK FILE')
print('Isi folder project:', os.listdir())
print('Isi folder data:', os.listdir('data'))

print_section('LOAD DATASET')

df1 = pd.read_csv(
    'data/data_final_identik.csv',
    engine='python',
    on_bad_lines='skip',
)

df2 = pd.read_excel('data/data_set_bahan_pangan_1000.xlsx')

print('Dataset berhasil diload.')

print_section('PROBLEM STATEMENT')
print(
    'Masalah utama: pengguna membutuhkan rekomendasi bahan pangan '
    'yang mempertimbangkan gizi dan harga.'
)
print(
    'Solusi utama: analisis dan rekomendasi makanan berbasis data '
    'menggunakan kategori, gizi, harga, dan skor kesehatan.'
)

print_section('DATA AWAL')
print('\nDataset 1:')
print(df1.head())
print('\nDataset 2:')
print(df2.head())

print_section('ASSESSING DATA')
print('\nInfo Dataset 1:')
df1.info()
print('\nInfo Dataset 2:')
df2.info()

assessment_summary = pd.DataFrame({
    'dataset': ['Dataset 1', 'Dataset 2'],
    'baris': [df1.shape[0], df2.shape[0]],
    'kolom': [df1.shape[1], df2.shape[1]],
    'jumlah_duplikat': [df1.duplicated().sum(), df2.duplicated().sum()],
})

print('\nRingkasan struktur data:')
print(assessment_summary)
print('\nMissing value Dataset 1:')
print(df1.isnull().sum())
print('\nMissing value Dataset 2:')
print(df2.isnull().sum())
print('\nDuplikat hanya dilaporkan, tidak dihapus.')

print_section('CLEANING DATA')

df2_clean = df2.rename(columns={
    'Bahan Pangan': 'nama_makanan',
    'Kalori (kkal/100g)': 'kalori',
    'Protein (g/100g)': 'protein',
    'Karbohidrat (g/100g)': 'karbo',
    'Lemak (g/100g)': 'lemak',
    'Harga (Rp/kg)': 'harga',
})

df2_clean['nama_makanan'] = df2_clean['nama_makanan'].astype(str).str.strip()

df2_clean['harga'] = (
    df2_clean['harga']
    .astype(str)
    .str.replace('Rp', '', regex=False)
    .str.replace('.', '', regex=False)
    .str.strip()
)

for column in NUMERIC_COLUMNS:
    df2_clean[column] = pd.to_numeric(df2_clean[column], errors='coerce')

missing_numeric = df2_clean[NUMERIC_COLUMNS].isnull().sum()

if missing_numeric.sum() > 0:
    df2_clean[NUMERIC_COLUMNS] = df2_clean[NUMERIC_COLUMNS].fillna(
        df2_clean[NUMERIC_COLUMNS].median()
    )

print('\nMissing value setelah konversi numerik:')
print(missing_numeric)
print('\nTipe data setelah cleaning:')
print(df2_clean.dtypes)
print('\nStatistik numerik setelah cleaning:')
print(df2_clean[NUMERIC_COLUMNS].describe())

print_section('KATEGORI DAN FEATURE ENGINEERING')

df2_clean['kategori'] = df2_clean['nama_makanan'].apply(kategori_makanan)
df2_clean['skor_kesehatan'] = (
    (df2_clean['protein'] * 2)
    + df2_clean['karbo']
    - df2_clean['lemak']
)

print('\nJumlah data per kategori:')
print(df2_clean['kategori'].value_counts())
print('\nRumus skor_kesehatan: (protein * 2) + karbo - lemak')

data_final = df2_clean[[
    'nama_makanan',
    'kategori',
    'kalori',
    'protein',
    'lemak',
    'karbo',
    'harga',
    'skor_kesehatan',
]]

print_section('DATA FINAL')
print(data_final.head())
print('\nInfo data final:')
data_final.info()
print('\nStatistik data final:')
print(data_final.describe())

print_section('BUSINESS QUESTIONS DAN PEMBAHASAN')
for number, question in enumerate(BUSINESS_QUESTIONS, start=1):
    print(f'{number}. {question}')

print_section('8.1 DISTRIBUSI KATEGORI BAHAN PANGAN')
distribusi_kategori = data_final['kategori'].value_counts()
kategori_terbanyak = distribusi_kategori.idxmax()
jumlah_kategori_terbanyak = distribusi_kategori.max()
total_data = len(data_final)

print(distribusi_kategori)
ax = distribusi_kategori.plot(kind='bar', figsize=(8, 5))
ax.set_title('Distribusi Kategori Bahan Pangan')
ax.set_xlabel('Kategori')
ax.set_ylabel('Jumlah Data')
plt.tight_layout()
plt.show()

print_interpretation(
    f'Berdasarkan hasil distribusi kategori, kategori {kategori_terbanyak} '
    f'menjadi kelompok bahan pangan paling dominan dengan jumlah '
    f'{jumlah_kategori_terbanyak} data dari total {total_data} data. '
    'Temuan ini menunjukkan bahwa komposisi dataset lebih banyak diwakili '
    'oleh kategori tersebut, sehingga proses rekomendasi makanan perlu '
    'memperhatikan proporsi kategori agar hasil analisis tidak hanya '
    'berfokus pada satu kelompok pangan.'
)

print_section('8.2 PROTEIN TERTINGGI PER 100 GRAM')
top_protein = data_final.sort_values(by='protein', ascending=False).head(10)
protein_tertinggi = top_protein.iloc[0]

print(top_protein[['nama_makanan', 'kategori', 'protein', 'harga']])
plot_barh(
    top_protein.sort_values('protein'),
    x='nama_makanan',
    y='protein',
    title='Top 10 Bahan Pangan dengan Protein Tertinggi',
    xlabel='Protein (g/100g)',
    ylabel='Nama Makanan',
)

print_interpretation(
    f'Hasil analisis menunjukkan bahwa {protein_tertinggi["nama_makanan"]} '
    f'merupakan bahan pangan dengan kandungan protein tertinggi, yaitu '
    f'{protein_tertinggi["protein"]} g/100g. Hal ini menunjukkan bahwa '
    'bahan pangan tersebut dapat diprioritaskan dalam rekomendasi menu '
    'apabila tujuan pengguna adalah meningkatkan asupan protein harian.'
)

print_section('8.3 HARGA PALING RENDAH')
top_murah = data_final.sort_values(by='harga', ascending=True).head(10)
makanan_termurah = top_murah.iloc[0]

print(top_murah[['nama_makanan', 'kategori', 'harga', 'protein', 'kalori']])
plot_barh(
    top_murah.sort_values('harga', ascending=False),
    x='nama_makanan',
    y='harga',
    title='Top 10 Bahan Pangan dengan Harga Terendah',
    xlabel='Harga (Rp/kg)',
    ylabel='Nama Makanan',
)

print_interpretation(
    f'Berdasarkan analisis harga, {makanan_termurah["nama_makanan"]} '
    f'menjadi bahan pangan dengan harga terendah, yaitu '
    f'Rp {makanan_termurah["harga"]:,.0f}/kg. Temuan ini relevan untuk '
    'kebutuhan rekomendasi menu hemat, karena bahan pangan dengan harga '
    'relatif rendah dapat digunakan sebagai kandidat awal dalam penyusunan '
    'menu yang ramah anggaran.'
)

print_section('8.4 KALORI TERTINGGI')
top_kalori = data_final.sort_values(by='kalori', ascending=False).head(10)
kalori_tertinggi = top_kalori.iloc[0]

print(top_kalori[['nama_makanan', 'kategori', 'kalori', 'harga']])
plot_barh(
    top_kalori.sort_values('kalori'),
    x='nama_makanan',
    y='kalori',
    title='Top 10 Bahan Pangan dengan Kalori Tertinggi',
    xlabel='Kalori (kkal/100g)',
    ylabel='Nama Makanan',
)

print_interpretation(
    f'Analisis menunjukkan bahwa {kalori_tertinggi["nama_makanan"]} '
    f'memiliki nilai kalori tertinggi, yaitu {kalori_tertinggi["kalori"]} '
    'kkal/100g. Bahan pangan dengan kalori tinggi dapat dipertimbangkan '
    'sebagai sumber energi utama, namun penggunaannya tetap perlu '
    'diseimbangkan dengan kandungan gizi lain seperti protein, lemak, '
    'dan karbohidrat.'
)

print_section('8.5 SKOR KESEHATAN TERTINGGI')
top_sehat = data_final.sort_values(by='skor_kesehatan', ascending=False).head(10)
skor_tertinggi = top_sehat.iloc[0]

print(top_sehat[[
    'nama_makanan',
    'kategori',
    'protein',
    'karbo',
    'lemak',
    'skor_kesehatan',
]])
plot_barh(
    top_sehat.sort_values('skor_kesehatan'),
    x='nama_makanan',
    y='skor_kesehatan',
    title='Top 10 Bahan Pangan dengan Skor Kesehatan Tertinggi',
    xlabel='Skor Kesehatan',
    ylabel='Nama Makanan',
)

print_interpretation(
    f'Berdasarkan fitur skor_kesehatan, {skor_tertinggi["nama_makanan"]} '
    f'memiliki skor tertinggi sebesar {skor_tertinggi["skor_kesehatan"]:.2f}. '
    'Nilai ini diperoleh dari kombinasi protein, karbohidrat, dan lemak, '
    'sehingga bahan pangan dengan skor tinggi dapat dijadikan kandidat '
    'rekomendasi awal untuk menu yang lebih seimbang secara komposisi gizi.'
)

print_section('8.6 A/B TESTING SKOR KESEHATAN')
median_harga = data_final['harga'].median()
group_a = data_final[data_final['harga'] <= median_harga]
group_b = data_final[data_final['harga'] > median_harga]

skor_group_a = group_a['skor_kesehatan'].dropna()
skor_group_b = group_b['skor_kesehatan'].dropna()

t_stat, p_value = ttest_ind(skor_group_a, skor_group_b, equal_var=False)

if p_value < 0.05:
    ab_test_kesimpulan = (
        'terdapat perbedaan rata-rata skor_kesehatan yang signifikan '
        'antara makanan murah dan mahal'
    )
else:
    ab_test_kesimpulan = (
        'tidak terdapat perbedaan rata-rata skor_kesehatan yang signifikan '
        'antara makanan murah dan mahal'
    )

ab_test_result = pd.DataFrame([
    {
        'group': 'Group A - Murah',
        'kriteria': 'harga <= median harga',
        'jumlah_data': len(group_a),
        'rata_rata_skor_kesehatan': round(skor_group_a.mean(), 2),
        't_statistic': round(t_stat, 4),
        'p_value': round(p_value, 4),
        'kesimpulan': ab_test_kesimpulan,
    },
    {
        'group': 'Group B - Mahal',
        'kriteria': 'harga > median harga',
        'jumlah_data': len(group_b),
        'rata_rata_skor_kesehatan': round(skor_group_b.mean(), 2),
        't_statistic': round(t_stat, 4),
        'p_value': round(p_value, 4),
        'kesimpulan': ab_test_kesimpulan,
    },
])

print('H0: rata-rata skor_kesehatan makanan murah dan mahal sama.')
print('H1: rata-rata skor_kesehatan makanan murah dan mahal berbeda.')
print(ab_test_result)

ax = ab_test_result.plot(
    kind='bar',
    x='group',
    y='rata_rata_skor_kesehatan',
    figsize=(7, 5),
    legend=False,
)
ax.set_title('Perbandingan Rata-rata Skor Kesehatan')
ax.set_xlabel('Kelompok')
ax.set_ylabel('Rata-rata Skor Kesehatan')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

print_interpretation(
    f'Hasil A/B testing menggunakan Welch t-test menunjukkan nilai '
    f'p-value = {p_value:.4f}. Dengan tingkat signifikansi 5%, hasil '
    f'tersebut menunjukkan bahwa {ab_test_kesimpulan}. Artinya, berdasarkan '
    'data yang dianalisis, perbedaan harga murah dan mahal belum tentu '
    'diikuti oleh perbedaan kualitas skor kesehatan yang bermakna secara '
    'statistik.'
)

print_section('RINGKASAN EDA PER KATEGORI')
eda_kategori = data_final.groupby('kategori').agg(
    jumlah_data=('nama_makanan', 'count'),
    rata_rata_harga=('harga', 'mean'),
    rata_rata_protein=('protein', 'mean'),
    rata_rata_kalori=('kalori', 'mean'),
    rata_rata_skor_kesehatan=('skor_kesehatan', 'mean'),
).round(2).sort_values(by='jumlah_data', ascending=False)

print(eda_kategori)
ax = eda_kategori['rata_rata_skor_kesehatan'].plot(kind='bar', figsize=(8, 5))
ax.set_title('Rata-rata Skor Kesehatan per Kategori')
ax.set_xlabel('Kategori')
ax.set_ylabel('Rata-rata Skor Kesehatan')
plt.tight_layout()
plt.show()

print_section('DATA DICTIONARY DAN MODEL-READY')

data_dictionary_df = pd.DataFrame(
    DATA_DICTIONARY.items(),
    columns=['kolom', 'deskripsi'],
)

data_model_ready = data_final[[
    'kategori',
    'kalori',
    'protein',
    'lemak',
    'karbo',
    'harga',
    'skor_kesehatan',
]]

print('\nData Dictionary:')
print(data_dictionary_df)
print('\nData Model-Ready:')
print(data_model_ready.head())

print_section('BUSINESS INSIGHT AKHIR')
kategori_skor_tertinggi = eda_kategori.sort_values(
    by='rata_rata_skor_kesehatan',
    ascending=False,
).iloc[0]

insights = [
    f'Dataset final berisi {len(data_final)} bahan pangan Indonesia.',
    f'Kategori terbanyak adalah {kategori_terbanyak} ({jumlah_kategori_terbanyak} data).',
    (
        f"Protein tertinggi: {protein_tertinggi['nama_makanan']} "
        f"({protein_tertinggi['protein']} g/100g)."
    ),
    (
        f"Harga terendah: {makanan_termurah['nama_makanan']} "
        f"(Rp {makanan_termurah['harga']:,.0f})."
    ),
    (
        f"Kalori tertinggi: {kalori_tertinggi['nama_makanan']} "
        f"({kalori_tertinggi['kalori']} kkal/100g)."
    ),
    (
        f"Skor kesehatan tertinggi: {skor_tertinggi['nama_makanan']} "
        f"({skor_tertinggi['skor_kesehatan']:.2f})."
    ),
    (
        f'Kategori dengan rata-rata skor kesehatan tertinggi adalah '
        f'{kategori_skor_tertinggi.name} '
        f"({kategori_skor_tertinggi['rata_rata_skor_kesehatan']:.2f})."
    ),
    f'Kesimpulan A/B testing: {ab_test_kesimpulan}.',
]

for number, insight in enumerate(insights, start=1):
    print(f'{number}. {insight}')

data_final.to_csv('data_final.csv', index=False)
data_dictionary_df.to_csv('data_dictionary.csv', index=False)
data_model_ready.to_csv('data_model_ready.csv', index=False)
ab_test_result.to_csv('ab_testing_result.csv', index=False)

print('\nOutput berhasil disimpan.')
