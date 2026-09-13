import { useState } from "react"
import { Link, NavLink, Outlet, useNavigate } from "react-router-dom"

function MainLayout() {
  const navigate = useNavigate()
  const [isLoggedIn, setIsLoggedIn] = useState(
    Boolean(localStorage.getItem("token"))
  )

  const getNavClass = ({ isActive }) =>
    isActive
      ? "font-medium text-green-700"
      : "text-slate-600 hover:text-green-700"

  const handleLogout = () => {
    localStorage.removeItem("token")
    setIsLoggedIn(false)
    navigate("/")
  }

  return (
    <div className="min-h-screen bg-slate-50">

      <nav className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">

          {/* Logo */}
          <Link
            to="/"
            className="text-2xl font-bold text-green-700"
          >
            KisanFlow
          </Link>

          {/* Navigation */}
          <div className="flex items-center gap-6">

            <NavLink
              to="/farmer"
              className={getNavClass}
            >
              Farmer Dashboard
            </NavLink>

            <NavLink
              to="/farmer/bookings"
              className={getNavClass}
            >
              My Bookings
            </NavLink>

            <div className="hidden h-6 w-px bg-slate-200 md:block" />

            <NavLink
              to="/operator"
              className={getNavClass}
            >
              Operator Dashboard
            </NavLink>

            <NavLink
              to="/operator/simulation"
              className={getNavClass}
            >
              Simulation
            </NavLink>

            {/* Authentication */}
            {isLoggedIn ? (
              <button
                onClick={handleLogout}
                className="rounded-lg border border-red-200 bg-white px-4 py-2 font-medium text-red-600 hover:bg-red-50"
              >
                Logout
              </button>
            ) : (
              <Link
                to="/login"
                className="rounded-lg bg-green-600 px-4 py-2 font-medium text-white hover:bg-green-700"
              >
                Login
              </Link>
            )}

          </div>

        </div>
      </nav>

      <main>
        <Outlet />
      </main>

    </div>
  )
}

export default MainLayout