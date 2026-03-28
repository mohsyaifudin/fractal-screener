from flask import Flask, render_template_string
import yfinance as yf
import pandas as pd

app = Flask(__name__)

def get_fractal_resistance(df):
    if len(df) < 6: return None
    for i in range(len(df) - 4, 2, -1):
        if (df['High'].iloc[i] > df['High'].iloc[i-1] and 
            df['High'].iloc[i] > df['High'].iloc[i-2] and 
            df['High'].iloc[i] > df['High'].iloc[i+1] and 
            df['High'].iloc[i] > df['High'].iloc[i+2]):
            return df['High'].iloc[i]
    return None

def cek_breakout(simbol):
    try:
        ticker = yf.Ticker(simbol)
        df = ticker.history(period="1mo", interval="1d")
        if df.empty or len(df) < 6: return None
        resistance = get_fractal_resistance(df)
        if resistance is None: return None
        
        high_hari_ini = df['High'].iloc[-1]
        close_hari_ini = df['Close'].iloc[-1]
        volume_hari_ini = df['Volume'].iloc[-1]
        high_kemarin = df['High'].iloc[-2]

        if high_hari_ini > resistance and high_kemarin <= resistance:
            if volume_hari_ini > 5000000:
                status = "CLOSE_ABOVE" if close_hari_ini > resistance else "HIGH_ONLY"
                return {"simbol": simbol, "status": status, "vol": volume_hari_ini, "res": resistance}
        return None
    except:
        return None

@app.route('/')
def home():
    # Daftar saham (saya perpendek untuk contoh, silakan masukkan semua list kamu di sini)
    saham_pilihan = ['BBCA.JK', 'BBRI.JK', 'TLKM.JK', 'ASII.JK', 'GOTO.JK', 'ANTM.JK'] 
    
    results = []
    for s in saham_pilihan:
        res = cek_breakout(s)
        if res: results.append(res)

    # Template HTML sederhana untuk menampilkan hasil
    html = """
    <html>
    <head><title>Stock Scanner</title></head>
    <body>
        <h1>📊 Hasil Screening Saham Hari Ini</h1>
        <table border="1">
            <tr><th>Simbol</th><th>Status</th><th>Volume</th><th>Resistance</th></tr>
            {% for r in results %}
            <tr>
                <td>{{ r.simbol }}</td>
                <td>{{ r.status }}</td>
                <td>{{ "{:,.0f}".format(r.vol) }}</td>
                <td>{{ r.res }}</td>
            </tr>
            {% endfor %}
        </table>
        {% if not results %}<p>Tidak ada saham yang breakout sesuai kriteria.</p>{% endif %}
    </body>
    </html>
    """
    return render_template_string(html, results=results)