import {
  Routes,
  Route,
} from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Shipments from "./pages/Shipments";
import Factories from "./pages/Factories";
import Suppliers from "./pages/Suppliers";
import WhatIf from "./pages/WhatIf";
import Rewind from "./pages/Rewind";

function App() {
  return (
    <Routes>
      <Route
        path="/"
        element={<Dashboard />}
      />

      <Route
        path="/shipments"
        element={<Shipments />}
      />

      <Route
        path="/factories"
        element={<Factories />}
      />

      <Route
        path="/suppliers"
        element={<Suppliers />}
      />

      <Route
        path="/what-if"
        element={<WhatIf />}
      />

      <Route
        path="/rewind"
        element={<Rewind />}
      />
    </Routes>
  );
}

export default App;