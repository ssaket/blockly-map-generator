import matplotlib.patches as patches
import matplotlib.pyplot as plt


def showLevelPNG(grid):
    """Generate a simple image of the maze.
    Args:
        grid (List[List[int]]): The maze grid.
    """
    plt.figure(figsize=(10, 5))
    plt.imshow(grid, cmap=plt.cm.binary, interpolation='nearest')
    plt.show()


def showLevelWithAgentPNG(grid, agent_paths):
    """Generate a simple image of the maze with agent path. The agent path is a list of coordinates.
    Args:
        grid (List[List[int]]): The maze grid.
        agent_paths (List[List[int]]): The agent path.
    """

    nrows = 1
    ncols = 1
    fig, ax = plt.subplots(nrows,
                           ncols,
                           sharex=False,
                           sharey=False,
                           squeeze=True)
    ax.imshow(grid, cmap=plt.cm.binary, interpolation='nearest')
    colors = ['maroon', 'royalblue', 'darkgray', 'coral', 'steelblue']

    for idx, path in enumerate(agent_paths):
        entrance_colors = ['dimgray', 'maroon']
        # for i, tile in enumerate(path):
        if idx == 0 or idx == len(agent_paths) - 1:
            color = entrance_colors.pop(idx % 2)
        else:
            color = colors[1]
        patch = patches.Circle((path[1], path[0]),
                               0.5,
                               linewidth=3,
                               edgecolor=color,
                               facecolor=color)
        ax.add_patch(patch)
    plt.show()


def showLevelPNGMark(grid, start, end):
    """Generate a simple image of the maze with start and end marker. The start and end are coordinates.
    Args:
        grid (List[List[int]]): The maze grid.
        start (List[int]): The start coordinate.
        end (List[int]): The end coordinate.
    """
    plt.figure(figsize=(10, 5))
    plt.imshow(grid, cmap=plt.cm.binary, interpolation='nearest')
    ax = plt.gca()
    start_patch = patches.Circle((start[1], start[0]),
                                 0.5,
                                 linewidth=3,
                                 edgecolor='r',
                                 facecolor='red')
    end_patch = patches.Circle((end[1], end[0]),
                               0.5,
                               linewidth=3,
                               edgecolor='g',
                               facecolor='green')
    ax.add_patch(start_patch)
    ax.add_patch(end_patch)
    plt.show()
