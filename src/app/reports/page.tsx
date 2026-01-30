"use client";

import { useEffect, useState } from "react";
import { analysisApi, employeeApi, Analysis, Employee } from "@/lib/api";

export default function ReportsPage() {
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [analysesData, employeesData] = await Promise.all([
          analysisApi.getAll(),
          employeeApi.getAll(),
        ]);
        setAnalyses(analysesData || []);
        setEmployees(employeesData || []);
      } catch (error) {
        console.error("Veri yüklenirken hata:", error);
        setAnalyses([]);
        setEmployees([]);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

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

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Raporlar</h1>
      <p className="text-gray-600 mb-6">Tüm analiz raporları.</p>
      <div className="card">
        {analyses.length === 0 ? (
          <p className="text-gray-500 text-center py-8">Henüz rapor bulunmuyor.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Çalışan</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Yıl</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Teorik Saat</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Gerçek Saat</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Verimlilik</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">İşlem</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {analyses.map((a) => (
                  <tr key={a.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">{getEmployeeName(a.employee_id)}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-500">{a.year}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-500">{a.theoretical_hours.toFixed(1)}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-500">{a.actual_hours.toFixed(1)}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          a.efficiency_percentage >= 90 ? "bg-green-100 text-green-800" :
                          a.efficiency_percentage >= 70 ? "bg-yellow-100 text-yellow-800" :
                          "bg-red-100 text-red-800"
                        }`}
                      >
                        {a.efficiency_percentage.toFixed(1)}%
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <a href={`/reports/${a.id}`} className="text-blue-600 hover:underline">Detay</a>
                    </td>
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
