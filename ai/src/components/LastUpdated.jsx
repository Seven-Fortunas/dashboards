export default function LastUpdated({ timestamp }) {
  if (!timestamp) return null

  const lastUpdate = new Date(timestamp)
  const nextUpdate = new Date(lastUpdate.getTime() + 6 * 60 * 60 * 1000) // +6 hours
  const formattedLast = lastUpdate.toLocaleString()
  const formattedNext = nextUpdate.toLocaleString()

  return (
    <div className="last-updated">
      <div>Last updated: {formattedLast}</div>
      <div>Next update: {formattedNext}</div>
    </div>
  )
}
