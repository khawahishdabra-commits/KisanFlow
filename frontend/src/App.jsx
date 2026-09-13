import { BrowserRouter, Routes, Route } from "react-router-dom"
import Home from "./pages/Home"
import MainLayout from "./layouts/MainLayout"
import Login from "./pages/Login"
import FarmerDashboard from "./pages/FarmerDashboard"
import FarmerBookings from "./pages/FarmerBookings"
import OperatorDashboard from "./pages/OperatorDashboard"
import OperatorSimulation from "./pages/OperatorSimulation"

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route element={<MainLayout />}>
          <Route path="/" element={<Home />} />

          <Route
            path="/login"
            element={<Login />}
          />

          <Route
            path="/register"
            element={<div className="p-8 text-2xl">Register Page</div>}
          />

          <Route
            path="/farmer"
            element={<FarmerDashboard />}
          />

          <Route
            path="/farmer/centres"
            element={<div className="p-8 text-2xl">Centre Intelligence</div>}
          />

          <Route
            path="/farmer/bookings"
            element={<FarmerBookings />}
          />

          <Route
            path="/operator"
            element={<OperatorDashboard />}
          />

          <Route
            path="/operator/simulation"
            element={<OperatorSimulation />}
          />
        </Route>

      </Routes>
    </BrowserRouter>
  )
}

export default App