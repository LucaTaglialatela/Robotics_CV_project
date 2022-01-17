import numpy as np

rotation_matrix = np.array([[np.cos(np.pi/4), -np.sin(np.pi/4)],
                            [np.sin(np.pi/4), np.cos(np.pi/4)]])
x_diff = 629.0421173517079- 629.5378878678919
y_diff = 388.90070240098277- 702.962791317086

pos = np.array([x_diff, y_diff])
new_pos = np.matmul(rotation_matrix, pos.T)
#new_pos = rotation_matrix @ pos.T
new_x_ratio = new_pos[0] / 100
new_y_ratio = new_pos[1]/ 100

print(new_x_ratio, new_y_ratio)