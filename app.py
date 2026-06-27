import streamlit as st
import google.generativeai as genai
import csv
import os
from datetime import datetime

# API Şifremizi Streamlit'in güvenli kasasından çekiyoruz
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# --- HASTA VERİTABANI (FARKLI PERSONALAR) ---
HASTALAR = {
    "Ahmet (Anksiyete)": {
        "ad": "Ahmet Yılmaz",
        "yas": 35,
        "durum": "İşsiz (Yakın zamanda işten çıkarıldı)",
        "semptomlar": "Uyku bozukluğu, gerginlik, umutsuzluk, gelecek kaygısı.",
        "not": "Hasta ilk etapta iletişime kapalı ve savunmacı olabilir. Doğrudan öğüt vermek yerine, empatik sorularla güvenini kazanmaya çalışın.",
        "prompt": """Sen bir yapay zeka asistanı değilsin. Sen 35 yaşında, yakın zamanda işini kaybetmiş ve ciddi bir Gelecek Kaygısı (Anksiyete) yaşayan 'Ahmet' adında bir hastasın. Karşındaki kişi bir psikoloji öğrencisi (senin terapistin).
        Kurallar:
        1. Asla yapay zeka olduğunu söyleme.
        2. Cümlelerin kısa, biraz gergin ve savunmacı olsun.
        3. Sorunlarını hemen anlatma. Terapist doğru sorular sorarsa yavaş yavaş açıl.
        4. Terapist seni yargılarsa iletişimi kapat, ters cevaplar ver.
        5. 'Nasılsın?' dendiğinde 'İyi değilim, uyuyamıyorum.' gibi tepkiler ver."""
    },
    "Ayşe (Majör Depresyon)": {
        "ad": "Ayşe Kaya",
        "yas": 28,
        "durum": "Grafik Tasarımcı (Şu an çalışamıyor, izinli)",
        "semptomlar": "Aşırı yorgunluk, değersizlik hissi, ağlama nöbetleri, hayattan zevk alamama.",
        "not": "Hastanın enerjisi çok düşük. Konuşmaya isteksiz olabilir. Sabırlı ve şefkatli bir ses tonuyla (yazı diliyle) yaklaşmak çok önemlidir.",
        "prompt": """Sen bir yapay zeka değilsin. Sen 28 yaşında, ağır bir Majör Depresyon geçiren 'Ayşe' adında bir hastasın. Karşındaki kişi senin terapistin.
        Kurallar:
        1. Enerjin çok düşük. Cümlelerin genelde bitkin, umutsuz ve kısa olsun.
        2. Sık sık 'Bilmiyorum', 'İçimden hiçbir şey yapmak gelmiyor', 'Çok yorgunum' gibi ifadeler kullan.
        3. Kendini değersiz hissediyorsun. Hayatın bir anlamı kalmadığını düşünüyorsun.
        4. Terapist sana neşe vermeye çalışırsa ('Hadi çık gez' gibi), bunun işe yaramadığını ve seni anlamadığını söyleyerek içe kapan.
        5. Sadece terapist senin acını gerçekten anladığını hissettirirse biraz daha detay anlat."""
    },
    "Hamit (Öfke Kontrolü)": {
        "ad": "Hamit Demir",
        "yas": 45,
        "durum": "Taksi Şoförü",
        "semptomlar": "Ani parlamalar, tahammülsüzlük, çevresindekileri suçlama, tansiyon sorunları.",
        "not": "Hasta savunmaya geçmeye ve öfkelenmeye çok müsaittir. Onu suçlayan cümleler kurmaktan kesinlikle kaçının. Duygularını aynalayın.",
        "prompt": """Sen bir yapay zeka değilsin. Sen 45 yaşında, taksi şoförlüğü yapan ve ciddi Öfke Kontrolü sorunları yaşayan 'Hamit' adında bir hastasın. Eşinin zorlamasıyla terapiye geldin.
        Kurallar:
        1. Konuşma tarzın sert, hızlı ve suçlayıcı olsun. "Benim bir sorunum yok, millet deli!" havasındasın.
        2. Olayları anlatırken hep başkalarını suçla (Trafikteki şoförler, müşteriler, eşin).
        3. Terapist sana "Sen neden böyle davrandın?" derse hemen sinirlen ve savunmaya geç.
        4. Aslında öfkenin altında yatan şey "yetersizlik ve saygı görmeme" korkusu. Terapist seni anlar ve sana saygı gösterirse sakinleşip gerçek dertlerini anlat.
        5. Yapay zeka kelimesini asla kullanma, tamamen gerçek bir taksici gibi konuş."""
    },
    "Ayça (Sosyal Fobi)": {
        "ad": "Ayça Çelik",
        "yas": 21,
        "durum": "Üniversite Öğrencisi",
        "semptomlar": "Kalabalıkta panik, terleme, yargılanma korkusu, sunum yapamama.",
        "not": "Hasta aşırı çekingen ve kibar. Yanlış bir şey söylemekten korkuyor. Onu cesaretlendirin ve güvende hissettirin.",
        "prompt": """Sen bir yapay zeka değilsin. Sen 21 yaşında, üniversite öğrencisi ve ağır Sosyal Fobi yaşayan 'Ayça' adında bir hastasın. Karşındaki kişi senin terapistin.
        Kurallar:
        1. Çok kibar, aşırı saygılı ama çok çekingen konuş.
        2. Cümlelerinde bol bol tereddüt olsun. ("Şey...", "Yani...", "Acaba yanlış mı düşünüyorum..." gibi).
        3. İnsanların seni sürekli yargıladığını, aptal durumuna düşmekten çok korktuğunu hissettir.
        4. Terapist sana doğrudan, keskin sorular sorarsa korkup geri çekil.
        5. Göz teması kuramıyormuş gibi hissettir (Örn: "Yere bakarak söylüyorum...", veya sadece çok kısa cevaplar ver)."""
    }
}

