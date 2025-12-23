"""
Streamlit app for collecting supervisor information.
Supervisors can specify their name, programs, capacity, and topic preferences with expertise levels.
"""

import streamlit as st
from pathlib import Path
import re
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Supervisor Registration",
    page_icon="👨‍🏫",
    layout="wide"
)

# Expertise levels
EXPERTISE_LEVELS = ["Expert", "Advanced", "Intermediate", "Beginner"]

# Program name mapping from Excel to standard format
PROGRAM_MAPPING = {
    "BDBA": "BDBA",
    "BCSAI": "BCSAI",
    "BBA+BDBA": "BBA+BDBA",
    "BBBA+BDBA (joint capstone)": "BBA+BDBA",
    "BDBA+BDBA (only BDBA)": "BBA+BDBA",
    "PPLE+DBA": "PPLE+DBA",
    "PPLE+BDA (only DBA)": "PPLE+DBA"
}

def load_topics_from_excel(excel_path: Path):
    """
    Load programs and topics from Excel file.
    Returns: dict mapping program -> list of (topic_num, topic_description) tuples
    """
    if not excel_path.exists():
        st.error(f"❌ Topics file not found: {excel_path}")
        return {}
    
    try:
        df = pd.read_excel(excel_path)
        
        # Group by program
        topics_by_program = {}
        
        for _, row in df.iterrows():
            program_raw = str(row['Program']).strip()
            topic_str = str(row['Topics']).strip()
            
            # Map program name to standard format
            program = PROGRAM_MAPPING.get(program_raw, program_raw)
            
            # Extract topic number from "TXX: Description" format
            match = re.search(r'T(\d+)', topic_str)
            if match:
                topic_num = int(match.group(1))
                
                if program not in topics_by_program:
                    topics_by_program[program] = []
                
                # Store (topic_num, full_description)
                topics_by_program[program].append((topic_num, topic_str))
        
        # Sort topics by number for each program
        for program in topics_by_program:
            topics_by_program[program].sort(key=lambda x: x[0])
        
        return topics_by_program
    
    except Exception as e:
        st.error(f"❌ Error loading topics from Excel: {str(e)}")
        return {}

def format_topic_id(program: str, topic_num: int) -> str:
    """Format topic ID as PROGRAM_TXX"""
    return f"{program}_T{topic_num:02d}"

def load_existing_supervisors(filepath: Path) -> list:
    """Load existing supervisors to avoid duplicates"""
    if not filepath.exists():
        return []
    
    supervisors = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # Extract supervisor name/ID (before first colon)
                if ':' in line:
                    sup_id = line.split(':')[0].strip()
                    supervisors.append(sup_id)
    return supervisors

def save_supervisor_entry(name: str, capacity: int, selections: dict, filepath: Path):
    """Save supervisor entry to file"""
    # Format: SupervisorName: Capacity, Program:Topic:ExpertiseLevel, ...
    parts = [f"{name}: {capacity}"]
    
    for program, topics in selections.items():
        for topic_num, expertise in topics.items():
            topic_id = format_topic_id(program, topic_num)
            parts.append(f"{program}:{topic_id}:{expertise}")
    
    entry = ", ".join(parts)
    
    # Append to file
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(entry + "\n")

