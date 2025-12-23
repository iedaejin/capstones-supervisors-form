# Supervisor Registration Form

A Streamlit web application for collecting supervisor information for capstone project matching.

## Features

- **Dynamic Topic Loading**: Automatically reads programs and topics from Excel file
- **Duplicate Prevention**: Prevents supervisors from submitting multiple times
- **Form Validation**: Ensures all required fields are completed
- **Expertise Levels**: Allows supervisors to specify their expertise level for each topic
- **Reset Functionality**: Easy form reset to start over
- **Real-time Preview**: Shows saved entry before submission

## Requirements

### Python Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install streamlit pandas openpyxl
```

### Data File

**Capstones_List_of_Topics.xlsx** must be in the `supervisor_form_app` directory. The Excel file should contain:

- **Program** column: Program names (e.g., BDBA, BCSAI, BBA+BDBA, PPLE+DBA)
- **Topics** column: Topic descriptions in format "TXX: Description" (e.g., "T01: Data Analysis...")
- **Remarks** column: Additional information (optional)

The app automatically reads programs and topics from this file to populate the form options.

## Installation

1. Ensure you have Python 3.7+ installed
2. Install dependencies:
   ```bash
   cd supervisor_form_app
   pip install -r requirements.txt
   ```
3. Place `Capstones_List_of_Topics.xlsx` in the `supervisor_form_app` directory
4. Run the app:
   ```bash
   streamlit run supervisor_form.py
   ```

## Usage

1. **Start the app**: Run `streamlit run supervisor_form.py`
2. **Fill out the form**:
   - Enter supervisor name/ID
   - Set capacity (1-10 students)
   - Select one or more programs
   - Select topics for each program
   - Set expertise level for each topic
3. **Submit**: Click "Submit Supervisor Information"
4. **Reset**: Use "Reset Form" button to clear all fields

## Output

The app saves supervisor entries to `supervisors.txt` in the same directory, in the format:

```
SupervisorName: Capacity, Program:Topic:ExpertiseLevel, ...
```

Example:
```
Dr. John Smith: 8, BDBA:BDBA_T01:Expert, BDBA:BDBA_T02:Advanced, BCSAI:BCSAI_T05:Intermediate
```

## Deployment

### Local Deployment

Simply run:
```bash
streamlit run supervisor_form.py
```

The app will be available at `http://localhost:8501`

### Streamlit Cloud Deployment

1. Push your code to GitHub (ensure `Capstones_List_of_Topics.xlsx` is included)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set the main file path to: `supervisor_form_app/supervisor_form.py`
5. Deploy!

### Other Cloud Platforms

For deployment on other platforms (Heroku, AWS, etc.), ensure:
- Python 3.7+ is available
- Dependencies from `requirements.txt` are installed
- The Excel file is accessible in the app directory
- Port 8501 (or configured port) is open

## File Structure

```
supervisor_form_app/
├── supervisor_form.py          # Main application file
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
├── Capstones_List_of_Topics.xlsx # Topics data file (required)
└── supervisors.txt             # Generated output file
```

## Troubleshooting

### Excel file not found
- Ensure `Capstones_List_of_Topics.xlsx` is in the `supervisor_form_app` directory
- Check file name spelling (case-sensitive)

### Duplicate submission error
- Each supervisor can only submit once
- Check existing entries in `supervisors.txt`

### Topics not loading
- Verify Excel file format (Program, Topics, Remarks columns)
- Check that topic format is "TXX: Description"
- Review error messages in the app

## Notes

- The app prevents duplicate submissions by checking supervisor names
- Topics are dynamically loaded from the Excel file on each app start
- Output file is created automatically on first submission
- Form state is preserved during the session until reset
