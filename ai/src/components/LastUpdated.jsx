export default function LastUpdated({ timestamp }) {
  if (!timestamp) return null

  const date = new Date(timestamp)
  const formatted = date.toLocaleString()

  return (
    <div className="last-updated">
      Last updated: {formatted}
    </div>
  )
}
