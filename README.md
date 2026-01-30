# HR Çalışma Süresi Analiz Sistemi (Esma)

Next.js frontend repo kökünde; backend `backend/` altında.

## Vercel'de deploy

1. Repoyu Vercel'e bağlayın (GitHub → Import Project).
2. Root Directory **boş bırakın** (kökte `package.json` var, Next.js otomatik algılanır).
3. Deploy edin.

## Yerel çalıştırma

- **Frontend:** `npm install && npm run dev` → http://localhost:3000
- **Backend:** `cd backend && pip install -r requirements.txt && uvicorn main:app --reload` → http://localhost:8000

**Backend bağlantısı:** Çalışan ekleme ve analiz oluşturma formlarının çalışması için backend'in çalışıyor olması ve frontend'in backend adresini bilmesi gerekir:

- **Yerel:** Proje kökünde `.env.local` içine `NEXT_PUBLIC_API_URL=http://localhost:8000` ekleyin.
- **Vercel:** Project → Settings → Environment Variables → `NEXT_PUBLIC_API_URL` = backend adresiniz (örn. `https://your-backend.onrender.com`).

Backend ayrıca deploy edilmelidir. **Adım adım:** [DEPLOY_BACKEND.md](./DEPLOY_BACKEND.md) dosyasına bakın (Render + PostgreSQL, ücretsiz tier). Sadece frontend Vercel'de ise API istekleri gidecek adres olmadığı için formlar çalışmaz; sitede "Backend bağlı değil" uyarısı görünür.
