export default function SourceFilter({ sources, selected, onChange }) {
  return (
    <div className="source-filter">
      <label htmlFor="source-select">Filter by source:</label>
      <select
        id="source-select"
        value={selected}
        onChange={(e) => onChange(e.target.value)}
        className="filter-select"
      >
        {sources.map(source => (
          <option key={source} value={source}>
            {source === 'all' ? 'All Sources' : source}
          </option>
        ))}
      </select>
    </div>
  )
}
