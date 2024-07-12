# Homifice Hotel Management System

## Overview

As a solo developer, inspired by the challenge of manual operations & liitations of our home-turned-mini-guest-house, I envisioned and built Homifice – a hotel management app. Homifice HMS is a comprehensive web application designed to streamline hotel operations and enhance user experience. This system provides a robust platform for users to manage bookings, connect with hoteliers, handle payments, and oversee various aspects of hotel management efficiently. Built using Django, Homifice leverages modern web technologies to offer a seamless and intuitive interface for both hotel administrators and guests.

## Features

### User Management
- **User Registration and Authentication:** Secure sign-up and sign-in processes ensure user data integrity and protection.
- **Profile Management:** Users can easily update their personal information and manage their account settings.

### Hotel Booking
- **Hotel Listing and Details:** Browse through available hotels, view detailed descriptions, and check room availability.
- **Room Booking:** Select and book rooms with ease, add optional services, and confirm reservations.
- **Session Management:** Utilizes sessions to carry user selections throughout the booking process, ensuring a smooth user experience.
- **Hotel and Room Type Detail Views:** Users can navigate from a list of hotels to detailed views of each hotel and their room types.

### Payment System
- **Secure Payments:** I integrated Paystack and Paypal to provide a secure and reliable payment gateway for processing transactions.
- **Booking Confirmation:** Receive instant confirmation and booking details via email after successful payment.

### Custom Features
- **Customized Django Admin System - Jazzmin:** A visually enhanced and user-friendly admin dashboard for managing hotel data.
- **Frontend Optimization:** Utilizes Django template inheritance to optimize front-end code and ensure a consistent user experience across the site.
- **Interactive Alerts:** Integrated Sweet Alert for JavaScript alerts and pop-ups, enhancing user interaction and feedback.
- **User Dashboard:** A dedicated dashboard for users to view their bookings, manage their profile, and access additional features.
- **Rich Text Formatting:** Integrated CKEditor 5 for rich text formatting, allowing hotel administrators to create detailed and attractive hotel descriptions.

## Technologies Used
- **Django:** Core framework for developing the backend and handling the server-side logic.
- **SQLite:** Database used for storing all application data securely.
- **HTML5, CSS3, JavaScript:** Frontend technologies used to create a responsive and user-friendly interface.
- **Ajax and jQuery:** For asynchronous requests and dynamic updates without reloading the page.
- **Bootstrap:** Ensures the application is mobile-friendly and visually appealing.
- **Jazzmin:** Customizes the Django admin interface to be more intuitive and visually appealing.
- **Sweet Alert:** Provides attractive and customizable alerts and pop-ups for user notifications.
- **CKEditor 5:** Adds rich text editing capabilities for better content management.
- **Paypal & Paystack:** Payment gateway integration for secure and reliable transaction processing.
- **Railway:** Used for hosting the application.

## Deployment
The current Homifice Hotel Management System v1.0 is deployed on Railway for reliable and scalable cloud hosting.
Landing Page: [https://tinyurl.com/homifice](https://tinyurl.com/homifice)
Link Here: [https://homifice.railway.app](homifice.railway.app)

## Future Enhancements
While the current focus is on delivering a Minimum Viable Product (MVP) with essential features, future updates may include:
- **Reviews and Ratings:** Guests will be able to share their feedback and help the hotels improve!
- **Notifications:** I will implement a realtime notification system to keep users informed about their bookings and updates.
- **Bookmarks:** Enable users to bookmark their favorite hotels for easy access.
- **Additional Payment Gateways:** I will integrate other payment options like Stripe.
- **Email Features:**  I will automate email notifications for various actions such as booking confirmation, reminders, and updates.

The Homifice Hotel Management System aims to provide an all-in-one solution for hotel management and guest services, ensuring a smooth and satisfying experience for all users.

## Source Control
- **GitHub:** The project uses GitHub for version control and collaboration.
Sure, here's a section on how to run the project:

---

## How to Run This Project

### Prerequisites
- Python 3.x
- Django
- SQLite (bundled with Django)
- Git

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/youruOK-Emmanuel/homifice.git
   cd hms
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply the database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (admin account):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   Open your web browser and navigate to `http://127.0.0.1:8000` to see the application. You can access the admin dashboard at `http://127.0.0.1:8000/admin` and log in with the superuser credentials you created earlier.

### Optional: Setting Up for Production

For a production environment, you'll need to set up a proper web server (like Amazon) and a production-ready database (like PostgreSQL). You should also configure environment variables for secret keys and database settings. Refer to the Django deployment documentation for more detailed instructions.


## Auhtor
- **Olawuni Emmanuel Kayode:** Software Engineer and Project Lead.

## 🤝 Contributing
Together, these features and technologies make the Homifice Hotel Management System a powerful and user-friendly solution for hotel management and guest services. Explore the project on GitHub and contribute to its development to enhance its functionality and usability.

I am open for collaborations and contributions. If you have any suggestions or improvements, please feel free to connect with me and submit a pull request or open an issue. Your feedback is highly appreciated!

## 📧 Contact
For any questions or inquiries, please contact me at [olawuniemmanuelk@gmail.com](mailto:olawuniemmanuelk@gmail.com)

Buy Me A Cofee: [https://www.buymeacoffee.com/okemmanuel](https://www.buymeacoffee.com/okemmanuel)