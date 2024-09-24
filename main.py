import os
import ccxt
import numpy as np
import pandas as pd
import mplfinance as mpf
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO

# صرافی بایننس
exchange = ccxt.binance()

# ترتیب تایم‌فریم‌ها
timeframes = ['15m', '30m', '1h', '2h', '4h', '1d']
symbols = ['BTC/USDT', 'TLM/USDT','SCRT/USDT', 'ATA/USDT', 'AVA/USDT', 'MINA/USDT', 'LINA/USDT', 'OM/USDT', 'RSR/USDT', 'SEI/USDT', 'AI/USDT', 'WLD/USDT', 'SHIB/USDT', 'SNX/USDT', 'MBL/USDT', 'LIT/USDT', 'GMT/USDT', 'PYR/USDT', 'SFP/USDT', 'ROSE/USDT', 'AVAX/USDT', 'REN/USDT', 'TFUEL/USDT', 'AMB/USDT', 'ETC/USDT', 'HARD/USDT', 'DGB/USDT', 'RVN/USDT', 'OCEAN/USDT', 'GRT/USDT', 'DYDX/USDT', 'WIN/USDT', 'ZEC/USDT', 'SUN/USDT', 'ERN/USDT', 'XAI/USDT', 'VOXEL/USDT', 'XMR/USDT', 'BAT/USDT', 'SXP/USDT', 'IOST/USDT', 'SYS/USDT', 'YGG/USDT', 'TRB/USDT', 'CVX/USDT', 'ILV/USDT', 'LQTY/USDT', 'TIA/USDT', 'ADA/USDT', 'OXT/USDT', 'APT/USDT', 'PHA/USDT', 'REQ/USDT', 'ID/USDT', 'IMX/USDT', 'SSV/USDT', 'MAGIC/USDT', 'FLOW/USDT', 'DATA/USDT', 'ORDI/USDT', 'ICX/USDT', 'XRP/USDT', 'BTC/USDT', 'LOKA/USDT', 'MANA/USDT', 'HFT/USDT', 'ANKR/USDT', 'RPL/USDT', 'KAVA/USDT', 'ETH/USDT', 'USDC/USDT', 'VANRY/USDT', 'AGIX/USDT', 'BURGER/USDT', 'ALPHA/USDT', 'GLM/USDT', 'PIXEL/USDT', 'KMD/USDT', 'LOOM/USDT', 'DYM/USDT', 'BAND/USDT', 'XEC/USDT', 'BULL/USDT', 'COMBO/USDT', 'BSV/USDT', 'BLUR/USDT', 'KLAY/USDT', 'TRU/USDT', 'PEPE/USDT', 'KSM/USDT', 'CHZ/USDT', 'ETHDOWN/USDT', 'LUNC/USDT', 'SKL/USDT', 'OGN/USDT', 'HIFI/USDT', 'SOL/USDT', 'ACH/USDT', 'ALPINE/USDT', 'FIDA/USDT', 'REEF/USDT', 'OMG/USDT', 'FET/USDT', 'ATOM/USDT', 'BICO/USDT', 'AUDIO/USDT', 'DASH/USDT', 'AERGO/USDT', 'JTO/USDT', 'VIDT/USDT', 'EOS/USDT', 'CELR/USDT', 'LRC/USDT', 'CLV/USDT', 'ENS/USDT', 'GTC/USDT', 'CFX/USDT', 'ONT/USDT', 'DEGO/USDT', 'EDU/USDT', 'COTI/USDT', 'GAL/USDT', 'CYBER/USDT', '1INCH/USDT', 'EPX/USDT', 'DEXE/USDT', 'ZEN/USDT', 'ASTR/USDT', 'FTM/USDT', 'GAS/USDT', 'QKC/USDT', 'NEO/USDT', 'CKB/USDT', 'OSMO/USDT', 'NFP/USDT', 'KNC/USDT', 'POLYX/USDT', 'UNI/USDT', 'JUP/USDT', 'BCH/USDT', 'POLS/USDT', 'LSK/USDT', 'QI/USDT', 'API3/USDT', 'DCR/USDT', 'RAY/USDT', 'BAL/USDT', 'AUCTION/USDT', 'CAKE/USDT', 'SUPER/USDT', 'ETHUP/USDT', 'HBAR/USDT', 'XEM/USDT', 'TRX/USDT', 'THETA/USDT', 'FXS/USDT', 'STG/USDT', 'CHR/USDT', 'LTO/USDT', 'BSW/USDT', 'JST/USDT', 'NTRN/USDT', 'NKN/USDT', 'AKRO/USDT', 'IOTX/USDT', 'VET/USDT', 'BTCDOWN/USDT', 'DODO/USDT', 'RENDER/USDT', 'AXS/USDT', 'MTL/USDT', 'GNS/USDT', 'SUI/USDT', 'UNFI/USDT', 'DIA/USDT', 'FRONT/USDT', 'HNT/USDT', 'LPT/USDT', 'PAXG/USDT', 'AGLD/USDT', 'RDNT/USDT', 'GLMR/USDT', 'WBTC/USDT', 'CRV/USDT', 'KDA/USDT', 'LDO/USDT', 'FORTH/USDT', 'HIGH/USDT', 'MAV/USDT', 'AAVE/USDT', 'QUICK/USDT', 'FTT/USDT', 'MANTA/USDT', 'MC/USDT', 'FIL/USDT', 'ALGO/USDT', 'ENJ/USDT', 'ICP/USDT', 'JASMY/USDT', 'NMR/USDT', 'STRK/USDT', 'USTC/USDT', 'SLP/USDT', 'EGLD/USDT', 'DOGE/USDT', 'ARPA/USDT', 'RLC/USDT', 'BONK/USDT', 'PEOPLE/USDT', 'MOVR/USDT', 'ADX/USDT', 'GMX/USDT', 'ACE/USDT', 'BOND/USDT', 'COMP/USDT', 'PUNDIX/USDT', 'PROM/USDT', 'ONE/USDT', 'YFI/USDT', 'PYTH/USDT', 'DUSK/USDT', 'WAXP/USDT', 'MASK/USDT', 'ZIL/USDT', 'XNO/USDT', 'CREAM/USDT', 'T/USDT', 'ARB/USDT', 'WOO/USDT', 'UMA/USDT', 'TWT/USDT', 'DENT/USDT', 'WAVES/USDT', 'LINK/USDT', 'AR/USDT', 'STORJ/USDT', 'FLUX/USDT', 'PERP/USDT', 'MEME/USDT', 'PENDLE/USDT', 'C98/USDT', 'STX/USDT', 'APE/USDT', 'AMP/USDT', 'GFT/USDT', 'LUNA/USDT', 'CTSI/USDT', 'ARKM/USDT', 'FLOKI/USDT', 'RUNE/USDT', 'MKR/USDT', 'ALT/USDT', 'LTC/USDT', 'WRX/USDT', 'USDP/USDT', 'XTZ/USDT', 'ELF/USDT', 'SAND/USDT', 'BLZ/USDT', 'PORTAL/USDT', 'IOTA/USDT', 'POND/USDT', 'BNB/USDT', 'NEAR/USDT', 'INJ/USDT', 'ORN/USDT', 'BTT/USDT', 'UTK/USDT', 'DAR/USDT', 'ALICE/USDT', 'CELO/USDT', 'QNT/USDT', 'XLM/USDT', 'MATIC/USDT', 'SYN/USDT', 'OP/USDT', 'BTCUP/USDT', 'SUSHI/USDT', 'ZRX/USDT', 'DOT/USDT']

