import React from 'react'

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  render() {
    if (this.state.hasError) {
      return (
        <main style={{ padding: 24, fontFamily: 'Arial, sans-serif' }}>
          <h1 style={{ color: '#b33' }}>Algo salió mal</h1>
          <p>{this.state.error?.message || 'Error inesperado'}</p>
          <button
            onClick={() => this.setState({ hasError: false, error: null })}
            style={{
              padding: '8px 16px',
              marginTop: 16,
              cursor: 'pointer',
            }}
          >
            Reintentar
          </button>
        </main>
      )
    }
    return this.props.children
  }
}
