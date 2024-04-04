import streamlit as st
import gettext

from utils.custom_css import custom_write_style
from utils.navigation import show_main_menu, get_localizator

_ = get_localizator()
st.set_page_config(page_title=_("FunGA - About"), page_icon='📚')

show_main_menu(_)

tabs_options = [_("Hello Darwin!"), _("Problem solving"), _("Similar approaches")]

tabs = st.tabs(tabs_options)
with tabs[0]:
    st.header(_('Natural selection and genetic algorithms'))
    custom_write_style()
    st.write(_("""The elegance of evolution theory lies in its simplicity, a testament to the genius of Charles Darwin. At its core, evolution paints a picture of remarkable change driven by a few fundamental principles: variation, inheritance, and selection. It is the variations within a population, those slight differences that make each individual unique, that provide the raw material upon which evolution acts. These traits are passed down through inheritance, a link between generations ensuring the continuation of both successful and less successful adaptations. Finally, selection is the force that shapes these variations, favoring traits that enhance an organism's ability to survive and reproduce in a given environment.  A never-ending dance of change, a gradual sculpting over countless generations, leading to the breathtaking diversity of life we see today.

It's this same elegance and inherent power of adaptation that inspired the field of genetic algorithms. Like biological evolution, genetic algorithms operate on a population of potential solutions. Here, a "solution" could be anything from the optimal design for an airplane wing to a strategy for winning a complex game. Each solution is represented by a kind of digital genome, a set of instructions or parameters that define it.

The process within a genetic algorithm mirrors natural selection. Solutions are evaluated for their fitness – how well they solve the problem at hand. The fittest solutions are then allowed to "reproduce." In this digital realm, reproduction involves combining and mutating the digital genomes of parent solutions, much like the shuffling and occasional changes that happen to genes in biological reproduction. These offspring, with their inherited and slightly modified traits, form the next generation of solutions.

Over successive generations, the genetic algorithm ruthlessly weeds out less optimal solutions and promotes more promising ones. Variations are explored, successful traits are combined, and gradually the average fitness of the population improves. The brilliance lies in how this blind, iterative process can navigate complex landscapes of possible solutions, often converging on unexpectedly effective and creative results.

From the grand tapestry of biological life, woven by natural selection, to the computational optimization of genetic algorithms, the idea of continuous, adaptive improvement is a potent one. Darwin's insights, born from meticulous observation of the natural world, have reverberated far beyond biology, laying the foundation for the astonishing problem-solving capabilities of modern computing."""))
with tabs[1]:
    st.header('Hello Holland/De Jong')
with tabs[2]:
    st.header('Hello others')