# اطلاعات ایمیل از متغیرهای محیطی
SENDER_EMAIL = os.getenv("EMAIL_SENDER")
RECEIVER_EMAIL = os.getenv("EMAIL_RECEIVER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(subject, body, attachments=[]):
    message = MIMEMultipart()
    message["From"] = EMAIL_SENDER
    message["To"] = EMAIL_RECEIVER
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    for filename, attachment in attachments:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.getvalue())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={filename}")
        message.attach(part)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, message.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

def get_ohlcv(symbol, timeframe):
    # دریافت داده‌های OHLCV
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
    return np.array(ohlcv)

def find_downward_trend(peaks):
    # چک کردن اینکه آیا سه قله به صورت نزولی هستند و یک خط ترند دقیق را تشکیل می‌دهند
    if len(peaks) < 3:
        return False
    return peaks[0][1] > peaks[1][1] > peaks[2][1]

def find_peaks(data):
    peaks = []
    for i in range(1, len(data) - 1):
        high = data[i][2]  # نوک شادوی بالای کندل (high)
        prev_high = data[i-1][2]
        next_high = data[i+1][2]
        
        # چک کردن قله (Peak)
        if high > prev_high and high > next_high:
            peaks.append((i, high))
            
        # نگه داشتن فقط سه قله آخر نزولی
        if len(peaks) > 3:
            peaks.pop(0)
            
    return peaks

def check_trend_break(data, peaks):
    # چک کردن شکست خط ترند و عدم پولبک
    trendline_slope = (peaks[2][1] - peaks[0][1]) / (peaks[2][0] - peaks[0][0])
    trendline_intercept = peaks[0][1] - trendline_slope * peaks[0][0]
    
    # بررسی شکسته شدن خط ترند
    for i in range(peaks[2][0], len(data)):
        high = data[i][2]  # نوک شادوی کندل‌های بعدی
        trend_value = trendline_slope * i + trendline_intercept
        if high > trend_value:
            # شکست اتفاق افتاده
            # حالا باید مطمئن شویم که پولبکی هنوز به خط ترند نزده
            for j in range(i + 1, len(data)):
                low = data[j][3]  # نوک شادوی پایین (low)
                if low <= trend_value:
                    return False  # پولبک زده، موقعیت مناسب نیست
            return True  # پولبک نزده، موقعیت مناسب است
    return False

