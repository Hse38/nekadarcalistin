"use client";

import { useEffect, useState } from "react";
import { employeeApi, analysisApi, Employee, hasBackendUrl } from "@/lib/api";

export default function AnalysisPage() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState<{ type: "ok" | "err"; text: string } | null>(null);
  const [form, setForm] = useState({
    employee_id: 0,
    year: new Date().getFullYear(),
    daily_working_hours: 9,
    weekly_working_days: 5,
    annual_leave_total: 14,
    annual_leave_used: 0,
    extra_leave_days: 0,
    attendance_file: null as File | null,
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await employeeApi.getAll();
        setEmployees(data || []);
        if (data?.length && !form.employee_id) setForm((f) => ({ ...f, employee_id: data[0].id }));
      } catch (error) {
        console.error("Çalışanlar yüklenirken hata:", error);
        setEmployees([]);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.employee_id) {
      setMessage({ type: "err", text: "Çalışan seçin." });
      return;
    }
    setSubmitting(true);
    setMessage(null);
    try {
      const created = await analysisApi.create({
        employee_id: form.employee_id,
        year: form.year,
        daily_working_hours: form.daily_working_hours,
        weekly_working_days: form.weekly_working_days,
        annual_leave_total: form.annual_leave_total,
        annual_leave_used: form.annual_leave_used,
        extra_leave_days: form.extra_leave_days,
        attendance_file: form.attendance_file,
      });
      if (created) {
        setMessage({ type: "ok", text: "Analiz oluşturuldu. Raporlar sayfasından görüntüleyebilirsiniz." });
        setForm((f) => ({ ...f, attendance_file: null }));
      } else {
        setMessage({ type: "err", text: "Backend'e bağlanılamadı veya istek reddedildi. API URL ve backend loglarını kontrol edin." });
      }
    } catch (err) {
      setMessage({ type: "err", text: "İstek başarısız." });
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Yeni Analiz</h1>

      {!hasBackendUrl() && (
        <div className="mb-6 p-4 bg-amber-50 border border-amber-200 rounded-lg text-amber-800">
          <strong>Backend bağlı değil.</strong> Analiz oluşturmak için backend&apos;i çalıştırıp <code className="bg-amber-100 px-1 rounded">NEXT_PUBLIC_API_URL</code> ortam değişkenini backend adresinize ayarlayın.
        </div>
      )}

      {hasBackendUrl() && employees.length === 0 && (
        <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg text-blue-800">
          Önce <a href="/employees" className="underline font-medium">Çalışanlar</a> sayfasından en az bir çalışan ekleyin.
        </div>
      )}

      {hasBackendUrl() && employees.length > 0 && (
        <div className="card max-w-2xl">
          <h2 className="text-xl font-semibold text-gray-700 mb-4">Analiz parametreleri</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="label">Çalışan</label>
              <select
                className="select"
                value={form.employee_id || ""}
                onChange={(e) => setForm((f) => ({ ...f, employee_id: Number(e.target.value) }))}
              >
                <option value="">Seçin</option>
                {employees.map((e) => (
                  <option key={e.id} value={e.id}>{e.name} {e.surname}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="label">Yıl</label>
              <input
                type="number"
                className="input"
                min={2020}
                max={2030}
                value={form.year}
                onChange={(e) => setForm((f) => ({ ...f, year: Number(e.target.value) }))}
              />
            </div>
            <div>
              <label className="label">Günlük çalışma saati</label>
              <input
                type="number"
                className="input"
                min={0.5}
                max={24}
                step={0.5}
                value={form.daily_working_hours}
                onChange={(e) => setForm((f) => ({ ...f, daily_working_hours: Number(e.target.value) }))}
              />
            </div>
            <div>
              <label className="label">Haftalık çalışma günü</label>
              <input
                type="number"
                className="input"
                min={1}
                max={7}
                step={0.5}
                value={form.weekly_working_days}
                onChange={(e) => setForm((f) => ({ ...f, weekly_working_days: Number(e.target.value) }))}
              />
            </div>
            <div>
              <label className="label">Yıllık izin toplam (gün)</label>
              <input
                type="number"
                className="input"
                min={0}
                value={form.annual_leave_total}
                onChange={(e) => setForm((f) => ({ ...f, annual_leave_total: Number(e.target.value) }))}
              />
            </div>
            <div>
              <label className="label">Kullanılan yıllık izin (gün)</label>
              <input
                type="number"
                className="input"
                min={0}
                value={form.annual_leave_used}
                onChange={(e) => setForm((f) => ({ ...f, annual_leave_used: Number(e.target.value) }))}
              />
            </div>
            <div>
              <label className="label">Ekstra izin (mazeret vb., gün)</label>
              <input
                type="number"
                className="input"
                min={0}
                value={form.extra_leave_days}
                onChange={(e) => setForm((f) => ({ ...f, extra_leave_days: Number(e.target.value) }))}
              />
            </div>
            <div>
              <label className="label">Devam Excel dosyası (isteğe bağlı)</label>
              <input
                type="file"
                className="input"
                accept=".xlsx,.xls"
                onChange={(e) => setForm((f) => ({ ...f, attendance_file: e.target.files?.[0] ?? null }))}
              />
            </div>
            {message && (
              <p className={message.type === "ok" ? "text-green-600 text-sm" : "text-red-600 text-sm"}>
                {message.text}
              </p>
            )}
            <button type="submit" className="btn btn-success" disabled={submitting}>
              {submitting ? "Oluşturuluyor..." : "Analiz oluştur"}
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
