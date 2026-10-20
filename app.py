from pathlib import Path

import duckdb
import pandas as pd
import plotly.express as px
import pydeck as pdk
import streamlit as st


# ============================================================
# KONFIGURASI DASAR
# ============================================================
st.set_page_config(
    page_title="Pola Pemanfaatan Lapangan Sepak Bola Jawa Timur",
    page_icon="⚽",
    layout="wide",
)


# ============================================================
# SISTEM DESAIN DASHBOARD
# ============================================================
PALETTE = {
    "forest": "#176447",
    "deep": "#102F26",
    "teal": "#2F8F83",
    "lime": "#B7E36A",
    "gold": "#E6B957",
    "coral": "#EF8068",
    "blue": "#5A8DEE",
    "ink": "#21372F",
    "muted": "#728078",
    "grid": "#E7EEE8",
}
CHART_COLORS = [PALETTE["forest"], PALETTE["gold"], PALETTE["coral"], PALETTE["teal"], PALETTE["blue"]]
COMPETITION_COLORS = {"Soeratin": PALETTE["forest"], "Liga 1": PALETTE["gold"], "AFF U-19": PALETTE["coral"]}

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    :root { --forest: #176447; --deep: #102F26; --lime: #B7E36A; --ink: #21372F; }
    html, body, [class*="css"] { font-family: 'DM Sans', 'Segoe UI', sans-serif; }
    [data-testid="stAppViewContainer"] { background: #F4F7F3; color: var(--ink); }
    [data-testid="stHeader"] { background: rgba(244,247,243,.92); }
    [data-testid="stMainBlockContainer"] { padding-top: 3.6rem; padding-bottom: 3rem; max-width: 1550px; }
    h1, h2, h3 { font-family: 'Manrope', 'DM Sans', sans-serif !important; color: #1D352A; letter-spacing: -0.035em; }
    h2 { font-size: 1.3rem !important; margin-top: 1.1rem !important; }
    h3 { font-size: 1.05rem !important; }
    p, label, [data-testid='stCaptionContainer'] { font-size: 1rem; }
    p, label, .stCaption { color: #617068; }

    /* Sidebar: dark green navigation panel */
    [data-testid="stSidebar"] { background: linear-gradient(165deg, #102F26 0%, #174B39 60%, #1B5841 100%); }
    [data-testid="stSidebar"] > div:first-child { background: transparent; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] strong,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color: #F3F8F3 !important; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label { padding: .22rem .1rem; }
    [data-testid="stSidebar"] input[type="radio"] { accent-color: #B7E36A; }
    [data-testid="stSidebar"] [data-baseweb="select"] > div { border-radius: 12px; }
    [data-testid="stSidebar"] [data-baseweb="tag"] { background: #B7E36A !important; border: 0 !important; }
    [data-testid="stSidebar"] [data-baseweb="tag"] span { color: #16382A !important; font-weight: 600; }
    [data-testid="stSidebar"] [data-testid="stRadio"] > label { color:#F3F8F3 !important; font-weight:700; }
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] { gap:.32rem; }
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label { border-radius:10px; padding:.48rem .55rem; transition:background .15s ease; }
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:hover { background:rgba(255,255,255,.09); }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.2); }
    .sidebar-brand { padding: .35rem 0 1.15rem 0; border-bottom: 1px solid rgba(255,255,255,.19); margin-bottom: 1.2rem; }
    .sidebar-brand-line { display:flex; align-items:center; gap:.65rem; color:#F6FAF6; font-weight:800; font-size:1.14rem; letter-spacing:-.03em; }
    .sidebar-ball { display:inline-flex; width:38px; height:38px; align-items:center; justify-content:center; background:rgba(183,227,106,.15); border:1px solid rgba(183,227,106,.38); border-radius:13px; font-size:1.35rem; }
    .sidebar-small { color:#BBD1C4; font-size:.77rem; margin-top:.45rem; letter-spacing:.06em; text-transform:uppercase; }

    /* Main hero */
    .hero-header { position:relative; z-index:1; overflow:visible; box-sizing:border-box; width:100%; padding:1.75rem 2rem 1.7rem; border-radius:26px; margin-top:.65rem; margin-bottom:1.35rem;
        background: radial-gradient(circle at 90% 18%, rgba(183,227,106,.22), transparent 24%), linear-gradient(120deg, #102F26 0%, #176447 62%, #21785A 100%);
        box-shadow: 0 12px 28px rgba(20,75,52,.13); }
    .hero-brand-row { display:flex; align-items:center; gap:1rem; margin-bottom:1.05rem; position:relative; z-index:2; }
    .hero-kicker { display:inline-block; padding:.38rem .78rem; border:1px solid rgba(218,245,178,.34); background:rgba(183,227,106,.12); border-radius:999px; color:#D9F5AC; font-size:.72rem; font-weight:800; letter-spacing:.12em; text-transform:uppercase; margin-bottom:.38rem; }
    .hero-brand-subline { color:#D4E4DA; font-size:.74rem; font-weight:600; letter-spacing:.08em; text-transform:uppercase; }
    .hero-title { color:#FFFFFF; font-family:'Manrope','DM Sans',sans-serif; font-size:clamp(1.65rem, 2.35vw, 2.15rem); line-height:1.22; font-weight:800; letter-spacing:-.04em; margin:0; white-space:normal; overflow-wrap:anywhere; max-width:100%; }
    .hero-subtitle { color:#D4E4DA; font-size:clamp(.88rem, 1vw, 1rem); line-height:1.55; margin:.8rem 0 0; white-space:normal; max-width:100%; }
    .hero-foot { display:flex; flex-wrap:wrap; gap:.55rem; margin-top:1.2rem; }
    .hero-tag { color:#EFF7F0; border:1px solid rgba(255,255,255,.2); background:rgba(255,255,255,.07); border-radius:999px; padding:.38rem .68rem; font-size:.78rem; }

    /* Metrics and visual containers */
    [data-testid="stMetric"] { background:#FFFFFF; border:1px solid #E2EAE2; padding:1rem .9rem; border-radius:19px; box-shadow:0 5px 16px rgba(28,61,44,.045); min-height:128px; height:auto; text-align:center; display:flex; flex-direction:column; justify-content:center; align-items:center; }
    [data-testid="stMetricLabel"] { width:100%; text-align:center !important; }
    [data-testid="stMetricLabel"] > div { white-space:normal !important; overflow:visible !important; text-overflow:clip !important; line-height:1.3 !important; min-height:2.6em; display:block !important; text-align:center !important; }
    [data-testid="stMetricLabel"] p { white-space:normal !important; overflow:visible !important; text-overflow:clip !important; line-height:1.3 !important; font-size:.9rem !important; text-align:center !important; }
    [data-testid="stMetricValue"] { font-size:1.9rem !important; text-align:center !important; width:100%; min-width:0; }
    [data-testid="stMetricValue"] > div { white-space:normal !important; overflow-wrap:anywhere !important; word-break:normal !important; line-height:1.2 !important; max-width:100%; }
    [data-testid="stMetric"] [data-testid="stMetricValue"] { min-width:0; overflow-wrap:anywhere; }
    [data-testid="stMetricLabel"] { color:#68786E !important; font-size:.83rem !important; font-weight:600 !important; }
    [data-testid="stMetricValue"] { color:#173F30 !important; font-family:'Manrope','DM Sans',sans-serif; font-weight:800; letter-spacing:-.045em; }
    .venue-kpi-card { box-sizing:border-box; width:100%; min-width:0; min-height:145px; height:100%; padding:1.25rem 1rem; border:1px solid #E2EAE2; border-radius:20px; background:#FFFFFF; box-shadow:0 7px 22px rgba(28,61,44,.05); display:flex; flex-direction:column; align-items:center; justify-content:center; gap:.8rem; text-align:center; }
    .venue-kpi-label { color:#68786E; font-size:1rem; line-height:1.35; }
    .venue-kpi-value { width:100%; min-width:0; color:#173F30; font-family:'Manrope','DM Sans',sans-serif; font-size:clamp(1.8rem, 2.6vw, 2.45rem); font-weight:800; line-height:1.18; letter-spacing:-.035em; overflow-wrap:anywhere; }
    .venue-kpi-value.venue-name { font-size:clamp(1.25rem, 1.8vw, 1.7rem); letter-spacing:-.025em; }
    [data-testid="stPlotlyChart"] { background:#FFFFFF; padding:.45rem .55rem .2rem; border:1px solid #E5ECE5; border-radius:19px; box-shadow:0 5px 16px rgba(28,61,44,.035); }
    [data-testid="stDataFrame"] { border:1px solid #E2EAE2; border-radius:16px; overflow:hidden; }
    [data-testid="stDownloadButton"] button, [data-testid="stButton"] button { background:#176447; color:white; border:1px solid #176447; border-radius:12px; font-weight:700; padding:.55rem 1rem; transition:all .15s ease; }
    [data-testid="stDownloadButton"] button:hover, [data-testid="stButton"] button:hover { background:#102F26; border-color:#102F26; color:white; }
    [data-testid="stAlert"] { border-radius:14px; }
    [data-testid="stMultiSelect"] [data-baseweb="tag"] { background:#E4F0E8 !important; color:#174B39 !important; border:1px solid #C6DCCB !important; border-radius:8px !important; }
    [data-testid="stMultiSelect"] [data-baseweb="tag"] span { color:#174B39 !important; }
    [data-testid="stMultiSelect"] [data-baseweb="tag"] svg { fill:#557565 !important; }
    [data-testid="stSelectbox"] [data-baseweb="select"] > div,
    [data-testid="stMultiSelect"] [data-baseweb="select"] > div,
    [data-testid="stDateInput"] input { border-radius:12px; }
    .section-note { color:#718078; font-size:.9rem; line-height:1.55; margin-top:-.3rem; margin-bottom:.65rem; }
    .footer-note { color:#829087; font-size:.78rem; padding-top:1rem; }

    /* Custom legend for stacked competition chart: always inline when space allows. */
    .stacked-legend { display:flex; flex-direction:row; flex-wrap:nowrap; align-items:center; justify-content:center;
        gap:clamp(.65rem, 2vw, 1.25rem); white-space:nowrap; overflow-x:auto; margin:.05rem 0 .45rem;
        padding:.42rem .35rem; color:#34483D; font-size:.9rem; line-height:1.3; }
    .stacked-legend-item { display:inline-flex; flex:0 0 auto; align-items:center; gap:.42rem; }
    .stacked-legend-swatch { width:13px; height:13px; border-radius:1px; display:inline-block; flex:0 0 13px; }
    @media (max-width: 430px) {
      .stacked-legend { justify-content:flex-start; gap:.7rem; font-size:.82rem; }
    }

    @media (max-width: 760px) {
      .hero-header { padding:1.35rem; border-radius:20px; margin-top:.35rem; overflow:visible; }
      .hero-brand-row { gap:.75rem; align-items:flex-start; }
      .hero-title { white-space:normal; font-size:clamp(1.45rem, 5vw, 2rem); }
      .hero-subtitle { white-space:normal; font-size:.9rem; }
      .hero-kicker { font-size:.63rem; letter-spacing:.08em; }
      [data-testid="stMetric"] { padding:.8rem; min-height:110px; height:auto; }
      .venue-kpi-card { min-height:120px; padding:1rem .7rem; }
      .venue-kpi-value.venue-name { font-size:1.15rem; }
      [data-testid="stMetricLabel"] > div { min-height:0; }
      [data-testid="stMetricValue"] { font-size:1.45rem !important; text-align:center !important; }
      [data-testid="stMetricValue"] > div { overflow-wrap:anywhere !important; white-space:normal !important; }
      .hero-title { font-size:clamp(1.5rem, 5.4vw, 2rem); }
      [data-testid="stMainBlockContainer"] { padding-top:3.4rem; padding-left:1rem; padding-right:1rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def style_plotly(fig, height: int = 410):
    """Apply consistent styling to all Plotly charts without changing their data."""
    fig.update_layout(
        template="plotly_white",
        colorway=CHART_COLORS,
        font={"family": "DM Sans, Segoe UI, sans-serif", "size": 12, "color": "#34483D"},
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="#FFFFFF",
        height=height,
        margin={"l": 18, "r": 18, "t": 24, "b": 24},
        hoverlabel={"bgcolor": "#102F26", "font": {"color": "#FFFFFF", "size": 12}, "bordercolor": "#102F26"},
        legend={"bgcolor": "rgba(255,255,255,0)", "orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "left", "x": 0},
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="#DCE6DD", tickfont={"color": "#65766B"}, automargin=True)
    fig.update_yaxes(showgrid=True, gridcolor="#E7EEE8", zeroline=False, linecolor="#DCE6DD", tickfont={"color": "#65766B"}, automargin=True)
    return fig

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR if (BASE_DIR / "shared_catalog.ducklake").exists() else BASE_DIR.parent
CATALOG_PATH = PROJECT_DIR / "shared_catalog.ducklake"


@st.cache_data(show_spinner="Memuat data dari DuckLake...")
def load_data(catalog_path: str):
    """Membaca tabel fakta, dimensi, dan data mart langsung dari DuckLake."""
    con = duckdb.connect()
    try:
        con.execute("LOAD ducklake")
        catalog = Path(catalog_path).resolve().as_posix().replace("'", "''")
        con.execute(f"ATTACH 'ducklake:{catalog}' AS lake (READ_ONLY)")

        # Fact dan dimension tetap dipakai untuk filter tanggal/kompetisi.
        events = con.execute("SELECT * FROM lake.analytics.fact_event").fetchdf()
        venues = con.execute("SELECT * FROM lake.fasilitas.dim_venue").fetchdf()

        # Data mart dipakai untuk ringkasan aktivitas, kompetisi, dan fasilitas.
        mart_activity = con.execute(
            "SELECT * FROM lake.analytics.mart_aktivitas_venue"
        ).fetchdf()
        mart_competition = con.execute(
            "SELECT * FROM lake.analytics.mart_kompetisi_venue"
        ).fetchdf()
        mart_facility = con.execute(
            "SELECT * FROM lake.analytics.mart_karakteristik_venue"
        ).fetchdf()
    finally:
        con.close()

    required_event_cols = {"id_event", "kompetisi_sumber", "venue_id"}
    required_venue_cols = {"venue_id", "nama_venue", "latitude", "longitude"}
    missing_event = required_event_cols - set(events.columns)
    missing_venue = required_venue_cols - set(venues.columns)
    if missing_event:
        raise ValueError(
            f"Kolom wajib tidak ada di lake.analytics.fact_event: {sorted(missing_event)}"
        )
    if missing_venue:
        raise ValueError(
            f"Kolom wajib tidak ada di lake.fasilitas.dim_venue: {sorted(missing_venue)}"
        )

    for frame in [venues, mart_facility]:
        for col in ["latitude", "longitude", "luas_m2", "kapasitas_penonton"]:
            if col in frame.columns:
                frame[col] = pd.to_numeric(frame[col], errors="coerce")

    if "tanggal_mulai_iso" in events.columns:
        events["tanggal_event"] = pd.to_datetime(
            events["tanggal_mulai_iso"], format="%Y-%m-%d", errors="coerce"
        )
    elif "tanggal_mulai" in events.columns:
        events["tanggal_event"] = pd.to_datetime(
            events["tanggal_mulai"], dayfirst=True, errors="coerce"
        )
    else:
        events["tanggal_event"] = pd.NaT

    events["kompetisi_sumber"] = events["kompetisi_sumber"].fillna("Tidak diketahui")
    venues["nama_venue"] = venues["nama_venue"].fillna("Nama venue tidak tersedia")

    for col in ["kecamatan", "kelurahan", "alamatlokasi", "nama_fasilitas_olahraga"]:
        if col not in venues.columns:
            venues[col] = pd.NA
        if col not in mart_facility.columns:
            if "venue_id" in mart_facility.columns:
                lookup = venues.set_index("venue_id")[col]
                mart_facility[col] = mart_facility["venue_id"].map(lookup)
            else:
                mart_facility[col] = pd.NA

    return events, venues, mart_activity, mart_competition, mart_facility


if not CATALOG_PATH.exists():
    st.title("⚽ Analisis Pola Pemanfaatan Lapangan Sepak Bola Jawa Timur")
    st.error("Katalog DuckLake belum ditemukan.")
    st.markdown(
        "Pastikan proses integrasi DuckLake sudah dijalankan dan file katalog "
        "tersedia di folder utama proyek."
    )
    st.code("shared_catalog.ducklake", language="text")
    st.info("Jalankan `python src/integrasi_data.py`, lalu refresh aplikasi.")
    st.stop()

try:
    events, venues, mart_activity, mart_competition, mart_facility = load_data(
        str(CATALOG_PATH)
    )
except Exception as exc:
    st.error(f"Gagal membaca tabel dari DuckLake: {exc}")
    st.markdown(
        "Pastikan ekstensi DuckLake tersedia, katalog dapat dibuka, dan tabel "
        "`lake.analytics.fact_event` serta `lake.fasilitas.dim_venue` sudah dibuat."
    )
    st.stop()


# ============================================================
# NAVIGASI SIDEBAR DAN FILTER UTAMA
# ============================================================
st.sidebar.markdown(
    """
    <div class="sidebar-brand">
      <div class="sidebar-brand-line"><span class="sidebar-ball">⚽</span><span>Lapangan Jatim</span></div>
      <div class="sidebar-small">Sports Venue Analytics · Jawa Timur</div>
    </div>
    """,
    unsafe_allow_html=True,
)
page = st.sidebar.radio(
    "Pilih halaman",
    ["Ringkasan Aktivitas", "Peta Persebaran Venue", "Analisis Kompetisi", "Analisis Fasilitas"],
)
st.sidebar.divider()
st.sidebar.caption("Gunakan menu di atas untuk menjelajahi analitik venue sepak bola.")

competition_options = sorted(events["kompetisi_sumber"].dropna().unique().tolist())
valid_dates = events["tanggal_event"].dropna()
year_options = sorted(valid_dates.dt.year.astype(int).unique().tolist()) if not valid_dates.empty else []

# ============================================================
# HELPER AGREGASI
# ============================================================
def get_activity_by_venue(
    event_df: pd.DataFrame,
    venue_df: pd.DataFrame,
    activity_mart: pd.DataFrame,
    use_mart: bool = False,
) -> pd.DataFrame:
    """Gunakan mart pada cakupan penuh; hitung ulang dari fact saat filter aktif."""
    if use_mart:
        mart_cols = [
            col for col in [
                "venue_id", "total_event", "total_soeratin", "total_liga1",
                "total_aff_u19", "event_pertama", "event_terakhir"
            ] if col in activity_mart.columns
        ]
        result = venue_df.merge(
            activity_mart[mart_cols], on="venue_id", how="left"
        )
        result["jumlah_pertandingan"] = pd.to_numeric(
            result["total_event"], errors="coerce"
        ).fillna(0).astype(int)
        return result

    matched = event_df.dropna(subset=["venue_id"])
    counts = (
        matched.groupby("venue_id", as_index=False)
        .size()
        .rename(columns={"size": "jumlah_pertandingan"})
    )
    result = venue_df.merge(counts, on="venue_id", how="left")
    result["jumlah_pertandingan"] = result["jumlah_pertandingan"].fillna(0).astype(int)
    return result


# ============================================================
# HEADER
# ============================================================
st.markdown(
    """
    <div class="hero-header">
      <div class="hero-brand-row">
        <div>
          <div class="hero-kicker">Sports Data Warehouse · Jawa Timur</div>
          <div class="hero-brand-subline">Portal Analitik Sepak Bola</div>
        </div>
      </div>
      <div class="hero-title">Pola Pemanfaatan Lapangan Sepak Bola Jawa Timur</div>
      <div class="hero-subtitle">Jelajahi aktivitas pertandingan, persebaran venue, kompetisi, dan karakteristik fasilitas dalam satu dashboard terintegrasi.</div>
      <div class="hero-foot">
        <span class="hero-tag">⚽ Soeratin</span>
        <span class="hero-tag">🏆 Liga 1</span>
        <span class="hero-tag">🌏 AFF U-19 2024</span>
        <span class="hero-tag">📍 67 venue terdata</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Filter diletakkan di area utama agar sidebar fokus pada navigasi halaman.
st.markdown("### Filter analisis")
f1, f2, f3 = st.columns([1.35, 1, 1])
with f1:
    selected_competitions_raw = st.multiselect(
        "Kompetisi", options=["Semua kompetisi"] + competition_options,
        default=["Semua kompetisi"], key="global_competition_filter",
        help="Pilih satu atau beberapa kompetisi, atau gunakan Semua kompetisi.",
    )
with f2:
    selected_year = st.selectbox(
        "Tahun pertandingan", options=["Semua tahun"] + year_options,
        index=0, key="global_year_filter",
    )
with f3:
    st.caption("Filter berlaku untuk seluruh grafik dan indikator pada halaman.")

if not selected_competitions_raw or "Semua kompetisi" in selected_competitions_raw:
    selected_competitions = competition_options
else:
    selected_competitions = selected_competitions_raw
filtered_events = events[events["kompetisi_sumber"].isin(selected_competitions)].copy()
if selected_year != "Semua tahun":
    filtered_events = filtered_events[filtered_events["tanggal_event"].dt.year == int(selected_year)].copy()
start_date = end_date = None
use_full_marts = (set(selected_competitions) == set(competition_options)) and (selected_year == "Semua tahun")

# Agregasi venue harus dilakukan setelah filter global dibuat.
activity_venues = get_activity_by_venue(
    filtered_events, venues, mart_activity, use_mart=use_full_marts
)


# ============================================================
# HALAMAN 1: RINGKASAN AKTIVITAS
# ============================================================
if page == "Ringkasan Aktivitas":
    linked_events = filtered_events[filtered_events["venue_id"].notna()]
    active_venue_count = linked_events["venue_id"].nunique()
    missing_venue_count = int(filtered_events["venue_id"].isna().sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pertandingan tercatat", f"{len(filtered_events):,}")
    c2.metric("Pertandingan dengan venue teridentifikasi", f"{len(linked_events):,}")
    c3.metric("Venue yang digunakan", f"{active_venue_count:,}")
    c4.metric("Pertandingan tanpa informasi venue", f"{missing_venue_count:,}")

    st.subheader("⚽ Jumlah pertandingan per kompetisi")
    comp_summary = (
        filtered_events.groupby("kompetisi_sumber", as_index=False)
        .size()
        .rename(columns={"size": "jumlah_pertandingan"})
        .sort_values("jumlah_pertandingan", ascending=False)
    )
    if comp_summary.empty:
        st.info("Tidak ada event yang sesuai dengan filter yang dipilih.")
    else:
        fig_comp = px.bar(
            comp_summary,
            x="kompetisi_sumber",
            y="jumlah_pertandingan",
            text="jumlah_pertandingan",
            labels={
                "kompetisi_sumber": "Kompetisi",
                "jumlah_pertandingan": "Jumlah pertandingan",
            },
            color="kompetisi_sumber",
            color_discrete_map=COMPETITION_COLORS,
        )
        fig_comp.update_traces(textposition="outside", cliponaxis=False, textfont_size=14)
        fig_comp.update_layout(xaxis_title=None, yaxis_title="Jumlah pertandingan", showlegend=False, uniformtext_minsize=12, uniformtext_mode="hide", yaxis_range=[0, max(comp_summary["jumlah_pertandingan"].max() * 1.16, 1)])
        st.plotly_chart(style_plotly(fig_comp, 390), width="stretch")

    left, right = st.columns(2)
    with left:
        st.subheader("🏟️ Venue dengan aktivitas terbanyak")

        # Tentukan 10 venue teratas dari total aktivitas pada filter yang sedang dipilih.
        top_venue_ids = activity_venues.nlargest(10, "jumlah_pertandingan")["venue_id"].tolist()

        # Hitung jumlah pertandingan per venue DAN per jenis kompetisi agar batang bisa ditumpuk.
        if use_full_marts:
            venue_comp_counts = mart_competition.rename(
                columns={"total_event": "jumlah_pertandingan"}
            ).copy()
        else:
            venue_comp_counts = (
                filtered_events.dropna(subset=["venue_id"])
                .groupby(["venue_id", "kompetisi_sumber"], as_index=False)
                .size()
                .rename(columns={"size": "jumlah_pertandingan"})
            )
        # Nama venue dari dimensi menjadi sumber utama agar tidak muncul nama_venue_x/y.
        # Normalisasi: satu baris untuk setiap kombinasi venue dan kompetisi.
        venue_comp_counts = venue_comp_counts.drop(columns=["nama_venue"], errors="ignore")
        venue_comp_counts["jumlah_pertandingan"] = pd.to_numeric(
            venue_comp_counts["jumlah_pertandingan"], errors="coerce"
        ).fillna(0)
        venue_comp_counts = (
            venue_comp_counts.groupby(
                ["venue_id", "kompetisi_sumber"], as_index=False
            )["jumlah_pertandingan"].sum()
        )
        top_venue_comp = venue_comp_counts[
            venue_comp_counts["venue_id"].isin(top_venue_ids)
        ].merge(
            venues[["venue_id", "nama_venue"]], on="venue_id", how="left"
        )
        top_venue_comp = top_venue_comp.dropna(subset=["nama_venue"])

        if top_venue_comp.empty:
            st.info("Tidak ada pertandingan ber-venue yang sesuai dengan filter.")
        else:
            # Pertahankan urutan venue berdasarkan total pertandingan, dari sedikit ke banyak,
            # agar venue dengan aktivitas terbesar tampil di bagian atas grafik horizontal.
            venue_order = (
                activity_venues[activity_venues["venue_id"].isin(top_venue_ids)]
                .sort_values("jumlah_pertandingan", ascending=True)["nama_venue"]
                .tolist()
            )
            competition_order = [
                comp for comp in ["Soeratin", "Liga 1", "AFF U-19"]
                if comp in top_venue_comp["kompetisi_sumber"].astype(str).unique()
            ]
            # Warna beda dan konsisten untuk tiap kompetisi, tetap sesuai tema hijau dashboard.
            competition_color_map = dict(COMPETITION_COLORS)
            # Beri warna fallback kalau nantinya ada sumber kompetisi baru.
            for i, comp in enumerate(sorted(top_venue_comp["kompetisi_sumber"].astype(str).unique())):
                if comp not in competition_color_map:
                    competition_color_map[comp] = CHART_COLORS[i % len(CHART_COLORS)]

            # Gunakan legenda HTML khusus agar kotak warna dan nama kompetisi selalu berjajar.
            # Legenda Plotly bawaan disembunyikan di bawah agar tidak kembali bertumpuk vertikal.
            legend_items = []
            for comp in ["Soeratin", "Liga 1", "AFF U-19"]:
                if comp in competition_order:
                    color = competition_color_map[comp]
                    legend_items.append(
                        f'<span class="stacked-legend-item">'
                        f'<span class="stacked-legend-swatch" style="background:{color};"></span>'
                        f'<span>{comp}</span></span>'
                    )
            st.markdown(
                '<div class="stacked-legend">' + ''.join(legend_items) + '</div>',
                unsafe_allow_html=True,
            )

            # Lengkapi semua pasangan venue-kompetisi; nilai yang tidak ada = 0.
            complete_index = pd.MultiIndex.from_product(
                [top_venue_ids, competition_order],
                names=["venue_id", "kompetisi_sumber"],
            ).to_frame(index=False)
            top_venue_comp = complete_index.merge(
                top_venue_comp.drop(columns=["nama_venue"], errors="ignore"),
                on=["venue_id", "kompetisi_sumber"], how="left"
            ).merge(
                venues[["venue_id", "nama_venue"]], on="venue_id", how="left"
            )
            top_venue_comp["jumlah_pertandingan"] = top_venue_comp[
                "jumlah_pertandingan"
            ].fillna(0)
            fig_top = px.bar(
                top_venue_comp,
                x="jumlah_pertandingan",
                y="nama_venue",
                color="kompetisi_sumber",
                orientation="h",
                barmode="stack",
                category_orders={
                    "nama_venue": venue_order,
                    "kompetisi_sumber": competition_order,
                },
                color_discrete_map=competition_color_map,
                labels={
                    "nama_venue": "Venue",
                    "jumlah_pertandingan": "Jumlah pertandingan",
                    "kompetisi_sumber": "Kompetisi",
                },
                custom_data=["venue_id"],
                hover_data={"jumlah_pertandingan": ":,", "venue_id": False},
            )
            fig_top.update_layout(
                yaxis_title=None,
                xaxis_title="Jumlah pertandingan",
                barmode="stack",
            )
            fig_top.update_traces(marker_line_width=0, textposition="outside", cliponaxis=False)
            fig_top.update_layout(barmode="stack", bargap=0.22)
            fig_top.update_yaxes(tickfont={"size": 11}, automargin=True)
            fig_top.update_xaxes(tickfont={"size": 11}, automargin=True)

            # Sembunyikan legenda Plotly bawaan; legenda inline sudah disediakan di atas.
            # Dengan demikian tampilan tidak bergantung pada cara Plotly membungkus item legend.
            fig_top = style_plotly(fig_top, max(430, 46 * len(venue_order)))
            # Penting: set mode pada layout setelah styling agar tidak tertimpa.
            fig_top.update_layout(
                barmode="stack",
                barnorm="",
                showlegend=False,
                margin={"l": 22, "r": 28, "t": 18, "b": 42},
            )
            st.plotly_chart(fig_top, width="stretch")

    with right:
        st.subheader("📈 Tren pertandingan dari waktu ke waktu")
        dated = filtered_events.dropna(subset=["tanggal_event"]).copy()
        if dated.empty:
            st.info("Tanggal event belum tersedia untuk membuat grafik tren.")
        else:
            dated["bulan"] = dated["tanggal_event"].dt.to_period("M").dt.to_timestamp()
            monthly = dated.groupby("bulan", as_index=False).size().rename(
                columns={"size": "jumlah_pertandingan"}
            )
            fig_trend = px.line(
                monthly,
                x="bulan",
                y="jumlah_pertandingan",
                markers=True,
                labels={
                    "bulan": "Bulan",
                    "jumlah_pertandingan": "Jumlah pertandingan",
                },
                color_discrete_sequence=[PALETTE["forest"]],
            )
            fig_trend.update_traces(line={"width": 3}, marker={"size": 7, "color": PALETTE["lime"], "line": {"color": PALETTE["forest"], "width": 1.5}})
            fig_trend.update_layout(xaxis_title=None, yaxis_title="Jumlah pertandingan")
            st.plotly_chart(style_plotly(fig_trend, 390), width="stretch")

    csv_bytes = filtered_events.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "Unduh event sesuai filter (CSV)",
        data=csv_bytes,
        file_name="event_hasil_filter.csv",
        mime="text/csv",
    )


# ============================================================
# HALAMAN 2: PETA PERSEBARAN VENUE
# ============================================================
elif page == "Peta Persebaran Venue":
    st.subheader("📍 Persebaran venue berdasarkan koordinat")
    st.write("Pilih titik pada peta untuk melihat detail venue dan daftar pertandingan yang tercatat.")

    map_df = activity_venues.copy()
    # Venue tanpa nilai kecamatan tetap dapat ditampilkan; diberi kategori filter tersendiri.
    map_df["_filter_kecamatan"] = map_df["kecamatan"].fillna("Tidak diketahui").astype(str)
    districts = sorted(map_df["_filter_kecamatan"].unique().tolist())
    selected_district = st.selectbox(
        "Kecamatan", options=["Semua kecamatan"] + districts, index=0,
        key="map_district_filter",
    )
    if selected_district != "Semua kecamatan":
        map_df = map_df[map_df["_filter_kecamatan"] == selected_district]
    map_df = map_df.dropna(subset=["latitude", "longitude"])

    if map_df.empty:
        st.warning("Tidak ada venue dengan koordinat pada filter yang dipilih.")
    else:
        map_center_lat = float(map_df["latitude"].median())
        map_center_lon = float(map_df["longitude"].median())
        map_layer = pdk.Layer(
            "ScatterplotLayer",
            id="venue_scatterplot",  # ID diperlukan agar titik bisa dipilih (click/select)
            data=map_df,
            get_position="[longitude, latitude]",
            get_radius=220,
            radius_min_pixels=6,
            radius_max_pixels=16,
            pickable=True,
            auto_highlight=True,
            get_fill_color=[183, 227, 106, 230],
            get_line_color=[16, 47, 38, 220],
            line_width_min_pixels=1,
        )
        deck = pdk.Deck(
            layers=[map_layer],
            initial_view_state=pdk.ViewState(
                latitude=map_center_lat,
                longitude=map_center_lon,
                zoom=6,
                pitch=0,
            ),
            tooltip={
                "html": (
                    "<b>{nama_venue}</b><br/>"
                    "Kecamatan: {kecamatan}<br/>"
                    "Pertandingan: {jumlah_pertandingan}<br/>"
                    "Kapasitas: {kapasitas_penonton}"
                ),
                "style": {"backgroundColor": "#102F26", "color": "white", "borderRadius": "10px", "padding": "10px"},
            },
            map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        )
        map_selection = st.pydeck_chart(
            deck,
            width="stretch",
            on_select="rerun",
            selection_mode="single-object",
            key="venue_map_select",
            height=560,
        )
        st.caption(
            f"Jumlah titik pada peta: {len(map_df)} venue. "
            "Klik satu titik untuk melihat detail venue; arahkan kursor untuk melihat tooltip."
        )

        # Tampilkan detail ketika pengguna memilih salah satu titik di peta.
        selected_rows = []
        try:
            selected_rows = map_selection.selection.objects.get("venue_scatterplot", [])
        except (AttributeError, KeyError, TypeError):
            selected_rows = []

        if selected_rows:
            selected_id = selected_rows[0].get("venue_id")
            if selected_id is not None:
                selected_match = map_df[map_df["venue_id"].astype(str) == str(selected_id)]
                if not selected_match.empty:
                    selected_venue = selected_match.iloc[0]
                    st.markdown("### Detail venue terpilih")
                    detail1, detail2, detail3 = st.columns([1.15, 1, 1], gap="medium")
                    venue_name = str(selected_venue.get("nama_venue", "-"))
                    match_count = f"{int(selected_venue.get('jumlah_pertandingan', 0)):,}"
                    capacity = selected_venue.get("kapasitas_penonton")
                    capacity_text = "Tidak tersedia" if pd.isna(capacity) else f"{capacity:,.0f}"
                    cards = [
                        ("Nama venue", venue_name, "venue-name"),
                        ("Jumlah pertandingan", match_count, ""),
                        ("Kapasitas penonton", capacity_text, ""),
                    ]
                    for column, (label, value, extra_class) in zip(
                        [detail1, detail2, detail3], cards
                    ):
                        with column:
                            st.markdown(
                                f"""
                                <div class="venue-kpi-card">
                                  <div class="venue-kpi-label">{label}</div>
                                  <div class="venue-kpi-value {extra_class}">{value}</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                    st.markdown("#### Informasi fasilitas")
                    info_lines = []
                    for label, col in [("Kecamatan", "kecamatan"), ("Kelurahan", "kelurahan"), ("Alamat", "alamatlokasi"), ("Luas (m²)", "luas_m2")]:
                        value = selected_venue.get(col)
                        if value is not None and not pd.isna(value) and str(value).strip():
                            info_lines.append(f"**{label}:** {value:,.0f}" if col == "luas_m2" and isinstance(value, (int, float)) else f"**{label}:** {value}")
                    st.markdown("  \n".join(info_lines) if info_lines else "Informasi fasilitas belum tersedia.")
                    selected_events = filtered_events[filtered_events["venue_id"].astype(str) == str(selected_id)].copy()
                    st.markdown("#### Pertandingan yang tercatat di venue ini")
                    if selected_events.empty:
                        st.info("Tidak ada pertandingan pada venue ini untuk filter yang dipilih.")
                    else:
                        cols = [c for c in ["tanggal_event", "kompetisi_sumber", "nama_event", "peserta_tim", "hasil_skor_normalisasi", "nama_venue"] if c in selected_events.columns]
                        selected_events = selected_events[cols].sort_values("tanggal_event", na_position="last")
                        selected_events = selected_events.rename(columns={"tanggal_event":"Tanggal", "kompetisi_sumber":"Kompetisi", "nama_event":"Nama event", "peserta_tim":"Tim peserta", "hasil_skor_normalisasi":"Skor", "nama_venue":"Venue"})
                        st.dataframe(selected_events, hide_index=True, width="stretch")


# ============================================================
# HALAMAN 3: ANALISIS KOMPETISI
# ============================================================
elif page == "Analisis Kompetisi":
    st.subheader("🏆 Perbandingan aktivitas antar-kompetisi")
    comp_summary = (
        filtered_events.groupby("kompetisi_sumber", as_index=False)
        .size()
        .rename(columns={"size": "jumlah_pertandingan"})
        .sort_values("jumlah_pertandingan", ascending=False)
    )
    if comp_summary.empty:
        st.info("Tidak ada event yang sesuai dengan filter.")
    else:
        fig = px.bar(
            comp_summary,
            x="kompetisi_sumber",
            y="jumlah_pertandingan",
            text="jumlah_pertandingan",
            labels={
                "kompetisi_sumber": "Kompetisi",
                "jumlah_pertandingan": "Jumlah pertandingan",
            },
            color_discrete_sequence=[PALETTE["forest"]],
        )
        fig.update_layout(xaxis_title=None, yaxis_title="Jumlah pertandingan")
        st.plotly_chart(style_plotly(fig, 390), width="stretch")

        if use_full_marts:
            comp_venue = mart_competition.rename(columns={"total_event": "jumlah_pertandingan"}).copy()
            comp_venue = comp_venue.drop(columns=["nama_venue"], errors="ignore")
            comp_venue = comp_venue.merge(venues[["venue_id", "nama_venue"]], on="venue_id", how="left")
        else:
            linked = filtered_events.dropna(subset=["venue_id"])
            comp_venue = (
                linked.groupby(["kompetisi_sumber", "venue_id"], as_index=False)
                .size()
                .rename(columns={"size": "jumlah_pertandingan"})
                .merge(venues[["venue_id", "nama_venue"]], on="venue_id", how="left")
            )
        if not comp_venue.empty:
            top_ids = (
                comp_venue.groupby("venue_id")["jumlah_pertandingan"]
                .sum()
                .nlargest(15)
                .index
            )
            comp_venue_top = comp_venue[comp_venue["venue_id"].isin(top_ids)]
            fig_mix = px.bar(
                comp_venue_top,
                x="jumlah_pertandingan",
                y="nama_venue",
                color="kompetisi_sumber",
                orientation="h",
                labels={
                    "nama_venue": "Venue",
                    "jumlah_pertandingan": "Jumlah pertandingan",
                    "kompetisi_sumber": "Kompetisi",
                },
                color_discrete_map=COMPETITION_COLORS,
            )
            fig_mix.update_layout(xaxis_title="Jumlah pertandingan", yaxis_title=None, barmode="stack", yaxis={"categoryorder":"total ascending"})
            fig_mix.update_yaxes(tickfont={"size": 11}, automargin=True)
            fig_mix.update_xaxes(tickfont={"size": 11}, automargin=True)
            fig_mix = style_plotly(fig_mix, max(450, 34 * len(comp_venue_top["nama_venue"].unique())))
            fig_mix.update_layout(barmode="stack", bargap=0.22)
            st.plotly_chart(fig_mix, width="stretch")




# ============================================================
# HALAMAN 4: ANALISIS FASILITAS
# ============================================================
if page == "Analisis Fasilitas":
    st.subheader("🏟️ Karakteristik fasilitas dan aktivitas venue")
    if use_full_marts:
        facility_df = mart_facility.copy()
        if "jumlah_pertandingan" not in facility_df.columns:
            facility_df["jumlah_pertandingan"] = pd.to_numeric(facility_df.get("total_event", 0), errors="coerce")
        if "nama_venue" not in facility_df.columns:
            facility_df = facility_df.merge(venues[["venue_id", "nama_venue"]], on="venue_id", how="left")
    else:
        facility_df = activity_venues.copy()

    if "nama_venue" not in facility_df.columns:
        facility_df = facility_df.drop(columns=["nama_venue_x", "nama_venue_y"], errors="ignore").merge(
            venues[["venue_id", "nama_venue"]], on="venue_id", how="left"
        )
    facility_df["jumlah_pertandingan"] = pd.to_numeric(facility_df["jumlah_pertandingan"], errors="coerce").fillna(0).astype(int)

    metric_cols = st.columns(3)
    metric_cols[0].metric("Jumlah venue terdata", f"{len(facility_df):,}")
    metric_cols[1].metric("Venue dengan data luas", f"{facility_df['luas_m2'].notna().sum():,}" if "luas_m2" in facility_df.columns else "0")
    metric_cols[2].metric("Venue dengan data kapasitas", f"{facility_df['kapasitas_penonton'].notna().sum():,}" if "kapasitas_penonton" in facility_df.columns else "0")

    st.caption("Klik satu titik pada grafik untuk menampilkan informasi venue dan daftar pertandingan di bawahnya.")
    chart_tab1, chart_tab2 = st.tabs(["Kapasitas penonton", "Luas fasilitas"])
    selected_venue_id = None
    with chart_tab1:
        if "kapasitas_penonton" in facility_df.columns:
            capacity_df = facility_df.dropna(subset=["kapasitas_penonton"]).copy().reset_index(drop=True)
            if not capacity_df.empty:
                fig_capacity = px.scatter(
                    capacity_df, x="kapasitas_penonton", y="jumlah_pertandingan",
                    custom_data=["venue_id"], hover_name="nama_venue",
                    hover_data={c: True for c in ["kecamatan", "kelurahan"] if c in capacity_df.columns},
                    labels={"kapasitas_penonton":"Kapasitas penonton", "jumlah_pertandingan":"Jumlah pertandingan"},
                    color_discrete_sequence=[PALETTE["teal"]], opacity=.88,
                )
                fig_capacity.update_traces(marker={"size":11,"line":{"width":1.5,"color":"#FFFFFF"}})
                fig_capacity.update_layout(xaxis_title="Kapasitas penonton", yaxis_title="Jumlah pertandingan")
                cap_event = st.plotly_chart(style_plotly(fig_capacity, 420), width="stretch", on_select="rerun", selection_mode="points", key="capacity_scatter")
                try:
                    inds = cap_event.selection.points
                    if inds:
                        selected_venue_id = capacity_df.iloc[int(inds[0]["point_index"])]["venue_id"]
                except (AttributeError, KeyError, IndexError, TypeError, ValueError):
                    pass
            else:
                st.info("Data kapasitas penonton belum tersedia untuk visualisasi.")

    with chart_tab2:
        if "luas_m2" in facility_df.columns:
            area_df = facility_df.dropna(subset=["luas_m2"]).copy().reset_index(drop=True)
            if not area_df.empty:
                fig_area = px.scatter(
                    area_df, x="luas_m2", y="jumlah_pertandingan",
                    custom_data=["venue_id"], hover_name="nama_venue",
                    hover_data={c: True for c in ["kecamatan", "kelurahan"] if c in area_df.columns},
                    labels={"luas_m2":"Luas fasilitas (m²)", "jumlah_pertandingan":"Jumlah pertandingan"},
                    color_discrete_sequence=[PALETTE["coral"]], opacity=.88,
                )
                fig_area.update_traces(marker={"size":11,"line":{"width":1.5,"color":"#FFFFFF"}})
                fig_area.update_layout(xaxis_title="Luas fasilitas (m²)", yaxis_title="Jumlah pertandingan")
                area_event = st.plotly_chart(style_plotly(fig_area, 420), width="stretch", on_select="rerun", selection_mode="points", key="area_scatter")
                try:
                    inds = area_event.selection.points
                    if inds:
                        selected_venue_id = area_df.iloc[int(inds[0]["point_index"])]["venue_id"]
                except (AttributeError, KeyError, IndexError, TypeError, ValueError):
                    pass
            else:
                st.info("Data luas fasilitas belum tersedia untuk visualisasi.")

    # Fallback dropdown juga memudahkan pemilihan venue tanpa harus klik titik.
    venue_lookup = facility_df[["venue_id", "nama_venue"]].drop_duplicates().sort_values("nama_venue")
    venue_names = venue_lookup["nama_venue"].fillna("Nama venue tidak tersedia").tolist()
    dropdown_name = st.selectbox("Atau pilih venue dari daftar", venue_names, key="facility_detail_venue") if venue_names else None
    # Jika pengguna mengklik titik, prioritaskan venue yang diklik. Dropdown menjadi alternatif.
    if selected_venue_id is not None:
        selected_rows_df = facility_df[facility_df["venue_id"].astype(str) == str(selected_venue_id)]
    else:
        selected_rows_df = facility_df[facility_df["nama_venue"] == dropdown_name] if dropdown_name else facility_df.iloc[0:0]

    if not selected_rows_df.empty:
        selected_row = selected_rows_df.iloc[0]
        st.markdown("### Detail venue")
        d1, d2, d3 = st.columns(3)
        d1.metric("Pertandingan tercatat", f"{int(selected_row['jumlah_pertandingan']):,}")
        cap = selected_row.get("kapasitas_penonton")
        d2.metric("Kapasitas penonton", "Tidak tersedia" if pd.isna(cap) else f"{cap:,.0f}")
        area = selected_row.get("luas_m2")
        d3.metric("Luas fasilitas", "Tidak tersedia" if pd.isna(area) else f"{area:,.0f} m²")
        detail_lines = []
        for label, col in [("Kecamatan", "kecamatan"), ("Kelurahan", "kelurahan"), ("Alamat", "alamatlokasi")]:
            value = selected_row.get(col)
            if value is not None and not pd.isna(value) and str(value).strip():
                detail_lines.append(f"**{label}:** {value}")
        st.markdown("  \n".join(detail_lines) if detail_lines else "Informasi lokasi belum tersedia.")
        selected_events = filtered_events[filtered_events["venue_id"].astype(str) == str(selected_row["venue_id"])].copy()
        st.markdown("#### Daftar pertandingan")
        if selected_events.empty:
            st.info("Tidak ada pertandingan yang cocok dengan filter pada venue ini.")
        else:
            detail_cols = [c for c in ["tanggal_event", "kompetisi_sumber", "nama_event", "peserta_tim", "hasil_skor_normalisasi"] if c in selected_events.columns]
            selected_events = selected_events[detail_cols].sort_values("tanggal_event", na_position="last")
            selected_events = selected_events.rename(columns={"tanggal_event":"Tanggal", "kompetisi_sumber":"Kompetisi", "nama_event":"Nama event", "peserta_tim":"Tim peserta", "hasil_skor_normalisasi":"Skor"})
            st.dataframe(selected_events, hide_index=True, width="stretch")

    st.caption("Catatan: luas dan kapasitas hanya dianalisis pada venue dengan data tersedia. Hubungan yang terlihat bersifat deskriptif, bukan bukti sebab-akibat.")

st.markdown(
    "<div class='footer-note'>Dibangun untuk eksplorasi data aktivitas pertandingan dan karakteristik venue sepak bola di Jawa Timur.</div>",
    unsafe_allow_html=True,
)
