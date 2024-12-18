# Pix2Print

## Overview
Pix2Print is a web-based application built with Python that enables users to upload 2D images and transform them into 3D-printable files. The application analyzes the uploaded image, extracts its distinct colors, and converts each color into a separate 3D-printable layer. This innovative process allows users to bring their 2D images to life as vibrant, multi-layered 3D prints.


## Features
- **PNG to STL Conversion**: Seamlessly converts PNG images into multiple STL file layers for 3D printing.
- **Customizable Layer Output**: Allows users to adjust the number of color layers extracted from the original image.
- **Configurable Resolution**: Provides the ability to modify the resolution of the generated 3D layers to suit user preferences or project requirements.
- **Tier-Based Subscription**: Offers flexible subscription plans, granting access to features like higher resolution outputs or additional layers based on the selected tier.
## Installation
1. Clone the repository:
    ```bash
    git clone git@github.com:IanStocker02/pix2print.git
    ```

2. Install dependencies:
    ```bash
    npm install
    ```

3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add your GitHub token to the `.env` file:
     ```
     GITHUB_TOKEN=your-github-token
     ```

4. Run the development server:
    ```bash
    npm run dev
    ```

## Usage
### Navigate to the Start Converting page:
- Upload your image in PNG format that you would like to convert
- Select amount of colors and resolution settings
- Click convert

### View Saved STL conversions:
- blank
- blank

## Project Structure
```plaintext



# colorverter
This application allows you to upload an image file and convert it into 3d-printable layers.
