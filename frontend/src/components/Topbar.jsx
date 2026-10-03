import {
  Bell,
  Search,
  Radio,
  ChevronDown
} from "lucide-react";


function Topbar() {

  return (
    <header className="topbar">

      <div>

        <div className="topbar-title">
          Supply Chain Command Center
        </div>

        <div className="topbar-subtitle">
          Real-time intelligence & decision optimization
        </div>

      </div>


      <div className="topbar-actions">

        <div className="live-pill">
          <Radio size={14} />
          LIVE
        </div>


        <div className="search-box">

          <Search size={17} />

          <input
            placeholder="Search shipments, factories..."
          />

        </div>


        <button className="icon-button">
          <Bell size={19} />
          <span className="notification-dot"></span>
        </button>


        <div className="profile">

          <div className="avatar">
            CT
          </div>

          <div>
            <strong>Operations</strong>
            <span>Control Room</span>
          </div>

          <ChevronDown size={15} />

        </div>

      </div>

    </header>
  );
}

export default Topbar;