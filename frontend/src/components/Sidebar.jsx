import { NavLink } from "react-router-dom";

import {
  LayoutDashboard,
  Truck,
  Factory,
  Boxes,
  Sparkles,
  FlaskConical,
  History,
  Network
} from "lucide-react";


function Sidebar() {

  const links = [
    {
      path: "/",
      name: "Command Center",
      icon: LayoutDashboard
    },
    {
      path: "/shipments",
      name: "Shipments",
      icon: Truck
    },
    {
      path: "/factories",
      name: "Factories",
      icon: Factory
    },
    {
      path: "/suppliers",
      name: "Suppliers",
      icon: Boxes
    },
    {
      path: "/what-if",
      name: "What-If Simulator",
      icon: FlaskConical
    },
    {
      path: "/rewind",
      name: "Rewind Engine",
      icon: History
    }
  ];


  return (
    <aside className="sidebar">

      <div className="brand">

        <div className="brand-icon">
          <Network size={23} />
        </div>

        <div>
          <h2>ChainTwin</h2>
          <span>AI CONTROL SYSTEM</span>
        </div>

      </div>


      <div className="sidebar-section">
        OPERATIONS
      </div>


      <nav>

        {links.map((link) => {

          const Icon = link.icon;

          return (

            <NavLink
              key={link.path}
              to={link.path}
              className={({ isActive }) =>
                isActive
                  ? "nav-item active"
                  : "nav-item"
              }
            >

              <Icon size={19} />

              <span>{link.name}</span>

            </NavLink>

          );

        })}

      </nav>


      <div className="sidebar-bottom">

        <div className="system-card">

          <div className="system-status">

            <span className="live-dot"></span>

            SYSTEM LIVE

          </div>

          <p>
            All intelligence engines operational
          </p>

        </div>

      </div>

    </aside>
  );
}

export default Sidebar;