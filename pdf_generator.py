from fpdf import FPDF
import os
from datetime import datetime
import locale
import io
import random

class ReportPDF(FPDF):
    def __init__(self):
        super().__init__()
        # Set larger margins (left, top, right) in mm
        self.set_margins(20, 10, 20)  # Increased from default 10mm to 20mm for left and right
        # Add Unicode font
        self.add_font('DejaVu', '', 'assets/DejaVuSansCondensed.ttf', uni=True)
        self.add_font('DejaVu', 'B', 'assets/DejaVuSansCondensed-Bold.ttf', uni=True)
        self.add_font('DejaVu', 'I', 'assets/DejaVuSansCondensed-Oblique.ttf', uni=True)

    def header(self):
        # Add logo
        if os.path.exists('assets/logo_tk.png'):
            self.image('assets/logo_tk.png', 20, 8, 50)  # Adjusted x position from 10 to 20
        
        # Add contact information
        self.set_font('DejaVu', '', 10)
        self.set_text_color(0, 136, 204)  # Gray color
        
        # Calculate width of text components for right alignment
        info_text = 'GitHub | '
        url_text = 'LinkedIn'
        info_width = self.get_string_width(info_text)
        url_width = self.get_string_width(url_text)
        total_width = info_width + url_width
        
        # Position for right alignment with new margin
        x_position = self.w - total_width - 20  # Adjusted from 10 to 20
        
        # Print email part
        self.set_x(x_position)
        self.cell(info_width, 8, info_text, 0, 0, link='https://github.com/Temurbek-stack')
        
        # Print URL as link
        self.set_text_color(0, 136, 204)  # Blue color for link
        self.cell(url_width, 8, url_text, 0, 0, link='www.linkedin.com/in/temurbek-khasanboev')
        self.ln(20)

        # Add horizontal line
        self.set_draw_color(0, 48, 73) # Blue color for line
        self.set_line_width(0.5)  # Make line thicker
        self.line(20, 28, self.w - 20, 28)  # Adjusted x positions from 10 to 20

    def footer(self):
        # Set position at 1.5 cm from bottom
        self.set_y(-15)
        # DejaVu italic 8
        self.set_font('DejaVu', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def format_price(price_str):
    try:
        # Remove $ and commas, then convert to float
        price = float(str(price_str).replace('$', '').replace(',', ''))
        # Format with spaces instead of commas
        return f"{price:,.0f}".replace(',', ' ')
    except (ValueError, AttributeError):
        return price_str

def create_report(property_details, predicted_price, price_range):
    # Create PDF object
    pdf = ReportPDF()
    
    # First page
    pdf.add_page()
    
    # Main title with dark blue color
    pdf.set_font('DejaVu', 'B', 24)
    pdf.set_text_color(0, 48, 73)  # Dark blue color
    pdf.cell(0, 10, "Estimated market price of the apartment", 0, 1, 'C')
    pdf.ln(5)
    
    # Price with blue color
    pdf.set_font('DejaVu', 'B', 36)
    pdf.set_text_color(0, 136, 204)  # Blue color
    formatted_price = format_price(predicted_price)
    pdf.cell(0, 15, f"{formatted_price} USD", 0, 1, 'C')
    pdf.ln(5)
    
    # Subtitle
    pdf.set_font('DejaVu', 'B', 14)
    pdf.set_text_color(0, 48, 73)  # Dark gray
    pdf.cell(0, 10, "Online automatic valuation platform", 0, 1, 'C')
    pdf.cell(0, 10, "calculated market price of the apartment.", 0, 1, 'C')
    pdf.ln(10)
    
    # Generate random ID and add report details
    report_id = ''.join([str(random.randint(0, 9)) for _ in range(11)])
    pdf.set_font('DejaVu', '', 12)
    
    # Label color (dark gray)
    pdf.set_text_color(0, 48, 73)
    pdf.cell(10, 8, "ID: ", 0, 0, 'L')
    # Value color (blue)
    pdf.set_text_color(0, 136, 204)
    pdf.cell(0, 8, f"{report_id}", 0, 1, 'L')
    
    # Label color (dark gray)
    pdf.set_text_color(0, 48, 73)
    pdf.cell(83, 8, "Date and time of platform usage: ", 0, 0, 'L')
    # Value color (blue)
    pdf.set_text_color(0, 136, 204)
    pdf.cell(0, 8, f"{datetime.now().strftime('%d.%m.%Y %H:%M')}", 0, 1, 'L')
    
    # Label color (dark gray)
    pdf.set_text_color(0, 48, 73)
    pdf.cell(32, 8, "User: ", 0, 0, 'L')
    # Value color (blue)
    pdf.set_text_color(0, 136, 204)
    pdf.cell(0, 8, "Max Mustermann", 0, 1, 'L')
    
    pdf.ln(15)
    
    # Property details with improved styling
    pdf.set_font('DejaVu', 'B', 16)
    pdf.set_text_color(0, 48, 73)  # Dark blue
    pdf.cell(0, 10, "Property information:", 0, 1, 'L')
    pdf.ln(5)
    
    # Property details in single column with page break support
    pdf.set_font('DejaVu', '', 11)
    pdf.set_text_color(51, 51, 51)  # Dark gray
    
    # Calculate available height on current page
    available_height = pdf.h - pdf.get_y() - pdf.b_margin
    line_height = 8
    
    # Single column layout with page break support
    for key, value in property_details.items():
        if value:
            # Check if we need a new page
            if pdf.get_y() + 2 * line_height > pdf.h - pdf.b_margin:
                pdf.add_page()
                pdf.set_font('DejaVu', 'B', 16)
                pdf.set_text_color(0, 48, 73)
                pdf.cell(0, 10, "Property information (continued):", 0, 1, 'L')
                pdf.ln(5)
                pdf.set_font('DejaVu', '', 11)
                pdf.set_text_color(51, 51, 51)
            
            # Save starting position
            start_x = pdf.get_x()
            start_y = pdf.get_y()
            
            # Print the key-value pair
            pdf.set_font('DejaVu', 'B', 11)
            key_width = 70
            pdf.cell(key_width, line_height, f"{key}:", 0, 0)
            
            # Print the value
            pdf.set_font('DejaVu', '', 11)
            value_width = pdf.w - key_width - pdf.r_margin - pdf.l_margin
            pdf.multi_cell(value_width, line_height, str(value))
            
            # Move to next line if needed
            next_y = max(pdf.get_y(), start_y + line_height)
            pdf.set_xy(start_x, next_y)
    
    pdf.ln(10)  # Add some space after the details

    # Second page
    pdf.add_page()
    
    # Methodology section with improved styling
    pdf.set_font('DejaVu', 'B', 18)
    pdf.set_text_color(0, 48, 73)  # Dark blue
    pdf.cell(0, 10, 'Calculation Methodology', 0, 1, 'C')
    pdf.ln(5)
    
    pdf.set_font('DejaVu', '', 11)
    pdf.set_text_color(51, 51, 51)  # Dark gray
    methodology_text1 = "The real estate valuation model based on machine learning uses historical data from the real estate market. Briefly, the process works as follows:"
    pdf.ln(5)

    # Write first part of methodology text
    pdf.multi_cell(0, 8, methodology_text1)
    pdf.ln(5)

    # Add report image with adjusted position and size
    if os.path.exists('assets/report_pic.png'):
        # Calculate center position
        image_width = 170
        x = (pdf.w - image_width) / 2
        pdf.image('assets/report_pic.png', x=x, y=pdf.get_y(), w=image_width)
        pdf.ln(80)  # Add space after image for next content

    # Write second part with bullet points
    methodology_text2 = """1. Data collection: The model collects more than 20 characteristics such as size, location, and condition of previously sold properties along with their prices from open platforms.
2. Data preparation: Data is cleaned, correcting errors or missing values. Additional indicators are created from some features.
3. Model training: A machine learning model is trained on this data.
4. Valuation: Once trained, the model estimates the market value of new properties based on input data."""
    
    pdf.multi_cell(0, 8, methodology_text2)
    pdf.ln(10)
    
    # Additional information with improved styling
    pdf.add_page()
    pdf.set_font('DejaVu', 'B', 18)
    pdf.set_text_color(0, 48, 73)  # Dark blue
    pdf.cell(0, 10, "Appendix: Indicator definitions", 0, 1, 'L')
    
    pdf.set_font('DejaVu', '', 11)
    pdf.set_text_color(51, 51, 51)  # Dark gray
    additional_info = """
• Number of rooms - All rooms in the house except the kitchen.
• House area — the total area of the house (e.g., 87.23)
• Which floor - Indicates the floor the apartment is on. It must not exceed the total number of floors. Max height: 50.
• Construction type - Shows what and how the house is built.
• Brick - if the building is made of bricks;
• Panel - if the building is made of concrete panels;
• Monolithic - if external and main internal walls are poured from solid concrete;
• Block - if constructed using cement-mixed blocks (e.g., foam blocks);
• Wooden - if structure and walls are made from wood.
• Layout type - reflects overall planning of the house, including wall divisions, bathroom, door, and window placements.
• Mixed - Combines features of various layouts for functionality.
• Separate - Rooms are divided by function.
• For small families (malosemeyka) - Small 1-2 room apartments from the 1960–1990s.
• Studio - All spaces except bathroom are in one room.
• Multi-level - Apartments with two levels connected by stairs.
• Penthouse - Large apartments located on the top floor with roof access.
"""
    
    pdf.multi_cell(0, 8, additional_info)
    
    # Disclaimers with improved styling
    pdf.add_page()
    pdf.set_font('DejaVu', 'B', 18)
    pdf.set_text_color(0, 48, 73)  # Dark blue
    pdf.cell(0, 10, 'Important notes', 0, 1, 'L')
    
    pdf.set_font('DejaVu', '', 11)
    pdf.set_text_color(51, 51, 51)  # Dark gray
    disclaimers = """1. This report is for informational purposes only and cannot be used as an official appraisal report.
2. The estimated price is based on current market data and may differ from the actual sale price.
3. The result may not fully reflect the property's real condition, as it’s based solely on the provided input.
4. This valuation should not be used for financial or legal decisions.

The model is continuously updated with new data for more accurate valuations.

The calculated price is valid for the indicated valuation year and month. As noted above, the model constantly improves, so the same property may yield different values depending on the date and time of use."""
    
    pdf.multi_cell(0, 8, disclaimers)

    # Create a bytes buffer and save the PDF to it
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_bytes = pdf_buffer.getvalue()
    pdf_buffer.close()
    
    return pdf_bytes