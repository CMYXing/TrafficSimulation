# Auxiliary function
# Returns the orthogonal vector of the input vector
def getOrthogonalVector(vector):
    x = vector[0]
    y = vector[1]
    orthogonalVector = [y, -x]
    return orthogonalVector

