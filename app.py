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
st.sidebar.title("Navigasi Dashboard")
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
st.title("⚽ Analisis Pola Pemanfaatan Lapangan Sepak Bola Jawa Timur")
st.caption(
    "Dashboard analitik yang mengintegrasikan data pertandingan Soeratin, Liga 1, "
    "AFF U-19 2024, dan karakteristik fasilitas venue."
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

    st.subheader("Jumlah pertandingan per kompetisi")
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
        )
        fig_comp.update_layout(xaxis_title=None, yaxis_title="Jumlah pertandingan")
        st.plotly_chart(fig_comp, use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.subheader("Venue dengan aktivitas terbanyak")
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
        )
        fig_top.update_layout(yaxis_title=None, xaxis_title="Jumlah pertandingan")
        st.plotly_chart(fig_top, use_container_width=True)

    with right:
        st.subheader("Tren pertandingan dari waktu ke waktu")
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
            )
            fig_trend.update_layout(xaxis_title=None, yaxis_title="Jumlah pertandingan")
            st.plotly_chart(fig_trend, use_container_width=True)

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
    st.subheader("Persebaran 67 venue berdasarkan koordinat")
    st.write(
        "Jumlah pertandingan pada peta mengikuti filter kompetisi dan periode di panel kiri. "
        "Venue yang tidak memiliki pertandingan pada filter saat ini tetap ditampilkan dengan nilai 0."
    )

    districts = sorted(
        activity_venues["kecamatan"].dropna().astype(str).unique().tolist()
    )
    selected_districts = st.multiselect(
        "Filter kecamatan (opsional)",
        options=districts,
        default=districts,
    )
    map_df = activity_venues.copy()
    map_df = map_df[map_df["kecamatan"].astype(str).isin(selected_districts)]
    map_df = map_df.dropna(subset=["latitude", "longitude"])

    if map_df.empty:
        st.warning("Tidak ada venue dengan koordinat pada filter yang dipilih.")
    else:
        map_center_lat = float(map_df["latitude"].median())
        map_center_lon = float(map_df["longitude"].median())
        map_layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position="[longitude, latitude]",
            get_radius=180,
            radius_min_pixels=4,
            radius_max_pixels=14,
            pickable=True,
            auto_highlight=True,
            get_fill_color=[20, 115, 180, 180],
            get_line_color=[255, 255, 255, 220],
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
                "style": {"backgroundColor": "#16202A", "color": "white"},
            },
            map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        )
        st.pydeck_chart(deck, use_container_width=True)
        st.caption(f"Jumlah titik pada peta: {len(map_df)} venue")

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
    st.subheader("Perbandingan aktivitas antar-kompetisi")
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
        )
        fig.update_layout(xaxis_title=None, yaxis_title="Jumlah pertandingan")
        st.plotly_chart(fig, use_container_width=True)

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
            )
            fig_mix.update_layout(xaxis_title=None, yaxis_title="Jumlah pertandingan")
            st.plotly_chart(fig_mix, use_container_width=True)

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
    st.subheader("Karakteristik fasilitas dan aktivitas venue")
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
            )
            fig_capacity.update_layout(xaxis_title="Kapasitas penonton", yaxis_title="Jumlah pertandingan")
            st.plotly_chart(fig_capacity, use_container_width=True)
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
            )
            fig_area.update_layout(xaxis_title="Luas fasilitas (m²)", yaxis_title="Jumlah pertandingan")
            st.plotly_chart(fig_area, use_container_width=True)
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
