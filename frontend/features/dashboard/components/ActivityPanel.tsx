export function ActivityPanel() {
  return (
    <section className="qwos-panel">
      <div className="qwos-panel-header">
        <div>
          <p className="qwos-panel-eyebrow">Overview</p>
          <h2 className="qwos-panel-title">
            Recent Activity
          </h2>
        </div>
      </div>

      <div className="qwos-empty-state">
        <div className="qwos-empty-icon">◷</div>

        <h3>No activity yet</h3>

        <p>
          Workforce activity will appear here once QWOS begins
          processing real operational data.
        </p>
      </div>
    </section>
  );
}