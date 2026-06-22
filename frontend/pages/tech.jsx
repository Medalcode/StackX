import React from 'react'

export default function TechPage({ techs, sanityConfigured }) {
  return (
    <main className="min-h-screen bg-gray-50 p-6 font-sans">
      <h1 className="text-3xl font-bold mb-6 text-gray-900">Tecnologías (desde Sanity/GROQ)</h1>

      {!sanityConfigured && (
        <div className="mb-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg text-yellow-800">
          SANITY_PROJECT_ID no configurado. Define variables de entorno para ver contenido real.
        </div>
      )}

      {techs.length === 0 ? (
        <div className="bg-white rounded-xl shadow-sm p-12 text-center text-gray-500">
          No se encontraron tecnologías.
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {techs.map((t) => (
            <div key={t._id || t.name} className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
              <strong className="text-lg text-gray-900">{t.name}</strong>
              {t.category?.name && (
                <div className="text-sm text-gray-500 mt-1">{t.category.name}</div>
              )}
              {t.description && (
                <p className="text-sm text-gray-700 mt-2">{t.description}</p>
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
  let sanityConfigured = !!process.env.SANITY_PROJECT_ID
  if (sanityConfigured) {
    try {
      const client = require('../lib/groqClient')
      const query = '*[_type == "technology"]{_id, name, description, category->{name}}'
      techs = await client.fetch(query)
    } catch (err) {
      console.error('GROQ fetch error', err)
      techs = []
    }
  }
  return { props: { techs, sanityConfigured }, revalidate: 60 }
}
