import matplotlib.pyplot as plt

x=[1, 2, 3, 4, 5]
power=[1, 0, 1, 1, 0]
plt.plot(x, power, #label='Freezer OnOff', 
            marker='o', markersize=2, linewidth=1, alpha=0.8, color='blue')

#plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
#plt.grid(True, alpha=0.3)
plt.ylim(-0.5, 1.5)

plt.tight_layout()
#plt.subplots_adjust(right=0.85)  # 凡例のスペースを確保
plt.show()