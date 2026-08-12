import React, { useState } from 'react'

export default function ComparePage() {
  const [weightsA, setWeightsA] = useState({ Escalabilidad: 0.9, Facilidad: 0.3 })
  const [weightsB, setWeightsB] = useState({ Escalabilidad: 0.3, Facilidad: 0.9 })
  const [stackA, setStackA] = useState(null)
  const [stackB, setStackB] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleCompare = async () => {
    setLoading(true)
    setError(null)
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

    try {
      const [resA, resB] = await Promise.all([
        fetch(`${apiUrl}/recommend-stack/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ weights: weightsA, proyecto: 'Opción A' }),
        }),
        fetch(`${apiUrl}/recommend-stack/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ weights: weightsB, proyecto: 'Opción B' }),
        }),
      ])

      if (resA.ok && resB.ok) {
        const dataA = await resA.json()
        const dataB = await resB.json()
        setStackA(dataA.recommendations || [])
        setStackB(dataB.recommendations || [])
      } else {
        setError('Error al obtener recomendaciones para la comparación.')
      }
    } catch (err) {
      setError('El servidor backend no está disponible.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-slate-900 text-white p-6 font-sans">
      <header className="max-w-6xl mx-auto mb-8 border-b border-slate-800 pb-4">
        <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400">
          Comparador Side-by-Side de Arquitecturas
        </h1>
        <p className="text-slate-400 mt-2">
          Contraste dos perfiles de prioridades para evaluar cuál stack se adapta mejor a sus objetivos técnicos.
        </p>
      </header>

      <section className="max-w-6xl mx-auto grid md:grid-cols-2 gap-6 mb-8">
        <div className="bg-slate-800/80 p-6 rounded-xl border border-slate-700">
          <h2 className="text-lg font-bold text-blue-400 mb-4">Opción A: Enfoque Escalabilidad</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-slate-300">Escalabilidad ({weightsA.Escalabilidad})</label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={weightsA.Escalabilidad}
                onChange={(e) => setWeightsA({ ...weightsA, Escalabilidad: parseFloat(e.target.value) })}
                className="w-full accent-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm text-slate-300">Facilidad ({weightsA.Facilidad})</label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={weightsA.Facilidad}
                onChange={(e) => setWeightsA({ ...weightsA, Facilidad: parseFloat(e.target.value) })}
                className="w-full accent-blue-500"
              />
            </div>
          </div>
        </div>

        <div className="bg-slate-800/80 p-6 rounded-xl border border-slate-700">
          <h2 className="text-lg font-bold text-indigo-400 mb-4">Opción B: Enfoque Velocidad MVP</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-slate-300">Escalabilidad ({weightsB.Escalabilidad})</label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={weightsB.Escalabilidad}
                onChange={(e) => setWeightsB({ ...weightsB, Escalabilidad: parseFloat(e.target.value) })}
                className="w-full accent-indigo-500"
              />
            </div>
            <div>
              <label className="block text-sm text-slate-300">Facilidad ({weightsB.Facilidad})</label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={weightsB.Facilidad}
                onChange={(e) => setWeightsB({ ...weightsB, Facilidad: parseFloat(e.target.value) })}
                className="w-full accent-indigo-500"
              />
            </div>
          </div>
        </div>
      </section>

      <div className="max-w-6xl mx-auto text-center mb-10">
        <button
          onClick={handleCompare}
          disabled={loading}
          className="px-8 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold rounded-xl shadow-lg transition-all"
        >
          {loading ? 'Calculando Matriz...' : 'Ejecutar Comparación Side-by-Side'}
        </button>
      </div>

      {error && (
        <div className="max-w-6xl mx-auto mb-6 p-4 bg-red-900/50 border border-red-700 rounded-xl text-red-200 text-center">
          {error}
        </div>
      )}

      {stackA && stackB && (
        <section className="max-w-6xl mx-auto grid md:grid-cols-2 gap-6">
          <div className="bg-slate-800 p-6 rounded-xl border border-blue-500/30">
            <h3 className="text-xl font-bold text-blue-400 mb-4">Stack Recomendado (Opción A)</h3>
            <div className="space-y-4">
              {stackA.map((item, i) => (
                <div key={i} className="p-4 bg-slate-900/60 rounded-lg border border-slate-700">
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-bold text-slate-200">{item.name}</span>
                    <span className="text-xs bg-blue-900/60 text-blue-300 px-2 py-1 rounded">Score: {item.final_score}</span>
                  </div>
                  <p className="text-xs text-slate-400 mt-2">{item.justification}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-800 p-6 rounded-xl border border-indigo-500/30">
            <h3 className="text-xl font-bold text-indigo-400 mb-4">Stack Recomendado (Opción B)</h3>
            <div className="space-y-4">
              {stackB.map((item, i) => (
                <div key={i} className="p-4 bg-slate-900/60 rounded-lg border border-slate-700">
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-bold text-slate-200">{item.name}</span>
                    <span className="text-xs bg-indigo-900/60 text-indigo-300 px-2 py-1 rounded">Score: {item.final_score}</span>
                  </div>
                  <p className="text-xs text-slate-400 mt-2">{item.justification}</p>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}
    </main>
  )
}
