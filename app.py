import streamlit as st
import pandas as pd

# Initialize session states
if 'show_checklist' not in st.session_state:
    st.session_state.show_checklist = False
if 'current_selections' not in st.session_state:
    st.session_state.current_selections = {
        'client': None,
        'payor': None,
        'denial_reason': None
    }

def reset_all_states():
    # Reset all session states to their default values
    st.session_state.show_checklist = False
    st.session_state.current_selections = {
        'client': None,
        'payor': None,
        'denial_reason': None
    }
    # Reset selectbox values
    if 'client_select' in st.session_state:
        del st.session_state.client_select
    if 'payor_select' in st.session_state:
        del st.session_state.payor_select
    if 'denial_select' in st.session_state:
        del st.session_state.denial_select
    st.rerun()

def on_selection_change():
    st.session_state.show_checklist = False

# Load your DataFrame here
# Replace this with your actual data loading mechanism
df = pd.read_json("checklists_american.json")
    
st.title('Virtual Denial Coach')

# Client dropdown (fixed to American Homecare Equipment)
selected_client = st.selectbox(
    'Select Client',
    ['American Homecare Equipment'],
    key='client_select',
    on_change=on_selection_change
)
st.session_state.current_selections['client'] = selected_client

# Get unique payers from the DataFrame
payers = sorted(df['payer'].unique())
selected_payer = st.selectbox(
    'Select Payer',
    payers,
    key='payor_select',
    on_change=on_selection_change
)
st.session_state.current_selections['payor'] = selected_payer

# Filter denial reasons based on selected payer
denial_reasons = sorted(df[df['payer'] == selected_payer]['denialreason'].unique())
selected_denial = st.selectbox(
    'Select Denial Reason',
    denial_reasons,
    key='denial_select',
    on_change=on_selection_change
)
st.session_state.current_selections['denial_reason'] = selected_denial

# View Checklist button
if st.button('View Checklist'):
    st.session_state.show_checklist = True

# Show checklist if button was clicked
if st.session_state.show_checklist:
    # Filter DataFrame to get the matching checklist
    filtered_data = df[
        (df['payer'] == selected_payer) &
        (df['denialreason'] == selected_denial)
    ]
    
    if not filtered_data.empty:
        st.markdown("## Checklist")
        checklist = filtered_data.iloc[0]['checklists']
        st.markdown(checklist)
        

    else:
        st.error("No checklist found for the selected combination.")

# Add Get New Checklist button
if st.button('🔄 Get New Checklist', type='primary'):
    reset_all_states()