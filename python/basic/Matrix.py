
#mnx is a M*N matrix
def set_zero(mn_matrix):
    """Write an algorithm such that if an element in an MxN matrix is 0, its entire row and column is set to 0"""     
    
    row_flag = [0]*len(mn_matrix)
    column_flag = [0]*len(mn_matrix[0])
    for i in range(0, len(row_flag)):
        for j in range(0, len(column_flag)):
            if mn_matrix[i][j] == 0:
                row_flag[i] = 1
                column_flag[j] = 1
    
    for i in range(0, len(row_flag)):
        for j in range(0, len(column_flag)):
            if row_flag[i] == 1 or  column_flag[j] == 1:                
                mn_matrix[i][j] = 0
                
    

alist = [1,2,3]
for i in range(0,len(alist)):
    alist[i] = 0
    
#print alist   

mn_matrix = [[1,2,3],[4,0,6]]
print mn_matrix
set_zero(mn_matrix) 
print mn_matrix
