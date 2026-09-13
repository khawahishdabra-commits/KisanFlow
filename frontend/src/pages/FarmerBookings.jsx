import { useEffect, useState } from "react"
import api from "../services/api"

function FarmerBookings() {
  const [bookings, setBookings] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    const loadBookings = async () => {
      try {
        const response = await api.get("/api/bookings")
        setBookings(response.data)
      } catch (error) {
        console.error("Failed to load bookings:", error)

        setError(
          error.response?.data?.detail ||
          "Unable to load your bookings."
        )
      } finally {
        setLoading(false)
      }
    }

    loadBookings()
  }, [])

  const getStatusClass = (status) => {
    switch (status?.toUpperCase()) {
      case "CONFIRMED":
        return "bg-green-100 text-green-700"

      case "PENDING":
        return "bg-yellow-100 text-yellow-700"

      case "COMPLETED":
        return "bg-blue-100 text-blue-700"

      case "CANCELLED":
        return "bg-red-100 text-red-700"

      default:
        return "bg-slate-100 text-slate-700"
    }
  }

  return (
    <div className="mx-auto max-w-7xl px-6 py-8">

      <div>
        <h1 className="text-3xl font-bold text-slate-900">
          My Bookings
        </h1>

        <p className="mt-2 text-slate-500">
          View and track your procurement bookings.
        </p>
      </div>

      {loading && (
        <div className="mt-8 rounded-xl border border-slate-200 bg-white p-6">
          <p className="text-slate-500">
            Loading your bookings...
          </p>
        </div>
      )}

      {error && (
        <div className="mt-8 rounded-xl bg-red-50 px-5 py-4 text-red-600">
          {error}
        </div>
      )}

      {!loading && !error && bookings.length === 0 && (
        <div className="mt-8 rounded-2xl border border-slate-200 bg-white p-8 text-center">
          <h2 className="text-xl font-semibold text-slate-900">
            No bookings yet
          </h2>

          <p className="mt-2 text-slate-500">
            Find the best procurement centre and book your first slot.
          </p>
        </div>
      )}

      {!loading && !error && bookings.length > 0 && (
        <div className="mt-8 space-y-5">

          {bookings.map((booking) => (
            <div
              key={booking.id}
              className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
            >

              <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">

                <div>
                  <p className="text-sm text-slate-500">
                    Booking ID
                  </p>

                  <h2 className="mt-1 text-2xl font-bold text-slate-900">
                    #{booking.id}
                  </h2>
                </div>

                <span
                  className={`w-fit rounded-full px-3 py-1 text-sm font-semibold ${getStatusClass(
                    booking.status
                  )}`}
                >
                  {booking.status}
                </span>

              </div>

              <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">

                <div className="rounded-lg bg-slate-50 p-4">
                  <p className="text-xs text-slate-500">
                    Centre
                  </p>

                  <p className="mt-1 font-semibold text-slate-900">
                    Centre #{booking.centre_id}
                  </p>
                </div>

                <div className="rounded-lg bg-slate-50 p-4">
                  <p className="text-xs text-slate-500">
                    Crop
                  </p>

                  <p className="mt-1 font-semibold text-slate-900">
                    Crop #{booking.crop_id}
                  </p>
                </div>

                <div className="rounded-lg bg-slate-50 p-4">
                  <p className="text-xs text-slate-500">
                    Date
                  </p>

                  <p className="mt-1 font-semibold text-slate-900">
                    {booking.booking_date}
                  </p>
                </div>

                <div className="rounded-lg bg-slate-50 p-4">
                  <p className="text-xs text-slate-500">
                    Slot
                  </p>

                  <p className="mt-1 font-semibold text-slate-900">
                    {booking.slot_time}
                  </p>
                </div>

                <div className="rounded-lg bg-slate-50 p-4">
                  <p className="text-xs text-slate-500">
                    Quantity
                  </p>

                  <p className="mt-1 font-semibold text-slate-900">
                    {booking.quantity} quintal
                  </p>
                </div>

              </div>

            </div>
          ))}

        </div>
      )}

    </div>
  )
}

export default FarmerBookings