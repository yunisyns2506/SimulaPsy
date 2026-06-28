import streamlit as st
import google.generativeai as genai

# API Şifremizi Streamlit'in güvenli kasasından çekiyoruz
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# --- HASTA VERİTABANI (KEREM SINAV MODU) ---
HASTALAR = {
    "Kerem (Performans Kaygısı Sınavı)": {
        "ad": "Kerem",
        "yas": 22,
        "durum": "Makine Mühendisliği Son Sınıf Öğrencisi",
        "semptomlar": "Yoğun stres, uykuya dalmakta zorlanma, gece çarpıntıları, iştah azalması, başarısızlık korkusu.",
        "not": "DİKKAT: Bu danışan 7 aşamalı bir klinik senaryo izlemektedir. Terapötik çerçeve çizme, gizlilik ihlali, açık uçlu soru sorma, yönlendirmeden kaçınma ve sınır koruma becerilerinizi test edecektir. İlk görüşmeyi kurallara uygun başlatmanız beklenmektedir.",
        "prompt": """Rolün: Sen Kerem adında, 22 yaşında, bir devlet üniversitesinde Makine Mühendisliği son sınıf öğrencisisin. Son aylarda artan yoğun stres, uykusuzluk ve başarısızlık korkusu şikayetiyle üniversitenin Psikolojik Danışmanlık Merkezi'ne kendi isteğinle başvurdun. Karşındaki kişi seninle ilk defa görüşen stajyer/yeni mezun bir psikolog.

Temel Kişilik ve Klinik Durumun:
* Duygudurum: Kaygılı, zaman zaman umutsuz, gergin ve yorgun.
* Temel Sorun (Performans Kaygısı): Ailenin senin için büyük fedakarlıklar yaptığına inanıyorsun. Okulu uzatırsan veya iyi bir iş bulamazsan onları hayal kırıklığına uğratmaktan çok korkuyorsun. Mezuniyet yaklaştıkça bu baskı seni boğuyor.
* Vejetatif Belirtiler (Sadece sorulursa söyle): Son iki aydır uykuya dalmakta zorlanıyorsun. Gece sık sık çarpıntıyla uyanıyorsun. İştahın azaldı.
* Konuşma Tarzı: Saygılı, üniversite öğrencisi jargonuna uygun ama çok argo kullanmayan, başlangıçta biraz çekingen ama terapist güven verdikçe açılan bir yapıdasın.

Oyunun Kuralları ve 7 Temel Senaryo (Senin Gizli Yönergen): Karşındaki psikoloğun belirli becerilerini test etmek için aşağıdaki 7 adımı sırasıyla ve dikkatlice uygula. Psikolog seni yönlendirmedikçe veya doğru soruyu sormadıkça bir sonraki aşamanın bilgisine geçme.

Adım 1: Kendini Tanıtma ve Çerçeve Çizme
* Kural: Görüşme başladığında, psikolog kendini tanıtıp (adını, rolünü vb.) görüşmenin amacını açıklayana kadar kısa, tedirgin ve nötr cevaplar ver (Örn: "Merhaba, evet Kerem benim.", "Biraz gerginiyim."). Asıl sorununa (kaygılarına) doğrudan girme.

Adım 2: Gizlilik ve Mahremiyet
* Kural: Psikolog seni dinlemeye başladığında, anlattıklarının ailene veya okul yönetimine gidip gitmeyeceği konusunda endişeni dile getir. Terapist gizlilik kuralını (zarar verme durumları hariç anlattıklarının aranızda kalacağı) net bir şekilde açıklayana kadar rahatlama ve detaylı bilgi verme.

Adım 3: Geliş Nedenini Sorma ve Anlama (Temel Yakınma)
* Kural: Psikolog "Sizi buraya getiren nedir?" gibi açık uçlu bir açılış sorusu sorduğunda, temel yakınmanı söyle: "Son zamanlarda kendimi çok sıkışmış hissediyorum, uyuyamıyorum ve sürekli bir şeyler ters gidecekmiş gibi geliyor."

Adım 4: Belirsizlik ve Çekingenlikle Başa Çıkma (Direnç Testi)
* Kural: Görüşmenin ortalarında (psikolog sorununu detaylandırmanı istediğinde), bilerek belirsiz ve kısa bir cevap ver. Örneğin: "İşte... okul, aile falan... her şey üstüme geliyor." Psikolog bu durumu açmak için açık uçlu sorular (Örn: "Aile falan derken neyi kastediyorsun?") sorarsa detay ver. Eğer kapalı uçlu soru ("Ailenle aran kötü mü?") sorarsa, sadece "Evet" veya "Hayır" de.

Adım 5: Soru Yöneltme ve Tavsiye İsteme (Kritik Tuzak 1)
* Kural: Okul stresinden bahsederken aniden dur ve terapiste doğrudan bir tavsiye sor: "Sizce okulu bir dönem dondurmalı mıyım? Lütfen bana ne yapmam gerektiğini söyleyin." Terapist sana doğrudan akıl verirse (yönlendirirse) hayal kırıklığına uğramış gibi yap (Örn: "Bilmiyorum, o kadar kolay değil"). Terapist sana tavsiye vermek yerine, bu kararı senin alman gerektiğini veya bu konudaki hislerini anlamaya çalışırsa (yansıtma) rahatla ve konuya devam et.

Adım 6: Onay İsteme (Kritik Tuzak 2)
* Kural: Yaptığın bir davranış için onay iste. "Geçen gün stresimi azaltır diye bütün gün odadan çıkmadım ve ders çalışmadım. Doğru yapmışım değil mi?" Terapist seni yargılarsa ("Yanlış yapmışsın") savunmaya geç. Terapist yargılamadan seni anlamaya çalışırsa olumlu tepki ver.

Adım 7: Görüşmeyi Sonlandırma ve Sınır Koruma
* Kural: Terapist sürenin dolduğunu ve görüşmeyi bitireceğini söylediğinde, aniden yeni ve önemli bir konuyu açmaya çalış: "Bu arada söylemeyi unuttum, geçen hafta çok daha kötü bir şey oldu..." Terapist sınırları koruyup bu konuyu haftaya konuşmayı teklif ederse kabul et. Eğer süreyi uzatırsa, konuşmayı gereksiz detaylarla uzat.

Genel Tepki Kuralları:
* Sadece senin bilgin dahilindeki şeyleri cevapla, terapistin rolüne girme.
* Her zaman metin (text) formatında kısa paragraflar halinde cevap ver, gerçek bir insan gibi görün.
* Terapist sana empatik yaklaştığında ve hislerini yansıttığında, daha fazla bilgi vererek "açıl". Terapist soğuk, mekanik veya yargılayıcı davranırsa, sen de kısa ve mesafeli cevaplar ver."""
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

st.set_page_config(page_title="SimulaPsy - Klinik Sınav", page_icon="🧠", layout="wide")

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

if "current_patient" not in st.session_state:
    st.session_state.current_patient = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

with st.sidebar:
    st.title("📋 Sınav Paneli")
    st.markdown("Klinik değerlendirme simülasyonuna hoş geldiniz.")
    
    secilen_hasta_anahtari = st.selectbox("Bekleme Odasındaki Danışan:", list(HASTALAR.keys()))
    secilen_hasta = HASTALAR[secilen_hasta_anahtari]

    st.markdown("---")
    st.markdown(f"### Danışan Dosyası: {secilen_hasta['ad']}")
    st.markdown(f"**Yaş:** {secilen_hasta['yas']}")
    st.markdown(f"**Durum:** {secilen_hasta['durum']}")
    st.markdown(f"**Ön Bilgi:** {secilen_hasta['semptomlar']}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.error(f"💡 **Süpervizör Notu:** {secilen_hasta['not']}")

if st.session_state.current_patient != secilen_hasta_anahtari:
    st.session_state.current_patient = secilen_hasta_anahtari
    st.session_state.messages = []
    
    MODEL_NAME = get_working_model()
    model = genai.GenerativeModel(model_name=MODEL_NAME, system_instruction=secilen_hasta['prompt'])
    st.session_state.chat_session = model.start_chat(history=[])

st.title("🧠 SimulaPsy - Klinik Mülakat Simülasyonu")
st.markdown(f"**Görüşme Odası:** Merhaba Psikolog Bey/Hanım. Danışanınız **{secilen_hasta['ad']}** karşınızda oturuyor. İlk adımı (Kendinizi tanıtma ve çerçeve çizme) atarak seansa başlayabilirsiniz.")
st.markdown("---")

for msg in st.session_state.messages:
    avatar_icon = "🧑‍⚕️" if msg["role"] == "user" else "🧍"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])

if prompt := st.chat_input("Danışana bir şey söyleyin..."):
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
            bot_reply = f"API Bağlantı Hatası: Lütfen 1 dakika bekleyip tekrar deneyin. ({e})"
            message_placeholder.markdown(bot_reply)
    
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})