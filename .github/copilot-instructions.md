# Copilot Instructions for WhatsApp Analysis App

## Overview
This project is a WhatsApp analysis application designed to process and analyze chat data. The repository is organized into multiple components, including:

- **`lite/`**: Contains the lightweight application logic, including `app.py` and modularized analysis and database utilities.
- **`heavy/`**: Includes workflows, scripts, and configurations for more complex operations.
- **`modules/`**: Core Python modules for feature extraction, analysis, and utility functions.
- **`pages/`**: Streamlit-based UI pages for different functionalities.
- **`data/`**: Stores input data, including chat logs and extracted features.
- **`tests/`**: Unit tests for validating the functionality of the application.

## Key Workflows

### Testing and Validation
To run tests and validate workflows, use the following commands:

```bash
pytest lite/tests
python heavy/scripts/validate_workflow.py --workflow heavy/workflows/main_workflow.json --schema heavy/workflows/schema.json
```

Resolve any errors encountered during these processes.

### Running the Application
- Use `lite/app.py` to start the lightweight application.
- Ensure all dependencies in `requirements.txt` are installed.

### Data Processing
- Input data is stored in `data/`.
- Processed features are saved in `data/extracted_features.csv`.

## Project-Specific Conventions
- **File Naming**: Use descriptive names for scripts and data files.
- **Modules**: Keep reusable logic in `modules/`.
- **UI Pages**: Use Streamlit for interactive dashboards and tools.

## External Dependencies
- Python packages listed in `requirements.txt`.
- N8N workflows for automation, located in `heavy/workflows/`.

## Notes for AI Agents
- Focus on modularity and reusability when adding new features.
- Follow the existing folder structure and naming conventions.
- Validate all changes with the provided test suite.

For more details, refer to the `README.md` and documentation in `doc/`.
