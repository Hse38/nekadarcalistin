"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { analysisApi, employeeApi, Analysis, Employee } from "@/lib/api";

export default function ReportDetailPage() {
  const params = useParams();
  const id = typeof params.id === "string" ? parseInt(params.id, 10) : NaN;
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    if (!id || isNaN(id)) {
      setNotFound(true);
      setLoading(false);
      return;
    }
    const fetchData = async () => {
      try {
        const [a, empList] = await Promise.all([
          analysisApi.getById(id),
          employeeApi.getAll(),
        ]);
        setAnalysis(a ?? null);
        setEmployees(empList || []);
        if (!a) setNotFound(true);
      } catch (error) {
        console.error("Rapor yüklenirken hata:", error);
        setNotFound(true);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id]);

  const getEmployeeName = (employeeId: number) => {
    const e = employees.find((x) => x.id === employeeId);
    return e ? `${e.name} ${e.surname}` : "Bilinmiyor";
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (notFound || !analysis) {
    return (
      <div>
        <h1 className="text-3xl font-bold text-gray-800 mb-8">Rapor bulunamadı</h1>
        <p className="text-gray-600">Belirtilen analiz raporu mevcut değil.</p>
        <a href="/reports" className="mt-4 inline-block text-blue-600 hover:underline">← Raporlara dön</a>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Rapor Detayı</h1>
      <div className="card space-y-4">
        <p><span className="font-semibold text-gray-700">Çalışan:</span> {getEmployeeName(analysis.employee_id)}</p>
        <p><span className="font-semibold text-gray-700">Yıl:</span> {analysis.year}</p>
        <p><span className="font-semibold text-gray-700">Teorik saat:</span> {analysis.theoretical_hours.toFixed(1)}</p>
        <p><span className="font-semibold text-gray-700">Gerçek saat:</span> {analysis.actual_hours.toFixed(1)}</p>
        <p>
          <span className="font-semibold text-gray-700">Verimlilik:</span>{" "}
          <span
            className={`inline-flex px-2 py-1 text-sm font-semibold rounded-full ${
              analysis.efficiency_percentage >= 90 ? "bg-green-100 text-green-800" :
              analysis.efficiency_percentage >= 70 ? "bg-yellow-100 text-yellow-800" :
              "bg-red-100 text-red-800"
            }`}
          >
            {analysis.efficiency_percentage.toFixed(1)}%
          </span>
        </p>
      </div>
      <a href="/reports" className="mt-6 inline-block text-blue-600 hover:underline">← Raporlara dön</a>
    </div>
  );
}
