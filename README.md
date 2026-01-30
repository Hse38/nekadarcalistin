# HR Çalışma Süresi Analiz Sistemi (Esma)

Next.js frontend repo kökünde; backend `backend/` altında.

## Vercel'de deploy

1. Repoyu Vercel'e bağlayın (GitHub → Import Project).
2. Root Directory **boş bırakın** (kökte `package.json` var, Next.js otomatik algılanır).
3. Deploy edin.

## Yerel çalıştırma

- **Frontend:** `npm install && npm run dev` → http://localhost:3000
- **Backend:** `cd backend && pip install -r requirements.txt && uvicorn main:app --reload` → http://localhost:8000

Frontend, backend API için `NEXT_PUBLIC_API_URL` (örn. `http://localhost:8000`) tanımlanabilir.
