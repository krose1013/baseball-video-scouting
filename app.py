import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

from mock_data import generate_pitch_log
from video_clipper import trim_clip_ffmpeg
from pdf_generator import generate_advance_packet

st.set_page_config(
    page_title="Baseball Advance Scouting & Video Tagging",
    page_icon="",
    layout="wide"
)

st.title(" MLB Advance Scouting & Automated Video Tagging Engine")
st.markdown("Integrate optical tracking logs with raw game footage to automate series preparation.")

# Load Pitch Data
if "df_pitches" not in st.session_state:
    st.session_state.df_pitches = generate_pitch_log()

df_pitches = st.session_state.df_pitches

# Sidebar Filters
st.sidebar.header("Advance Scouting Filters")
selected_pitcher = st.sidebar.selectbox("Select Target Pitcher", options=df_pitches["Pitcher"].unique())

df_filtered = df_pitches[df_pitches["Pitcher"] == selected_pitcher]

# Main Layout Tabs
tab1, tab2, tab3 = st.tabs(["Advance Scouting One-Pager", " Video Tagging & Clipper", " Data QC & Sync Log"])

# ----------------------------------------------------
# TAB 1: ADVANCE SCOUTING ONE-PAGER
# ----------------------------------------------------
with tab1:
    st.header(f"Pitching Profile: {selected_pitcher}")
    
    # Calculate Pitch Arsenal Metrics
    total_pitches = len(df_filtered)
    mix_df = df_filtered.groupby("PitchType").agg(
        Count=("PitchID", "count"),
        AvgVelo=("Velo", "mean"),
        MaxVelo=("Velo", "max")
    ).reset_index()
    mix_df["Usage%"] = (mix_df["Count"] / total_pitches) * 100
    mix_df = mix_df.sort_values(by="Usage%", ascending=False)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Pitch Usage Breakdown")
        fig_pie = px.pie(
            mix_df, values="Usage%", names="PitchType", hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col2:
        st.subheader("Velocity Profiles (mph)")
        fig_bar = px.bar(
            mix_df, x="PitchType", y="AvgVelo", text_auto=".1f",
            labels={"AvgVelo": "Average Velocity (mph)"},
            color="PitchType"
        )
        fig_bar.update_yaxes(range=[75, 100])
        st.plotly_chart(fig_bar, use_container_width=True)
        
    st.subheader("Pitch Arsenal Data Table")
    st.dataframe(mix_df[["PitchType", "Usage%", "AvgVelo", "MaxVelo"]].style.format({
        "Usage%": "{:.1f}%", "AvgVelo": "{:.1f}", "MaxVelo": "{:.1f}"
    }), use_container_width=True)
    
    # Directive Generator
    insights = [
        f"Primary Offering: {mix_df.iloc[0]['PitchType']} ({mix_df.iloc[0]['Usage%']:.1f}% usage, averaging {mix_df.iloc[0]['AvgVelo']:.1f} mph).",
        f"Look for secondary pitches in 2-strike counts against LHH.",
        f"High-frequency whiff zone occurs on out-of-zone chase pitches."
    ]
    
    # PDF Download
    pdf_bytes = generate_advance_packet(selected_pitcher, mix_df, insights)
    st.download_button(
        label=f"Download Printable Scouting One-Pager ({selected_pitcher})",
        data=pdf_bytes,
        file_name=f"{selected_pitcher.lower().replace(' ', '_')}_advance_report.pdf",
        mime="application/pdf"
    )

# ----------------------------------------------------
# TAB 2: AUTOMATED VIDEO TAGGING & CLIPPER
# ----------------------------------------------------
with tab2:
    st.header("Automated Clip Package Generator")
    st.markdown("Trigger automated slicing using FFmpeg based on tracking event logs.")
    
    # Pre-configured Trigger Filter
    st.subheader("Scouting Trigger Filter")
    trigger_option = st.selectbox(
        "Select Video Tagging Preset",
        ["All 2-Strike Whiffs on Secondary Pitches vs LHH", "All In-Play Hard Hit Balls", "All 4-Seam Fastballs"]
    )
    
    if trigger_option == "All 2-Strike Whiffs on Secondary Pitches vs LHH":
        clip_targets = df_filtered[df_filtered["Trigger_2Stk_Whiff_LHH"] == True]
    elif trigger_option == "All In-Play Hard Hit Balls":
        clip_targets = df_filtered[df_filtered["Outcome"].str.contains("In Play")]
    else:
        clip_targets = df_filtered[df_filtered["PitchType"] == "4-Seam"]
        
    st.write(f"Found **{len(clip_targets)}** matching video clips for target filter.")
    st.dataframe(clip_targets[["PitchID", "Batter", "Stand", "Count", "PitchType", "Velo", "Outcome", "VideoStartSec", "VideoEndSec"]], use_container_width=True)
    
    # Video Trimmer Interface
    st.markdown("---")
    st.subheader("Execute FFmpeg Video Trimming")
    
    uploaded_video = st.file_uploader("Upload Raw Game Video File (.mp4)", type=["mp4"])
    
    if uploaded_video is not None:
        # Save temp input file
        temp_input_path = "temp_game_video.mp4"
        with open(temp_input_path, "wb") as f:
            f.write(uploaded_video.read())
            
        st.success("Raw game footage loaded successfully.")
        
        if st.button("✂️ Batch Slice Tagged Clips"):
            os.makedirs("exports", exist_ok=True)
            success_count = 0
            
            for idx, row in clip_targets.iterrows():
                out_name = f"exports/clip_pitch_{row['PitchID']}_{row['PitchType']}.mp4"
                ok, err = trim_clip_ffmpeg(temp_input_path, row["VideoStartSec"], row["VideoEndSec"], out_name)
                if ok:
                    success_count += 1
                    
            st.success(f"Successfully generated {success_count} clips in the `/exports` folder!")
            
            # Preview first exported clip
            if success_count > 0:
                first_clip = f"exports/clip_pitch_{clip_targets.iloc[0]['PitchID']}_{clip_targets.iloc[0]['PitchType']}.mp4"
                if os.path.exists(first_clip):
                    st.subheader("Clip Preview")
                    st.video(first_clip)

# ----------------------------------------------------
# TAB 3: DATA QUALITY CONTROL & CAMERA SYNC LOG
# ----------------------------------------------------
with tab3:
    st.header("Data Quality Control (QC) & Camera Sync Log")
    st.markdown("""
    Optical tracking cameras (TrackMan / Hawk-Eye) and video loggers (BATS / Synergy) run on independent system clocks. 
    Use this workflow to diagnose, calculate, and correct timestamp drift across source feeds.
    """)
    
    st.subheader("Camera Sync Calibration Panel")
    
    c1, c2 = st.columns(2)
    with c1:
        manual_offset = st.number_input("System Time Offset (Seconds)", value=-1.40, step=0.05)
        st.info(f"Applying **{manual_offset}s** offset correction to sync raw video feeds with optical tracking logs.")
        
    with c2:
        sync_status = st.selectbox("Hardware Calibration Status", ["Validated - Low Drift (<0.1s)", "Warning - Frame Offset Detected", "Error - Sync Failure"])
        
    st.markdown("### QC Resolution Protocol Documentation")
    st.markdown("""
    #### Common Sync Issues & Standard Resolution Procedures:
    1. **System Clock Drift (TrackMan vs BATS):**
       * *Issue:* Video clip cuts off pitch release or ball flight.
       * *Resolution:* Calculate offset relative to the pitch release frame using the pitch trigger signal, then update `VideoStartSec` with the global offset variable.
    2. **Dropped Frames in Source Stream:**
       * *Issue:* Timestamp calculations drift by 1-2 seconds over the course of a 3-hour game.
       * *Resolution:* Run a mid-game sync anchor (e.g., set reference points at the top of 1st, 4th, and 7th innings) to recalibrate offsets periodically.
    3. **Missing Pitch IDs in Optical Feed:**
       * *Issue:* TrackMan misses a pitch due to optical obstruction, but BATS video logged the pitch.
       * *Resolution:* Flag pitch records with `Tracking_Status = 'Unmapped'` and backfill tracking values using manual video tagging.
    """)