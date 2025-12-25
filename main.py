import os

import streamlit as st
from dotenv import load_dotenv
from streamlit_folium import st_folium

from config import APP_SUBTITLE, APP_TITLE, MAP_TILES, SLIDERS, START_INDEX
from core.ant_algorithm import ant_colony_opt
from core.matrix_utils import build_distance_matrix
from data.coordinates import LOCATIONS
from visual.plotting import build_history_chart, build_route_map


def load_api_key() -> str:
    load_dotenv()
    return os.environ.get("GOOGLE_MAPS_API_KEY") or st.secrets.get("GOOGLE_MAPS_API_KEY", "")


@st.cache_data(show_spinner=False)
def get_distance_matrix(api_key: str):
    return build_distance_matrix(LOCATIONS, api_key)


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    st.title(APP_TITLE)
    st.caption(APP_SUBTITLE)

    if "run" not in st.session_state:
        st.session_state["run"] = False

    api_key = load_api_key()
    if not api_key:
        st.info("GOOGLE_MAPS_API_KEY bulunamadi; haversine (kus ucusu) mesafesi kullanilacak.")

    col_left, col_right = st.columns([1, 2], gap="large")

    with col_left:
        st.subheader("Parametreler")
        iterations = st.slider("Iterasyon", *SLIDERS["iterations"])
        num_ants = st.slider("Karinca sayisi", *SLIDERS["num_ants"])
        alpha = st.slider("a (feromon etkisi)", *SLIDERS["alpha"])
        beta = st.slider("b (mesafe etkisi)", *SLIDERS["beta"])
        evaporation = st.slider("Buharlasma orani", *SLIDERS["evaporation"])
        q = st.slider("Q (birakilan feromon)", *SLIDERS["q"])

        if st.button("Algoritmayi Calistir", type="primary"):
            st.session_state["run"] = True

        st.subheader("Toplanma Alanlari")
        st.dataframe(
            [{"id": i, **loc} for i, loc in enumerate(LOCATIONS)],
            use_container_width=True,
            hide_index=True,
        )

    with col_right:
        if st.session_state.get("run"):
            with st.spinner("Mesafe matrisi aliniyor..."):
                dist_matrix, source, error = get_distance_matrix(api_key)

            if source == "google":
                st.success("Google Distance Matrix (driving distance) kullanildi.")
            else:
                if error:
                    st.warning(
                        "Google Distance Matrix cagrisi basarisiz oldu, haversine (kus ucusu) mesafeye gecildi. "
                        f"Detay: {error}"
                    )
                st.info("Haversine (kus ucusu) mesafesi kullanildi.")

            with st.spinner("Karinca kolonisi calisiyor..."):
                best_route, best_length, history = ant_colony_opt(
                    dist_matrix,
                    iterations=iterations,
                    num_ants=num_ants,
                    alpha=alpha,
                    beta=beta,
                    evaporation=evaporation,
                    q=q,
                    start_index=START_INDEX,
                )

            km = best_length / 1000
            order_ids = best_route + [best_route[0]]
            order_labels = " -> ".join(str(i) for i in order_ids)
            order_names = " -> ".join(LOCATIONS[i]["name"] for i in order_ids)

            st.metric("En iyi rota mesafesi", f"{km:.2f} km")
            st.write("Rota sirasi (id):", order_labels)
            st.write("Rota (isimler):", order_names)

            st.subheader("Harita")
            fmap = build_route_map(LOCATIONS, best_route, MAP_TILES)
            st_folium(fmap, width=None, height=480)

            st.subheader("Iterasyonlara gore en iyi mesafe (km)")
            chart = build_history_chart(history).properties(height=280)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Parametreleri ayarlayip 'Algoritmayi Calistir' butonuna tiklayin.")


if __name__ == "__main__":
    main()
