import os
import numpy as np
import cv2
from astropy.io import fits

# Set the directory containing your FITS files
fits_directory = './2025-04-19/M_44/Light'  # <-- Change this!
output_directory = os.path.join(fits_directory, 'png_output')
os.makedirs(output_directory, exist_ok=True)

for filename in os.listdir(fits_directory):
    if filename.lower().endswith(('.fits', '.fit')):
        filepath = os.path.join(fits_directory, filename)

        with fits.open(filepath) as hdul:
            data = hdul[0].data

            if data is None:
                continue

            if data.ndim == 3:
                data = data[0]

            data = np.nan_to_num(data)
            data_min, data_max = np.min(data), np.max(data)

            if data_max > data_min:
                norm_data = (data - data_min) / (data_max - data_min)
                image_8bit = np.uint8(norm_data * 255)

                # Convert single channel grayscale to 3-channel grayscale
                image_rgb = cv2.cvtColor(image_8bit, cv2.COLOR_GRAY2BGR)

                output_path = os.path.join(
                    output_directory,
                    filename.rsplit('.', 1)[0] + '.png'  # safer replace
                )
                cv2.imwrite(output_path, image_rgb)

print("Conversion complete.")
