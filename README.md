# FunGA

![FunGA_logo1_small](https://github.com/ticklish-caiman/FunGA/assets/91501936/49f9182c-15fc-4e71-9a74-b7eadd630728)

<p align="justify">
"In life sciences, funga is a recent term for the kingdom fungi similar to the longstanding fauna for animals and flora for plants."
  <p align="right">Source: https://en.wikipedia.org/wiki/Funga</p>
<p align="justify">
But in this app FunGA stands for Fun with Genetic Algorithms!
An awesome way to understand the coding techniques inspired by Darwinian natural selection.
</p>


# The plan
Must-haves:

    • easy to use web interface in Streamlit
    • some theory - necessary boring part
    • some practice - awesome fun part, interactive GA
 

Should-haves:


    • basic optimization - caching and maybe some JS magic
    • unit tests

Could-haves:


    • some database solution for saving and loading experiments
    • other fun topics like Conway's Game of life
    • Neural-Networks also would be NEAT ;) 
    • Second language

Won't-haves:


    • Integrated chat-bot
    • Loot-boxes
    • Micro-transactions


<p align="justify">
Possible problems:
</p>
    
    • Streamlit may not be enough for some functionality - switching to other library may be necessary
  UPDATE: <br/>
  Pure Python approach is nice, all seems easy at first, 
  but the lack of robust native support for persistent client-side storage is a valid limitation of Streamlit.
  I am also not a fan of top-down refreshes on almost every action.
  Well... let's look for different library.<br/>
  UPDATE 2: <br/>
  2h of research and I still don't know what to do :( <br/>
  Going Flask with some template is one idea, but I don't want to spend too much time dealing with front end.
  <br/>So... there the options are:

    • accept the Streamlit flaws (no user-side data) and design the whole app without "memory"
    • use Streamlit with use st.query_params, but that will do only for parameters, not large data
    • use Streamlit with handwritten server-side cache (some solution for user ID required - st.query_params?)
    • use Streamlit with additional libraries like streamlit-cookies-manager
    • use Streamlit with database (probably would still require some additional libraries for users management)
    • migrate to Anvil, Panel, Dash or Flask

It's important do decide soon! <br/>
I could start building other components in Streamlit - if that goes well I may stick with SL, but if I hit another wall I'll switch to a different framework.

# Roadmap
1. GUI template<br/>
![2%](https://progress-bar.dev/2?title=progress&width=400)
2. Theory<br/>
![0%](https://progress-bar.dev/0?title=progress&width=400)
3. Pipelines:<br/>
   a) Treevolution<br/>
   ![0%](https://progress-bar.dev/0?title=progress&width=400) <br/>
   b) Shapevo<br/>
   ![0%](https://progress-bar.dev/0?title=progress&width=400) <br/>
   c) TSP <br/>
   ![0%](https://progress-bar.dev/0?title=progress&width=400) <br/>
   d) ? <br/>
   e) ? <br/>
     

