import React from 'react'

export default function TechPage({ techs, error }) {
  return (
    <main className="min-h-screen bg-gray-50 p-6 font-sans">
      <h1 className="text-3xl font-bold mb-6 text-gray-900">Catálogo de Tecnologías</h1>

      {error && (
        <div className="mb-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg text-yellow-800">
          Atención: {error}
        </div>
      )}

      {techs.length === 0 ? (
        <div className="bg-white rounded-xl shadow-sm p-12 text-center text-gray-500">
          No se encontraron tecnologías en el catálogo.
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {techs.map((t) => (
            <div key={t.tech_id || t.name} className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
              <strong className="text-lg text-gray-900">{t.name}</strong>
              {t.category && (
                <div className="text-sm text-blue-600 mt-1 font-medium">{t.category}</div>
              )}
              {t.final_score !== undefined && (
                <p className="text-sm text-gray-500 mt-2">Score base: {t.final_score}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </main>
  )
}

export async function getStaticProps() {
  let techs = []
  let error = null
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    const weightsJson = encodeURIComponent(JSON.stringify({ Escalabilidad: 1.0 }))
    const res = await fetch(`${apiUrl}/recommend-stack/?weights=${weightsJson}&limit=50`)
    if (res.ok) {
      const data = await res.json()
      techs = data.recommendations || []
    } else {
      error = 'No se pudo cargar el catálogo desde el servidor.'
    }
  } catch (err) {
    error = 'El servidor backend no está disponible en este momento.'
  }
  return { props: { techs, error }, revalidate: 60 }
}

