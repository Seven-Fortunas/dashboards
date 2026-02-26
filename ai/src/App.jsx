import { useState, useEffect } from 'react'
import UpdateCard from './components/UpdateCard'
import SourceFilter from './components/SourceFilter'
import SearchBar from './components/SearchBar'
import ErrorBanner from './components/ErrorBanner'
import LastUpdated from './components/LastUpdated'
import './styles/dashboard.css'

function App() {
  const [updates, setUpdates] = useState([])
  const [filteredUpdates, setFilteredUpdates] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedSource, setSelectedSource] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [lastUpdated, setLastUpdated] = useState(null)
  const [errorSources, setErrorSources] = useState([])

  useEffect(() => {
    fetch('./data/cached_updates.json')
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch data')
        return res.json()
      })
      .then(data => {
        // Staleness check: 7 days = 168 hours
        const lastUpdate = new Date(data.last_updated)
        const now = new Date()
        const hoursDiff = (now - lastUpdate) / (1000 * 60 * 60)

        if (hoursDiff > 168) {
          setError(`Data is stale (last updated ${Math.floor(hoursDiff / 24)} days ago)`)
        }

        setUpdates(data.updates || [])
        setFilteredUpdates(data.updates || [])
        setLastUpdated(data.last_updated)
        setErrorSources(data.errors || [])
        setLoading(false)
      })
      .catch(err => {
        console.error('Error loading updates:', err)
        setError(err.message)
        setLoading(false)
      })
  }, [])

  useEffect(() => {
    let filtered = updates

    // Filter by source
    if (selectedSource !== 'all') {
      filtered = filtered.filter(u => u.source === selectedSource)
    }

    // Filter by search term
    if (searchTerm) {
      const term = searchTerm.toLowerCase()
      filtered = filtered.filter(u =>
        u.title?.toLowerCase().includes(term) ||
        u.summary?.toLowerCase().includes(term)
      )
    }

    setFilteredUpdates(filtered)
  }, [selectedSource, searchTerm, updates])

  if (loading) {
    return <div className="loading">Loading AI updates...</div>
  }

  if (error) {
    return (
      <div className="dashboard">
        <header className="dashboard-header">
          <h1>🤖 AI Advancements Dashboard</h1>
        </header>
        <ErrorBanner errors={[{ source: 'Dashboard', message: error }]} />
      </div>
    )
  }

  const sources = ['all', ...new Set(updates.map(u => u.source))]

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>🤖 AI Advancements Dashboard</h1>
        <p className="subtitle">Latest developments in artificial intelligence</p>
        <LastUpdated timestamp={lastUpdated} />
      </header>

      {errorSources.length > 0 && <ErrorBanner errors={errorSources} />}

      <div className="controls">
        <SearchBar value={searchTerm} onChange={setSearchTerm} />
        <SourceFilter
          sources={sources}
          selected={selectedSource}
          onChange={setSelectedSource}
        />
      </div>

      <div className="results-info">
        Showing {filteredUpdates.length} of {updates.length} updates
      </div>

      <div className="updates-grid">
        {filteredUpdates.map((update, i) => (
          <UpdateCard key={i} update={update} />
        ))}
      </div>

      {filteredUpdates.length === 0 && (
        <div className="no-results">
          No updates found matching your criteria
        </div>
      )}
    </div>
  )
}

export default App
