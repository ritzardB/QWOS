type QuickAction = {
  label: string;
  description: string;
  icon: string;
};

const quickActions: QuickAction[] = [
  {
    label: "Add Employee",
    description: "Create a new workforce record",
    icon: "+",
  },
  {
    label: "Review Leave",
    description: "View pending leave requests",
    icon: "✓",
  },
  {
    label: "View Reports",
    description: "Open workforce reports",
    icon: "▤",
  },
];

export function QuickActions() {
  return (
    <section className="qwos-panel">
      <div className="qwos-panel-header">
        <div>
          <p className="qwos-panel-eyebrow">Actions</p>
          <h2 className="qwos-panel-title">Quick Actions</h2>
        </div>
      </div>

      <div className="qwos-action-list">
        {quickActions.map((action) => (
          <button
            key={action.label}
            type="button"
            className="qwos-action"
          >
            <span className="qwos-action-icon">{action.icon}</span>

            <span className="qwos-action-content">
              <span className="qwos-action-label">
                {action.label}
              </span>

              <span className="qwos-action-description">
                {action.description}
              </span>
            </span>

            <span className="qwos-action-arrow">→</span>
          </button>
        ))}
      </div>
    </section>
  );
}