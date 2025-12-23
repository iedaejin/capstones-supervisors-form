# Quick Start Guide

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Ensure Excel File is Present

Make sure `Capstones_List_of_Topics.xlsx` is in the `supervisor_form_app` directory.

## 3. Run the App

```bash
streamlit run supervisor_form.py
```

## 4. Access the App

Open your browser to: **http://localhost:8501**

## That's it! 🎉

The app will:
- ✅ Load topics from the Excel file automatically
- ✅ Prevent duplicate submissions
- ✅ Save entries to `supervisors.txt`
- ✅ Show real-time statistics

## Troubleshooting

**Can't find Excel file?**
- Check the file is named exactly: `Capstones_List_of_Topics.xlsx`
- Verify it's in the same folder as `supervisor_form.py`

**Port already in use?**
```bash
streamlit run supervisor_form.py --server.port 8502
```

**Import errors?**
```bash
pip install --upgrade streamlit pandas openpyxl
```

