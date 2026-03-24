# Çok Kaynaklı RSS Feed Üretici

17 kaynaktan otomatik RSS feed üretir. GitHub Actions ile saatte bir güncellenir.

## Üretilen Feed'ler

| Dosya | Kaynak |
|---|---|
| `feeds/bddk_basin.xml` | BDDK Basın Duyuruları |
| `feeds/bddk_mevzuat.xml` | BDDK Mevzuat Duyuruları |
| `feeds/bddk_rg_kurul.xml` | BDDK Resmi Gazete Kurul Kararları |
| `feeds/bddk_rg_disi.xml` | BDDK Resmi Gazete Dışı Kurul Kararları |
| `feeds/bddk_dergi.xml` | BDDK Bankacılık Dergisi |
| `feeds/kvkk_duyurular.xml` | KVKK Duyurular |
| `feeds/rekabet_guncel.xml` | Rekabet Kurumu Güncel |
| `feeds/isbank_haberler.xml` | İş Bankası Haberler |
| `feeds/isbank_ozel_durum.xml` | İş Bankası Özel Durum Açıklamaları |
| `feeds/kgk_duyurular.xml` | KGK Duyurular |
| `feeds/kgk_son_yayinlar.xml` | KGK Son Yayımlanlar |
| `feeds/kgk_tezler.xml` | KGK Uzmanlık Tezleri |
| `feeds/dkbp_yaptirim.xml` | DKBP İdari Yaptırım |
| `feeds/tcmb_basin.xml` | TCMB Basın Duyuruları |
| `feeds/tbb_dergi.xml` | TBB Bankacılar Dergisi |
| `feeds/tbb_kitaplar.xml` | TBB Kitaplar |
| `feeds/tbb_duyurular.xml` | TBB Duyurular |

## Kurulum (5 dakika)

### 1. Yerel test
```bash
pip install requests beautifulsoup4 feedgen
python scraper.py
```

### 2. GitHub'a yükle
1. Yeni bir **public** GitHub repo oluştur
2. Bu dosyaları yükle
3. **Settings → Pages** → Source: `main` branch → Save
4. İlk çalıştırma için: **Actions** sekmesi → "RSS Feed Güncelle" → "Run workflow"

### 3. RSS URL'lerin
```
https://<kullanici>.github.io/<repo>/feeds/bddk_mevzuat.xml
https://<kullanici>.github.io/<repo>/feeds/kvkk_duyurular.xml
# ... vb.
```

## Notlar
- **TBB ve TCMB** bazı IP'lerden bot koruması uygulayabilir. İlk testte ⚠️ uyarısı alırsan normal.
- **DKBP** robots.txt kısıtlaması nedeniyle erişilemeyebilir.
- KGK sayfaları JavaScript render gerektiriyorsa boş dönebilir.
- Sorunlu siteler için script hata vermez, sadece uyarı basar ve devam eder.
