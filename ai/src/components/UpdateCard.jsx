export default function UpdateCard({ update }) {
  const date = update.published ? new Date(update.published).toLocaleDateString() : 'N/A'

  return (
    <div className="update-card">
      <div className="card-header">
        <span className="source-badge">{update.source}</span>
        <time className="date">{date}</time>
      </div>
      <h3 className="title">{update.title}</h3>
      {update.summary && (
        <p className="summary">{update.summary}</p>
      )}
      <a
        href={update.link}
        target="_blank"
        rel="noopener noreferrer"
        className="read-more"
      >
        Read more →
      </a>
    </div>
  )
}
