from imports import *

#FUNCTIONS
@st.cache
def load_data(nb_taxis):
    all_files = os.listdir("release/taxi_log_2008_by_id")   # imagine you're one directory above test dir
    location_history = pd.read_fwf("release/taxi_log_2008_by_id/1.txt", delimiter = ',', names = ["id", "date/time", "lat/lon"])
    y = 0
    for i in all_files[0:10]:
        print(y)
        y += 1
        file_path = "release/taxi_log_2008_by_id/" + i
        df = pd.read_fwf(file_path, delimiter = ',', names = ["id", "date/time", "lat/lon"])
        location_history = pd.concat([location_history, df], ignore_index = True)
    location_history[['longitude','latitude']] = location_history["lat/lon"].str.split(",", expand = True)
    location_history['latitude'] = pd.to_numeric(location_history['latitude'])
    location_history['longitude'] = pd.to_numeric(location_history['longitude'])
    location_history = location_history.drop(["lat/lon"], axis = 1)
    location_history = location_history.dropna().reset_index(drop = True)
    return location_history

def dbscan_clustering(location_history, eps, min_samples) :
    lonlat = location_history[["longitude", "latitude"]]

    db = DBSCAN(eps = eps, min_samples = min_samples).fit(lonlat)
    core_samples_mask = np.zeros_like(db.labels_, dtype = bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)
    st.write("Estimated number of clusters : %d" % n_clusters_)
    st.write("Estimated number of noise points : %d" % n_noise_)

    #Taking off noise points
    save = []
    cst = 0
    for i in labels :
        if i == -1 :
            save.append(cst)
        cst += 1
    db.labels_ = np.delete(labels, save)
    lonlat = lonlat.drop(labels = save, axis = 0)
    
    return lonlat, labels

def plot_clusters(lat, lng, zoom, map_type, long, lati):
    gmap_options = GMapOptions(lat = lat, lng = lng, map_type = map_type, zoom = zoom)
    p = gmap("AIzaSyAB40FfjoLqTHLVWLHUeYysIlJlTg8gbEI", gmap_options,
             title = 'Beijing congestion points', width = 800, height = 800, tools = ['hover', 'reset', 'wheel_zoom', 'pan'])
    p.circle(long, lati, size = 5, alpha = 0.5, color = "red")
    
    return p


def main_part_a():
    location_history = load_data(100)
    st.write("Data of the 100 first taxis")
    #location_history

    col1, col2 = st.columns([1,4])
    with col1:
        eps = st.slider("Select size of clusters (in meters)", 10, 100, 20, step = 5)
        eps = eps / 100000
        min_samples = st.slider("Select minimum number of samples to make a cluster", 50, 500, 100, step = 50)
        lonlat, labels = dbscan_clustering(location_history, eps, min_samples)
    with col2:
        p = plot_clusters(39.93, 116.4, 10, 'roadmap', lonlat["longitude"], lonlat["latitude"])
        st.bokeh_chart(p)
