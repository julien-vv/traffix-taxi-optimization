import streamlit as st
from astar import *

st.markdown("# Commute Time")

# part B page B
def main_part_b() :
    #start =str((39.843, 116.359))
    st.write("Hi! Please enter 2 coordinates and we will try to find the best path for you to take :)")
    col1, col2 = st.columns(2)
    with col1:
        start = input_user('Start')
    with col2:
        end = input_user('End')
    #start = str((39.984, 116.455))
    nb = 100
    st.write('If you want to try it out... : (39.887, 116.657) , (39.907, 116.509)')
    commute(start,end,nb)


main_part_b()