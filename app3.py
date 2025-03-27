
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": st.secrets.AppSettings.chatbot_setting}
        ]

# 入力欄をクリアするためのコールバック関数
def clear_text_input():
    st.session_state.user_input = ""

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state.messages
    user_message = {"role": "user", "content": st.session_state.user_input}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    # コールバック関数を使用して入力欄をクリア
    clear_text_input()

# ユーザーインターフェイスの構築
st.title("成長企業のリスクテイク戦略")
st.write("ChatKKK:ChatGPT-4o (API)を使ったチャットボットです。")
st.write("※ ブラウザの自動翻訳機能を使用しないでください")
st.image("startup_business_strategy.png")

user_input = st.text_area("メッセージを入力してください。", key="user_input")
if st.button("送信", on_click=communicate):  # 送信ボタンにコールバック関数を割り当て
    pass  # ボタンクリック時の処理はcommunicate()関数で実行される

if st.session_state.messages:
    messages = st.session_state.messages
    for message in reversed(messages[1:]):
        speaker = "🙂" if message["role"] == "user" else "🤖"
        st.write(speaker + ": " + message["content"])
