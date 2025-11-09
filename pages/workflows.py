"""
Workflows Page
Create, edit, and manage scanning workflows
"""

import streamlit as st
import json
from datetime import datetime


def render_workflows_page():
    """Render the workflows page"""
    
    st.markdown('<div class="main-header"><h1>🔧 Workflow Management</h1><p>Create and manage your custom scanning workflows</p></div>', unsafe_allow_html=True)
    
    # Two column layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        render_workflow_list()
    
    with col2:
        render_workflow_editor()


def render_workflow_list():
    """Display list of workflows"""
    
    st.subheader("📋 Your Workflows")
    
    # Display existing workflows
    for workflow_name in st.session_state.workflows.keys():
        is_active = (workflow_name == st.session_state.active_workflow)
        
        with st.container():
            col_name, col_btns = st.columns([3, 1])
            
            with col_name:
                if is_active:
                    st.markdown(f"**✨ {workflow_name}** (Active)")
                else:
                    st.markdown(f"**{workflow_name}**")
            
            with col_btns:
                if not is_active:
                    if st.button("✓", key=f"activate_{workflow_name}", help="Set as active"):
                        st.session_state.active_workflow = workflow_name
                        st.rerun()
                
                if workflow_name != 'Default Scanner':
                    if st.button("🗑", key=f"delete_{workflow_name}", help="Delete workflow"):
                        del st.session_state.workflows[workflow_name]
                        if st.session_state.active_workflow == workflow_name:
                            st.session_state.active_workflow = 'Default Scanner'
                        st.rerun()
        
        st.divider()
    
    # Add new workflow button
    if st.button("➕ Create New Workflow", use_container_width=True, type="primary"):
        st.session_state.editing_workflow = 'NEW'
        st.session_state.new_workflow_name = ''
        st.rerun()


def render_workflow_editor():
    """Edit workflow settings"""
    
    # Determine which workflow to edit
    if 'editing_workflow' in st.session_state and st.session_state.editing_workflow == 'NEW':
        st.subheader("➕ Create New Workflow")
        editing_new = True
        workflow_name = st.session_state.get('new_workflow_name', '')
        workflow = {
            'indicators': [],
            'patterns': [],
            'setups': [],
            'timeframes': {'Wave': '4h', 'Tide': '1d', 'SuperTide': '1wk'}
        }
    else:
        editing_new = False
        workflow_name = st.session_state.active_workflow
        workflow = st.session_state.workflows[workflow_name]
        st.subheader(f"✏️ Edit: {workflow_name}")
    
    # Workflow name (only for new workflows)
    if editing_new:
        new_name = st.text_input(
            "Workflow Name",
            value=workflow_name,
            placeholder="Enter workflow name",
            key="workflow_name_input"
        )
        st.session_state.new_workflow_name = new_name
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Indicators",
        "📐 Patterns",
        "🎯 Setups",
        "💾 Summary"
    ])
    
    with tab1:
        render_indicators_selector(workflow)
    
    with tab2:
        render_patterns_selector(workflow)
    
    with tab3:
        render_setups_selector(workflow)
    
    with tab4:
        render_workflow_summary(workflow, workflow_name, editing_new)


def render_indicators_selector(workflow):
    """Select indicators for the workflow"""
    
    st.write("### Select Indicators")
    
    # Available indicators
    available_indicators = {
        'Core Indicators': ['Yoda', 'RSI', 'MACD', 'BB', 'ATR'],
        'Trend Indicators': ['ADX', 'EMA_5', 'EMA_20', 'EMA_50', 'SMA_200'],
        'Momentum & Volume': ['Stochastic', 'OBV', 'VWAP']
    }
    
    selected_indicators = workflow.get('indicators', [])
    
    for category, indicators in available_indicators.items():
        st.write(f"**{category}**")
        cols = st.columns(3)
        
        for idx, indicator in enumerate(indicators):
            with cols[idx % 3]:
                is_selected = indicator in selected_indicators
                if st.checkbox(indicator, value=is_selected, key=f"ind_{indicator}_{category}"):
                    if indicator not in selected_indicators:
                        selected_indicators.append(indicator)
                else:
                    if indicator in selected_indicators:
                        selected_indicators.remove(indicator)
    
    workflow['indicators'] = selected_indicators
    st.success(f"✅ Selected {len(selected_indicators)} indicators")


