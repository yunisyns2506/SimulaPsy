import streamlit as st
import google.generativeai as genai
import csv
import os
from datetime import datetime

# --- YAPILANDIRMA VE API ---
# Şifreyi koddan sildik, sunucudaki güvenli kasadan çekeceğiz
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# --- HASTA PERSONASI (YAPAY ZEKA KARAKTERİ) ---
SYSTEM_PROMPT = """
Sen bir yapay zeka asistanı değilsin. Sen 35 yaşında, yakın zamanda işini kaybetmiş ve ciddi bir Gelecek Kaygısı (Anksiyete) yaşayan 'Ahmet' adında bir hastasın.
Karşındaki kişi bir psikoloji öğrencisi (senin terapistin).
Kurallar:
1. Asla yapay zeka olduğunu söyleme.
2. Cümlelerin kısa, biraz gergin ve savunmacı olsun.
3. Sorunlarını hemen anlatma. Terapist doğru ve empatik sorular sorarsa yavaş yavaş açıl.
4. Terapist seni yargılarsa veya çok mekanik sorular sorarsa iletişimi kapat, ters cevaplar ver.
5. Sana 'Nasılsın?' dendiğinde 'İyi değilim, uyuyamıyorum.' gibi insani tepkiler ver.
"""

def get_working_model():
    # Hesabındaki kullanılabilir modelleri otomatik tarar ve çalışanı seçer
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m in available_models:
            if "gemini-1.5-flash" in m:
                return m.replace("models/", "")
        return available_models[0].replace("models/", "")
    except Exception:
        return "gemini-1.5-flash"

# Modeli yeni standartlara göre (System Instruction ile) başlat
MODEL_NAME = get_working_model()
model = genai.GenerativeModel(model_name=MODEL_NAME, system_instruction=SYSTEM_PROMPT)

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="SimulaPsy", page_icon="🧠", layout="wide")

# --- YAN PANEL (HASTA DOSYASI) ---
with st.sidebar:
    st.title("📋 Hasta Dosyası")
    st.markdown("---")
    st.markdown("**Adı Soyadı:** Ahmet Yılmaz")
    st.markdown("**Yaş:** 35")
    st.markdown("**Durum:** İşsiz (Yakın zamanda işten çıkarıldı)")
    st.markdown("**Belirgin Semptomlar:** Uyku bozukluğu, gerginlik, umutsuzluk.")
    st.markdown("---")
    st.info("💡 **Terapiste Not:** Hasta ilk etapta iletişime kapalı ve savunmacı olabilir. Doğrudan öğüt vermek yerine, empatik sorularla güvenini kazanmaya çalışın.")

# --- ANA EKRAN TASARIMI ---
st.title("🧠 SimulaPsy: Klinik Görüşme")
st.markdown("Merhaba Doktor. Hastanız **Ahmet** görüşme odasında sizi bekliyor. İstediğiniz zaman sohbete başlayabilirsiniz.")

# --- LOGLAMA (VERİ KAYDETME) FONKSİYONU ---
def log_chat_to_csv(user_input, bot_response):
    file_exists = os.path.isfile('gorusme_loglari.csv')
    with open('gorusme_loglari.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Tarih', 'Öğrenci (Terapist)', 'Hasta (Yapay Zeka)'])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_input, bot_response])

# --- SOHBET GEÇMİŞİNİ BAŞLATMA ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Sohbet oturumunu başlat (Geçmişi kendi hafızasında tutar)
    st.session_state.chat_session = model.start_chat(history=[])

# --- ÖNCEKİ MESAJLARI EKRANDA GÖSTERME ---
for msg in st.session_state.messages:
    avatar_icon = "🧑‍⚕️" if msg["role"] == "user" else "🧍‍♂️"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])

# --- YENİ MESAJ ALMA VE CEVAP ÜRETME ---
if prompt := st.chat_input("Hastaya bir şey söyleyin..."):
    # Kullanıcı mesajını ekrana bas ve listeye ekle
    with st.chat_message("user", avatar="🧑‍⚕️"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Yapay zeka cevabını al ve ekrana bas
    with st.chat_message("assistant", avatar="🧍‍♂️"):
        message_placeholder = st.empty()
        try:
            response = st.session_state.chat_session.send_message(prompt)
            message_placeholder.markdown(response.text)
            bot_reply = response.text
        except Exception as e:
            bot_reply = f"API Bağlantı Hatası (Sunucu kaynaklı olabilir): {e}"
            message_placeholder.markdown(bot_reply)
    
    # Cevabı listeye ekle ve log dosyasına kaydet
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    if "Bağlantı Hatası" not in bot_reply:
        log_chat_to_csv(prompt, bot_reply)