# Deployment Checklist

## Pre-Deployment

- [x] All dependencies listed in `requirements.txt`
- [x] Excel file (`Capstones_List_of_Topics.xlsx`) is in the directory
- [x] Code is clean and tested
- [x] README.md is up to date
- [x] .gitignore is configured

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Excel file:**
   - File name: `Capstones_List_of_Topics.xlsx`
   - Location: `supervisor_form_app/` directory
   - Contains: Program, Topics, Remarks columns

3. **Run the app:**
   ```bash
   streamlit run supervisor_form.py
   ```

4. **Access the app:**
   - Local: http://localhost:8501
   - Network: http://your-ip:8501

## Streamlit Cloud Deployment

1. **Prepare repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select repository
   - Set main file: `supervisor_form_app/supervisor_form.py`
   - Click "Deploy"

3. **Verify deployment:**
   - Check that Excel file is accessible
   - Test form submission
   - Verify output file creation

## Environment Variables (Optional)

If needed, you can set environment variables:
- `STREAMLIT_SERVER_PORT`: Port number (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: localhost)

## Post-Deployment

- [ ] Test form submission
- [ ] Verify duplicate prevention works
- [ ] Check output file format
- [ ] Test reset functionality
- [ ] Verify Excel file loading

## Troubleshooting

**Port already in use:**
```bash
streamlit run supervisor_form.py --server.port 8502
```

**Excel file not found:**
- Check file is in the same directory as `supervisor_form.py`
- Verify file name is exactly `Capstones_List_of_Topics.xlsx`

**Import errors:**
```bash
pip install --upgrade streamlit pandas openpyxl
```

