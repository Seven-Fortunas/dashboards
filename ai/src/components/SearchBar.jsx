export default function SearchBar({ value, onChange }) {
  return (
    <div className="search-bar">
      <label htmlFor="search-input" className="visually-hidden">Search</label>
      <input
        id="search-input"
        type="text"
        placeholder="Search updates..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="search-input"
      />
      {value && (
        <button
          onClick={() => onChange('')}
          className="clear-button"
          aria-label="Clear search"
        >
          ×
        </button>
      )}
    </div>
  )
}
