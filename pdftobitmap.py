import cv2
import numpy as np

def convert_siteplan(input_path, output_path, threshold=None, invert=False, upscale_factor=1):
    """
    Convert a site plan image to a 120x80 B/W grid while preserving details.
    
    Parameters:
    - input_path: Path to input PNG file
    - output_path: Path to save output PNG
    - threshold: Pixel value threshold (0-255), None for Otsu's method
    - invert: Set True if image has white lines on black background
    - upscale_factor: Scale factor to preserve thin lines (1 = no scaling)
    """
    # Read image
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Could not read image from {input_path}")

    # Upscale image to preserve thin lines
    # if upscale_factor > 1:
    #     img = cv2.resize(img, None, 
    #                     fx=upscale_factor, 
    #                     fy=upscale_factor, 
    #                     interpolation=cv2.INTER_CUBIC)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    if threshold is None:
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    # Invert colors if needed
    # if invert:
    #     thresh = cv2.bitwise_not(thresh)

    # Calculate grid cell dimensions
    height, width = thresh.shape
    grid_width = 120
    grid_height = 80

    # Create output grid
    grid = np.ones((grid_height, grid_width), dtype=np.uint8) * 255

    # Calculate cell dimensions
    cell_w = width / grid_width
    cell_h = height / grid_height

    # Check each grid cell
    for y in range(grid_height):
        for x in range(grid_width):
            # Calculate cell boundaries
            x_start = int(x * cell_w)
            x_end = int((x + 1) * cell_w)
            y_start = int(y * cell_h)
            y_end = int((y + 1) * cell_h)
            
            # Extract cell region
            cell = thresh[y_start:y_end, x_start:x_end]
            
            # Mark black if any black pixels found
            if np.any(cell == 0):
                grid[y, x] = 0

    # Save output
    cv2.imwrite(output_path, grid)
    print(f"Successfully saved grid image to {output_path}")

# Example usage
if __name__ == "__main__":
    convert_siteplan(
        input_path="assets/simpleSitePlan.png",
        output_path="output2.png",
        threshold=None,  # Use Otsu's automatic threshold
        invert=False,    # Set True if white lines on black background
        upscale_factor=4 # Increase to preserve thinner lines
    )