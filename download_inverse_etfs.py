import yfinance as yf
from datetime import datetime
import os

# 다운로드할 레버리지 인버스 ETF 목록
inverse_etfs = {
    # 2x 인버스
    'SDS': 'ProShares UltraShort S&P500 (SPY -2x)',
    'QID': 'ProShares UltraShort QQQ (QQQ -2x)',
    'DOG': 'ProShares UltraShort Dow30 (DIA -2x)',
    'RWM': 'ProShares UltraShort Russell2000 (IWM -2x)',
    
    # 3x 인버스
    'SPXU': 'ProShares UltraPro Short S&P500 (SPY -3x)',
    'SQQQ': 'ProShares UltraPro Short QQQ (QQQ -3x)',
    'SDOW': 'ProShares UltraPro Short Dow30 (DIA -3x)',
    'TZA': 'Direxion Daily Small Cap Bear 3X (IWM -3x)'
}

# 시작일 (3x ETF들이 2009년에 출시됨)
start_date = '2009-01-01'
end_date = datetime.now().strftime('%Y-%m-%d')

print("=" * 60)
print("레버리지 인버스 ETF 데이터 다운로드")
print("=" * 60)
print(f"기간: {start_date} ~ {end_date}")
print()

# 데이터 다운로드
for ticker, description in inverse_etfs.items():
    try:
        print(f"다운로드 중: {ticker} ({description})...", end=' ')
        
        # 데이터 다운로드
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        if len(data) > 0:
            # CSV 저장
            filename = f"{ticker}.csv"
            data.to_csv(filename)
            print(f"✅ 완료 ({len(data)} rows)")
        else:
            print(f"⚠️  데이터 없음")
            
    except Exception as e:
        print(f"❌ 오류: {e}")

print()
print("=" * 60)
print("다운로드 완료!")
print("=" * 60)

# 다운로드된 파일 목록 출력
print("\n다운로드된 파일:")
for ticker in inverse_etfs.keys():
    filename = f"{ticker}.csv"
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f"  📁 {filename} ({size:,} bytes)")