def render_patterns_selector(workflow):
    """Select patterns for the workflow"""
    
    st.write("### Select Chart Patterns")
    
    # Available patterns
    available_patterns = {
        'Reversal Patterns': ['Double_Bottom', 'Double_Top', 'Head_Shoulders', 'Inv_Head_Shoulders'],
        'Continuation Patterns': ['Flag', 'Triangle', 'Cup_Handle'],
        'Breakout Patterns': ['TL_Break_Up', 'TL_Break_Down', 'Rising_Wedge', 'Falling_Wedge']
    }
    
    selected_patterns = workflow.get('patterns', [])
    
    for category, patterns in available_patterns.items():
        st.write(f"**{category}**")
        cols = st.columns(2)
        
        for idx, pattern in enumerate(patterns):
            with cols[idx % 2]:
                is_selected = pattern in selected_patterns
                if st.checkbox(pattern, value=is_selected, key=f"pat_{pattern}_{category}"):
                    if pattern not in selected_patterns:
                        selected_patterns.append(pattern)
                else:
                    if pattern in selected_patterns:
                        selected_patterns.remove(pattern)
    
    workflow['patterns'] = selected_patterns
    st.success(f"✅ Selected {len(selected_patterns)} patterns")


def render_setups_selector(workflow):
    """Select setups for the workflow"""
    
    st.write("### Select Trading Setups")
    
    # Available setups
    available_setups = ['Momentum_Long', 'Momentum_Short', 'Breakout']
    
    selected_setups = workflow.get('setups', [])
    
    st.write("**Standard Setups**")
    for setup in available_setups:
        is_selected = setup in selected_setups
        if st.checkbox(setup, value=is_selected, key=f"setup_{setup}"):
            if setup not in selected_setups:
                selected_setups.append(setup)
        else:
            if setup in selected_setups:
                selected_setups.remove(setup)
    
    workflow['setups'] = selected_setups
    st.success(f"✅ Selected {len(selected_setups)} setups")
    
    # Timeframe configuration
    st.divider()
    st.write("### Multi-Timeframe Configuration")
    
    timeframes = workflow.get('timeframes', {'Wave': '4h', 'Tide': '1d', 'SuperTide': '1wk'})
    
    tf_options = ['15m', '30m', '1h', '2h', '4h', '1d', '1wk', '1mo']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Wave**")
        wave_tf = st.selectbox(
            "Short-term",
            tf_options,
            index=tf_options.index(timeframes.get('Wave', '4h')),
            key='wave_tf_select'
        )
        timeframes['Wave'] = wave_tf
    
    with col2:
        st.write("**Tide**")
        tide_tf = st.selectbox(
            "Medium-term",
            tf_options,
            index=tf_options.index(timeframes.get('Tide', '1d')),
            key='tide_tf_select'
        )
        timeframes['Tide'] = tide_tf
    
    with col3:
        st.write("**SuperTide**")
        supertide_tf = st.selectbox(
            "Long-term",
            tf_options,
            index=tf_options.index(timeframes.get('SuperTide', '1wk')),
            key='supertide_tf_select'
        )
        timeframes['SuperTide'] = supertide_tf
    
    workflow['timeframes'] = timeframes


def render_workflow_summary(workflow, workflow_name, editing_new):
    """Display workflow summary and save options"""
    
    st.write("### Workflow Summary")
    
    # Display configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📊 Indicators**")
        if workflow['indicators']:
            for ind in workflow['indicators']:
                st.markdown(f"- {ind}")
        else:
            st.caption("No indicators selected")
        
        st.write("**📐 Patterns**")
        if workflow['patterns']:
            for pat in workflow['patterns']:
                st.markdown(f"- {pat}")
        else:
            st.caption("No patterns selected")
    
    with col2:
        st.write("**🎯 Setups**")
        if workflow['setups']:
            for setup in workflow['setups']:
                st.markdown(f"- {setup}")
        else:
            st.caption("No setups selected")
        
        st.write("**🕐 Timeframes**")
        for tf_name, tf_value in workflow['timeframes'].items():
            st.markdown(f"- **{tf_name}:** {tf_value}")
    
    # JSON export
    st.divider()
    st.write("**JSON Configuration**")
    workflow_json = json.dumps(workflow, indent=2)
    st.code(workflow_json, language='json')
    
    # Action buttons
    st.divider()
    
    col_btn1, col_btn2 = st.columns([1, 1])
    
    with col_btn1:
        if editing_new:
            if st.button("💾 Save Workflow", type="primary", use_container_width=True):
                new_name = st.session_state.get('new_workflow_name', '')
                if new_name:
                    st.session_state.workflows[new_name] = workflow
                    st.session_state.active_workflow = new_name
                    if 'editing_workflow' in st.session_state:
                        del st.session_state.editing_workflow
                    st.success(f"✅ Workflow '{new_name}' created!")
                    st.rerun()
                else:
                    st.error("Please enter a workflow name")
        else:
            if st.button("💾 Save Changes", type="primary", use_container_width=True):
                st.session_state.workflows[workflow_name] = workflow
                st.success(f"✅ Changes saved to '{workflow_name}'")
    
    with col_btn2:
        # Export workflow
        st.download_button(
            label="📥 Export JSON",
            data=workflow_json,
            file_name=f"workflow_{workflow_name.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )
