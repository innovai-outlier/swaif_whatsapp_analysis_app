# Prompt for AI Code Architect/Developer

## Objective
Design and implement the entire codebase for a WhatsApp analysis application. The application should process and analyze chat data, providing insights through a user-friendly interface. The architecture must be modular, scalable, and adhere to best practices for maintainability and reusability.

## Key Requirements

### Architecture
- **Modular Design**: Organize the codebase into logical components:
  - `lite/`: Lightweight application logic, including `app.py` and modularized utilities.
  - `heavy/`: Complex workflows, scripts, and configurations.
  - `modules/`: Core Python modules for feature extraction, analysis, and utility functions.
  - `pages/`: Streamlit-based UI pages for interactive dashboards.
  - `data/`: Input data storage and processed feature outputs.
  - `tests/`: Unit tests for validating functionality.

### Features
1. **Data Processing**:
   - Parse and process WhatsApp chat logs.
   - Extract features and save them in `data/extracted_features.csv`.
2. **Analysis**:
   - Perform detailed analysis and save results in `data/detailed_analysis_results.json`.
3. **UI**:
   - Build Streamlit pages for dashboards and configuration tools.
4. **Automation**:
   - Integrate N8N workflows for automated tasks.

### Developer Workflows
- **Testing**:
  - Use `pytest` for unit tests in `lite/tests`.
  - Validate workflows with:
    ```bash
    python heavy/scripts/validate_workflow.py --workflow heavy/workflows/main_workflow.json --schema heavy/workflows/schema.json
    ```
- **Running the Application**:
  - Start the lightweight app with `lite/app.py`.
  - Ensure dependencies in `requirements.txt` are installed.

### Conventions
- Use descriptive file and function names.
- Keep reusable logic in `modules/`.
- Follow the existing folder structure.

### External Dependencies
- Python packages listed in `requirements.txt`.
- N8N workflows located in `heavy/workflows/`.

## Deliverables
- A fully functional codebase adhering to the specified architecture.
- Comprehensive unit tests in `tests/`.
- Documentation in `README.md` and `doc/`.

## Notes for the AI Agent
- Focus on modularity and reusability.
- Validate all changes with the provided test suite.
- Ensure the application is user-friendly and visually appealing.

## Design Patterns and Guidelines

### Code Patterns
- **Feature Extraction**: Use modular functions to extract features from data, as seen in `extract_features.py`.
- **Data Analysis**: Implement exploratory data analysis (EDA) scripts with clear visualizations, e.g., `analyze_features.py`.
- **Reusable Components**: Centralize reusable logic in `modules/`.

### UI Design
- **Streamlit Pages**: Use Streamlit for interactive dashboards, following the structure in `pages/`.
- **Color Scheme**: Maintain a clean and professional look with white backgrounds and grid-based layouts (e.g., `sns.set_style("whitegrid")`).
- **Labels and Titles**: Use descriptive titles for charts and sections, such as "Duração da Conversa" and "Mensagens do Paciente".

### Labels and Features
- **Key Features**:
  - Duration of conversations.
  - Total messages.
  - Interaction counts.
  - Keywords for scheduling and pricing.
- **Labels**: Clearly distinguish between success and failure cases in data.

### Visualization Standards
- **Boxplots**: Use for comparing distributions (e.g., `sns.boxplot`).
- **Correlation Matrices**: Highlight feature relationships with heatmaps (e.g., `sns.heatmap`).
- **File Outputs**: Save visualizations with descriptive filenames like `feature_distributions.png` and `correlation_matrix.png`.

### Documentation
- **Feature Definitions**: Document all features in `features.md`.
- **Reports**: Provide detailed analysis in markdown files, e.g., `report.md`.

### Integration
- **Data Flow**: Ensure seamless integration between feature extraction, analysis, and visualization.
- **Automation**: Leverage workflows (e.g., N8N) for repetitive tasks.

These guidelines ensure consistency and reusability across projects. For more details, refer to the existing project structure and documentation.

For more details, refer to the `.github/copilot-instructions.md` and `README.md`.
