from src.file_read_jpsi import read_file
import numpy as np
import matplotlib.pyplot as plt

plus_two_body = read_file(mode=4, interest="B+", MAX_EVENTS=10, selection=True)
plt.hist(plus_two_body, bins=100)