"use client";

import { useEffect, useState } from "react";
import { employeeApi, Employee, hasBackendUrl } from "@/lib/api";

export default function EmployeesPage() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [name, setName] = useState("");
  const [surname, setSurname] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState<{ type: "ok" | "err"; text: string } | null>(null);

  const fetchData = async () => {
    try {
      const data = await employeeApi.getAll();
      setEmployees(data || []);
    } catch (error) {
      console.error("Çalışanlar yüklenirken hata:", error);
      setEmployees([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !surname.trim()) {
      setMessage({ type: "err", text: "Ad ve soyad girin." });
      return;
    }
    setSubmitting(true);
    setMessage(null);
    try {
      const created = await employeeApi.create(name.trim(), surname.trim());
      if (created) {
        setName("");
        setSurname("");
        setMessage({ type: "ok", text: "Çalışan eklendi." });
        fetchData();
      } else {
        setMessage({ type: "err", text: "Backend'e bağlanılamadı. API URL ayarlandığından emin olun." });
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
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Çalışanlar</h1>

      {!hasBackendUrl() && (
        <div className="mb-6 p-4 bg-amber-50 border border-amber-200 rounded-lg text-amber-800">
          <strong>Backend bağlı değil.</strong> Çalışan eklemek ve analiz oluşturmak için backend&apos;i çalıştırıp Vercel ortam değişkeninde <code className="bg-amber-100 px-1 rounded">NEXT_PUBLIC_API_URL</code> ile backend adresini (örn. http://localhost:8000) ayarlayın.
        </div>
      )}

      {hasBackendUrl() && (
        <div className="card mb-8">
          <h2 className="text-xl font-semibold text-gray-700 mb-4">Yeni Çalışan Ekle</h2>
          <form onSubmit={handleSubmit} className="space-y-4 max-w-md">
            <div>
              <label className="label">Ad</label>
              <input
                type="text"
                className="input"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Ad"
              />
            </div>
            <div>
              <label className="label">Soyad</label>
              <input
                type="text"
                className="input"
                value={surname}
                onChange={(e) => setSurname(e.target.value)}
                placeholder="Soyad"
              />
            </div>
            {message && (
              <p className={message.type === "ok" ? "text-green-600 text-sm" : "text-red-600 text-sm"}>
                {message.text}
              </p>
            )}
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? "Ekleniyor..." : "Ekle"}
            </button>
          </form>
        </div>
      )}

      <div className="card">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Çalışan Listesi</h2>
        {employees.length === 0 ? (
          <p className="text-gray-500 text-center py-8">Henüz çalışan bulunmuyor.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ad</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Soyad</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {employees.map((e) => (
                  <tr key={e.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-gray-500">{e.id}</td>
                    <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">{e.name}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-700">{e.surname}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
