import { navigationSections } from "./navigationItems";

type SidebarProps = {
  onLogout: () => void;
};

export function Sidebar({ onLogout }: SidebarProps) {
  return (
    <aside className="qwos-sidebar">
      <div className="qwos-sidebar-brand">
        <div className="qwos-brand-mark">Q</div>

        <div>
          <h1 className="qwos-brand-name">QWOS</h1>
          <p className="qwos-brand-subtitle">Quantum Workforce OS</p>
        </div>
      </div>

      <nav className="qwos-sidebar-nav">
        {navigationSections.map((section) => (
          <div key={section.title} className="qwos-nav-section">
            <p className="qwos-nav-section-title">{section.title}</p>

            <div className="qwos-nav-items">
              {section.items.map((item) => (
                <a
                  key={item.href}
                  href={item.href}
                  className={`qwos-nav-item ${
                    window.location.pathname === item.href
                      ? "qwos-nav-item-active"
                      : ""
                  }`} 
                >
                  <span className="qwos-nav-icon">{item.icon}</span>
                  <span>{item.label}</span>
                </a>
              ))}
            </div>
          </div>
        ))}
      </nav>

      <div className="qwos-sidebar-user">
        <div className="qwos-user-avatar">RB</div>

        <div className="qwos-user-details">
          <p className="qwos-user-name">Richard</p>
          <p className="qwos-user-role">Administrator</p>
        </div>

        <button
          type="button"
          className="qwos-logout-button"
          onClick={onLogout}
        >
          Sign out
        </button>
      </div>
    </aside>
  );
}