from astar import *
from density import * 
#from beijing import *

#MAIN
def main() :
    st.title("Analyzing the commute of taxi drivers in Beijing")

    #INTRODUCTION
    st.header("Introduction to the project")
    st.subheader("A couple of data visualizations")

    #PART A
    st.header("The streets of highest congestion rate")
    main_part_a()

    #PART B
    #st.header("Part B. The average time needed to reach from point A to point B​")
    #main_part_b()

    #PART C
    #st.header("Part C. The average car density of the city")
    #main_part_c()

st.markdown("# Main page")
st.sidebar.markdown("# Main page")

main()







