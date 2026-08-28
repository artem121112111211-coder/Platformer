import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
for num in range(1, 5):
    level_name = f"level{num}.json"
    with open(f"Levels/{level_name}", "r") as file:
        level_matrix = json.load(file)
    grid = np.array(level_matrix)
    rows, cols = grid.shape
    color_list = [
        '#FFFFFF',
        '#CD853F',
        '#7CFC00',
        '#FF4500',
        '#FFFFFF',
        '#4F4F4F',
        '#FFD700'
    ]
    cmap = ListedColormap(color_list)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(grid, cmap=cmap, vmin=0, vmax=len(color_list)-0.5)
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    ax.grid(which='minor', color='#555555', linestyle='-', linewidth=0.5)
    ax.axis('off')
    output_image_name = level_name.replace(".json", ".png")
    output_path = f'Levels/level{num}.png'
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0, dpi=300)
    plt.close()
    print(f"Изображение карты уровня успешно сохранено как {output_path}")