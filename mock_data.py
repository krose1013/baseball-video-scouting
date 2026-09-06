import pandas as pd
import numpy as np

def generate_pitch_log(num_pitches=120):
    np.random.seed(42)
    
    pitchers = ["Gavin Stone", "Jackson Jobe", "Caden Dana"]
    batters = ["Heston Kjerstad", "Colson Montgomery", "Brooks Lee", "Jasson Dominguez"]    
    pitch_types = ["4-Seam", "Slider", "Changeup", "Sweeper", "Curveball"]
    outcomes = ["Whiff", "Called Strike", "Foul", "In Play Out", "In Play Single", "In Play HR"]
    stands = ["L", "R"]
    
    data = []
    current_time_sec = 15.0  # Game video start offset (15s mark)
    
    for pitch_id in range(1, num_pitches + 1):
        pitcher = np.random.choice(pitchers, p=[0.5, 0.3, 0.2])
        batter = np.random.choice(batters)
        stand = np.random.choice(stands, p=[0.6, 0.4])  # 60% LHH focus for scouting
        p_type = np.random.choice(pitch_types, p=[0.4, 0.25, 0.15, 0.10, 0.10])
        strikes = np.random.choice([0, 1, 2], p=[0.3, 0.3, 0.4])
        balls = np.random.choice([0, 1, 2, 3], p=[0.3, 0.3, 0.2, 0.2])
        
        # Velocity ranges by pitch type
        velo_map = {"4-Seam": (94.0, 98.5), "Slider": (83.0, 87.5), "Changeup": (85.0, 89.0), "Sweeper": (80.0, 84.5), "Curveball": (78.0, 82.0)}
        min_v, max_v = velo_map[p_type]
        velo = np.round(np.random.uniform(min_v, max_v), 1)
        
        outcome = np.random.choice(outcomes, p=[0.25, 0.20, 0.25, 0.15, 0.10, 0.05])
        
        # Timestamp logging (15-25 seconds between pitches)
        duration = np.random.uniform(18.0, 26.0)
        start_timestamp = current_time_sec
        end_timestamp = start_timestamp + 8.0  # 8-second clip window
        current_time_sec += duration
        
        # Flag specific high-value scouting triggers
        is_two_strike = (strikes == 2)
        is_whiff = (outcome == "Whiff")
        is_secondary = (p_type != "4-Seam")
        trigger_flag = is_two_strike and is_whiff and is_secondary and (stand == "L")
        
        data.append({
            "PitchID": pitch_id,
            "Pitcher": pitcher,
            "Batter": batter,
            "Stand": stand,
            "Balls": balls,
            "Strikes": strikes,
            "Count": f"{balls}-{strikes}",
            "PitchType": p_type,
            "Velo": velo,
            "Outcome": outcome,
            "VideoStartSec": np.round(start_timestamp, 2),
            "VideoEndSec": np.round(end_timestamp, 2),
            "Trigger_2Stk_Whiff_LHH": trigger_flag,
            "Zone": np.random.choice(range(1, 10))
        })
        
    return pd.DataFrame(data)