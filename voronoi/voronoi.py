#!/usr/bin/env python3

from __future__ import annotations

import numpy as np
from scipy.spatial import qhull, Voronoi, voronoi_plot_2d, cKDTree

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection, PolyCollection


LINE_WIDTH = 0.25
# COLORS = ['#000000', '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF', '#808080', '#FF8080', '#80FF80', '#8080FF', '#008080', '#800080', '#808000', '#FFFF80', '#80FFFF', '#FF80FF', '#FF0080', '#80FF00', '#0080FF', '#00FF80', '#8000FF', '#FF8000', '#000080', '#800000', '#008000', '#404040', '#FF4040', '#40FF40', '#4040FF', '#004040', '#400040', '#404000', '#804040', '#408040', '#404080', '#FFFF40', '#40FFFF', '#FF40FF', '#FF0040', '#40FF00', '#0040FF', '#FF8040', '#40FF80', '#8040FF', '#00FF40', '#4000FF', '#FF4000', '#000040', '#400000', '#004000', '#008040', '#400080', '#804000', '#80FF40', '#4080FF', '#FF4080', '#800040', '#408000', '#004080', '#808040', '#408080', '#804080', '#C0C0C0', '#FFC0C0', '#C0FFC0', '#C0C0FF', '#00C0C0', '#C000C0', '#C0C000', '#80C0C0', '#C080C0', '#C0C080', '#40C0C0', '#C040C0', '#C0C040', '#FFFFC0', '#C0FFFF', '#FFC0FF', '#FF00C0', '#C0FF00', '#00C0FF', '#FF80C0', '#C0FF80', '#80C0FF', '#FF40C0', '#C0FF40', '#40C0FF', '#00FFC0', '#C000FF', '#FFC000', '#0000C0', '#C00000', '#00C000', '#0080C0', '#C00080', '#80C000', '#0040C0', '#C00040', '#40C000', '#80FFC0', '#C080FF', '#FFC080', '#8000C0', '#C08000', '#00C080', '#8080C0', '#C08080', '#80C080', '#8040C0', '#C08040', '#40C080', '#40FFC0', '#C040FF', '#FFC040', '#4000C0', '#C04000', '#00C040', '#4080C0', '#C04080', '#80C040', '#4040C0', '#C04040', '#40C040', '#202020', '#FF2020', '#20FF20']
COLORS = ['#000000', '#00FF00', '#0000FF', '#FF0000', '#01FFFE', '#FFA6FE', '#FFDB66', '#006401', '#010067', '#95003A', '#007DB5', '#FF00F6', '#FFEEE8', '#774D00', '#90FB92', '#0076FF', '#D5FF00', '#FF937E', '#6A826C', '#FF029D', '#FE8900', '#7A4782', '#7E2DD2', '#85A900', '#FF0056', '#A42400', '#00AE7E', '#683D3B', '#BDC6FF', '#263400', '#BDD393', '#00B917', '#9E008E', '#001544', '#C28C9F', '#FF74A3', '#01D0FF', '#004754', '#E56FFE', '#788231', '#0E4CA1', '#91D0CB', '#BE9970', '#968AE8', '#BB8800', '#43002C', '#DEFF74', '#00FFC6', '#FFE502', '#620E00', '#008F9C', '#98FF52', '#7544B1', '#B500FF', '#00FF78', '#FF6E41', '#005F39', '#6B6882', '#5FAD4E', '#A75740', '#A5FFD2', '#FFB167', '#009BFF', '#E85EBE']
np.random.shuffle(COLORS)


# TODO : Parallelize
def generate_voronoi(layers: list[int]) -> list[qhull.Voronoi]:
  return [Voronoi(np.random.rand(count, 2)) for count in layers]


# TODO : Parallelize
def group_voronoi(layers: list[qhull.Voronoi], i: int = 1) -> list[list[int]]:
  assert(len(layers) >= 2)

  previous_vor = layers[i-1]
  current_vor = layers[i]

  tree = cKDTree(previous_vor.points)

  # This gives us a list of previous_vor.points indexes
  # The index in to this list is the index into current_vor.points
  result = tree.query(current_vor.points, workers=-1)[1]

  if i + 1 == len(layers):
    return [result]
  return [result] + group_voronoi(layers, i + 1)


def resolve_grouping(voronoi_grouping: list[qhull.Voronoi], element: int, group_index: int = 0) -> int:
  if group_index + 1 == len(voronoi_grouping):
    return voronoi_grouping[group_index][element]
  return voronoi_grouping[group_index][resolve_grouping(voronoi_grouping, element, group_index + 1)]


# TODO : Dict return annotations
def initialize_color_grouping(count: int):
  color_grouping = {}
  for color in range(count):
    color_grouping[COLORS[color]] = []
  color_grouping['white'] = []
  return color_grouping


# TODO : calculate infinate regions vertices
# TODO : type annotations
# TODO : parallelize
def associative_plot(voronoi_list, voronoi_grouping, ax):
  smallest_vor = voronoi_list[-1]

  color_grouping = initialize_color_grouping(voronoi_list[0].npoints)
  for i in range(smallest_vor.npoints):
    color = COLORS[resolve_grouping(voronoi_grouping, i)]

    region = np.asarray(smallest_vor.regions[smallest_vor.point_region[i]])
    if np.all(region >= 0):
      color_grouping[color].append(smallest_vor.vertices[region])

  for color, region in color_grouping.items():
    ax.add_collection(PolyCollection(region, lw=LINE_WIDTH, facecolor = color, edgecolor=color))


def main():
  voronoi_list = generate_voronoi([17, 125, 625, 3125, 15625, 78125, 390625])
  # voronoi_list = generate_voronoi([17, 125, 625])
  voronoi_grouping = group_voronoi(voronoi_list)

  fig, ax = plt.subplots()
  ax.axis('off')
  fig.tight_layout(pad = 0)

  # line_alpha = 1.0
  # linr_alpha_delta = 1.0 / len(voronoi_list)
  # voronoi_plot_2d(voronoi_list[0], ax, show_points = True, show_vertices = False, line_alpha = line_alpha)

  # for vor in voronoi_list[1:-1]:
  #   line_alpha -= linr_alpha_delta
  #   voronoi_plot_2d(vor, ax, show_points = False, show_vertices = False, line_alpha = line_alpha)

  # Associate smallest regions with the bigger ones and graph/color-code correctly
  associative_plot(voronoi_list, voronoi_grouping, ax)

  # for x1, y1 in voronoi_list[0].points:
  #   magnitude = np.random.uniform(low=0.0, high=0.1)
  #   direction = np.random.uniform(low=0.0, high=360.0)
  #   x2 = magnitude * np.cos(direction)
  #   y2 = magnitude * np.sin(direction)
  #   plt.annotate("", (x1+x2, y1+y2), xytext=(x1, y1), arrowprops={'arrowstyle': '->'})

  plt.box(None)
  plt.xlim(0, 1)
  plt.ylim(0, 1)
  plt.get_current_fig_manager().resize(2880, 961)
  plt.show()


if __name__ == "__main__":
  main()
