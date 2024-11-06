import streamlit as st
import pandas as pd

# Initialize session states
if 'show_content' not in st.session_state:
    st.session_state.show_content = False
if 'current_selections' not in st.session_state:
    st.session_state.current_selections = {
        'client': None,
        'payor': None,
        'denial_reason': None
    }

def reset_all_states():
    # Reset all session states to their default values
    st.session_state.show_content = False
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
    st.session_state.show_content = False

# Load both DataFrames
df_american = pd.read_json("checklists_american.json")
df_vital = pd.read_csv("flowcharts_vital.csv")
    
st.title('Virtual Denial Coach')

# Client dropdown (both clients)
selected_client = st.selectbox(
    'Select Client',
    ['American Homecare Equipment', 'Vital Care'],
    key='client_select',
    on_change=on_selection_change
)
st.session_state.current_selections['client'] = selected_client

# Use appropriate DataFrame based on selected client
current_df = df_american if selected_client == 'American Homecare Equipment' else df_vital

# Get unique payers from the current DataFrame
payers = sorted(current_df['payer'].unique())
selected_payer = st.selectbox(
    'Select Payer',
    payers,
    key='payor_select',
    on_change=on_selection_change
)
st.session_state.current_selections['payor'] = selected_payer

# Filter denial reasons based on selected payer
denial_reasons = sorted(current_df[current_df['payer'] == selected_payer]['denialreason'].unique())
selected_denial = st.selectbox(
    'Select Denial Reason',
    denial_reasons,
    key='denial_select',
    on_change=on_selection_change
)
st.session_state.current_selections['denial_reason'] = selected_denial

# View button (dynamic text based on client)
button_text = 'View Checklist' if selected_client == 'American Homecare Equipment' else 'View Flowchart'
if st.button(button_text):
    st.session_state.show_content = True

# Show content if button was clicked
if st.session_state.show_content:
    # Filter DataFrame to get the matching content
    filtered_data = current_df[
        (current_df['payer'] == selected_payer) &
        (current_df['denialreason'] == selected_denial)
    ]
    
    if not filtered_data.empty:
        if selected_client == 'American Homecare Equipment':
            st.markdown("## Checklist")
            content = filtered_data.iloc[0]['checklists']
        else:
            st.markdown("## Flowchart")
            content = filtered_data.iloc[0]['flowcharts']
            
        
        st.markdown(content)
    else:
        st.error(f"No {'checklist' if selected_client == 'American Homecare Equipment' else 'flowchart'} found for the selected combination.")

# Add Get New button (dynamic text based on client)
new_button_text = '🔄 Get New Checklist' if selected_client == 'American Homecare Equipment' else '🔄 Get New Flowchart'
if st.button(new_button_text, type='primary'):
    reset_all_states()