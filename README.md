#  Automated Advance Scouting & Video-Tagging System

A video-processing and advance scouting workflow tool built for MiLB Video & Technology operations. The system processes pitch-by-pitch tracking logs, auto-clips game footage based on specific scouting triggers using FFmpeg, and generates printable series advance packets.

---

##  Live Links & Project Demo

- **Live Dashboard:** [Streamlit App](baseball-video-scouting-5d9kblmwf6pamkrvzoxq3m.streamlit.app)
- **GitHub Repository:** [https://github.com/krose1013/baseball-video-scouting.git](https://github.com/krose1013/baseball-video-scouting.git)

---

##  Project Architecture & Key Features

### 1. Advance Scouting One-Pager
* **Pitch Arsenal Metrics:** Calculates usage rates, average velocity, and max velocity across pitch types.
* **Printable Series Packet:** Generates a clean 1-page advance PDF report via `reportlab` for dugout and locker room distribution.

### 2. Automated Video Tagging Engine
* **Trigger-Based Trimming:** Auto-slices footage based on specific conditions (e.g., *"All 2-Strike Whiffs on Secondary Pitches vs. LHH"*).
* **Instant Processing:** Uses `FFmpeg` stream copying (`-c copy`) via Python subprocess to trim video clips in milliseconds without re-encoding media.

### 3. Data Quality Control (QC) & Camera Sync Log
* **Hardware Calibration Panel:** Allows video coordinators to apply time offsets to sync optical tracking logs (TrackMan/Hawk-Eye) with video cameras (BATS).
* **Sync Log Documentation:** Standard Operating Procedures for resolving clock drift, dropped frames, and unmapped tracking records.

---

##  Data Sources & Production Readiness

> **Note on Data Feed:**
> The current version of this application runs on simulated practice player data (`mock_data.py`) to demonstrate the underlying data pipeline, video clipper, and UI mechanics. 
> 
> In a live organizational setting, this application can be directly connected to production data sources (such as **TrackMan**, **Rapsodo**, **Hawk-Eye**, or **BATS Video Logs**). Once connected, the dashboard automatically scales to render real-time roster breakdowns, live pitch design metrics, and synchronized camera feeds.

---

##  Tech Stack

* **UI / Framework:** [Streamlit](https://streamlit.io/)
* **Video Engine:** FFmpeg CLI & Python `subprocess`
* **Data Engine:** `pandas`, `numpy`
* **Data Visualization:** `plotly`
* **Report Engine:** `reportlab`
* **Hosting & Version Control:** Git, GitHub, Streamlit Community Cloud

---

##  Project Structure

```text
video-scouting/
├── app.py              # Main Streamlit dashboard interface
├── mock_data.py        # Practice player data generator & timestamp log
├── video_clipper.py    # FFmpeg video slicing engine
├── pdf_generator.py    # ReportLab PDF report generator
├── requirements.txt    # Project dependencies
├── .gitignore          # Git ignore rules (venv, mp4 files, cache)
└── README.md           # Project documentation