def plot_chart_with_trendline(symbol, timeframe, data, peaks, candle_count):
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    
    # محاسبه و رسم خط روند
    trendline_slope = (peaks[2][1] - peaks[0][1]) / (peaks[2][0] - peaks[0][0])
    trendline_intercept = peaks[0][1] - trendline_slope * peaks[0][0]

    # تولید نمودار
    df_subset = df.tail(candle_count)
    
    # محاسبه x_vals و y_vals برای خط روند
    x_vals = np.arange(peaks[0][0], peaks[2][0] + 1)  # +1 برای اطمینان از اینکه آخرین نقطه در محدوده است
    y_vals = trendline_slope * x_vals + trendline_intercept

    # تنظیمات رسم نمودار
    fig, axlist = mpf.plot(df_subset, type='candle', volume=True, style='yahoo', returnfig=True)

    ax = axlist[0]
    ax.set_yscale('log')  # استفاده از مقیاس لگاریتمی
    # رسم خط روند به صورت خط چین
    ax.plot(df.index[x_vals[x_vals < len(df_subset)]], y_vals[x_vals < len(df_subset)], color='red', linewidth=2, linestyle='--', label='Trendline')
    ax.legend()

    # اضافه کردن عنوان به تصویر
    ax.text(0.05, 0.95, f"{symbol}, {timeframe}, {candle_count} candles", transform=ax.transAxes,
            fontsize=12, verticalalignment='top', horizontalalignment='left', bbox=dict(facecolor='white', alpha=0.5))

    # ذخیره نمودار در حافظه به صورت باینری
    image_stream = BytesIO()
    fig.savefig(image_stream, dpi=100, bbox_inches="tight")
    image_stream.seek(0)
    
    return image_stream

# لیست برای جمع‌آوری پیوست‌های ایمیل
all_attachments = []
email_body = ""

for symbol in symbols:
    for timeframe in timeframes:
        try:
            data = get_ohlcv(symbol, timeframe)
            peaks = find_peaks(data)
            if len(peaks) == 3 and find_downward_trend(peaks):
                if check_trend_break(data, peaks):
                    # رسم نمودار تایم‌فریم اصلی
                    if timeframe in ['15m', '30m']:
                        candle_count = 50
                    elif timeframe == '1h':
                        candle_count = 100
                    elif timeframe in ['2h', '4h']:
                        candle_count = 150
                    elif timeframe == '1d':
                        candle_count = 250

                    chart_image = plot_chart_with_trendline(symbol, timeframe, data, peaks, candle_count)
                    filename = f"{symbol.replace('/', '_')}, {timeframe}, {candle_count} candles.png"
                    all_attachments.append((filename, chart_image))

                    # به‌دست آوردن تایم‌فریم پایین‌تر
                    lower_timeframe_idx = max(0, timeframes.index(timeframe) - 1)
                    lower_tf = timeframes[lower_timeframe_idx]
                    lower_data = get_ohlcv(symbol, lower_tf)
                    lower_peaks = find_peaks(lower_data)

                    # تعیین تعداد کندل‌ها برای تایم‌فریم پایین‌تر
                    if lower_tf in ['15m', '30m']:
                        candle_count = 100
                    elif lower_tf == '1h':
                        candle_count = 150
                    elif lower_tf in ['2h', '4h']:
                        candle_count = 250
                    elif lower_tf == '1d':
                        candle_count = 250

                    # رسم نمودار برای تایم‌فریم پایین‌تر
                    lower_chart_image = plot_chart_with_trendline(symbol, lower_tf, lower_data, lower_peaks, candle_count)
                    lower_filename = f"{symbol.replace('/', '_')}, {lower_tf}, {candle_count} candles.png"
                    all_attachments.append((lower_filename, lower_chart_image))

                    # به‌روزرسانی محتوای ایمیل
                    email_body += f"Found a downward trendline break for {symbol} on {timeframe} timeframe.\n"
                    email_body += f"Main chart: {filename}\n"
                    email_body += f"Lower timeframe chart: {lower_filename}\n"
        
        except Exception as e:
            print(f"Error processing {symbol} on {timeframe}: {e}")

# ارسال ایمیل با تمام پیوست‌ها
if all_attachments:
    email_body += "\nPlease find the attached charts."
    send_email("Downward Trendline Breaks Detected", email_body, all_attachments)
else:
    print("No valid trendline breaks found.")
