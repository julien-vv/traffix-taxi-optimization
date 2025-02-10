from data_process import *
from density import plot_clusters

df = pd.read_fwf('release/taxi_log_2008_by_id/1.txt' , delimiter = ',')

files = os.listdir('release/taxi_log_2008_by_id/')


# from original data to average

def get_taxi_and_labels (data):
    df = pd.DataFrame(np.nan, index = range(len(data)), columns = range(len(data)))
    for i in range (len(data)):
        for j in range (len(data)):
            if i+1 == j:
                df[i+1][j-1] = data.iloc[i+1,5]
    

    df['lat'] = data['latitude']
    df['lon'] = data['longitude']
    df = df.groupby(['lat', 'lon']).mean()
    # list of all coordinates remaining
    locations = list(zip(df.index))
    df = df.reset_index(drop= True)
    df2 =df.T
    df2['lat'] = data['latitude']
    df2['lon'] = data['longitude']
    df2 = df2.groupby(['lat', 'lon']).mean()
    df2 = df2.reset_index(drop= True)
    maze = df2.T
    return maze, locations


def graph_to_dict(maze):
    test= {}
    for i in range (len(maze)):
        for j in range(len(maze)):
            if np.isnan(maze.iloc[i,j]) == False:
                if i in test:
                    test[i].append(j)
                else:
                    test[i] = [j]
    return test


def get_path_and_cost(path, locations, maze):
    coord_path =[]
    cost =0
    if path == None:
        return 0,0
    # return list of coordinates
    for i in range (len(path)):
        # coord_path.append(locations[path[i]][0]) method1
        coord_path.append(locations.iloc[path[i],0])
        if i+1 in range(len(path)):
            cost += maze.iloc[path[i],path[i+1]]
    return coord_path, cost

def display_route(route):
    if len(route) != 0:
        route = pd.DataFrame(route)
        route['lat'], route['lon'] = 0,0
        for i in range (len(route)):
            route[0][i] = route[0][i][1:-1]
            route['lon'][i] = float(route[0][i].split(',')[1])
            route['lat'][i] = float(route[0][i].split(',')[0])
        route = route.drop([0], axis = 1)
        #st.write(route)
        return route

def display_cost(cost):
    if cost!=0:
        st.write(str(round(cost/60)), 'minutes for this route!')
    else: st.write('no path found for this taxi')

def compare_times(old, new):
    if new < old or old == 0:
        old = new
    return old

def compare_routes(old, new, t_old, t_new):
    if t_old == t_new:
        old = new
    return old

# A star algorithm
def find_shortest_path(graph,maze, start, end, path=[]):
            path = path + [start]
            if start == end:
                return path
            if start not in graph:
                return None
            shortest = None
            new_cost = 0
            for node in graph[start]:
                if node not in path:
                    newpath = find_shortest_path(graph,maze, node, end, path)
                    if newpath:
                        old_cost = new_cost
                        new_cost = 0
                        for i in range (len(newpath)-1):
                            new_cost += maze.iloc[newpath[i],newpath[i+1]]
                        if not shortest or old_cost ==0 or new_cost < old_cost:
                            shortest = newpath
            return shortest


def commute (start, end, nb):
    shortest_time = 0
    best_route = pd.DataFrame()
    # methode 2 pour parcourir les fichiers txt
    for p in range (0,nb):

        # if labels exist
        labels_path = 'data/labels'+ str(p+1) + '.txt'
        labels =pd.read_csv(labels_path) 
        i3=0
        i4=0

        for i2 in range (len(labels)):
            if labels.iloc[i2,0] == end:
                i3= i2
            if labels.iloc[i2,0] == start :
                i4 = i2
            
        if i2 != 0 and i3 !=0:
                pa = 'data/taxi'+ str(p+1) + '.txt'
                da =pd.read_csv(pa) 
                if len(da) < 400:
                    #st.write(str(p),': the file is a bit long... we will see if we have better options for now')
                #else:
                    #st.write(str(p), ': we found a path with this taxi!')
                    t = graph_to_dict(da)

                    rt = find_shortest_path(t, da, i4, i3)
                    gt, go = get_path_and_cost(rt, labels, da)

                    shortest_time = compare_times(shortest_time, go)
                    best_route = compare_routes(best_route, gt, shortest_time,go)

    display_cost(shortest_time)
    best = display_route(best_route)
    if shortest_time != 0:
        p = plot_clusters(39.93, 116.4, 10, 'roadmap', best["lon"], best["lat"])
        st.bokeh_chart(p)



def input_user(title):
    ## entrée
    st.write(title + ' coordinates: ')
    deb_lat = st.number_input(label= title + ' latitude',step=1.,format="%.3f", min_value= 39.700, max_value=40.100)
    deb_lon = st.number_input(label= title + ' longitude',step=1.,format="%.3f", min_value= 116.100, max_value=116.700)
    start = '('+str(deb_lat)+', '+str(deb_lon) +')'
    return start
