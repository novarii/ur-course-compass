# UR Course Compass

An AI-powered course scheduling system for University of Rochester students that generates optimized academic plans while considering major requirements, cluster requirements, and graduation criteria.

## Features

- **Major Track Support**
  - Computer Science
  - Mathematics
  - Financial Economics

- **Intelligent Schedule Generation**
  - Automatic prerequisite validation
  - Time conflict resolution
  - Credit requirement tracking
  - Division/cluster requirement handling

- **Division & Cluster Management**
  - Natural Sciences and Engineering
  - Humanities
  - Social Sciences
  - 3-course cluster validation
  - Cross-division requirement tracking

- **Schedule Optimization**
  - Prioritizes major declaration prerequisites
  - Balances core courses with clusters
  - Strategic elective placement
  - Considers completed coursework

## Technical Requirements

- Python 3.8+
- Flask
- OpenAI API key
- Pandas 2.2.0+
- Modern web browser

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

5. Configure environment variables:
   ```bash
   # Create .env file
   cp .env.example .env
   # Add your OpenAI API key to .env
   OPENAI_API_KEY=your_api_key_here
   ```

6. Start the application:
   ```bash
   python app.py
   ```

7. Access the application at [http://localhost:5000](http://localhost:5000)

## Usage Guide

1. **Input Your Information**
   - Select your major
   - Indicate cluster interests
   - Enter completed courses
   - Specify graduation year

2. **Generate Schedule**
   - System analyzes requirements
   - Creates optimized schedule
   - Validates all constraints
   - Provides alternative options

3. **Review and Modify**
   - View generated schedule
   - Check requirement satisfaction
   - Request modifications if needed
   - Export schedule

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
We follow PEP 8 guidelines. Run flake8 before committing:
```bash
flake8 src/
```

## Contributing

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

## API Documentation

### Endpoints

- `POST /api/generate-schedule`
  - Generates course schedule based on student input
  - Requires student data in JSON format

- `GET /api/validate-schedule`
  - Validates existing schedule
  - Returns validation results and suggestions

## Error Handling

The system provides detailed error messages for:
- Invalid major selection
- Prerequisite violations
- Time conflicts
- Credit requirement issues
- Division/cluster requirement violations

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:
- Open an issue in the GitHub repository
- Contact the development team at [team-email@example.com]

## Acknowledgments

- University of Rochester Computer Science Department
- Contributors and maintainers
- All students providing valuable feedback

---
Made with ❤️ for University of Rochester students