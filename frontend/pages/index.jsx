import { useState } from 'react'
import { getRecommendations } from '../services/recommendation'

export default function Home() {
  const [escalabilidad, setEscalabilidad] = useState(8)
  const [facilidad, setFacilidad] = useState(8)
  const [ecosistema, setEcosistema] = useState(8)
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      const weights = { Escalabilidad: escalabilidad, Facilidad: facilidad, Ecosistema: ecosistema }
      const res = await getRecommendations(weights, 'MVP')
      setResults(res)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gray-50 p-6 font-sans">
      <h1 className="text-3xl font-bold mb-6 text-gray-900">Stack Recommender — Demo</h1>

      <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-sm p-6 max-w-md space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Escalabilidad: <span className="font-bold">{escalabilidad}</span>
          </label>
          <input
            type="range" min="1" max="10" value={escalabilidad}
            onChange={e => setEscalabilidad(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Facilidad: <span className="font-bold">{facilidad}</span>
          </label>
          <input
            type="range" min="1" max="10" value={facilidad}
            onChange={e => setFacilidad(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Ecosistema: <span className="font-bold">{ecosistema}</span>
          </label>
          <input
            type="range" min="1" max="10" value={ecosistema}
            onChange={e => setEcosistema(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <button
          type="submit" disabled={loading}
          className="w-full bg-blue-600 text-white font-medium py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Buscando...
            </span>
          ) : 'Recomendar'}
        </button>
      </form>

      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          Error: {error}
        </div>
      )}

      {results && (
        <section className="mt-6 max-w-2xl space-y-4">
          <h2 className="text-2xl font-semibold text-gray-900">Resultados</h2>
          {results.recommendations.map((r) => (
            <div key={r.name} className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
              <div className="flex items-center justify-between mb-2">
                <strong className="text-lg text-gray-900">{r.name}</strong>
                <span className="bg-blue-100 text-blue-800 text-sm font-medium px-3 py-1 rounded-full">
                  Score: {r.final_score}
                </span>
              </div>
              {r.category && (
                <p className="text-sm text-gray-500 mb-2">{r.category}</p>
              )}
              <pre className="text-sm text-gray-700 whitespace-pre-wrap bg-gray-50 p-3 rounded-lg">
                {r.justification}
              </pre>
            </div>
          ))}
        </section>
      )}
    </main>
  )
}
