import numpy as np

z_i = 64.86
i_height = 1.612
t_height = 0.5

v = 105.5636
s_dist = 14.1658

z_t = z_i + i_height + (s_dist * np.cos(v * np.pi/180)) - t_height
print(z_t)
