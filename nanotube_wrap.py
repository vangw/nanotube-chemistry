import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d
import matplotlib.colors
import copy

with open("path to aux file", "r") as aux:
    dim = np.genfromtxt(aux, skip_header =3, max_rows = 1)

n = int(input("Enter the value for n: "))
m = int(input("Enter the value for m: "))

 

# Open coordinate file and import data to array
with open("path to crds file", "r") as crds:
    array = np.genfromtxt(crds)
# Defines the chiral vector based on a1 and a2 vectors
# This is then used to manipulate x,y coords onto the vector 
cos_theta = 0

# Doubles length of tube this will help when growing flakes on tube
def stack():
    x_array = copy.deepcopy(array)
    x_array[:,0] = np.add(x_array[:,0], np.array([dim[0] for i in range(x_array.shape[0])]))
    return np.vstack((array, x_array))
    
array = stack()   

def chiral_vector(n, m):
    # a1 vector is set along x axis
    a1 = np.array([np.sqrt(3),0])
    a2 = np.array([np.sqrt(3)/2, 3/2])
    # chiral vector is the dot product of n * a1 and m * a2
    chiral = np.add(np.multiply(a1, n), np.multiply(a2, m))
    print(chiral)
    return chiral/np.linalg.norm(chiral)
 
# Compute projections (direction* (dot product between direction and vector))
def project_point(point, chiral):
    projection = (point.T@chiral)
    return projection


# Wrap the 2d coordinates into a cylinder by maniuplating
# the y cooridnates and generating z coordinates,
# x coordinates changed based on chiral vector
def wrap(n, m):
    # Normalise to max length of the dimensions of the input celL
    cv = chiral_vector(n, m)
    print(cv)
    print(np.linalg.norm(cv))
    # Dot product formula to find cos theta
    cos_theta = np.dot(cv, np.array([1,0]))
    theta = np.arccos(cos_theta)
    # Make projections
    X = np.array([project_point(x, cv) for x in array])
    # Make orthogonals
    print(cos_theta)
    ortho_cv = np.array([-cv[1], cv[0]])
    Y = np.array([project_point(y, ortho_cv) for y in array])
    # After projecting array, move atoms back into the pbc box
    # so that wrapping produces flat ends
    x = 2 * ((dim[0] - np.sin(theta)) * np.cos(theta))
    V = np.multiply(cv, 2 * dim[0])
    for i in range(X.shape[0]):
        if X[i] > x:
            X[i] -= V[0]
            Y[i] += V[1]
    plt.scatter(X,Y)
    plt.show()
    # d is diameter
    d = dim[1]/ cos_theta
    # r is radius
    r = d / (2* np.pi)
    # Normalize those distances so that the furthest point gets converted to 2*pi
    y_length_factor = (2* np.pi) / d
    # Get the corresponding roll angle
    THETA = Y *y_length_factor
    # Generate Y and Z by shift to cylindrical coords
    Y_ = r * np.sin(THETA)
    Z = r * np.cos(THETA)
    # Stack X,Y,Z into (n,3) array
    tube = np.vstack((X, Y_, Z))
    # Transpose array to make (3,n) array of 3D coordinates
    tube = np.transpose(tube)
    return tube

 
    
# Plotting function
def plot_tube():
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection='3d')
    plot = ax.scatter(tube[:,0], tube[:,1], tube[:,2])
    plt.show()
    return

tube = wrap(n, m)       
print(tube)
plot_tube()


# create file and write it to vmd for visualisation
with open("path/nanotube_{:}_{:}.xyz".format(n, m), "w") as vmd:
    vmd.write("{:}\n\n " .format(tube.shape[0]))
    for i in range(tube.shape[0]):
        vmd.write("C{:} {:<10} {:<10} {:<10}\n" .format(i+1, tube[i,0], tube[i,1], tube[i,2]))
        
