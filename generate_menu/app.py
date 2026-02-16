import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# --- 1. データの読み込み ---
@st.cache_data
def load_data():
    menus_df = pd.read_csv('menus.csv')
    ingredients_df = pd.read_csv('ingredients.csv')
    menu_ingredients_df = pd.read_csv('menu_ingredients.csv')
    history_df = pd.read_csv('history.csv', parse_dates=['cook_date'])
    return menus_df, ingredients_df, menu_ingredients_df, history_df

menus, ingredients, recipes, history = load_data()

# --- 2. 献立生成ロジック ---
def generate_menus(days=3, target_season='冬'):
    today = pd.to_datetime('today')
    
    # 履歴から各メニューの「最後に作った日」を取得
    last_cooked = history.groupby('menu_id')['cook_date'].max().reset_index()
    
    # menusと最後に作った日を結合
    merged_menus = pd.merge(menus, last_cooked, on='menu_id', how='left')
    
    # 経過日数を計算（一度も作ってない場合は1000日とする）
    merged_menus['days_since'] = (today - merged_menus['cook_date']).dt.days
    merged_menus['days_since'] = merged_menus['days_since'].fillna(1000)
    
    # フィルタリング条件：アクティブ ＆ 季節が合う ＆ クールダウン期間を過ぎている
    available_menus = merged_menus[
        (merged_menus['is_active'] == True) & 
        (merged_menus['season'].isin([target_season, '通年'])) &
        (merged_menus['days_since'] >= merged_menus['cooldown_days'])
    ]
    
    # 指定日数分をランダムに抽出（候補が足りない場合はある分だけ）
    sample_size = min(days, len(available_menus))
    if sample_size == 0:
        return []
    
    selected = available_menus.sample(n=sample_size)['menu_id'].tolist()
    return selected

# --- 3. 買い物リスト生成ロジック ---
def generate_shopping_list(selected_menu_ids):
    if not selected_menu_ids:
        return pd.DataFrame()
        
    # 選ばれたメニューのレシピ（必要な食材）を抽出
    target_recipes = recipes[recipes['menu_id'].isin(selected_menu_ids)]
    
    # 食材マスターと結合
    shopping_df = pd.merge(target_recipes, ingredients, on='ingredient_id', how='left')
    
    # 常備品（is_staple == True）を除外
    shopping_df = shopping_df[shopping_df['is_staple'] == False]
    
    # 同じ食材をグループ化して分量を合算
    shopping_list = shopping_df.groupby(['shop_section', 'ingredient_name', 'unit'])['quantity'].sum().reset_index()
    
    # 売り場の順序を定義してソート（スーパーの導線に合わせる）
    section_order = {'野菜': 1, '鮮魚': 2, '精肉': 3, '日配品': 4, '調味料': 5}
    shopping_list['sort_order'] = shopping_list['shop_section'].map(section_order).fillna(99)
    shopping_list = shopping_list.sort_values('sort_order').drop('sort_order', axis=1)
    
    return shopping_list

# --- UI部分（Streamlit） ---
st.title("🍽️ 自動献立＆買い物リスト生成アプリ")

# サイドバーで設定
st.sidebar.header("設定")
plan_days = st.sidebar.slider("何日分の献立を作りますか？", min_value=1, max_value=7, value=3)
current_season = st.sidebar.selectbox("季節", ["春", "夏", "秋", "冬"], index=3)

if st.button("献立を作成する！"):
    # 献立生成
    selected_ids = generate_menus(days=plan_days, target_season=current_season)
    
    if not selected_ids:
        st.warning("条件に合うメニューがありません。履歴や季節設定を見直してください。")
    else:
        st.subheader(f"📅 むこう{plan_days}日分の献立")
        selected_menu_names = menus[menus['menu_id'].isin(selected_ids)]['menu_name'].tolist()
        for i, name in enumerate(selected_menu_names, 1):
            st.write(f"Day {i}: **{name}**")
            
        st.markdown("---")
        
        # 買い物リスト生成
        st.subheader("🛒 買い物リスト（売り場順）")
        shopping_list = generate_shopping_list(selected_ids)
        
        # 売り場ごとに表示
        for section, group in shopping_list.groupby('shop_section'):
            st.write(f"**【{section}】**")
            for _, row in group.iterrows():
                # チェックボックス付きで表示
                st.checkbox(f"{row['ingredient_name']} : {row['quantity']} {row['unit']}", key=row['ingredient_name'])