def main():
    st.title("👨‍🏫 Supervisor Registration Form")
    st.markdown("---")
    
    # Initialize session state
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'form_key' not in st.session_state:
        st.session_state.form_key = 0
    
    # Load topics from Excel file
    excel_path = Path("Capstones_List_of_Topics.xlsx")
    topics_by_program = load_topics_from_excel(excel_path)
    
    if not topics_by_program:
        st.error("❌ Could not load topics. Please ensure Capstones_List_of_Topics.xlsx is in the supervisor_form_app directory.")
        return
    
    # Get available programs
    available_programs = sorted(list(topics_by_program.keys()))
    
    # File path for saving - save in the same folder as the app
    output_file = Path("supervisors.txt")
    
    # Load existing supervisors to check for duplicates
    existing_supervisors = load_existing_supervisors(output_file)
    
    # Display info banner if topics loaded successfully
    if topics_by_program:
        st.info(f"📚 Loaded {sum(len(topics) for topics in topics_by_program.values())} topics across {len(available_programs)} program(s)")
    
    with st.form(f"supervisor_form_{st.session_state.form_key}"):
        st.subheader("Supervisor Information")
        
        # Supervisor name
        supervisor_name = st.text_input(
            "Supervisor Name *",
            placeholder="e.g., Dr. John Smith or SUP01",
            help="Enter the supervisor's name or ID"
        )
        
        # Capacity
        capacity = st.number_input(
            "Maximum Capacity (1-10) *",
            min_value=1,
            max_value=10,
            value=5,
            help="Maximum number of students this supervisor can handle (1-10)"
        )
        
        st.markdown("---")
        st.subheader("Program Selection")
        
        # Program selection (multi-select)
        selected_programs = st.multiselect(
            "Select Programs to Supervise *",
            options=available_programs,
            help="Select one or more programs you can supervise"
        )
        
        st.markdown("---")
        st.subheader("Topic Selection & Expertise Levels")
        
        # Topic selections organized by program
        topic_selections = {}
        
        if not selected_programs:
            st.warning("⚠️ Please select at least one program to continue.")
        else:
            for program in selected_programs:
                st.markdown(f"### {program} Topics")
                
                # Get available topics for this program from Excel data
                if program not in topics_by_program:
                    st.warning(f"⚠️ No topics found for {program}")
                    continue
                
                program_topics = topics_by_program[program]
                
                # Create columns for better layout
                cols = st.columns(2)
                
                with cols[0]:
                    # Create options with descriptions
                    topic_options = {f"T{topic_num:02d}: {desc.split(':', 1)[1].strip() if ':' in desc else desc}": topic_num 
                                    for topic_num, desc in program_topics}
                    
                    selected_topic_labels = st.multiselect(
                        f"Select {program} Topics *",
                        options=list(topic_options.keys()),
                        key=f"topics_{program}",
                        help=f"Select topics you can supervise for {program}"
                    )
                    
                    # Convert labels back to topic numbers
                    selected_topic_nums = [topic_options[label] for label in selected_topic_labels] if selected_topic_labels else []
                
                # Store topic selections with expertise levels
                if selected_topic_nums:
                    topic_selections[program] = {}
                    
                    with cols[1]:
                        st.markdown("**Set Expertise Level for Each Topic:**")
                        
                        # Create a container for expertise selections
                        for topic_num in selected_topic_nums:
                            topic_id = format_topic_id(program, topic_num)
                            # Find the description for this topic
                            topic_desc = next((desc for num, desc in program_topics if num == topic_num), "")
                            short_desc = topic_desc.split(':', 1)[1].strip() if ':' in topic_desc else topic_desc
                            short_desc = short_desc[:50] + "..." if len(short_desc) > 50 else short_desc
                            
                            expertise = st.selectbox(
                                f"{topic_id}",
                                options=EXPERTISE_LEVELS,
                                index=0,  # Default to Expert
                                key=f"expertise_{program}_{topic_num}",
                                help=short_desc
                            )
                            topic_selections[program][topic_num] = expertise
                else:
                    st.info(f"💡 Select topics for {program} above")
        
        st.markdown("---")
        
        # Validation and submission
        submitted = st.form_submit_button("Submit Supervisor Information", type="primary")
        
        if submitted:
            # Validation
            errors = []
            
            if not supervisor_name or not supervisor_name.strip():
                errors.append("❌ Supervisor name is required")
            
            # Check for duplicate supervisor name
            if supervisor_name and supervisor_name.strip():
                normalized_name = supervisor_name.strip()
                if normalized_name in existing_supervisors:
                    errors.append(f"❌ Supervisor '{normalized_name}' has already submitted their information. Each supervisor can only submit once.")
            
            if not selected_programs:
                errors.append("❌ At least one program must be selected")
            
            # Check minimum topics (3-5 recommended) - only a warning, not an error
            total_topics = sum(len(topics) for topics in topic_selections.values())
            if total_topics > 0 and total_topics < 3:
                st.warning(f"⚠️ You've selected only {total_topics} topic(s). It's recommended to select 3-5 topics.")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Save to file
                try:
                    # Ensure data directory exists
                    output_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    # If file doesn't exist, add header
                    if not output_file.exists():
                        with open(output_file, 'w', encoding='utf-8') as f:
                            f.write("# Supervisors choose 3-5 topics (program:topic:expertise)\n")
                            f.write("# Format: SupervisorID: Capacity, Prog:Topic:Level, ...\n")
                            f.write("# Programs: BDBA_T01-20, BCSAI_T01-20, BBA+BDBA_T01-20, PPLE+DBA_T01-20\n")
                            f.write("\n")
                    
                    # Save entry
                    save_supervisor_entry(supervisor_name, capacity, topic_selections, output_file)
                    
                    st.success("✅ Supervisor information saved successfully!")
                    st.session_state.submitted = True
                    st.session_state.last_saved_name = supervisor_name
                    st.session_state.last_saved_entry = topic_selections
                    
                    # Show preview
                    st.markdown("### 📋 Preview of Saved Entry:")
                    parts = [f"**{supervisor_name}**: {capacity}"]
                    for program, topics in topic_selections.items():
                        for topic_num, expertise in topics.items():
                            topic_id = format_topic_id(program, topic_num)
                            parts.append(f"{program}:{topic_id}:{expertise}")
                    st.code(", ".join(parts))
                    
                except Exception as e:
                    st.error(f"❌ Error saving supervisor information: {str(e)}")
    
    # Add reset button outside the form
    st.markdown("---")
    # Reset button - always visible
    if st.button("🔄 Reset Form", help="Clear all form fields and start over"):
        # Clear all session state related to the form
        keys_to_delete = [key for key in st.session_state.keys() 
                         if key.startswith('topics_') or key.startswith('expertise_')]
        for key in keys_to_delete:
            del st.session_state[key]
        st.session_state.submitted = False
        st.session_state.last_saved_name = None
        st.session_state.last_saved_entry = None
        # Increment form key to force form reset
        st.session_state.form_key += 1
        st.rerun()
    
    # Sidebar with instructions
    with st.sidebar:
        st.header("📖 Instructions")
        st.markdown("""
        **Required Fields:**
        1. Supervisor Name
        2. Capacity (1-10 students)
        3. At least one Program
        4. At least one Topic per selected Program
        
        **Recommendations:**
        - Select at least 3 topics per program
        - Choose appropriate expertise levels
        - Capacity should reflect your availability
        
        **Expertise Levels:**
        - **Expert**: Deep knowledge and experience
        - **Advanced**: Strong understanding
        - **Intermediate**: Good knowledge
        - **Beginner**: Basic familiarity
        """)
        
        st.markdown("---")
        st.header("📊 Summary")
        
        if 'submitted' in st.session_state and st.session_state.submitted:
            st.success("Last submission: ✅ Saved")
        else:
            st.info("No submissions yet")
        
        # Show file location
        if output_file.exists():
            with open(output_file, 'r', encoding='utf-8') as f:
                lines = [l for l in f if l.strip() and not l.strip().startswith('#')]
                st.metric("Total Supervisors", len(lines))
        
        st.markdown("---")
        st.markdown(f"**Output File:** `{output_file}`")

if __name__ == "__main__":
    main()

