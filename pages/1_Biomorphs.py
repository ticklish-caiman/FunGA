import streamlit as st

from utils.custom_css import custom_buttons_style, custom_write_style
from utils.genetic.biomorphs.biomorphs_evolve import draw_biomorph_pil, test_pass_choice, init_biomorphs_population, \
    evolve_biomrophs
from utils.genetic.biomorphs.biomorphs_phenotype import get_base64_of_image
from utils.navigation import show_main_menu
from utils.localization_helper import get_localizator

_ = get_localizator()
st.set_page_config(page_title=_("FunGA - About"), page_icon='🕹️')
show_main_menu(_)

st.header(_('Biomorphs'))
st.header(_('🚧 Project not yet ready 🚧'))
with st.expander(_("Biomorphs? What's this all about? (click to expand)"), expanded=False):
    custom_write_style()
    st.write(
        _("Witness the power of evolution in your hands! Biomorphs are like digital creatures in a race. Click on "
          "your favorite, and watch it inspire the next generation, with cooler shapes and features spreading through "
          "the pack. It's like playing God, but with way more clicks!"))
    st.write(_('Want to know full story behind Biomorphs?'))
    st.page_link('pages/4_Theory.py', label=_("Yes! (Click here)"))

custom_buttons_style()

num_columns = 3
num_rows = 4

if "clicked" not in st.session_state:
    st.session_state["clicked"] = None

if "biomorphs" not in st.session_state:
    st.session_state["biomorphs"] = init_biomorphs_population(num_columns * num_rows)

if "first_run" not in st.session_state:
    st.session_state["first_run"] = True

if not st.session_state["first_run"]:
    if st.button(_("🔄 START  AGAIN 🔄"), type='primary'):
        del st.session_state["biomorphs"]
        del st.session_state["first_run"]
        del st.session_state["clicked"]
        st.rerun()

biomorphs_img = []

for bm in st.session_state["biomorphs"]:
    biomorphs_img.append(get_base64_of_image(draw_biomorph_pil(bm)))


def on_click():
    if st.session_state["clicked"] is not None:
        biomorphs = evolve_biomrophs(st.session_state["biomorphs"], st.session_state["clicked"])
        st.session_state["biomorphs"] = biomorphs
        for biomorph in biomorphs:
            biomorphs_img.append(get_base64_of_image(draw_biomorph_pil(biomorph)))
        st.session_state["clicked"] = None
        # Forcing rerun so the page gets updated after the first click (BUT DOESN'T SHOW EVOLVED POPULATION!)
        # The workaround: make the user click once to initiate and only then display biomorphs
        st.rerun()


biomorph_id = 0
# Dynamic grid creation
for row in range(num_rows):
    cols = st.columns(num_columns)
    start_index = row * num_columns
    end_index = start_index + num_columns

    for i, biomorph_img in enumerate(biomorphs_img[start_index:end_index]):
        col_index = i % num_columns  # Get the column index within the current row
        with cols[col_index]:
            with st.container(border=1):
                if not st.session_state["first_run"]:
                    if st.button(_("⬇️ Choose me ⬇️"), key=biomorph_id, on_click=on_click()):
                        st.session_state["clicked"] = biomorph_id
                        test_pass_choice(biomorph_id)
                    st.image(biomorph_img, width=200)
                else:
                    # To bypass "the double click bug" we make the user click on a blank array first
                    if st.button(_("START GENERATING"), key=biomorph_id, on_click=on_click()):
                        st.session_state["clicked"] = biomorph_id
                        test_pass_choice(biomorph_id)
                        st.session_state["first_run"] = False
            biomorph_id += 1
