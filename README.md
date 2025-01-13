# UR Course Compass

A web application designed to help University of Rochester students manage their courses, assignments, and grades efficiently.

## Features

- **Home Page**: Overview of the application with intuitive navigation
- **Authentication**: Secure login and signup functionality
- **Student Dashboard**: Personalized view of enrolled courses and upcoming assignments
- **Assignment Tracker**: Comprehensive management of course assignments and grades
- **Profile Management**: User account and preferences configuration

## Getting Started

### Prerequisites

- Python 3.x
- Git
- Web browser (Chrome, Firefox, or Safari recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/novarii/ur-course-compass.git
   ```

2. Navigate to the project directory:
   ```bash
   cd ur-course-compass
   ```

3. Set up a virtual environment (recommended):
   ```bash
   python -m venv venv
   # On Unix or MacOS:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Initialize the database:
   ```bash
   python database.py
   ```

6. Start the application:
   ```bash
   python server.py
   ```

7. Access the application at [http://localhost:5000](http://localhost:5000)

## Usage Guide

### For Students

1. **Create an Account**: Sign up with your university email
2. **Dashboard Navigation**: View all your courses and upcoming assignments
3. **Assignment Management**: Track deadlines and submissions
4. **Grade Monitoring**: Keep track of your academic performance
5. **Profile Settings**: Update your personal information and preferences

## Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add amazing feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please:
- Open an issue in the GitHub repository
- Contact the development team at [email protected]

## Acknowledgments

- University of Rochester Computer Science Department
- Contributors and maintainers
- All students providing valuable feedback

---
Made with ❤️ for University of Rochester students