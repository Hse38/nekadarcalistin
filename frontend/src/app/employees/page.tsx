"use client";

import { useEffect, useState } from "react";
import { employeeApi, Employee } from "@/lib/api";

export default function EmployeesPage() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
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
    fetchData();
  }, []);

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
      <p className="text-gray-600 mb-6">
        Çalışan listesi. Yeni çalışan eklemek için backend API kullanılır.
      </p>
      <div className="card">
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
