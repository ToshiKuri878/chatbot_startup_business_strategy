
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": st.secrets.AppSettings.chatbot_setting}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    # ユーザー入力を改行コードで分割
    user_message_lines = st.session_state["user_input"].split("\n") 
    user_message_content = "\n".join(user_message_lines) # 改行コードを維持

    user_message = {"role": "user", "content": user_message_content}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去

# ユーザーインターフェイスの構築
st.title("成長企業のリスクテイク戦略")
st.write("ChatGPT-4o (API)を使ったチャットボットです。")
st.write("※ ブラウザの自動翻訳機能を使用しないでください")
st.image("startup_business_strategy.png")
user_input = st.text_area("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
