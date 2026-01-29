"use client";

import { useEffect, useState } from "react";
import { analysisApi, employeeApi, Analysis, Employee } from "@/lib/api";

export default function HomePage() {
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
    const employee = employees.find((e) => e.id === employeeId);
    return employee?.name || "Bilinmiyor";
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
      <h1 className="text-3xl font-bold text-gray-800 mb-8">
        HR Çalışma Süresi Analiz Sistemi
      </h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="card bg-gradient-to-r from-blue-500 to-blue-600 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-100">Toplam Çalışan</p>
              <p className="text-3xl font-bold mt-2">{employees.length}</p>
            </div>
            <svg
              className="w-12 h-12 text-blue-200"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
              />
            </svg>
          </div>
        </div>

        <div className="card bg-gradient-to-r from-green-500 to-green-600 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100">Toplam Analiz</p>
              <p className="text-3xl font-bold mt-2">{analyses.length}</p>
            </div>
            <svg
              className="w-12 h-12 text-green-200"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
              />
            </svg>
          </div>
        </div>

        <div className="card bg-gradient-to-r from-purple-500 to-purple-600 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-100">Ortalama Verimlilik</p>
              <p className="text-3xl font-bold mt-2">
                {analyses.length > 0
                  ? (
                      analyses.reduce((acc, a) => acc + a.efficiency_percentage, 0) /
                      analyses.length
                    ).toFixed(1)
                  : 0}
                %
              </p>
            </div>
            <svg
              className="w-12 h-12 text-purple-200"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
              />
            </svg>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Hızlı İşlemler</h2>
        <div className="flex gap-4">
          <a
            href="/employees"
            className="btn bg-blue-600 hover:bg-blue-700 text-white"
          >
            <svg
              className="w-5 h-5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 6v6m0 0v6m0-6h6m-6 0H6"
              />
            </svg>
            Yeni Çalışan Ekle
          </a>
          <a
            href="/analysis"
            className="btn bg-green-600 hover:bg-green-700 text-white"
          >
            <svg
              className="w-5 h-5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            Yeni Analiz Oluştur
          </a>
        </div>
      </div>

      {/* Recent Analyses */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Son Analizler</h2>
        {analyses.length === 0 ? (
          <p className="text-gray-500 text-center py-8">
            Henüz analiz bulunmuyor. Yeni bir analiz oluşturmak için{" "}
            <a href="/analysis" className="text-blue-600 hover:underline">
              buraya tıklayın
            </a>
            .
          </p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Çalışan
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Yıl
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Teorik Saat
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Gerçek Saat
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Verimlilik
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    İşlemler
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {analyses.slice(0, 5).map((analysis) => (
                  <tr key={analysis.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="font-medium text-gray-900">
                        {getEmployeeName(analysis.employee_id)}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-500">
                      {analysis.year}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-500">
                      {analysis.theoretical_hours.toFixed(1)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-500">
                      {analysis.actual_hours.toFixed(1)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          analysis.efficiency_percentage >= 90
                            ? "bg-green-100 text-green-800"
                            : analysis.efficiency_percentage >= 70
                            ? "bg-yellow-100 text-yellow-800"
                            : "bg-red-100 text-red-800"
                        }`}
                      >
                        {analysis.efficiency_percentage.toFixed(1)}%
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <a
                        href={`/reports/${analysis.id}`}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        Detay
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        {analyses.length > 5 && (
          <div className="mt-4 text-center">
            <a href="/reports" className="text-blue-600 hover:underline">
              Tüm analizleri görüntüle →
            </a>
          </div>
        )}
      </div>
    </div>
  );
}
