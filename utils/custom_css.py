import streamlit as st


# Setting custom style for tabs
def custom_css():
    st.markdown("""
    <style>
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: #e0e5ec; /* Light color */
    border-radius: 4px 4px 0px 0px;
    gap: 1px;
    padding-top: 10px;
    padding-bottom: 10px;
    padding-left: 10px;
    padding-right: 10px;
    transition: background-color 0.2s ease; /* Add transition */
}

.stTabs [aria-selected="true"] {
    background-color: #FFFFFF;
}

.stTabs [data-baseweb="tab"]:hover {
    background-color: #d1d8e0; /* Slightly darker on hover */
} 

// Custom style for sidebar buttons
div.stButton > button:first-child {
    background-color: #578a00;
    color:#ffffff;
}
div.stButton > button:hover {
    background-color: #00128a;
    color:#ffffff;
    }
    </style>""", unsafe_allow_html=True)

    # Setting custom width spectrum for sidebar, hide default menu
    st.sidebar.markdown("""
        <style>
        [data-testid="stSidebar"][aria-expanded="true"]{
       min-width: 350px;
       max-width: 800px;
           }   
        [data-testid="stSidebarNavItems"] {
        max-height: 0px;
        visibility: hidden;
        }
        [data-testid="stSidebarNavSeparator"] {
        visibility: hidden;
        }
     </style>""", unsafe_allow_html=True)


def custom_buttons_style():
    st.sidebar.markdown("""
    <style>
        div.element-container div.row-widget.stButton { 
            display: flex;
            justify-content: center; /* Horizontal Centering */
            # align-items: center;     /* Vertical Centering */
        }
        div.element-container div.row-widget.stButton > button { 
            background-color: #228B22; 
            color: #ffffff;
        }
        div.element-container div.row-widget.stButton > button:hover { 
            background-color: #00FF00; 
            color: #ffffff;
        }
    </style>
    """, unsafe_allow_html=True)


def custom_write_style():
    st.sidebar.markdown("""
    <style>
    p {
      text-align: justify;
    }
    </style>
    """, unsafe_allow_html=True)
