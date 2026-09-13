import { useState } from "react"
import { useNavigate } from "react-router-dom"
import api from "../services/api"

function Login() {
  const navigate = useNavigate()

  const [phone, setPhone] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()

    setError("")
    setLoading(true)

    try {
      const response = await api.post("/api/auth/login", {
        phone,
        password,
      })

      localStorage.setItem("token", response.data.access_token)

      navigate("/farmer")
    } catch (error) {
      setError(
        error.response?.data?.detail ||
        "Login failed. Please check your credentials."
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-[calc(100vh-73px)] items-center justify-center px-6">
      <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-sm border border-slate-200">

        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-green-700">
            Welcome to KisanFlow
          </h1>

          <p className="mt-2 text-slate-500">
            Login to continue
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">
              Phone Number
            </label>

            <input
              type="tel"
              value={phone}
              onChange={(event) => setPhone(event.target.value)}
              placeholder="Enter phone number"
              required
              className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-green-500"
            />
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">
              Password
            </label>

            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Enter password"
              required
              className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-green-500"
            />
          </div>

          {error && (
            <div className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-600">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-green-600 px-4 py-3 font-medium text-white hover:bg-green-700 disabled:opacity-50"
          >
            {loading ? "Logging in..." : "Login"}
          </button>

        </form>

      </div>
    </div>
  )
}

export default Login