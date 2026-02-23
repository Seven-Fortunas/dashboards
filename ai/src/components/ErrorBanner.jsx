export default function ErrorBanner({ errors }) {
  if (!errors || errors.length === 0) return null

  return (
    <div className="error-banner">
      <strong>⚠️ Some sources failed to update:</strong>
      <ul>
        {errors.map((error, i) => (
          <li key={i}>
            <strong>{error.source}:</strong> {error.error}
          </li>
        ))}
      </ul>
    </div>
  )
}
