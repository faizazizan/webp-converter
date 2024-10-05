import streamlit as st
from PIL import Image
import io
import zipfile

# Define a dictionary of predefined image sizes
IMAGE_SIZES = {
    "Open Graph Protocol": {
        "1600 x 900 (16:9)": (1600, 900),
        "1200 x 675 (16:9)": (1200, 675),
        "1200 x 1200 (1:1)": (1200, 1200),
        "1200 x 900 (4:3)": (1200, 900)
    },
    "Google Discover": {
        "1200 x 675 (16:9)": (1200, 675),
        "1200 x 900 (4:3)": (1200, 900),
        "1200 x 1200 (1:1)": (1200, 1200)
    },
    "Google News": {
        "1200 x 675 (16:9)": (1200, 675),
        "1200 x 900 (4:3)": (1200, 900),
        "1200 x 1200 (1:1)": (1200, 1200)
    },
    "Blog or Article Hero Images": {
        "1600 x 900 (16:9)": (1600, 900),
        "1200 x 675 (16:9)": (1200, 675),
        "1200 x 1200 (1:1)": (1200, 1200),
        "1200 x 900 (4:3)": (1200, 900)
    },
    "Infographic Image Sizing": {
        "600 x 2400 (1:4)": (600, 2400)
    },
    "Google Business Profile Image Sizes": {
        "Google Business posts: 1200 x 900 (4:3)": (1200, 900),
        "Google Business logo: 720 x 720 (1:1)": (720, 720),
        "Other Google Business photos: 1200 x 900 (4:3)": (1200, 900),
        "1200 x 1200 (1:1)": (1200, 1200),
        "1200 x 675 (16:9)": (1200, 675)
    },
    "Product Images on eCommerce Websites": {
        "At least 1500 x 1500 (1:1)": (1500, 1500)
    },
    "Product Images for Google Merchant Center (Google Shopping)": {
        "At least 1500 x 1500 (1:1)": (1500, 1500)
    }
}

def convert_to_webp(image, quality=80):
    with io.BytesIO() as output:
        image.save(output, format="WEBP", quality=quality)
        return output.getvalue()

def resize_image(image, size):
    return image.resize(size, Image.LANCZOS)

def main():
    st.title("WebP Converter with Resize Options")
    
    st.write("Upload your images (PNG or JPEG) to convert and resize them to WebP format for SEO-friendly purposes.")
    
    uploaded_files = st.file_uploader("Choose images", type=["png", "jpeg", "jpg"], accept_multiple_files=True)
    
    if uploaded_files:
        resize_option = st.selectbox("Select the resize option", list(IMAGE_SIZES.keys()))
        
        if resize_option:
            size_option = st.selectbox("Select the size", list(IMAGE_SIZES[resize_option].keys()))
            selected_size = IMAGE_SIZES[resize_option][size_option]
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:
            for uploaded_file in uploaded_files:
                image = Image.open(uploaded_file)
                resized_image = resize_image(image, selected_size)
                webp_data = convert_to_webp(resized_image)
                
                # Creating a name for the output file
                output_filename = uploaded_file.name.rsplit('.', 1)[0] + '.webp'
                
                # Writing the webp data to a new file in the zip
                zf.writestr(output_filename, webp_data)
        
        # Make sure the zip buffer is at the beginning of the stream
        zip_buffer.seek(0)
        
        # Provide a download link for the zip file
        st.download_button(
            label="Download All WebP Images",
            data=zip_buffer,
            file_name="converted_images.zip",
            mime="application/zip"
        )

if __name__ == "__main__":
    main()
