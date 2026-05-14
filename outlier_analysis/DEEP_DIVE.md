# Deep Dive Analysis

## Hybrid Resize Performance
### Top 5 Images (Resize)
|    | Category        |   NC_Resize_Hybrid |   EdgeDensity |   Entropy |   Brightness |
|---:|:----------------|-------------------:|--------------:|----------:|-------------:|
| 35 | electric_guitar |           0.75     |       38.2129 |   3.08316 |      22.8734 |
| 42 | flamingo_head   |           0.71875  |       10.8947 |   7.13053 |      83.2514 |
|  9 | bass            |           0.703125 |       38.7571 |   5.8035  |      73.586  |
| 48 | headphone       |           0.6875   |       41.4821 |   2.73397 |     163.34   |
| 70 | panda           |           0.6875   |       23.8127 |   7.50107 |      94.7012 |

### Bottom 5 Images (Resize)
|    | Category   |   NC_Resize_Hybrid |   EdgeDensity |   Entropy |   Brightness |
|---:|:-----------|-------------------:|--------------:|----------:|-------------:|
|  4 | accordion  |           0        |     1170.39   |   6.87795 |      77.6548 |
| 71 | pigeon     |           0        |      323.997  |   6.75552 |     190.819  |
| 82 | sea_horse  |           0        |       37.0241 |   5.68693 |      83.2176 |
| 85 | stapler    |           0        |      295.911  |   6.03899 |     191.833  |
| 10 | beaver     |           0.390625 |      537.905  |   4.22618 |     172.858  |

## Hybrid JPEG Performance
### Top 5 Images (JPEG)
|    | Category   |   NC_JPEG_Hybrid |   EdgeDensity |   Entropy |   Brightness |
|---:|:-----------|-----------------:|--------------:|----------:|-------------:|
|  4 | accordion  |         0.828125 |      1170.39  |   6.87795 |      77.6548 |
|  1 | Faces_easy |         0.8125   |       197.355 |   7.48304 |     136.9    |
| 28 | crocodile  |         0.8125   |       763.972 |   7.65166 |     136.958  |
| 34 | dragonfly  |         0.8125   |      5167.02  |   5.14904 |     209.853  |
| 90 | sunflower  |         0.8125   |       144.951 |   5.17372 |      66.3139 |

### Bottom 5 Images (JPEG)
|    | Category        |   NC_JPEG_Hybrid |   EdgeDensity |   Entropy |   Brightness |
|---:|:----------------|-----------------:|--------------:|----------:|-------------:|
| 97 | wild_cat        |         0.59375  |      108.279  |   7.70827 |     150.853  |
| 85 | stapler         |         0.609375 |      295.911  |   6.03899 |     191.833  |
| 35 | electric_guitar |         0.625    |       38.2129 |   3.08316 |      22.8734 |
| 42 | flamingo_head   |         0.625    |       10.8947 |   7.13053 |      83.2514 |
| 43 | garfield        |         0.625    |     1020.66   |   3.49826 |     229.216  |

