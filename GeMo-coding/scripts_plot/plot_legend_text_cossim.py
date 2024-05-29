import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.legend_handler import HandlerPatch
import seaborn as sns
import matplotlib.lines as mlines

# Define the colors and text labels
# colors = ['#222222', '#444444', '#666666', '#888888', '#AAAAAA', '#CCCCCC']

palette = sns.color_palette("Paired")
palette_set2 = sns.color_palette("Set2")

colors = [palette_set2[0]] + palette[6:10]

labels = [
    'src', 
    '$T=0.5,p=0.9$',
    '$T=0.5,p=1.0$',
    '$T=1.0,p=0.9$',
    '$T=1.0,p=1.0$',
]

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 1))

# Turn off axis and set transparent background
ax.set_axis_off()
fig.patch.set_visible(False)

# Create a list of rectangle markers
# markers = [mpatches.Rectangle((0, 0), 10, 10, facecolor=color, edgecolor='none') for color in colors]
markers = [mlines.Line2D([], [], color=color, marker='_', linestyle='-', linewidth=3) for color in colors]


# Create the legend
legend = ax.legend(markers, labels, loc='center', ncol=5, frameon=False,
                   handler_map={mpatches.Rectangle: HandlerPatch(patch_func=None)},
                   handlelength=0.8, handletextpad=0.4)

# Adjust the legend layout
plt.setp(legend.get_texts(), ha='center', va='center')

# Display the legend
plt.savefig('figs/fig_legend_text_cossim.pdf', bbox_inches='tight')