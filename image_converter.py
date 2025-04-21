import os
import numpy as np
import cv2
from astropy.io import fits

# Set the root directory containing your FITS files
fits_directory = './2025-04-19/M_81'  # <-- Change this!
output_root = os.path.join(fits_directory, 'png_output')

for root, _, files in os.walk(fits_directory):
    for filename in files:
        if filename.lower().endswith(('.fits', '.fit')):
            filepath = os.path.join(root, filename)

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

                    # Create the output path, maintaining relative directory structure
                    relative_path = os.path.relpath(root, fits_directory)
                    output_dir = os.path.join(output_root, relative_path)
                    os.makedirs(output_dir, exist_ok=True)

                    output_path = os.path.join(
                        output_dir,
                        filename.rsplit('.', 1)[0] + '.png'
                    )
                    cv2.imwrite(output_path, image_rgb)

print("Recursive conversion complete.")
