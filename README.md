# 🧥 Virtual Dressing Room & E-Commerce Try-On Platform
Welcome to the **Virtual Dressing Room**, a modern e-commerce web application powered by **Flask** and **Pillow (PIL)**. This application lets users browse a catalog of men's and women's clothing, manage their shopping carts, experience a simulated payment gateway, and—most importantly—virtually "try on" clothes by uploading their photo!
---
## 🚀 Key Features
*   **🛒 Complete E-Commerce Workflow**:
    *   Browse categorized products (Men's & Women's clothing).
    *   Interactive shopping cart to add, view, remove, or clear items.
    *   Mock **Payment Gateway Integration** for visual feedback of checkouts.
*   **🖼️ Smart Virtual Try-On**:
    *   Upload a personal photograph on the product page.
    *   The backend automatically analyzes the product size and gender parameters.
    *   Utilizes advanced **Pillow-based dynamic bounding box estimation** to overlay clothing over the person's upper body.
    *   Applies aspect-ratio preservation, intelligent scaling based on image size, and smooth alpha blending for natural try-on previews.
*   **🎨 Responsive UI/UX**:
    *   Clean aesthetics with a modern landing page, category navigation, and high-fidelity layouts.
    *   Interactive feedback and visual instructions for uploading images.
---
## 📂 Project Structure
```text
├── app.py                      # Main Flask application with routing and checkout APIs
├── products.py                 # Product database with image configurations and metadata
├── try_on.py                   # Virtual Try-On processing engine (Image processing & overlay)
├── static/
│   ├── images/                 # Catalog apparel assets and system graphics
│   ├── uploads/                # Directory storing temporary user-uploaded photos
│   ├── results/                # Output directory for processed try-on images
│   └── styles.css              # Custom styled CSS sheets for styling components
├── templates/
│   ├── base.html               # Main base template holding header, footer, & CDNs
│   ├── home.html               # Landing page with category buttons (Men / Women)
│   ├── shop.html               # Product list grid filterable by gender category
│   ├── cart.html               # Session-based shopping cart list and actions
│   ├── try_on.html             # Virtual try-on UI allowing file uploads and displaying results
│   ├── about.html              # Core information page
│   └── payment-gateway-integration/  # Built-in modular checkout simulation templates
```
---
## 🛠️ Installation & Setup
Follow these steps to get the Virtual Dressing Room up and running locally:
### Prerequsites
Make sure you have **Python 3.8+** installed.
### 1. Clone the Repository
```bash
git clone https://github.com/your-username/virtual-dressing-room.git
cd virtual-dressing-room
```
### 2. Install Dependencies
Install the required packages. The application depends on **Flask** and **Pillow**:
```bash
pip install Flask Pillow
```
### 3. Run the Application
Start the Flask development server:
```bash
python app.py
```
Open your browser and navigate to:
```text
http://127.0.0.1:5000/
```
---
## 💡 How it Works (Under the Hood)
The Virtual Try-On processing pipeline inside `try_on.py` performs the following steps:
1.  **Image Loading**: Standardizes both the user's uploaded portrait and the selected apparel image into `RGBA` mode to maintain alpha transparency channels.
2.  **Adaptive Scaling**: Reads the size of the uploaded portrait. If it's a high-resolution image ($> 500\text{px}$ width), it scales the apparel size by a factor of `2.5x`; otherwise, it scales by `1.2x` to fit.
3.  **Upper-Body Bounding Box Estimation**: Automatically maps out the ideal coordinate sector for the upper torso (estimating the height at `45%` and width at `70%` of the portrait canvas).
4.  **Alpha Composition & Blending**: Overlay is generated with precise aspect-ratio constraints. It blends the scaled apparel onto the user's upper body with a blend factor (`alpha = 0.9`), converting it back into a standard high-quality `RGB` image saved directly under `static/results/output_try_on.png` for instant display.
---
## 💳 Mock Payment Gateway Simulation
The application features a built-in mock payment processing flow integrated under `/payment_gateway`. It displays standard checkout screens, card input forms, and successful transaction pages to replicate a fully functioning production e-commerce store experience.
