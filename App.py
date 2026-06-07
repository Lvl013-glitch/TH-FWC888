import streamlit as st
import pandas as pd

# ==========================================
# 1. ฐานข้อมูลจำลอง (Mock Data)
# ==========================================
MANAGERS = ["พี่ไอซ์", "พี่เอ", "พี่ปิง", "พี่ม็อบ", "พี่บูม", "พี่เกรียง", "พี่แอร์", "พี่แป๊บ"]

# ข้อมูลโถของแต่ละทีม (ตัวอย่างบางส่วน)
teams_db = {
    "Argentina": {"manager": "พี่ไอซ์", "pot": 1},
    "Brazil": {"manager": "พี่เอ", "pot": 1},
    "France": {"manager": "พี่ปิง", "pot": 1},
    "England": {"manager": "พี่ม็อบ", "pot": 1},
    "Spain": {"manager": "พี่บูม", "pot": 2},
    "Portugal": {"manager": "พี่เกรียง", "pot": 2},
    "Japan": {"manager": "พี่แอร์", "pot": 3},
    "Thailand": {"manager": "พี่แป๊บ", "pot": 4},
}

# ==========================================
# 2. ฟังก์ชันคำนวณตามกติกา
# ==========================================
def calculate_fines(team_pot, opponent_pot, is_lose, yellow_cards, red_cards, penalties_conceded, own_goals):
    fine = 0
    # ค่าปรับแพ้พลิกล็อก (ใน 90 นาที)
    if is_lose:
        if team_pot == 1 and opponent_pot == 4: fine += 200
        elif team_pot == 1 and opponent_pot == 3: fine += 100
        elif team_pot == 2 and opponent_pot == 4: fine += 100
        elif team_pot == 2 and opponent_pot == 3: fine += 50
            
    # ฟาวล์/ผิดพลาด
    fine += (yellow_cards * 20)
    fine += (red_cards * 100)
    fine += (penalties_conceded * 50)
    fine += (own_goals * 100)
    return fine

# ==========================================
# 3. หน้าจอแอปพลิเคชัน (UI)
# ==========================================
st.set_page_config(page_title="WC 2026 Draft", page_icon="🏆", layout="wide")
st.title("🏆 FIFA World Cup 2026 Office Draft")

tab1, tab2 = st.tabs(["📝 บันทึกผลแมตช์", "💸 ตารางค่าปรับ"])

with tab1:
    st.subheader("อัปเดตผลการแข่งขัน")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**ทีม A**")
        team_a = st.selectbox("เลือกทีม A", list(teams_db.keys()), key="team_a")
        team_a_goals = st.number_input("ประตู (ทีม A)", min_value=0, step=1, key="g_a")
        team_a_yc = st.number_input("ใบเหลือง (ทีม A)", min_value=0, step=1, key="yc_a")
        team_a_rc = st.number_input("ใบแดง (ทีม A)", min_value=0, step=1, key="rc_a")
        team_a_pen = st.number_input("เสียจุดโทษ (ทีม A)", min_value=0, step=1, key="pen_a")
        team_a_og = st.number_input("ทำเข้าประตูตัวเอง (ทีม A)", min_value=0, step=1, key="og_a")

    with col2:
        st.markdown("**ทีม B**")
        team_b = st.selectbox("เลือกทีม B", list(teams_db.keys()), index=1, key="team_b")
        team_b_goals = st.number_input("ประตู (ทีม B)", min_value=0, step=1, key="g_b")
        team_b_yc = st.number_input("ใบเหลือง (ทีม B)", min_value=0, step=1, key="yc_b")
        team_b_rc = st.number_input("ใบแดง (ทีม B)", min_value=0, step=1, key="rc_b")
        team_b_pen = st.number_input("เสียจุดโทษ (ทีม B)", min_value=0, step=1, key="pen_b")
        team_b_og = st.number_input("ทำเข้าประตูตัวเอง (ทีม B)", min_value=0, step=1, key="og_b")
        
    if st.button("💾 คำนวณและบันทึกผล", use_container_width=True):
        if team_a == team_b:
            st.error("เลือกทีมซ้ำกันไม่ได้ครับ!")
        else:
            pot_a = teams_db[team_a]["pot"]
            pot_b = teams_db[team_b]["pot"]
            a_loses = team_a_goals < team_b_goals
            b_loses = team_b_goals < team_a_goals
            
            fine_a = calculate_fines(pot_a, pot_b, a_loses, team_a_yc, team_a_rc, team_a_pen, team_a_og)
            fine_b = calculate_fines(pot_b, pot_a, b_loses, team_b_yc, team_b_rc, team_b_pen, team_b_og)
            
            st.success("✅ คำนวณเสร็จสิ้น!")
            st.info(f"🚨 **สรุปค่าปรับ:** \n- {team_a} (โถ {pot_a} - {teams_db[team_a]['manager']}) โดนปรับ **{fine_a}** บาท \n- {team_b} (โถ {pot_b} - {teams_db[team_b]['manager']}) โดนปรับ **{fine_b}** บาท")

with tab2:
    st.subheader("💸 ตารางค่าปรับสะสม (เตรียมจ่ายเข้ากองกลาง)")
    # ตารางจำลอง
    data = {"ผู้จัดการทีม": MANAGERS, "ค่าปรับสะสม (บาท)": [300, 150, 0, 500, 20, 0, 100, 50]}
    df = pd.DataFrame(data).sort_values(by="ค่าปรับสะสม (บาท)", ascending=False)
    st.dataframe(df, use_container_width=True, hide_index=True)
