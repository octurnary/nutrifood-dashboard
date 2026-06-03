from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from scipy.stats import ttest_ind


st.set_page_config(
    page_title='Dashboard Analisis Bahan Pangan',
    page_icon='',
    layout='wide',
    initial_sidebar_state='expanded',
)

PALETTE = {
    'ink': '#1B3C53',
    'steel': '#456882',
    'sand': '#D2C1B6',
    'paper': '#F9F3EF',
    'white': '#FFFFFF',
    'line': '#E6DED8',
    'muted': '#6B7280',
    'soft': '#F3F4F6',
}

BASE_DIR = Path(__file__).resolve().parent
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


def apply_theme():
    st.markdown(
        f"""
        <style>
        :root {{
            --ink: {PALETTE['ink']};
            --steel: {PALETTE['steel']};
            --sand: {PALETTE['sand']};
            --paper: {PALETTE['paper']};
            --white: {PALETTE['white']};
            --line: {PALETTE['line']};
            --muted: {PALETTE['muted']};
            --soft: {PALETTE['soft']};
        }}

        .stApp {{
            background: var(--paper);
            color: var(--ink);
        }}

        .block-container {{
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }}

        header[data-testid="stHeader"] {{
            background: var(--ink);
            border-bottom: 1px solid rgba(249, 243, 239, 0.18);
        }}

        header[data-testid="stHeader"] * {{
            color: var(--paper) !important;
        }}

        section[data-testid="stSidebar"] {{
            background: var(--ink);
            border-right: 1px solid rgba(249, 243, 239, 0.16);
        }}

        section[data-testid="stSidebar"] * {{
            color: var(--paper) !important;
        }}

        h1, h2, h3 {{
            color: var(--ink);
            letter-spacing: 0;
        }}

        h1 {{
            font-size: 2.25rem;
            line-height: 1.15;
            margin-bottom: 0.75rem;
        }}

        h2 {{
            border-bottom: 1px solid var(--line);
            padding-bottom: 0.45rem;
            margin-top: 2.25rem;
        }}

        h3 {{
            margin-top: 1.25rem;
        }}

        div[data-testid="stMetric"] {{
            background: var(--white);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 8px 24px rgba(27, 60, 83, 0.06);
        }}

        div[data-testid="stMetricLabel"] p {{
            color: var(--muted) !important;
            font-size: 0.9rem;
        }}

        div[data-testid="stMetricValue"] {{
            color: var(--ink);
        }}

        div[data-testid="stDataFrame"] {{
            border: 1px solid var(--line);
            border-radius: 8px;
            overflow: hidden;
            background: var(--white);
        }}

        div[data-testid="stExpander"] {{
            background: var(--white);
            border: 1px solid var(--line);
            border-radius: 8px;
        }}

        .app-hero {{
            background: linear-gradient(135deg, var(--ink), var(--steel));
            color: var(--paper);
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 14px 36px rgba(27, 60, 83, 0.18);
        }}

        .app-hero h1 {{
            color: var(--paper);
            margin: 0 0 0.5rem 0;
        }}

        .app-hero p {{
            color: rgba(249, 243, 239, 0.88);
            max-width: 760px;
            margin: 0;
            line-height: 1.6;
        }}

        .section-note {{
            background: var(--white);
            border-left: 5px solid var(--steel);
            border-radius: 8px;
            padding: 1rem 1.1rem;
            margin: 0.75rem 0 1rem 0;
            color: var(--ink);
            box-shadow: 0 8px 20px rgba(27, 60, 83, 0.05);
        }}

        .problem-card,
        .solution-card {{
            background: linear-gradient(90deg, rgba(27, 60, 83, 0.13) 0%, rgba(210, 193, 182, 0.16) 18%, var(--white) 44%);
            border: 1px solid var(--line);
            border-left: 8px solid var(--ink);
            border-radius: 8px;
            padding: 1.4rem 1.5rem;
            box-shadow: 0 12px 28px rgba(27, 60, 83, 0.08);
        }}

        .problem-card {{
            margin: 1rem 0 1rem 0;
        }}

        .solution-card {{
            margin: 0 0 1.5rem 0;
        }}

        .problem-card .label,
        .solution-card .label {{
            color: var(--steel);
            font-size: 0.9rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            margin-bottom: 0.4rem;
            text-transform: uppercase;
        }}

        .problem-card h2,
        .solution-card h2 {{
            border: 0;
            color: var(--ink);
            font-size: 1.85rem;
            line-height: 1.25;
            margin: 0 0 0.9rem 0;
            padding: 0;
        }}

        .solution-card h2 {{
            font-size: 1.65rem;
        }}

        .problem-card p,
        .solution-card p {{
            color: var(--ink);
            font-size: 1.05rem;
            line-height: 1.65;
            margin: 0.65rem 0 0 0;
        }}

        .problem-card strong,
        .solution-card strong {{
            color: var(--ink);
        }}

        .question-list {{
            background: var(--white);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1rem 1.25rem;
            margin-bottom: 1rem;
        }}

        .question-list ol {{
            margin: 0;
            padding-left: 1.25rem;
        }}

        .question-list li {{
            margin: 0.45rem 0;
            line-height: 1.55;
        }}

        .caption-muted {{
            color: var(--muted);
            font-size: 0.95rem;
            line-height: 1.55;
        }}

        .stButton > button {{
            border-radius: 8px;
            border: 1px solid var(--steel);
            background: var(--steel);
            color: var(--white);
        }}

        .anchor-target {{
            scroll-margin-top: 5.5rem;
            height: 1px;
        }}

        .sidebar-title {{
            color: var(--paper);
            font-size: 1.05rem;
            font-weight: 700;
            margin: 0.25rem 0 0.75rem 0;
        }}

        .sidebar-nav {{
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
        }}

        .sidebar-nav a {{
            color: rgba(249, 243, 239, 0.9) !important;
            text-decoration: none;
            line-height: 1.35;
            padding: 0.55rem 0.65rem;
            border: 1px solid rgba(249, 243, 239, 0.12);
            border-radius: 8px;
            background: rgba(249, 243, 239, 0.06);
        }}

        .sidebar-nav a:hover {{
            background: rgba(210, 193, 182, 0.22);
            border-color: rgba(210, 193, 182, 0.5);
            color: var(--white) !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def kategori_makanan(nama):
    nama = str(nama).lower()

    for kategori, keywords in CATEGORY_RULES.items():
        if any(keyword in nama for keyword in keywords):
            return kategori

    return 'Lainnya'


def prepare_final_data(data):
    data = data.copy()
    data = data.rename(columns={
        'Bahan Pangan': 'nama_makanan',
        'Kalori (kkal/100g)': 'kalori',
        'Protein (g/100g)': 'protein',
        'Karbohidrat (g/100g)': 'karbo',
        'Lemak (g/100g)': 'lemak',
        'Harga (Rp/kg)': 'harga',
    })

    if 'harga_rp;' in data.columns:
        if 'harga' not in data.columns:
            data['harga'] = data['harga_rp;']
        else:
            data['harga'] = data['harga'].where(data['harga'].notna(), data['harga_rp;'])

    required_columns = ['nama_makanan', *NUMERIC_COLUMNS]
    missing_columns = [column for column in required_columns if column not in data.columns]

    if missing_columns:
        raise ValueError(f'Kolom dataset belum lengkap: {", ".join(missing_columns)}')

    data['nama_makanan'] = data['nama_makanan'].astype(str).str.strip()

    if not pd.api.types.is_numeric_dtype(data['harga']):
        harga_text = data['harga'].astype(str).str.strip()
        harga_rupiah = (
            harga_text.str.contains('Rp|;', case=False, regex=True)
            | harga_text.str.contains(r'^\d{1,3}(?:\.\d{3})+$', regex=True)
        )
        harga_clean = (
            harga_text
            .str.replace('Rp', '', regex=False)
            .str.replace(';', '', regex=False)
            .str.strip()
        )
        harga_clean = harga_clean.where(
            ~harga_rupiah,
            harga_clean.str.replace('.', '', regex=False),
        )
        harga_clean = harga_clean.str.replace(',', '.', regex=False)
        data['harga'] = harga_clean

    for column in NUMERIC_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors='coerce')
        median_value = data[column].median()

        if pd.isna(median_value):
            median_value = 0

        data[column] = data[column].fillna(median_value)

    if 'kategori' not in data.columns:
        data['kategori'] = data['nama_makanan'].apply(kategori_makanan)

    data['skor_kesehatan'] = (
        (data['protein'] * 2)
        + data['karbo']
        - data['lemak']
    )

    return data[[
        'nama_makanan',
        'kategori',
        'kalori',
        'protein',
        'lemak',
        'karbo',
        'harga',
        'skor_kesehatan',
    ]]


@st.cache_data
def load_data():
    final_path = BASE_DIR / 'data_final.csv'
    excel_path = BASE_DIR / 'data' / 'data_set_bahan_pangan_1000.xlsx'
    fallback_csv_path = BASE_DIR / 'data' / 'data_final_identik.csv'

    if final_path.exists():
        return prepare_final_data(pd.read_csv(final_path))

    if excel_path.exists():
        return prepare_final_data(pd.read_excel(excel_path))

    if fallback_csv_path.exists():
        return prepare_final_data(
            pd.read_csv(fallback_csv_path, engine='python', on_bad_lines='skip')
        )

    raise FileNotFoundError(
        'File data tidak ditemukan. Pastikan data_final.csv atau file dataset '
        'di folder data sudah ikut terunggah ke repository.'
    )


def add_health_score(data):
    if 'skor_kesehatan' in data.columns:
        return data

    data = data.copy()
    data['skor_kesehatan'] = (
        (data['protein'] * 2)
        + data['karbo']
        - data['lemak']
    )
    return data


def run_ab_test(data):
    median_harga = data['harga'].median()
    group_a = data[data['harga'] <= median_harga]
    group_b = data[data['harga'] > median_harga]

    score_a = group_a['skor_kesehatan'].dropna()
    score_b = group_b['skor_kesehatan'].dropna()
    t_stat, p_value = ttest_ind(score_a, score_b, equal_var=False)

    if p_value < 0.05:
        conclusion = (
            'terdapat perbedaan rata-rata skor_kesehatan yang signifikan '
            'antara makanan murah dan mahal'
        )
    else:
        conclusion = (
            'tidak terdapat perbedaan rata-rata skor_kesehatan yang signifikan '
            'antara makanan murah dan mahal'
        )

    result = pd.DataFrame([
        {
            'group': 'Group A - Murah',
            'kriteria': 'harga <= median harga',
            'jumlah_data': len(group_a),
            'rata_rata_skor_kesehatan': round(score_a.mean(), 2),
            't_statistic': round(t_stat, 4),
            'p_value': round(p_value, 4),
            'kesimpulan': conclusion,
        },
        {
            'group': 'Group B - Mahal',
            'kriteria': 'harga > median harga',
            'jumlah_data': len(group_b),
            'rata_rata_skor_kesehatan': round(score_b.mean(), 2),
            't_statistic': round(t_stat, 4),
            'p_value': round(p_value, 4),
            'kesimpulan': conclusion,
        },
    ])

    return result, conclusion, p_value


def horizontal_bar_chart(data, x, y, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(8, 5))
    data.plot(
        kind='barh',
        x=x,
        y=y,
        ax=ax,
        legend=False,
        color=PALETTE['steel'],
        edgecolor=PALETTE['ink'],
        linewidth=0.6,
    )
    ax.set_title(title, color=PALETTE['ink'], pad=12)
    ax.set_xlabel(xlabel, color=PALETTE['ink'])
    ax.set_ylabel(ylabel, color=PALETTE['ink'])
    ax.set_facecolor(PALETTE['white'])
    fig.patch.set_facecolor(PALETTE['paper'])
    ax.grid(axis='x', color=PALETTE['line'], linewidth=0.8)
    ax.spines[['top', 'right']].set_visible(False)
    ax.spines['left'].set_color(PALETTE['line'])
    ax.spines['bottom'].set_color(PALETTE['line'])
    ax.tick_params(colors=PALETTE['ink'])
    plt.tight_layout()
    return fig


def vertical_bar_chart(series, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(8, 5))
    series.plot(
        kind='bar',
        ax=ax,
        color=PALETTE['steel'],
        edgecolor=PALETTE['ink'],
        linewidth=0.6,
    )
    ax.set_title(title, color=PALETTE['ink'], pad=12)
    ax.set_xlabel(xlabel, color=PALETTE['ink'])
    ax.set_ylabel(ylabel, color=PALETTE['ink'])
    ax.set_facecolor(PALETTE['white'])
    fig.patch.set_facecolor(PALETTE['paper'])
    ax.grid(axis='y', color=PALETTE['line'], linewidth=0.8)
    ax.spines[['top', 'right']].set_visible(False)
    ax.spines['left'].set_color(PALETTE['line'])
    ax.spines['bottom'].set_color(PALETTE['line'])
    ax.tick_params(colors=PALETTE['ink'])
    plt.tight_layout()
    return fig


def show_interpretation(text):
    st.markdown(
        f'<div class="section-note"><strong>Interpretasi:</strong> {text}</div>',
        unsafe_allow_html=True,
    )


def anchor(anchor_id):
    st.markdown(
        f'<div id="{anchor_id}" class="anchor-target"></div>',
        unsafe_allow_html=True,
    )


apply_theme()
df = add_health_score(load_data())

st.markdown(
    """
    <div id="top" class="app-hero">
        <h1>Dashboard Analisis Bahan Pangan Indonesia</h1>
        <p>
            Dashboard ini menganalisis bahan pangan Indonesia untuk membantu
            menjawab pertanyaan utama: bahan pangan mana yang paling relevan
            untuk dipilih berdasarkan kategori, harga, protein, kalori, dan
            skor kesehatan.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
    <div class="sidebar-title">Navigasi Dashboard</div>
    <div class="sidebar-nav">
        <a href="#top">Ringkasan Dashboard</a>
        <a href="#problem-statement">Problem Statement</a>
        <a href="#data-final">Data Final</a>
        <a href="#business-questions">Business Questions</a>
        <a href="#q1">8.1 Distribusi Kategori</a>
        <a href="#q2">8.2 Protein Tertinggi</a>
        <a href="#q3">8.3 Harga Terendah</a>
        <a href="#q4">8.4 Kalori Tertinggi</a>
        <a href="#q5">8.5 Skor Kesehatan</a>
        <a href="#q6">8.6 A/B Testing</a>
        <a href="#summary-eda">Ringkasan EDA</a>
        <a href="#dictionary">Data Dictionary</a>
        <a href="#final-insight">Insight Akhir</a>
    </div>
    """,
    unsafe_allow_html=True,
)

anchor('problem-statement')
st.markdown(
    """
    <div class="problem-card">
        <div class="label">Problem Statement</div>
        <h2>Pengguna membutuhkan pilihan bahan pangan yang seimbang antara gizi dan harga.</h2>
        <p>
            Permasalahan utama dalam pemilihan bahan pangan adalah sulitnya
            membandingkan kandungan gizi dan harga secara bersamaan. Analisis ini
            membantu mengidentifikasi bahan pangan yang unggul berdasarkan
            kategori, protein, harga, kalori, dan <code>skor_kesehatan</code>.
        </p>
    </div>
    <div class="solution-card">
        <div class="label">Main Solution</div>
        <h2>Dashboard analisis bahan pangan berbasis data untuk mendukung rekomendasi menu.</h2>
        <p>
            Solusi utama yang dikembangkan adalah dashboard analisis bahan
            pangan yang menyajikan distribusi kategori, protein tertinggi,
            harga terendah, kalori tertinggi, skor kesehatan, dan hasil A/B
            testing. Dengan pendekatan ini, rekomendasi menu dapat
            dipertimbangkan secara lebih objektif, terukur, dan mudah dipahami.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

anchor('data-final')
st.header('Data Final')

col1, col2, col3, col4 = st.columns(4)
col1.metric('Jumlah Data', f'{len(df):,}')
col2.metric('Jumlah Kategori', df['kategori'].nunique())
col3.metric('Rata-rata Harga', f"Rp {df['harga'].mean():,.0f}")
col4.metric('Rata-rata Skor', round(df['skor_kesehatan'].mean(), 2))

with st.expander('Lihat Data Final'):
    st.dataframe(df, width='stretch')

with st.expander('Lihat Statistik Data Final'):
    st.dataframe(df.describe(), width='stretch')

anchor('business-questions')
st.header('Business Questions dan Pembahasan')
question_items = ''.join(
    f'<li>{question}</li>' for question in BUSINESS_QUESTIONS
)
st.markdown(
    f'<div class="question-list"><ol>{question_items}</ol></div>',
    unsafe_allow_html=True,
)

anchor('q1')
st.subheader('8.1 Bagaimana distribusi kategori bahan pangan dalam dataset?')

distribusi_kategori = df['kategori'].value_counts()
kategori_terbanyak = distribusi_kategori.idxmax()
jumlah_kategori_terbanyak = distribusi_kategori.max()
total_data = len(df)

left, right = st.columns([0.42, 0.58])
with left:
    st.dataframe(distribusi_kategori.to_frame('jumlah_data'), width='stretch')
with right:
    st.pyplot(
        vertical_bar_chart(
            distribusi_kategori,
            title='Distribusi Kategori Bahan Pangan',
            xlabel='Kategori',
            ylabel='Jumlah Data',
        )
    )

show_interpretation(
    f'Berdasarkan hasil distribusi kategori, kategori <strong>{kategori_terbanyak}</strong> '
    f'menjadi kelompok bahan pangan paling dominan dengan jumlah '
    f'<strong>{jumlah_kategori_terbanyak} data</strong> dari total '
    f'<strong>{total_data} data</strong>. Temuan ini menunjukkan bahwa komposisi '
    'dataset lebih banyak diwakili oleh kategori tersebut, sehingga proses '
    'rekomendasi makanan perlu memperhatikan proporsi kategori agar hasil '
    'analisis tidak hanya berfokus pada satu kelompok pangan.'
)

anchor('q2')
st.subheader('8.2 Bahan pangan apa saja yang memiliki protein tertinggi per 100 gram?')

top_protein = df.sort_values(by='protein', ascending=False).head(10)
protein_tertinggi = top_protein.iloc[0]

left, right = st.columns([0.48, 0.52])
with left:
    st.dataframe(
        top_protein[['nama_makanan', 'kategori', 'protein', 'harga']],
        width='stretch',
    )
with right:
    st.pyplot(
        horizontal_bar_chart(
            top_protein.sort_values('protein'),
            x='nama_makanan',
            y='protein',
            title='Top 10 Bahan Pangan dengan Protein Tertinggi',
            xlabel='Protein (g/100g)',
            ylabel='Nama Makanan',
        )
    )

show_interpretation(
    f'Hasil analisis menunjukkan bahwa <strong>{protein_tertinggi["nama_makanan"]}</strong> '
    f'merupakan bahan pangan dengan kandungan protein tertinggi, yaitu '
    f'<strong>{protein_tertinggi["protein"]} g/100g</strong>. Hal ini menunjukkan '
    'bahwa bahan pangan tersebut dapat diprioritaskan dalam rekomendasi menu '
    'apabila tujuan pengguna adalah meningkatkan asupan protein harian.'
)

anchor('q3')
st.subheader('8.3 Bahan pangan apa saja yang memiliki harga paling rendah?')

top_murah = df.sort_values(by='harga', ascending=True).head(10)
makanan_termurah = top_murah.iloc[0]

left, right = st.columns([0.48, 0.52])
with left:
    st.dataframe(
        top_murah[['nama_makanan', 'kategori', 'harga', 'protein', 'kalori']],
        width='stretch',
    )
with right:
    st.pyplot(
        horizontal_bar_chart(
            top_murah.sort_values('harga', ascending=False),
            x='nama_makanan',
            y='harga',
            title='Top 10 Bahan Pangan dengan Harga Terendah',
            xlabel='Harga (Rp/kg)',
            ylabel='Nama Makanan',
        )
    )

show_interpretation(
    f'Berdasarkan analisis harga, <strong>{makanan_termurah["nama_makanan"]}</strong> '
    f'menjadi bahan pangan dengan harga terendah, yaitu '
    f'<strong>Rp {makanan_termurah["harga"]:,.0f}/kg</strong>. Temuan ini relevan '
    'untuk kebutuhan rekomendasi menu hemat, karena bahan pangan dengan harga '
    'relatif rendah dapat digunakan sebagai kandidat awal dalam penyusunan menu '
    'yang ramah anggaran.'
)

anchor('q4')
st.subheader('8.4 Bahan pangan apa saja yang memiliki kalori tertinggi?')

top_kalori = df.sort_values(by='kalori', ascending=False).head(10)
kalori_tertinggi = top_kalori.iloc[0]

left, right = st.columns([0.48, 0.52])
with left:
    st.dataframe(
        top_kalori[['nama_makanan', 'kategori', 'kalori', 'harga']],
        width='stretch',
    )
with right:
    st.pyplot(
        horizontal_bar_chart(
            top_kalori.sort_values('kalori'),
            x='nama_makanan',
            y='kalori',
            title='Top 10 Bahan Pangan dengan Kalori Tertinggi',
            xlabel='Kalori (kkal/100g)',
            ylabel='Nama Makanan',
        )
    )

show_interpretation(
    f'Analisis menunjukkan bahwa <strong>{kalori_tertinggi["nama_makanan"]}</strong> '
    f'memiliki nilai kalori tertinggi, yaitu '
    f'<strong>{kalori_tertinggi["kalori"]} kkal/100g</strong>. Bahan pangan dengan '
    'kalori tinggi dapat dipertimbangkan sebagai sumber energi utama, namun '
    'penggunaannya tetap perlu diseimbangkan dengan kandungan gizi lain seperti '
    'protein, lemak, dan karbohidrat.'
)

anchor('q5')
st.subheader('8.5 Bahan pangan apa saja yang memiliki skor_kesehatan tertinggi?')

top_sehat = df.sort_values(by='skor_kesehatan', ascending=False).head(10)
skor_tertinggi = top_sehat.iloc[0]

left, right = st.columns([0.5, 0.5])
with left:
    st.dataframe(
        top_sehat[[
            'nama_makanan',
            'kategori',
            'protein',
            'karbo',
            'lemak',
            'skor_kesehatan',
        ]],
        width='stretch',
    )
with right:
    st.pyplot(
        horizontal_bar_chart(
            top_sehat.sort_values('skor_kesehatan'),
            x='nama_makanan',
            y='skor_kesehatan',
            title='Top 10 Bahan Pangan dengan Skor Kesehatan Tertinggi',
            xlabel='Skor Kesehatan',
            ylabel='Nama Makanan',
        )
    )

show_interpretation(
    f'Berdasarkan fitur <code>skor_kesehatan</code>, '
    f'<strong>{skor_tertinggi["nama_makanan"]}</strong> memiliki skor tertinggi '
    f'sebesar <strong>{skor_tertinggi["skor_kesehatan"]:.2f}</strong>. Nilai ini '
    'diperoleh dari kombinasi protein, karbohidrat, dan lemak, sehingga bahan '
    'pangan dengan skor tinggi dapat dijadikan kandidat rekomendasi awal untuk '
    'menu yang lebih seimbang secara komposisi gizi.'
)

anchor('q6')
st.subheader('8.6 Apakah rata-rata skor_kesehatan makanan murah berbeda dengan makanan mahal?')

ab_test_result, ab_test_kesimpulan, p_value = run_ab_test(df)

st.markdown(
    """
    <div class="section-note">
        <strong>H0:</strong> rata-rata skor_kesehatan makanan murah dan mahal sama.<br>
        <strong>H1:</strong> rata-rata skor_kesehatan makanan murah dan mahal berbeda.
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([0.48, 0.52])
with left:
    st.dataframe(ab_test_result, width='stretch')
with right:
    st.pyplot(
        vertical_bar_chart(
            ab_test_result.set_index('group')['rata_rata_skor_kesehatan'],
            title='Perbandingan Rata-rata Skor Kesehatan',
            xlabel='Kelompok',
            ylabel='Rata-rata Skor Kesehatan',
        )
    )

show_interpretation(
    f'Hasil A/B testing menggunakan Welch t-test menunjukkan nilai '
    f'<strong>p-value = {p_value:.4f}</strong>. Dengan tingkat signifikansi 5%, '
    f'hasil tersebut menunjukkan bahwa <strong>{ab_test_kesimpulan}</strong>. '
    'Artinya, berdasarkan data yang dianalisis, perbedaan harga murah dan mahal '
    'belum tentu diikuti oleh perbedaan kualitas skor kesehatan yang bermakna '
    'secara statistik.'
)

anchor('summary-eda')
st.header('Ringkasan EDA per Kategori')

eda_kategori = df.groupby('kategori').agg(
    jumlah_data=('nama_makanan', 'count'),
    rata_rata_harga=('harga', 'mean'),
    rata_rata_protein=('protein', 'mean'),
    rata_rata_kalori=('kalori', 'mean'),
    rata_rata_skor_kesehatan=('skor_kesehatan', 'mean'),
).round(2).sort_values(by='jumlah_data', ascending=False)

st.dataframe(eda_kategori, width='stretch')
st.pyplot(
    vertical_bar_chart(
        eda_kategori['rata_rata_skor_kesehatan'],
        title='Rata-rata Skor Kesehatan per Kategori',
        xlabel='Kategori',
        ylabel='Rata-rata Skor Kesehatan',
    )
)

anchor('dictionary')
st.header('Data Dictionary dan Data Model-Ready')

try:
    data_dictionary_df = pd.read_csv(BASE_DIR / 'data_dictionary.csv')
except FileNotFoundError:
    data_dictionary_df = pd.DataFrame(
        DATA_DICTIONARY.items(),
        columns=['kolom', 'deskripsi'],
    )

data_model_ready = df[[
    'kategori',
    'kalori',
    'protein',
    'lemak',
    'karbo',
    'harga',
    'skor_kesehatan',
]]

with st.expander('Lihat Data Dictionary'):
    st.dataframe(data_dictionary_df, width='stretch')

with st.expander('Lihat Data Model-Ready'):
    st.dataframe(data_model_ready.head(), width='stretch')

anchor('final-insight')
st.header('Business Insight Akhir')

kategori_skor_tertinggi = eda_kategori.sort_values(
    by='rata_rata_skor_kesehatan',
    ascending=False,
).iloc[0]

insights = [
    f'Dataset final berisi {len(df)} bahan pangan Indonesia.',
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

st.markdown(
    '<div class="question-list"><ol>'
    + ''.join(f'<li>{insight}</li>' for insight in insights)
    + '</ol></div>',
    unsafe_allow_html=True,
)

st.markdown('---')
st.markdown(
    '<p class="caption-muted">Capstone Project - Sistem Optimasi Menu Makanan Berbasis AI<br>Role: Data Scientist</p>',
    unsafe_allow_html=True,
)
