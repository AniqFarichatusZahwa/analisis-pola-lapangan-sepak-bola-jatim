from pathlib import Path

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
# SISTEM DESAIN DASHBOARD — INSPIRED BY BLUE/GOLD EAST JAVA IDENTITY
# ============================================================
# Warna diambil sebagai interpretasi visual dari referensi pengguna,
# bukan palet resmi Pemerintah Provinsi Jawa Timur.
PALETTE = {
    "forest": "#1757A6",  # biru utama untuk grafik
    "deep": "#102A5E",    # navy
    "teal": "#247DB6",    # biru sekunder
    "lime": "#F2C14E",    # aksen emas
    "gold": "#F2C14E",    # aksen emas
    "coral": "#C44D5E",   # aksen merah untuk pembeda
    "blue": "#72B7F2",    # biru muda
    "ink": "#1D2C46",     # teks utama
    "muted": "#6B7890",   # teks sekunder
    "grid": "#E2E9F3",    # garis grid
}
CHART_COLORS = [PALETTE["forest"], PALETTE["teal"], PALETTE["gold"], PALETTE["coral"], PALETTE["blue"]]

# Logo proyek berbentuk perisai olahraga, dibuat khusus untuk dashboard ini.
# Bukan logo resmi pemerintah atau federasi sepak bola.
LOGO_SVG = """
<svg viewBox="0 0 100 112" role="img" aria-label="Logo Lapangan Jatim" xmlns="http://www.w3.org/2000/svg">
  <path d="M50 5 L88 19 L84 59 Q78 84 50 105 Q22 84 16 59 L12 19 Z" fill="#163B7A" stroke="#F2C14E" stroke-width="4"/>
  <path d="M25 31 Q50 20 75 31" fill="none" stroke="#FFFFFF" stroke-width="2" opacity=".8"/>
  <circle cx="50" cy="48" r="17" fill="#FFFFFF" stroke="#F2C14E" stroke-width="2.5"/>
  <path d="M50 38 L59 44 L56 55 L44 55 L41 44 Z" fill="#163B7A"/>
  <path d="M50 31 L50 38 M65 41 L59 44 M61 61 L56 55 M39 61 L44 55 M35 41 L41 44" stroke="#163B7A" stroke-width="2.5" fill="none"/>
  <path d="M29 73 H71 M33 80 H67 M40 87 H60" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" opacity=".95"/>
</svg>
"""

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
      --navy: #102A5E;
      --royal: #1757A6;
      --royal-light: #2875C7;
      --sky: #72B7F2;
      --gold: #F2C14E;
      --ink: #1D2C46;
      --muted: #6B7890;
      --canvas: #F3F6FB;
      --line: #E2E9F3;
    }
    html, body, [class*="css"] { font-family: 'DM Sans', 'Segoe UI', sans-serif; }
    [data-testid="stAppViewContainer"] { background: var(--canvas); color: var(--ink); }
    [data-testid="stHeader"] { background: rgba(243,246,251,.96); }
    [data-testid="stMainBlockContainer"] { padding-top: 1.4rem; padding-bottom: 3rem; max-width: 1580px; }
    h1, h2, h3 { font-family: 'Manrope', 'DM Sans', sans-serif !important; color: var(--navy); letter-spacing: -.03em; }
    h2 { font-size: 1.42rem !important; margin-top: 1.15rem !important; }
    h3 { font-size: 1.12rem !important; }
    p, label, .stCaption { color: var(--muted); }

    /* Sidebar bergaya portal institusi: navy dengan aksen emas */
    [data-testid="stSidebar"] { background: linear-gradient(165deg, #102A5E 0%, #153D7D 58%, #1D5599 100%); }
    [data-testid="stSidebar"] > div:first-child { background: transparent; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] strong,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color: #F4F7FC !important; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label { padding: .24rem .1rem; }
    [data-testid="stSidebar"] input[type="radio"] { accent-color: var(--gold); }
    [data-testid="stSidebar"] [data-baseweb="select"] > div { border-radius: 12px; }
    [data-testid="stSidebar"] [data-baseweb="tag"] { background: var(--gold) !important; border: 0 !important; }
    [data-testid="stSidebar"] [data-baseweb="tag"] span { color: var(--navy) !important; font-weight: 700; }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.22); }
    .sidebar-brand { padding: .35rem 0 1.15rem 0; border-bottom: 1px solid rgba(255,255,255,.22); margin-bottom: 1.2rem; }
    .sidebar-brand-line { display:flex; align-items:center; gap:.72rem; color:#FFFFFF; font-weight:800; font-size:1.08rem; letter-spacing:-.025em; }
    .brand-logo-small { display:inline-flex; width:43px; min-width:43px; align-items:center; justify-content:center; }
    .brand-logo-small svg { width:42px; height:48px; display:block; }
    .sidebar-small { color:#C8D8F0; font-size:.72rem; margin-top:.45rem; margin-left:3.45rem; letter-spacing:.105em; text-transform:uppercase; }

    /* Banner utama: navy/royal blue, logo proyek, aksen emas */
    .hero-header { position:relative; overflow:hidden; padding:1.7rem 2rem 1.8rem; border-radius:8px; margin-bottom:1.35rem;
        background: radial-gradient(circle at 91% 12%, rgba(114,183,242,.27), transparent 23%),
                    radial-gradient(circle at 80% 120%, rgba(242,193,78,.15), transparent 28%),
                    linear-gradient(118deg, #102A5E 0%, #174A92 57%, #1D62AF 100%);
        box-shadow: 0 12px 28px rgba(16,42,94,.15); }
    .hero-header:after { content:''; position:absolute; width:340px; height:340px; border:1px solid rgba(255,255,255,.12); border-radius:50%; right:-95px; top:-155px; box-shadow:0 0 0 28px rgba(255,255,255,.025),0 0 0 56px rgba(255,255,255,.02); pointer-events:none; }
    .hero-brand-row { position:relative; z-index:1; display:flex; align-items:center; gap:.9rem; margin-bottom:1.15rem; }
    .hero-logo { display:flex; align-items:center; justify-content:center; width:58px; min-width:58px; height:64px; }
    .hero-logo svg { width:54px; height:61px; display:block; }
    .hero-brand-title { color:#FFFFFF; font-weight:800; font-size:.91rem; letter-spacing:.13em; text-transform:uppercase; }
    .hero-brand-subtitle { color:#C8D8F0; font-size:.78rem; margin-top:.16rem; }
    .hero-kicker { position:relative; z-index:1; display:inline-block; padding:.34rem .7rem; border:1px solid rgba(242,193,78,.62); background:rgba(242,193,78,.12); border-radius:3px; color:#FFE5A1; font-size:.71rem; font-weight:800; letter-spacing:.13em; text-transform:uppercase; margin-bottom:.8rem; }
    .hero-title { position:relative; z-index:1; color:#FFFFFF; font-family:'Manrope','DM Sans',sans-serif; font-size:clamp(1.65rem, 3vw, 2.5rem); line-height:1.18; font-weight:800; letter-spacing:-.04em; margin:0; max-width:1000px; }
    .hero-subtitle { position:relative; z-index:1; color:#DBE7F8; font-size:.98rem; line-height:1.65; margin:.8rem 0 0; max-width:930px; }
    .hero-foot { position:relative; z-index:1; display:flex; flex-wrap:wrap; gap:.55rem; margin-top:1.2rem; }
    .hero-tag { color:#F6F8FC; border:1px solid rgba(255,255,255,.24); background:rgba(255,255,255,.08); border-radius:4px; padding:.4rem .7rem; font-size:.78rem; }

    /* KPI, grafik, tabel, dan kontrol */
    [data-testid="stMetric"] { background:#FFFFFF; border:1px solid #DCE5F2; border-top:3px solid var(--royal); padding:1.02rem 1.15rem; border-radius:8px; box-shadow:0 5px 17px rgba(16,42,94,.045); min-height:112px; }
    [data-testid="stMetricLabel"] { color:#687892 !important; font-size:.83rem !important; font-weight:600 !important; }
    [data-testid="stMetricValue"] { color:var(--navy) !important; font-family:'Manrope','DM Sans',sans-serif; font-weight:800; letter-spacing:-.04em; }
    [data-testid="stPlotlyChart"] { background:#FFFFFF; padding:.45rem .55rem .2rem; border:1px solid #E1E8F2; border-radius:8px; box-shadow:0 5px 16px rgba(16,42,94,.035); }
    [data-testid="stDataFrame"] { border:1px solid #DCE5F2; border-radius:8px; overflow:hidden; }
    [data-testid="stDownloadButton"] button, [data-testid="stButton"] button { background:var(--royal); color:white; border:1px solid var(--royal); border-radius:6px; font-weight:700; padding:.55rem 1rem; transition:all .15s ease; }
    [data-testid="stDownloadButton"] button:hover, [data-testid="stButton"] button:hover { background:var(--navy); border-color:var(--navy); color:white; }
    [data-testid="stAlert"] { border-radius:8px; }
    [data-testid="stSelectbox"] [data-baseweb="select"] > div,
    [data-testid="stMultiSelect"] [data-baseweb="select"] > div,
    [data-testid="stDateInput"] input { border-radius:8px; }
    .section-note { color:#718098; font-size:.9rem; line-height:1.55; margin-top:-.3rem; margin-bottom:.65rem; }
    .footer-note { color:#8190A6; font-size:.78rem; padding-top:1rem; border-top:1px solid #DFE7F2; margin-top:1.5rem; }

    @media (max-width: 760px) {
      .hero-header { padding:1.25rem; border-radius:8px; }
      .hero-logo { width:47px; min-width:47px; }
      .hero-logo svg { width:45px; height:51px; }
      .hero-brand-title { font-size:.75rem; }
      [data-testid="stMetric"] { padding:.8rem; min-height:95px; }
      [data-testid="stMainBlockContainer"] { padding-left:1rem; padding-right:1rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def style_plotly(fig, height: int = 410):
    """Apply consistent blue-and-gold styling to Plotly charts without changing their data."""
    fig.update_layout(
        template="plotly_white",
        colorway=CHART_COLORS,
        font={"family": "DM Sans, Segoe UI, sans-serif", "size": 12, "color": "#34435D"},
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="#FFFFFF",
        height=height,
        margin={"l": 18, "r": 18, "t": 24, "b": 24},
        hoverlabel={"bgcolor": PALETTE["deep"], "font": {"color": "#FFFFFF", "size": 12}, "bordercolor": PALETTE["deep"]},
        legend={"bgcolor": "rgba(255,255,255,0)", "orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "left", "x": 0},
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="#DCE5F2", tickfont={"color": "#65748D"}, automargin=True)
    fig.update_yaxes(showgrid=True, gridcolor="#E2E9F3", zeroline=False, linecolor="#DCE5F2", tickfont={"color": "#65748D"}, automargin=True)
    return fig

BASE_DIR = Path(__file__).resolve().parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
FACT_PATH = PROCESSED_DIR / "fact_event.csv"
VENUE_PATH = PROCESSED_DIR / "dim_venue.csv"


@st.cache_data(show_spinner="Memuat data dari hasil integrasi...")
def load_data(fact_path: str, venue_path: str):
    """Membaca CSV hasil integrasi dari notebook audit_data.ipynb."""
    events = pd.read_csv(fact_path, sep=";", encoding="utf-8-sig")
    venues = pd.read_csv(venue_path, sep=";", encoding="utf-8-sig")

    # Pastikan nama kolom ID dan atribut utama tersedia.
    required_event_cols = {"id_event", "kompetisi_sumber", "venue_id"}
    required_venue_cols = {"venue_id", "nama_venue", "latitude", "longitude"}
    missing_event = required_event_cols - set(events.columns)
    missing_venue = required_venue_cols - set(venues.columns)
    if missing_event:
        raise ValueError(f"Kolom wajib tidak ada di fact_event.csv: {sorted(missing_event)}")
    if missing_venue:
        raise ValueError(f"Kolom wajib tidak ada di dim_venue.csv: {sorted(missing_venue)}")

    # Konversi angka koordinat dan karakteristik fasilitas.
    for col in ["latitude", "longitude", "luas_m2", "kapasitas_penonton"]:
        if col in venues.columns:
            venues[col] = pd.to_numeric(venues[col], errors="coerce")

    # Gunakan tanggal ISO dari preprocessing jika tersedia.
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

    # Beberapa kolom teks bisa tidak tersedia pada sebagian data.
    for col in ["kecamatan", "kelurahan", "alamatlokasi", "nama_fasilitas_olahraga"]:
        if col not in venues.columns:
            venues[col] = pd.NA

    return events, venues


if not FACT_PATH.exists() or not VENUE_PATH.exists():
    st.title("⚽ Analisis Pola Pemanfaatan Lapangan Sepak Bola Jawa Timur")
    st.error("File data hasil integrasi belum ditemukan.")
    st.markdown(
        "Pastikan notebook `audit_data.ipynb` sudah dijalankan sampai selesai, "
        "kemudian letakkan kedua file berikut di folder `data/processed/` dalam repository:"
    )
    st.code(
        "data/processed/fact_event.csv\n"
        "data/processed/dim_venue.csv",
        language="text",
    )
    st.info(
        "File tersebut dibuat oleh notebook pada tahap integrasi event dan dimensi venue. "
        "Setelah keduanya tersedia, refresh aplikasi ini."
    )
    st.stop()

try:
    events, venues = load_data(str(FACT_PATH), str(VENUE_PATH))
except Exception as exc:
    st.error(f"Gagal membaca data: {exc}")
    st.stop()


# ============================================================
# FILTER GLOBAL
# ============================================================
st.sidebar.markdown(
    f"""
    <div class="sidebar-brand">
      <div class="sidebar-brand-line"><span class="brand-logo-small">{LOGO_SVG}</span><span>Lapangan Jatim</span></div>
      <div class="sidebar-small">Sports venue analytics</div>
    </div>
    """,
    unsafe_allow_html=True,
)
page = st.sidebar.radio(
    "Pilih halaman",
    [
        "Ringkasan Aktivitas",
        "Peta Persebaran Venue",
        "Analisis Kompetisi",
        "Analisis Fasilitas",
    ],
)

st.sidebar.divider()
st.sidebar.subheader("Filter data")
competition_options = sorted(events["kompetisi_sumber"].dropna().unique().tolist())
selected_competitions = st.sidebar.multiselect(
    "Kompetisi",
    options=competition_options,
    default=competition_options,
)

valid_dates = events["tanggal_event"].dropna()
if not valid_dates.empty:
    date_min = valid_dates.min().date()
    date_max = valid_dates.max().date()
    start_date = st.sidebar.date_input(
        "Tanggal mulai",
        value=date_min,
        min_value=date_min,
        max_value=date_max,
    )
    end_date = st.sidebar.date_input(
        "Tanggal akhir",
        value=date_max,
        min_value=date_min,
        max_value=date_max,
    )
else:
    start_date = end_date = None
    st.sidebar.caption("Tanggal event tidak tersedia untuk difilter.")

filtered_events = events[events["kompetisi_sumber"].isin(selected_competitions)].copy()
if start_date is not None and end_date is not None:
    if start_date > end_date:
        st.sidebar.warning("Tanggal mulai melebihi tanggal akhir.")
    else:
        filtered_events = filtered_events[
            filtered_events["tanggal_event"].dt.date.between(start_date, end_date)
            | filtered_events["tanggal_event"].isna()
        ].copy()


# ============================================================
# HELPER AGREGASI
# ============================================================
def get_activity_by_venue(event_df: pd.DataFrame, venue_df: pd.DataFrame) -> pd.DataFrame:
    matched = event_df.dropna(subset=["venue_id"])
    counts = (
        matched.groupby("venue_id", as_index=False)
        .size()
        .rename(columns={"size": "jumlah_pertandingan"})
    )
    result = venue_df.merge(counts, on="venue_id", how="left")
    result["jumlah_pertandingan"] = result["jumlah_pertandingan"].fillna(0).astype(int)
    return result


activity_venues = get_activity_by_venue(filtered_events, venues)


# ============================================================
# HEADER
# ============================================================
st.markdown(
    f"""
    <div class="hero-header">
      <div class="hero-brand-row">
        <div class="hero-logo">{LOGO_SVG}</div>
        <div>
          <div class="hero-brand-title">Lapangan Jatim</div>
          <div class="hero-brand-subtitle">Portal Analitik Sepak Bola · Jawa Timur</div>
        </div>
      </div>
      <div class="hero-kicker">Data Warehouse · Sports Venue Intelligence</div>
      <div class="hero-title">Analisis Pola Pemanfaatan<br>Lapangan Sepak Bola Jawa Timur</div>
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


# ============================================================
# HALAMAN 1: RINGKASAN AKTIVITAS
# ============================================================
if page == "Ringkasan Aktivitas":
    linked_events = filtered_events[filtered_events["venue_id"].notna()]
    active_venue_count = linked_events["venue_id"].nunique()
    missing_venue_count = int(filtered_events["venue_id"].isna().sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total event sesuai filter", f"{len(filtered_events):,}")
    c2.metric("Event dengan venue", f"{len(linked_events):,}")
    c3.metric("Venue aktif", f"{active_venue_count:,}")
    c4.metric("Event tanpa venue", f"{missing_venue_count:,}")

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
            color_discrete_sequence=[PALETTE["forest"]],
        )
        fig_comp.update_layout(xaxis_title=None, yaxis_title="Jumlah pertandingan")
        st.plotly_chart(style_plotly(fig_comp, 390), use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.subheader("🏟️ Venue dengan aktivitas terbanyak")
        top_venues = activity_venues.nlargest(10, "jumlah_pertandingan")
        fig_top = px.bar(
            top_venues.sort_values("jumlah_pertandingan"),
            x="jumlah_pertandingan",
            y="nama_venue",
            orientation="h",
            labels={
                "nama_venue": "Venue",
                "jumlah_pertandingan": "Jumlah pertandingan",
            },
            color_discrete_sequence=[PALETTE["teal"]],
        )
        fig_top.update_layout(yaxis_title=None, xaxis_title="Jumlah pertandingan")
        st.plotly_chart(style_plotly(fig_top, 440), use_container_width=True)

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
            st.plotly_chart(style_plotly(fig_trend, 390), use_container_width=True)

    st.subheader("Ringkasan data")
    st.dataframe(
        comp_summary.rename(
            columns={
                "kompetisi_sumber": "Kompetisi",
                "jumlah_pertandingan": "Jumlah pertandingan",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

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
    st.write(
        "Jumlah pertandingan pada peta mengikuti filter kompetisi dan periode di panel kiri. "
        "Venue yang tidak memiliki pertandingan pada filter saat ini tetap ditampilkan dengan nilai 0."
    )

    map_df = activity_venues.copy()
    # Venue tanpa nilai kecamatan tetap dapat ditampilkan; diberi kategori filter tersendiri.
    map_df["_filter_kecamatan"] = map_df["kecamatan"].fillna("Tidak diketahui").astype(str)
    districts = sorted(map_df["_filter_kecamatan"].unique().tolist())
    selected_districts = st.multiselect(
        "Filter kecamatan (opsional)",
        options=districts,
        default=districts,
    )
    map_df = map_df[map_df["_filter_kecamatan"].isin(selected_districts)]
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
            get_fill_color=[37, 112, 196, 235],
            get_line_color=[242, 193, 78, 245],
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
                "style": {"backgroundColor": "#102A5E", "color": "white", "borderRadius": "8px", "padding": "10px", "border": "1px solid #F2C14E"},
            },
            map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        )
        map_selection = st.pydeck_chart(
            deck,
            use_container_width=True,
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
                    detail1, detail2, detail3 = st.columns(3)
                    detail1.metric("Nama venue", str(selected_venue.get("nama_venue", "-")))
                    detail2.metric(
                        "Jumlah pertandingan",
                        f"{int(selected_venue.get('jumlah_pertandingan', 0)):,}",
                    )
                    capacity = selected_venue.get("kapasitas_penonton")
                    detail3.metric(
                        "Kapasitas penonton",
                        "Tidak tersedia" if pd.isna(capacity) else f"{capacity:,.0f}",
                    )
                    detail_cols = [
                        col for col in [
                            "nama_venue", "kecamatan", "kelurahan", "alamatlokasi",
                            "luas_m2", "kapasitas_penonton", "jumlah_pertandingan",
                            "latitude", "longitude",
                        ] if col in selected_match.columns
                    ]
                    st.dataframe(selected_match[detail_cols], hide_index=True, use_container_width=True)

    display_cols = [
        col for col in [
            "nama_venue", "kecamatan", "kelurahan", "jumlah_pertandingan",
            "latitude", "longitude", "alamatlokasi"
        ]
        if col in map_df.columns
    ]
    st.dataframe(
        map_df[display_cols].sort_values("jumlah_pertandingan", ascending=False),
        use_container_width=True,
        hide_index=True,
    )


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
        st.plotly_chart(style_plotly(fig, 390), use_container_width=True)

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
                x="nama_venue",
                y="jumlah_pertandingan",
                color="kompetisi_sumber",
                barmode="stack",
                labels={
                    "nama_venue": "Venue",
                    "jumlah_pertandingan": "Jumlah pertandingan",
                    "kompetisi_sumber": "Kompetisi",
                },
                color_discrete_sequence=CHART_COLORS,
            )
            fig_mix.update_layout(xaxis_title=None, yaxis_title="Jumlah pertandingan")
            st.plotly_chart(style_plotly(fig_mix, 470), use_container_width=True)

        st.dataframe(
            comp_summary.rename(
                columns={
                    "kompetisi_sumber": "Kompetisi",
                    "jumlah_pertandingan": "Jumlah pertandingan",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# HALAMAN 4: ANALISIS FASILITAS
# ============================================================
if page == "Analisis Fasilitas":
    st.subheader("🏟️ Karakteristik fasilitas dan aktivitas venue")
    facility_df = activity_venues.copy()

    metric_cols = st.columns(3)
    metric_cols[0].metric("Total venue", f"{len(facility_df):,}")
    metric_cols[1].metric(
        "Luas tersedia",
        f"{facility_df['luas_m2'].notna().sum():,}" if "luas_m2" in facility_df.columns else "0",
    )
    metric_cols[2].metric(
        "Kapasitas tersedia",
        f"{facility_df['kapasitas_penonton'].notna().sum():,}" if "kapasitas_penonton" in facility_df.columns else "0",
    )

    if "kapasitas_penonton" in facility_df.columns:
        capacity_df = facility_df.dropna(subset=["kapasitas_penonton"]).copy()
        if not capacity_df.empty:
            fig_capacity = px.scatter(
                capacity_df,
                x="kapasitas_penonton",
                y="jumlah_pertandingan",
                hover_name="nama_venue",
                hover_data=[col for col in ["kecamatan", "kelurahan"] if col in capacity_df.columns],
                labels={
                    "kapasitas_penonton": "Kapasitas penonton",
                    "jumlah_pertandingan": "Jumlah pertandingan",
                },
                color_discrete_sequence=[PALETTE["teal"]],
                opacity=0.86,
            )
            fig_capacity.update_traces(marker={"size": 10, "line": {"width": 1.5, "color": "#FFFFFF"}})
            fig_capacity.update_layout(xaxis_title="Kapasitas penonton", yaxis_title="Jumlah pertandingan")
            st.plotly_chart(style_plotly(fig_capacity, 420), use_container_width=True)
        else:
            st.info("Data kapasitas penonton belum tersedia untuk visualisasi.")

    if "luas_m2" in facility_df.columns:
        area_df = facility_df.dropna(subset=["luas_m2"]).copy()
        if not area_df.empty:
            fig_area = px.scatter(
                area_df,
                x="luas_m2",
                y="jumlah_pertandingan",
                hover_name="nama_venue",
                hover_data=[col for col in ["kecamatan", "kelurahan"] if col in area_df.columns],
                labels={
                    "luas_m2": "Luas fasilitas (m²)",
                    "jumlah_pertandingan": "Jumlah pertandingan",
                },
                color_discrete_sequence=[PALETTE["coral"]],
                opacity=0.86,
            )
            fig_area.update_traces(marker={"size": 10, "line": {"width": 1.5, "color": "#FFFFFF"}})
            fig_area.update_layout(xaxis_title="Luas fasilitas (m²)", yaxis_title="Jumlah pertandingan")
            st.plotly_chart(style_plotly(fig_area, 420), use_container_width=True)
        else:
            st.info("Data luas fasilitas belum tersedia untuk visualisasi.")

    cols = [
        col for col in [
            "nama_venue", "kecamatan", "kelurahan", "alamatlokasi",
            "nama_fasilitas_olahraga", "luas_m2", "kapasitas_penonton",
            "jumlah_pertandingan", "latitude", "longitude"
        ]
        if col in facility_df.columns
    ]
    st.dataframe(
        facility_df[cols].sort_values("jumlah_pertandingan", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Catatan: luas dan kapasitas hanya dianalisis pada venue yang memiliki nilai tersedia. "
        "Grafik menunjukkan hubungan deskriptif, bukan bukti sebab-akibat."
    )


st.markdown(
    "<div class='footer-note'>Dibangun untuk eksplorasi data aktivitas pertandingan dan karakteristik venue sepak bola di Jawa Timur.</div>",
    unsafe_allow_html=True,
)
