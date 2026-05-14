# Correlation Analysis: Image Features vs Watermark Robustness

## Method: LSB
### Attack: JPEG
|             |   NC_JPEG_LSB |
|:------------|--------------:|
| Brightness  |     -0.267776 |
| Contrast    |     -0.3026   |
| EdgeDensity |     -0.132456 |
| Entropy     |      0.578367 |


### Attack: Resize
|             |   NC_Resize_LSB |
|:------------|----------------:|
| Brightness  |       0.387027  |
| Contrast    |      -0.0230493 |
| EdgeDensity |       0.083318  |
| Entropy     |       0.0688953 |


## Method: DFT
### Attack: JPEG
|             |   NC_JPEG_DFT |
|:------------|--------------:|
| Brightness  |    -0.0878951 |
| Contrast    |    -0.0270762 |
| EdgeDensity |     0.276497  |
| Entropy     |     0.161651  |


### Attack: Resize
|             |   NC_Resize_DFT |
|:------------|----------------:|
| Brightness  |       -0.138933 |
| Contrast    |       -0.145805 |
| EdgeDensity |       -0.101015 |
| Entropy     |       -0.150669 |


## Method: Hybrid
### Attack: JPEG
|             |   NC_JPEG_Hybrid |
|:------------|-----------------:|
| Brightness  |       -0.109852  |
| Contrast    |       -0.0359098 |
| EdgeDensity |        0.28095   |
| Entropy     |        0.173782  |


### Attack: Resize
|             |   NC_Resize_Hybrid |
|:------------|-------------------:|
| Brightness  |          0.0835862 |
| Contrast    |         -0.0724127 |
| EdgeDensity |         -0.0783809 |
| Entropy     |         -0.168834  |


## SSIM vs Image Features
### Method: LSB
|             |   SSIM_LSB |
|:------------|-----------:|
| Brightness  |  0.0861727 |
| Contrast    | -0.219371  |
| EdgeDensity | -0.0143275 |
| Entropy     |  0.43291   |


### Method: DFT
|             |   SSIM_DFT |
|:------------|-----------:|
| Brightness  | -0.0640875 |
| Contrast    | -0.0878682 |
| EdgeDensity |  0.0962005 |
| Entropy     |  0.368542  |


### Method: Hybrid
|             |   SSIM_Hybrid |
|:------------|--------------:|
| Brightness  |    -0.0639851 |
| Contrast    |    -0.0878649 |
| EdgeDensity |     0.0962289 |
| Entropy     |     0.368511  |


