# Backend deploy rehberi (Render)

Backend’i [Render](https://render.com) üzerinde ücretsiz deploy etmek için aşağıdaki adımları izleyin. Render ücretsiz planda 15 dakika işlem yoksa uyur; ilk istek 30–60 saniye sürebilir.

---

## 1. Render hesabı ve repo bağlantısı

1. [render.com](https://render.com) → **Get Started** → GitHub ile giriş yapın.
2. **Dashboard** → **New +** → **Web Service**.
3. **Connect a repository** ile `Hse38/nekadarcalistin` (veya kendi reponuz) bağlayın. Repo görünmüyorsa **Configure account** ile Render’a repo erişimi verin.

---

## 2. Web Service ayarları

| Ayar | Değer |
|------|--------|
| **Name** | `esma-backend` (veya istediğiniz isim) |
| **Region** | Frankfurt (veya size yakın) |
| **Branch** | `master` |
| **Root Directory** | `backend` |
| **Runtime** | Python |
| **Build Command** | `pip install --upgrade pip setuptools wheel && pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

---

## 3. Veritabanı (PostgreSQL)

Render’da backend kalıcı veri için PostgreSQL kullanın (ücretsiz tier var).

1. **Dashboard** → **New +** → **PostgreSQL**.
2. **Name:** `esma-db`, **Region:** Web Service ile aynı, **Create Database**.
3. Açılan sayfada **Internal Database URL**’i kopyalayın (örn. `postgresql://user:pass@host/dbname`).

Sonra Web Service’e dönün:

4. **Environment** bölümünde **Add Environment Variable**:
   - **Key:** `DATABASE_URL`
   - **Value:** Az önce kopyaladığınız PostgreSQL URL.

---

## 4. Build hatası alırsanız (metadata-generation-failed)

Render loglarında `metadata-generation-failed` veya `Encountered error while generating package metadata` görürseniz:

1. **Build Command** alanını şu şekilde güncelleyin (Dashboard → Service → Settings → Build & Deploy):
   ```text
   pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
   ```
2. **Save Changes** → **Manual Deploy** → **Deploy latest commit** ile tekrar deneyin.

Bu komut pip ve build araçlarını günceller; çoğu metadata hatası böyle çözülür.

---

## 5. Deploy

1. **Create Web Service** (veya **Save Changes**) tıklayın.
2. İlk deploy 2–5 dakika sürebilir. **Logs** sekmesinden ilerlemeyi takip edin.
3. Bittiğinde sağ üstte backend URL’iniz çıkar, örn: `https://esma-backend.onrender.com`.

---

## 5. Frontend’e backend adresini verme (Vercel)

1. [Vercel](https://vercel.com) → Projeniz → **Settings** → **Environment Variables**.
2. **Add**:
   - **Name:** `NEXT_PUBLIC_API_URL`
   - **Value:** Backend URL’iniz (**sonunda / olmadan**), örn: `https://esma-backend.onrender.com`
3. **Save** → **Redeploy** (Deployments → son deploy → ⋮ → Redeploy).

Bundan sonra sitedeki formlar bu backend’e istek atar.

---

## Özet kontrol listesi

- [ ] Render’da Web Service oluşturuldu, **Root Directory** = `backend`
- [ ] **Build Command:** `pip install --upgrade pip setuptools wheel && pip install -r requirements.txt`
- [ ] **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] PostgreSQL oluşturuldu, **DATABASE_URL** Web Service env’e eklendi
- [ ] Vercel’de **NEXT_PUBLIC_API_URL** = backend URL (örn. `https://esma-backend.onrender.com`)
- [ ] Vercel’de redeploy yapıldı

---

## Alternatif: Railway

1. [railway.app](https://railway.app) → GitHub ile giriş → **New Project** → **Deploy from GitHub** → reponuzu seçin.
2. Servisi seçin → **Settings** → **Root Directory:** `backend`.
3. **Variables** → `DATABASE_URL` ekleyin (Railway’de **Postgres** ekleyip otomatik gelen URL’i kullanın).
4. **Deploy**; çıkan public URL’i Vercel’de `NEXT_PUBLIC_API_URL` olarak ayarlayın.

Start komutu Railway’de genelde otomatik bulunur; bulunmazsa: `uvicorn main:app --host 0.0.0.0 --port $PORT`.