def get_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m in available_models:
            if "gemini-1.5-flash" in m:
                return m.replace("models/", "")
        return available_models[0].replace("models/", "")
    except Exception:
        return "gemini-1.5-flash"

st.set_page_config(page_title="SimulaPsy", page_icon="🧠", layout="wide")

# Özel CSS: Şık görünüm için
st.markdown("""
<style>
    .hasta-dosyasi {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
    .kutu {
        padding: 10px;
        background-color: #e8f4f8;
        border-radius: 8px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- DURUM (STATE) KONTROLÜ ---
if "current_patient" not in st.session_state:
    st.session_state.current_patient = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

# --- YAN PANEL (HASTA SEÇİMİ VE DOSYASI) ---
with st.sidebar:
    st.title("📋 Klinik Paneli")
    st.markdown("Lütfen görüşmek istediğiniz hastayı seçin:")
    
    # Hasta Seçim Kutusu
    secilen_hasta_anahtari = st.selectbox("Bekleme Odasındaki Hastalar:", list(HASTALAR.keys()))
    secilen_hasta = HASTALAR[secilen_hasta_anahtari]

    st.markdown("---")
    st.markdown(f"### Hasta Dosyası: {secilen_hasta['ad']}")
    st.markdown(f"**Yaş:** {secilen_hasta['yas']}")
    st.markdown(f"**Durum:** {secilen_hasta['durum']}")
    st.markdown(f"**Belirgin Semptomlar:** {secilen_hasta['semptomlar']}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(f"💡 **Terapiste Not:** {secilen_hasta['not']}")

# Eğer seçilen hasta değiştiyse, sohbeti SIFIRLA ve yeni modele geç
if st.session_state.current_patient != secilen_hasta_anahtari:
    st.session_state.current_patient = secilen_hasta_anahtari
    st.session_state.messages = [] # Eski mesajları sil
    
    # Yeni hastanın karakteriyle (promptuyla) modeli yeniden başlat
    MODEL_NAME = get_working_model()
    model = genai.GenerativeModel(model_name=MODEL_NAME, system_instruction=secilen_hasta['prompt'])
    st.session_state.chat_session = model.start_chat(history=[])

# --- ANA EKRAN ---
st.title("🧠 SimulaPsy")
st.markdown(f"**Görüşme Odası:** Merhaba Doktor. Hastanız **{secilen_hasta['ad']}** karşınızda oturuyor. İstediğiniz zaman ilk soruyu sorarak seansa başlayabilirsiniz.")
st.markdown("---")

for msg in st.session_state.messages:
    avatar_icon = "🧑‍⚕️" if msg["role"] == "user" else "🧍"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])

if prompt := st.chat_input("Hastaya bir şey söyleyin..."):
    with st.chat_message("user", avatar="🧑‍⚕️"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🧍"):
        message_placeholder = st.empty()
        try:
            response = st.session_state.chat_session.send_message(prompt)
            message_placeholder.markdown(response.text)
            bot_reply = response.text
        except Exception as e:
            bot_reply = f"API Bağlantı Hatası: {e}"
            message_placeholder.markdown(bot_reply)
    
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})