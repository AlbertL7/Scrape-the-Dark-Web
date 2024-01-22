import re
import sys

def strip_html_tags_keep_images_remove_javascript(html_content):
    # Remove JavaScript
    no_script = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

    # Pattern to find image file paths within HTML tags
    img_pattern = r'(<img[^>]*src\s*=\s*["\']?)([a-zA-Z0-9\s_\\.\-\(\):\/]+?\.(jpg|jpeg|png))(["\']?[^>]*>)'

    # Replace image tags with a placeholder that includes the image path
    placeholder_format = "IMAGE_PLACEHOLDER_{0}"
    placeholders = {}
    def replace_with_placeholder(match):
        img_path = match.group(2)  # Image path is in group 2
        placeholder = placeholder_format.format(img_path)
        placeholders[placeholder] = img_path
        return placeholder
    no_script = re.sub(img_pattern, replace_with_placeholder, no_script, flags=re.IGNORECASE)
    
    # Remove HTML tags
    no_html = re.sub(r'<[^>]+>', '', no_script)

    # Collapse multiple whitespace characters into a single space
    no_html = re.sub(r'\s+', ' ', no_html)
    
    # Replace placeholders with actual image paths
    for placeholder, img_path in placeholders.items():
        no_html = no_html.replace(placeholder, img_path)
    
    return no_html

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_file_path output_file_path")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    # Read HTML content from file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Process the HTML content
    cleaned_content = strip_html_tags_keep_images_remove_javascript(html_content)

    # Write the cleaned content to output file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

    print(f"Processed content written to {output_file_path}")
