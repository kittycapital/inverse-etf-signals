import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import os

print("=" * 60)
print("Inverse ETF Volume Spike Dashboard - Data Update")
print("=" * 60)
print(f"Update Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 기초 자산
base_assets = ['SPY', 'QQQ', 'DIA', 'IWM']

# 레버리지 인버스 ETF
inverse_etfs = {
    # 2x 인버스
    'SDS': 'ProShares UltraShort S&P500',
    'QID': 'ProShares UltraShort QQQ',
    'DOG': 'ProShares UltraShort Dow30',
    'RWM': 'ProShares UltraShort Russell2000',
    
    # 3x 인버스
    'SPXU': 'ProShares UltraPro Short S&P500',
    'SQQQ': 'ProShares UltraPro Short QQQ',
    'SDOW': 'ProShares UltraPro Short Dow30',
    'TZA': 'Direxion Daily Small Cap Bear 3X'
}

# 시작일 설정
start_date = '2009-01-01'  # 3x ETF 출시 이후
end_date = datetime.now().strftime('%Y-%m-%d')

def download_and_save(ticker, description, output_filename):
    """데이터 다운로드 및 저장"""
    try:
        print(f"Downloading {ticker} ({description})...", end=' ')
        
        # 데이터 다운로드
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        if len(data) > 0:
            # 필요한 컬럼만 선택하고 재정렬
            data = data[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
            
            # 인덱스를 Date 컬럼으로 변환
            data.reset_index(inplace=True)
            data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
            
            # 컬럼 순서 재정렬
            data = data[['Date', 'Close', 'High', 'Low', 'Open', 'Volume']]
            
            # 저장
            data.to_csv(output_filename, index=False)
            print(f"✅ {len(data)} rows")
            return True
        else:
            print(f"⚠️  No data")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# 기초 자산 다운로드
print("📊 Downloading Base Assets...")
print("-" * 60)
for asset in base_assets:
    download_and_save(asset, f"{asset} ETF", f"{asset}.csv")

print()

# 인버스 ETF 다운로드
print("📉 Downloading Inverse ETFs...")
print("-" * 60)
for ticker, description in inverse_etfs.items():
    download_and_save(ticker, description, f"{ticker}_cleaned.csv")

print()
print("=" * 60)
print("✅ Data Update Complete!")
print("=" * 60)

# 업데이트 로그 생성
with open('last_update.txt', 'w') as f:
    f.write(f"Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
    f.write(f"Assets: {', '.join(base_assets)}\n")
    f.write(f"Inverse ETFs: {', '.join(inverse_etfs.keys())}\n")

print("\n📝 Update log saved to last_update.txt")
