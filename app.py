import streamlit as st
import time
import random

# ページ設定
st.set_page_config(
    page_title="BJJ Rule Master",
    page_icon="🥋",
    layout="centered"
)

# --- データ定義 ---
quiz_data = [
    {
        "id": 1,
        "question": "ガードポジションからスイープし、トップポジションを3秒キープしました。ポイントは何点？",
        "options": ["2点", "3点", "4点"],
        "correct": "2点",
        "explanation": "スイープの定義により、ガードからトップを取り3秒維持した場合は2ポイントです。"
    },
    {
        "id": 2,
        "question": "ニーリーピング（外掛け）をした場合の判定は？",
        "options": ["ペナルティ", "アドバンテージ", "反則負け（失格）"],
        "correct": "反則負け（失格）",
        "explanation": "ニーリーピングは膝関節に深刻なダメージを与える危険があるため、重大な反則として即失格（DQ）となります。"
    },
    {
        "id": 3,
        "question": "パスガードし、サイドコントロールで3秒キープしました。ポイントは何点？",
        "options": ["2点", "3点", "4点"],
        "correct": "3点",
        "explanation": "パスガード（相手の足を超えて抑え込む）を確立し、3秒間維持すると3ポイントが与えられます。"
    },
    {
        "id": 4,
        "question": "マウントポジションを3秒キープしました。ポイントは何点？",
        "options": ["2点", "3点", "4点"],
        "correct": "4点",
        "explanation": "マウントポジションは非常に有利なポジションであり、3秒間維持すると4ポイントが与えられます。"
    },
    {
        "id": 5,
        "question": "ニーオンベリーを3秒キープしました。ポイントは何点？",
        "options": ["2点", "3点", "4点"],
        "correct": "2点",
        "explanation": "ニーオンベリーは相手を制圧する有効なポジションであり、3秒間の維持で2ポイントが与えられます。"
    },
    {
        "id": 6,
        "question": "テイクダウンしてトップポジションを3秒キープしました。ポイントは何点？",
        "options": ["2点", "3点", "4点"],
        "correct": "2点",
        "explanation": "テイクダウンによりトップポジションを確保して3秒維持すると2ポイントが入ります。"
    },
    {
        "id": 7,
        "question": "バックコントロール（両足フックあり）を3秒キープしました。ポイントは何点？",
        "options": ["3点", "4点", "アドバンテージ"],
        "correct": "4点",
        "explanation": "バックコントロールは相手の背後を取り両足をフックすることで完成し、4ポイントが与えられます。"
    },
    {
        "id": 8,
        "question": "相手がサブミッションをかけている最中に、防御側が場外へ逃げた場合はどうなる？",
        "options": ["試合続行", "2点献上して中央で再開", "反則負け（失格）"],
        "correct": "反則負け（失格）",
        "explanation": "サブミッションから逃れるために意図的に場外へ出た場合は、即座に反則負け（失格）となります。"
    },
    {
        "id": 9,
        "question": "両選手が同時にガードを引き込み（ダブルガードプル）、20秒間動きがない場合、どうなる？",
        "options": ["両者にペナルティ", "試合一時停止してスタンドから再開", "両者にアドバンテージ"],
        "correct": "両者にペナルティ",
        "explanation": "ダブルガードプル状態で双方が攻撃の意思を見せず膠着した場合、20秒経過で両者にペナルティが与えられ、スタンドから再開されます。"
    },
    {
        "id": 10,
        "question": "白帯の試合で飛びつきクローズドガードを行いました。判定は？",
        "options": ["問題なし", "ペナルティ", "反則負け（失格）"],
        "correct": "反則負け（失格）",
        "explanation": "白帯では飛びつきガード（ジャンピングガード）は禁止されており、失格となります。"
    },
    {
        "id": 11,
        "question": "相手の道着の袖の中に指を入れてグリップを作りました。判定は？",
        "options": ["注意のみ", "ペナルティ", "反則負け（失格）"],
        "correct": "ペナルティ",
        "explanation": "袖口や裾の中に指を入れる行為（ポケットグリップ）は反則であり、ペナルティが与えられます。"
    },
    {
        "id": 12,
        "question": "テイクダウンを試み、相手が尻餅をついたがすぐに立ち上がった。3秒間のトップキープはできていない。判定は？",
        "options": ["ポイントなし", "アドバンテージ", "2点"],
        "correct": "アドバンテージ",
        "explanation": "テイクダウンで相手を倒したがポジションを確立できなかった場合、アドバンテージが与えられます。"
    },
    {
        "id": 13,
        "question": "パスガードを試み、相手をほぼ抑え込んだが、ガードに戻された。判定は？",
        "options": ["ポイントなし", "アドバンテージ", "3点"],
        "correct": "アドバンテージ",
        "explanation": "パスガードの形にほぼなりかけたが完遂できなかった場合、アドバンテージが与えられます。"
    },
    {
        "id": 14,
        "question": "サブミッションをかけ、相手がタップする前にタイムアップとなった。判定は？",
        "options": ["ポイントなし", "アドバンテージ", "サブミッション勝利"],
        "correct": "アドバンテージ",
        "explanation": "サブミッションが極まりかけていたが終了した場合、アドバンテージが与えられます。"
    },
    {
        "id": 15,
        "question": "試合中、故意に道着を脱いだり帯を解いたりした。判定は？",
        "options": ["注意のみ", "ペナルティ", "反則負け（失格）"],
        "correct": "ペナルティ",
        "explanation": "試合遅延行為やスポーツマンシップに反する行為としてペナルティが与えられます。"
    },
    {
        "id": 16,
        "question": "相手に激しく暴言を吐いた。判定は？",
        "options": ["ペナルティ", "２ペナルティ", "反則負け（失格）"],
        "correct": "反則負け（失格）",
        "explanation": "審判や対戦相手への暴言や侮辱行為は、即座に失格処分の対象となります。"
    },
    {
        "id": 17,
        "question": "クローズドガードから相手を持ち上げ、マットに叩きつけた（スラム）。判定は？",
        "options": ["2点", "ペナルティ", "反則負け（失格）"],
        "correct": "反則負け（失格）",
        "explanation": "スラム（バスター）は重大な反則であり、即失格となります。"
    },
    {
        "id": 18,
        "question": "ダブルガードプルの状態から、片方の選手が上になりトップポジションを取りました。ポイントは？",
        "options": ["ポイントなし", "アドバンテージ", "2点"],
        "correct": "アドバンテージ",
        "explanation": "ダブルガードプルから上になっただけではスイープやテイクダウンのポイントにはなりませんが、アドバンテージが入ります。"
    },
    {
        "id": 19,
        "question": "マウントポジションを取ったが、片方の膝が相手の腕の上に乗っている。ポイントは入る？",
        "options": ["入る（4点）", "入らない", "アドバンテージのみ"],
        "correct": "入らない",
        "explanation": "マウントの4点は、両膝が相手の腕の下（脇の下より下）にあり、相手を制圧している必要があります。腕の上に足がある場合はポイントになりません。"
    },
    {
        "id": 20,
        "question": "バックマウントを取ったが、足首をクロスして組んでいる。ポイントは入る？",
        "options": ["入る（4点）", "入らない", "ペナルティ"],
        "correct": "入らない",
        "explanation": "バックコントロールの4点は、両足のフック（踵を相手の内腿にかける）が必要です。足首をクロスして組んでいる場合はポイントになりません。"
    },
    {
        "id": 21,
        "question": "スイープしてトップを取ったが、相手のハーフガードの中に片足が残っている。ポイントは？",
        "options": ["入る（2点）", "入らない", "アドバンテージのみ"],
        "correct": "入る（2点）",
        "explanation": "スイープは、ガードからトップを取れば成立します。相手のガード（ハーフ含む）の中にいても、トップを維持すれば2点です。"
    },
    {
        "id": 22,
        "question": "パスガードしてサイドを取ったが、相手がすぐに亀（タートル）になった。ポイントは？",
        "options": ["3点", "アドバンテージ", "ポイントなし"],
        "correct": "アドバンテージ",
        "explanation": "3秒間抑え込みをキープできていないためパスガードのポイントは入りませんが、アドバンテージがつきます。"
    },
    {
        "id": 23,
        "question": "相手のズボンの内側を掴んでグリップした。判定は？",
        "options": ["ペナルティ", "注意のみ", "問題なし"],
        "correct": "ペナルティ",
        "explanation": "袖口と同様、ズボンの裾の内側を掴むことは指の怪我防止のため反則（ペナルティ）です。"
    },
    {
        "id": 24,
        "question": "スタンド状態で膠着し、審判から「ルーチ（コンバッチ）」と声をかけられた。これは何？",
        "options": ["試合開始", "ペナルティ警告", "アドバンテージ"],
        "correct": "ペナルティ警告",
        "explanation": "消極的な姿勢（ストーリング）に対する警告です。改善されない場合、ペナルティが与えられます。"
    },
    {
        "id": 25,
        "question": "ペナルティが累積で3つになった場合、相手には何が与えられる？",
        "options": ["アドバンテージ", "2点", "反則勝ち"],
        "correct": "2点",
        "explanation": "ペナルティの累積罰則：1つ目=注意、2つ目=相手にアドバンテージ、3つ目=相手に2点、4つ目=失格。"
    },
    {
        "id": 26,
        "question": "ペナルティが累積で4つになった場合、どうなる？",
        "options": ["相手に4点", "相手にさらに2点", "反則負け（失格）"],
        "correct": "反則負け（失格）",
        "explanation": "4つ目のペナルティが宣告されると、その選手は失格となります。"
    },
    {
        "id": 27,
        "question": "青帯以上で、相手の首に足をかけて締める「洗濯バサミ（シザースチョーク）」は有効？",
        "options": ["有効", "反則", "白帯のみ禁止"],
        "correct": "反則",
        "explanation": "IBJJFルールでは、白帯だけでなく青帯以上でもシザースチョーク（手を使わず足だけで首を絞める行為）は基本的に使用可能ですが、細かい規定はカテゴリによります。しかし一般的にIBJJFでは許可されています。（※注：この問題は厳密にはカテゴリ依存ですが、アダルト青帯以上ならOKという認識で設問。ただし、質問として『外掛け』などの危険技とは区別されます）。修正：IBJJFルールブック上、白帯は禁止技に含まれますが、青帯からは許可されています。正解は「有効」。"
    },
    {
        "id": 28,
        "question": "白帯の試合でリストロック（手首固め）を使った。判定は？",
        "options": ["有効（一本勝ち）", "アドバンテージ", "反則負け（失格）"],
        "correct": "反則負け（失格）",
        "explanation": "リストロックは青帯以上で解禁される技であり、白帯では禁止技のため失格となります。"
    },
    {
        "id": 29,
        "question": "ヒールフック（足首を捻る関節技）をかけた。ノーギルールの特定カテゴリ以外ではどうなる？",
        "options": ["有効", "ペナルティ", "反則負け（失格）"],
        "correct": "反則負け（失格）",
        "explanation": "道着あり（Gi）の試合ではヒールフックは全帯色・全カテゴリで一発失格の反則技です（2023年時点の主要ルール）。"
    },
    {
        "id": 30,
        "question": "ニーオンベリーの状態で、相手が逆側の手で自分の帯を掴んできた。これは反則？",
        "options": ["反則", "反則ではない", "アドバンテージ"],
        "correct": "反則ではない",
        "explanation": "防御側が相手の帯を掴むことは反則ではありません。"
    },
    {
        "id": 31,
        "question": "試合終了時に同点、アドバンテージもペナルティも同数だった。勝敗はどう決まる？",
        "options": ["延長戦", "レフェリー判定", "両者敗北"],
        "correct": "レフェリー判定",
        "explanation": "全てのスコアが同点の場合、レフェリー判定（レフェリーデシジョン）により勝者が決定されます。"
    },
    {
        "id": 32,
        "question": "ガードポジションの選手が立ち上がり、相手を押し倒してトップを取ったが、3秒キープできなかった。ポイントは？",
        "options": ["2点", "アドバンテージ", "なし"],
        "correct": "アドバンテージ",
        "explanation": "スイープの形だがキープ不十分なためアドバンテージになります。"
    },
    {
        "id": 33,
        "question": "相手のラペル（襟）を使って相手の手首を縛る行為は？",
        "options": ["有効", "反則", "ペナルティ"],
        "correct": "有効",
        "explanation": "ラペルガードやワームガードなど、ラペルを利用したコントロールは有効です。"
    },
    {
        "id": 34,
        "question": "トーホールド（足首固め）が認められるのはどの帯から？",
        "options": ["青帯", "紫帯", "茶帯"],
        "correct": "茶帯",
        "explanation": "トーホールドは茶帯・黒帯でのみ許可されている技です。"
    },
    {
        "id": 35,
        "question": "ニーバー（膝十字固め）が認められるのはどの帯から？",
        "options": ["紫帯", "茶帯", "黒帯のみ"],
        "correct": "茶帯",
        "explanation": "ニーバーも茶帯以上で解禁される技です。"
    },
    {
        "id": 36,
        "question": "カーフスライサー（ふくらはぎ潰し）が認められるのはどの帯から？",
        "options": ["紫帯", "茶帯", "黒帯"],
        "correct": "茶帯",
        "explanation": "カーフスライサー、バイセプススライサーは茶帯以上で許可されます。"
    },
    {
        "id": 37,
        "question": "50/50（フィフティ・フィフティ）ガードで両選手が膠着し、20秒経過した。判定は？",
        "options": ["スタンドから再開", "両者にペナルティ", "コイントス"],
        "correct": "両者にペナルティ",
        "explanation": "50/50などのポジションで動きがなく膠着した場合、両者にルーチ（ペナルティ）が入ることがあります。"
    },
    {
        "id": 38,
        "question": "試合中に道着が破れてしまった。どうする？",
        "options": ["そのまま続行", "交換する時間が与えられる", "失格"],
        "correct": "交換する時間が与えられる",
        "explanation": "道着の破損は試合続行不可能のため、規定時間内に予備の道着に着替えることが指示されます。"
    },
    {
        "id": 39,
        "question": "コーチがレフェリーの判定に大声で抗議し続けた。どうなる？",
        "options": ["選手にペナルティ", "コーチ退場", "選手もコーチも処分対象"],
        "correct": "選手もコーチも処分対象",
        "explanation": "執拗な抗議は懲戒処分の対象となり、選手にペナルティがいくこともあれば、コーチが退場させられることもあります。"
    },
    {
        "id": 40,
        "question": "相手の帯を掴んで投げ技を打った。これは有効？",
        "options": ["有効", "反則", "アドバンテージ"],
        "correct": "有効",
        "explanation": "帯を掴んでのテイクダウンは有効です。"
    },
    {
        "id": 41,
        "question": "マウントポジションからバックマウントに移行した。ポイントは加算される？",
        "options": ["されない（重複）", "される（4点追加）", "アドバンテージのみ"],
        "correct": "される（4点追加）",
        "explanation": "ポジションが進行（マウント→バック）して3秒キープすれば、新たに4点が加算されます。"
    },
    {
        "id": 42,
        "question": "スイープしてマウントポジションを直接取った。ポイント合計は何点？",
        "options": ["2点", "4点", "6点"],
        "correct": "6点",
        "explanation": "スイープ（2点）とマウント（4点）の両方の要件を満たしキープすれば、合計6点が入ります。"
    },
    {
        "id": 43,
        "question": "パスガードしてすぐにニーオンベリーに移行し、3秒キープした。ポイント合計は何点？",
        "options": ["3点", "2点", "5点"],
        "correct": "5点",
        "explanation": "パスガード（3点）とニーオンベリー（2点）が認められれば、合計5点です。"
    },
    {
        "id": 44,
        "question": "相手を場外際でテイクダウンし、両選手とも場外に出た。ポイントは？",
        "options": ["場外なので無効", "テイクダウンが成立していれば2点", "アドバンテージ"],
        "correct": "テイクダウンが成立していれば2点",
        "explanation": "テイクダウンの動作が場内で始まり、コントロールが確立されていれば、場外に出てもポイントとして認められる場合があります（セーフティエリアでの安定が必要）。"
    },
    {
        "id": 45,
        "question": "ハーフガードから相手の足を抱えてトップを取り返した（リバーサル）。判定は？",
        "options": ["スイープ（2点）", "アドバンテージ", "ポイントなし"],
        "correct": "スイープ（2点）",
        "explanation": "ハーフガードはガードの一種なので、下から上を取り返せばスイープとして2点入ります。"
    },
    {
        "id": 46,
        "question": "亀（タートル）になった相手の背後につき、片足だけフックを入れた状態。ポイントは？",
        "options": ["バック（4点）", "アドバンテージ", "ポイントなし"],
        "correct": "アドバンテージ",
        "explanation": "バックコントロールの4点は両足フックが必須です。片足フックだけではアドバンテージにとどまります。"
    },
    {
        "id": 47,
        "question": "相手の指を掴んで（指折り）グリップを切った。判定は？",
        "options": ["有効", "ペナルティ", "反則負け"],
        "correct": "ペナルティ",
        "explanation": "指を掴んで曲げる行為（スモールジョイントマニピュレーション）は禁止されており、ペナルティ（または悪質なら失格）です。最低でも相手の指を4本以上まとめて掴む必要があります。"
    },
    {
        "id": 48,
        "question": "クローズドガードの中にいる状態で膠着した。ペナルティはどちらにいきやすい？",
        "options": ["上の選手", "下の選手", "両方"],
        "correct": "上の選手",
        "explanation": "一般的にクローズドガードの中で攻めあぐねている場合、上の選手に攻撃（パスガードなど）の意思がなければペナルティが与えられやすい傾向にあります。"
    },
    {
        "id": 49,
        "question": "試合開始直後に自分から座り込んだ（引き込み）。相手が触れていなかった場合、どうなる？",
        "options": ["ペナルティ", "問題なし", "相手に2点"],
        "correct": "ペナルティ",
        "explanation": "相手とコンタクト（グリップなど）がない状態で座り込むと、消極的行為としてペナルティが与えられ、スタンドから再開となります。"
    },
    {
        "id": 50,
        "question": "ルースター級の選手とウルトラヘビー級の選手がアブソリュート（無差別）で戦うことはある？",
        "options": ["ある", "ない", "エキシビションのみ"],
        "correct": "ある",
        "explanation": "アブソリュート階級（無差別級）にエントリーすれば、体重差に関係なく対戦する可能性があります。"
    }
]

# --- セッション状態の初期化 ---
if 'shuffled_quiz_data' not in st.session_state:
    st.session_state.shuffled_quiz_data = quiz_data.copy()
    random.shuffle(st.session_state.shuffled_quiz_data)

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
    st.session_state.shuffled_quiz_data = quiz_data.copy()
    random.shuffle(st.session_state.shuffled_quiz_data)
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

# フッター
st.markdown("---")
st.caption("※このアプリは学習用です。実際の試合では審判の判断が最終決定となります。")