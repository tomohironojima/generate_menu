import streamlit as st
import time
import random
import json

# ページ設定
st.set_page_config(
    page_title="BJJ Rule Master",
    page_icon="🥋",
    layout="centered"
)

# --- データ定義 ---
def load_quiz_data():
    try:
        with open('quiz_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("エラー: クイズデータ（quiz_data.json）が見つかりません。")
        return []
    except json.JSONDecodeError:
        st.error("エラー: クイズデータの読み込みに失敗しました。")
        return []

quiz_data = load_quiz_data()

# --- セッション状態の初期化 ---
if 'shuffled_quiz_data' not in st.session_state:
    full_data = quiz_data.copy()
    random.shuffle(full_data)
    st.session_state.shuffled_quiz_data = full_data[:10]

if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'quiz_finished' not in st.session_state:
    st.session_state.quiz_finished = False
if 'show_feedback' not in st.session_state:
    st.session_state.show_feedback = False
if 'last_answer_correct' not in st.session_state:
    st.session_state.last_answer_correct = False

# --- 関数定義 ---
def restart_quiz():
    """クイズをリセットして最初から始める"""
    full_data = quiz_data.copy()
    random.shuffle(full_data)
    st.session_state.shuffled_quiz_data = full_data[:10]
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.quiz_finished = False
    st.session_state.show_feedback = False
    st.rerun()

def submit_answer(selected_option, correct_option):
    """回答が選択されたときの処理"""
    is_correct = (selected_option == correct_option)
    st.session_state.last_answer_correct = is_correct
    
    if is_correct:
        st.session_state.score += 1
    
    st.session_state.show_feedback = True

def next_question():
    """次の問題へ進む"""
    st.session_state.show_feedback = False
    
    # 次の問題があるかチェック
    if st.session_state.current_question_index + 1 < len(st.session_state.shuffled_quiz_data):
        st.session_state.current_question_index += 1
    else:
        st.session_state.quiz_finished = True
    
    st.rerun()

# --- UI描画 ---
st.title("🥋 ブラジリアン柔術 ルールクイズ")
st.markdown("IBJJFルールに基づいた、選手のためのポイント・反則学習アプリ")

# プログレスバーの表示
progress = 0
if len(st.session_state.shuffled_quiz_data) > 0:
    progress = (st.session_state.current_question_index) / len(st.session_state.shuffled_quiz_data)

st.progress(progress)

if st.session_state.quiz_finished:
    # 結果画面
    st.success("🎉 クイズ終了！")
    
    final_score = st.session_state.score
    total_questions = len(st.session_state.shuffled_quiz_data)
    accuracy = (final_score / total_questions) * 100
    
    st.metric(label="あなたの最終スコア", value=f"{final_score} / {total_questions}", delta=f"正解率 {accuracy:.1f}%")
    
    if accuracy == 100:
        st.balloons()
        st.markdown("### 素晴らしい！ ルールマスターです！ 🥇")
    elif accuracy >= 80:
        st.markdown("### かなり詳しいですね！ 🥈")
    else:
        st.markdown("### 復習して再度チャレンジしましょう！ 🥋")
        
    if st.button("もう一度挑戦する"):
        restart_quiz()
        
else:
    # 問題表示画面
    if len(st.session_state.shuffled_quiz_data) > 0:
        current_q = st.session_state.shuffled_quiz_data[st.session_state.current_question_index]
        
        st.header(f"Q{st.session_state.current_question_index + 1}. {current_q['question']}")
        
        # まだ回答していない（フィードバック表示前）場合
        if not st.session_state.show_feedback:
            st.markdown("##### 選択肢を選んでください:")
            
            # 3つのカラムを作ってボタンを横並びにするレイアウト（スマホなどでは縦になる）
            col1, col2, col3 = st.columns(3)
            
            options = current_q['options']
            
            with col1:
                if st.button(options[0], use_container_width=True):
                    submit_answer(options[0], current_q['correct'])
                    st.rerun()
            with col2:
                if st.button(options[1], use_container_width=True):
                    submit_answer(options[1], current_q['correct'])
                    st.rerun()
            with col3:
                if st.button(options[2], use_container_width=True):
                    submit_answer(options[2], current_q['correct'])
                    st.rerun()
                    
        else:
            # 回答後のフィードバック画面
            if st.session_state.last_answer_correct:
                st.success("✅ **正解です！**")
            else:
                st.error(f"❌ **不正解...** (正解: {current_q['correct']})")
                
            st.info(f"💡 **解説:**\n\n{current_q['explanation']}")
            
            if st.button("次の問題へ 👉", type="primary"):
                next_question()
    else:
        st.error("クイズデータがありません。")

# フッター
st.markdown("---")
st.caption("※このアプリは学習用です。そのため、実際の試合では審判の判断が最終決定となります。")