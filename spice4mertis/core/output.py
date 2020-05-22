import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def output(path):
    df = pd.read_csv(path)
    print(df.head())
    print(df.iloc[1])

    df.plot(x='et', y='emissn')
    #lt.show()

    s = df.max()
    nx, ny = int(s['pixlin']), int(s['pixsam'])
    x = np.linspace(1, nx,nx)
    y = np.linspace(1, ny,ny)
    phase_matrix = np.zeros((nx+1, ny+1))

    for i in x:
        for j in y:
            sdf = df.loc[(df['pixlin'] == i) & (df['pixsam'] == j)]
            phase = sdf.loc[:,'phase'].values[0]
            phase_matrix[int(i),int(j)] = phase

    plt.imshow(phase_matrix)
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    output("../tests/spice4mertis.csv")