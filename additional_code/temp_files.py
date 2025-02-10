from astar import *
# because out computers had a hard time handling the amount of data, for time puposes i created curated files to analyze thanks to this functions

# for space saving

def create_alt_data(nb_start, nb_end, files, path):
    col = ['id_taxi', 'date', 'loc']
    for k in range (0,0):
        path = 'release/taxi_log_2008_by_id/' + files[k]
        st.write(path)
        data = pd.read_fwf(path, delimiter=',', names = col)
        data['date'] = pd.to_datetime(data['date'])
        for i in range (len(data)):
            data.iloc[i,0] = i
        #st.write(data.head())
        # i set round to 3 because my computer is not strong enough to support more precision at this time
        data['latitude'] = round(data['loc'].map(get_latitude),3)
        data['longitude'] = round(data['loc'].map(get_longitude),3)
        data['temps'] = np.nan 
        
        # créer le graphique à partir des données
        date  =[]
        for i in range (len(data)-1):
            a = data.iloc[i+1,1] - data.iloc[i,1]
            data.iloc[i+1,5] = (a.total_seconds())
        
        # fct to create graph of all average time from 1 taxi    
        maze, labels = get_taxi_and_labels(data)

        labels_to_csv(labels,k)
        graph_to_csv(maze, k)


def labels_to_csv(labels,k):
    labels = pd.DataFrame(labels)
    pat = 'data/labels' + str(k+1)
    labels.to_csv(pat + '.txt', sep=',', index=False)

def graph_to_csv(maze, k):
    pat = 'data/taxi' + str(k+1)
    maze.to_csv(pat + '.txt', sep=',', index=False)