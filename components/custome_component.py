import streamlit as st


def draw_custom_tile(Name, value, bg_color="White", color="Black"):
    card_class = "metric-card"
    if bg_color == "red" or bg_color == "Red":
        card_class += " alert"
    
    st.markdown(
        f"""
        <div class="{card_class}">
            <p class="label">{Name}</p>
            <p class="value">{value}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
