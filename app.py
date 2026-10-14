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
