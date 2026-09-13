import { useEffect, useState } from "react"
import api from "../services/api"
import { DEMO_FARMER_LOCATION } from "../utils/constants"

function FarmerDashboard() {
  const [crops, setCrops] = useState([])
  const [selectedCrop, setSelectedCrop] = useState("")
  const [quantity, setQuantity] = useState(25)

  const [recommendation, setRecommendation] = useState(null)

  const [bookingDate, setBookingDate] = useState("")
  const [slotTime, setSlotTime] = useState("10:00")

  const [booking, setBooking] = useState(null)

  const [loadingCrops, setLoadingCrops] = useState(true)
  const [loadingRecommendation, setLoadingRecommendation] =
    useState(false)
  const [loadingBooking, setLoadingBooking] = useState(false)

  const [error, setError] = useState("")
  const [bookingError, setBookingError] = useState("")

  useEffect(() => {
    const loadCrops = async () => {
      try {
        const response = await api.get("/api/crops")

        setCrops(response.data)

        if (response.data.length > 0) {
          setSelectedCrop(response.data[0].id)
        }
      } catch (error) {
        console.error("Failed to load crops:", error)
        setError("Unable to load crops.")
      } finally {
        setLoadingCrops(false)
      }
    }

    loadCrops()
  }, [])

  const findBestCentre = async () => {
    if (!selectedCrop) {
      setError("Please select a crop.")
      return
    }

    if (!quantity || Number(quantity) <= 0) {
      setError("Please enter a valid quantity.")
      return
    }

    setError("")
    setBooking(null)
    setBookingError("")
    setLoadingRecommendation(true)

    try {
      const response = await api.post(
        "/api/recommendations/centres",
        {
          crop_id: Number(selectedCrop),
          quantity: Number(quantity),
          location: DEMO_FARMER_LOCATION,
        }
      )

      setRecommendation(response.data)
    } catch (error) {
      console.error("Failed to get recommendation:", error)

      setError(
        error.response?.data?.detail ||
        "Unable to get centre recommendation."
      )
    } finally {
      setLoadingRecommendation(false)
    }
  }

  const bookRecommendedCentre = async () => {
    if (!recommendation?.recommended_centre) {
      setBookingError("Please find a recommended centre first.")
      return
    }

    if (!bookingDate) {
      setBookingError("Please select a booking date.")
      return
    }

    if (!slotTime) {
      setBookingError("Please select a slot time.")
      return
    }

    if (!quantity || Number(quantity) <= 0) {
      setBookingError("Please enter a valid quantity.")
      return
    }

    setBookingError("")
    setBooking(null)
    setLoadingBooking(true)

    try {
      const response = await api.post(
        "/api/bookings",
        {
          centre_id:
            recommendation.recommended_centre.id,
          crop_id: Number(selectedCrop),
          booking_date: bookingDate,
          slot_time: `${slotTime}:00`,
          quantity: Number(quantity),
        }
      )

      setBooking(response.data)
    } catch (error) {
      console.error("Booking failed:", error)

      setBookingError(
        error.response?.data?.detail ||
        "Unable to create booking."
      )
    } finally {
      setLoadingBooking(false)
    }
  }

  const formatCurrency = (value) => {
    return `₹${Number(value).toLocaleString("en-IN")}`
  }

  const formatDistance = (value) => {
    return `${Number(value).toFixed(1)} km`
  }

  const formatWaitTime = (value) => {
    return `${Math.round(Number(value))} min`
  }

  const getCongestionClass = (congestion) => {
    switch (congestion) {
      case "LOW":
        return "bg-green-100 text-green-700"

      case "MODERATE":
        return "bg-yellow-100 text-yellow-700"

      case "HIGH":
        return "bg-orange-100 text-orange-700"

      case "CRITICAL":
        return "bg-red-100 text-red-700"

      default:
        return "bg-slate-100 text-slate-700"
    }
  }

  const today = new Date()
    .toISOString()
    .split("T")[0]

  return (
    <div className="mx-auto max-w-7xl px-6 py-8">

      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-slate-900">
          Farmer Dashboard
        </h1>

        <p className="mt-2 text-slate-500">
          Find the best procurement centre using price,
          waiting time, congestion and distance.
        </p>
      </div>

      {/* Procurement Intelligence */}
      <div className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

        <h2 className="text-lg font-semibold text-slate-900">
          Procurement Intelligence
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          KisanFlow analyzes available procurement centres
          and recommends the best option for you.
        </p>

        <div className="mt-5 grid gap-5 md:grid-cols-3">

          {/* Crop */}
          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">
              Crop
            </label>

            <select
              value={selectedCrop}
              onChange={(event) =>
                setSelectedCrop(Number(event.target.value))
              }
              disabled={loadingCrops}
              className="w-full rounded-lg border border-slate-300 bg-white px-4 py-3 outline-none focus:border-green-500"
            >
              {loadingCrops ? (
                <option>Loading crops...</option>
              ) : (
                crops.map((crop) => (
                  <option
                    key={crop.id}
                    value={crop.id}
                  >
                    {crop.name}
                  </option>
                ))
              )}
            </select>
          </div>

          {/* Quantity */}
          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">
              Quantity (Quintal)
            </label>

            <input
              type="number"
              value={quantity}
              min="1"
              onChange={(event) =>
                setQuantity(event.target.value)
              }
              className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-green-500"
            />
          </div>

          {/* Analyze */}
          <div className="flex items-end">
            <button
              type="button"
              onClick={findBestCentre}
              disabled={loadingRecommendation}
              className="w-full rounded-lg bg-green-600 px-4 py-3 font-medium text-white hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loadingRecommendation
                ? "Analyzing Centres..."
                : "Find Best Centre"}
            </button>
          </div>

        </div>

        {error && (
          <div className="mt-5 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-600">
            {error}
          </div>
        )}
      </div>

      {/* Recommended Centre */}
      {recommendation?.recommended_centre && (
        <div className="mt-8 rounded-2xl border border-green-200 bg-green-50 p-6">

          <div className="flex flex-col gap-6 md:flex-row md:items-start md:justify-between">

            <div>
              <p className="text-sm font-semibold tracking-wide text-green-700">
                RECOMMENDED CENTRE
              </p>

              <h2 className="mt-2 text-3xl font-bold text-slate-900">
                {recommendation.recommended_centre.name}
              </h2>

              <p className="mt-3 max-w-2xl text-slate-600">
                {recommendation.recommended_centre.reason}
              </p>
            </div>

            <div className="rounded-xl bg-white px-6 py-4 text-center shadow-sm">

              <p className="text-sm text-slate-500">
                Intelligence Score
              </p>

              <p className="mt-1 text-3xl font-bold text-green-700">
                {Number(
                  recommendation.recommended_centre.score
                ).toFixed(2)}
              </p>

              <p className="text-xs text-slate-400">
                / 100
              </p>

            </div>

          </div>

          {/* Intelligence Metrics */}
          <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

            <div className="rounded-xl bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">
                Procurement Price
              </p>

              <p className="mt-2 text-2xl font-bold text-slate-900">
                {formatCurrency(
                  recommendation.recommended_centre.price
                )}
              </p>

              <p className="mt-1 text-xs text-slate-400">
                per quintal
              </p>
            </div>

            <div className="rounded-xl bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">
                Expected Waiting Time
              </p>

              <p className="mt-2 text-2xl font-bold text-slate-900">
                {formatWaitTime(
                  recommendation.recommended_centre.eta_minutes
                )}
              </p>

              <p className="mt-1 text-xs text-slate-400">
                predicted ETA
              </p>
            </div>

            <div className="rounded-xl bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">
                Congestion
              </p>

              <div className="mt-3">
                <span
                  className={`rounded-full px-3 py-1 text-sm font-semibold ${getCongestionClass(
                    recommendation.recommended_centre.congestion
                  )}`}
                >
                  {recommendation.recommended_centre.congestion}
                </span>
              </div>
            </div>

            <div className="rounded-xl bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">
                Distance
              </p>

              <p className="mt-2 text-2xl font-bold text-slate-900">
                {formatDistance(
                  recommendation.recommended_centre.distance_km
                )}
              </p>

              <p className="mt-1 text-xs text-slate-400">
                from your location
              </p>
            </div>

          </div>

          {/* Net Return */}
          <div className="mt-4 rounded-xl bg-white p-5 shadow-sm">

            <p className="text-sm text-slate-500">
              Expected Net Return
            </p>

            <p className="mt-1 text-3xl font-bold text-green-700">
              {formatCurrency(
                recommendation.recommended_centre.expected_net_return
              )}
            </p>

            <p className="mt-1 text-sm text-slate-500">
              Estimated after travel and waiting costs
            </p>

          </div>

          {/* Booking Form */}
          <div className="mt-6 rounded-xl border border-green-200 bg-white p-5">

            <h3 className="text-lg font-semibold text-slate-900">
              Book Procurement Slot
            </h3>

            <p className="mt-1 text-sm text-slate-500">
              Book directly at the recommended centre.
            </p>

            <div className="mt-5 grid gap-5 md:grid-cols-3">

              {/* Date */}
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">
                  Booking Date
                </label>

                <input
                  type="date"
                  min={today}
                  value={bookingDate}
                  onChange={(event) =>
                    setBookingDate(event.target.value)
                  }
                  className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-green-500"
                />
              </div>

              {/* Time */}
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">
                  Slot Time
                </label>

                <input
                  type="time"
                  value={slotTime}
                  onChange={(event) =>
                    setSlotTime(event.target.value)
                  }
                  className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-green-500"
                />
              </div>

              {/* Quantity */}
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">
                  Quantity (Quintal)
                </label>

                <input
                  type="number"
                  min="1"
                  value={quantity}
                  onChange={(event) =>
                    setQuantity(event.target.value)
                  }
                  className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-green-500"
                />
              </div>

            </div>

            {bookingError && (
              <div className="mt-4 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-600">
                {bookingError}
              </div>
            )}

            <button
              type="button"
              onClick={bookRecommendedCentre}
              disabled={loadingBooking}
              className="mt-5 rounded-lg bg-green-600 px-6 py-3 font-medium text-white hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loadingBooking
                ? "Booking..."
                : "Confirm Booking"}
            </button>

          </div>

          {/* Booking Success */}
          {booking && (
            <div className="mt-5 rounded-xl border border-green-200 bg-white p-5">

              <p className="text-sm font-semibold text-green-700">
                BOOKING CONFIRMED
              </p>

              <h3 className="mt-2 text-xl font-bold text-slate-900">
                Your procurement slot is booked
              </h3>

              <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">

                <div>
                  <p className="text-xs text-slate-500">
                    Booking ID
                  </p>

                  <p className="font-semibold text-slate-900">
                    #{booking.id}
                  </p>
                </div>

                <div>
                  <p className="text-xs text-slate-500">
                    Date
                  </p>

                  <p className="font-semibold text-slate-900">
                    {booking.booking_date}
                  </p>
                </div>

                <div>
                  <p className="text-xs text-slate-500">
                    Slot
                  </p>

                  <p className="font-semibold text-slate-900">
                    {booking.slot_time}
                  </p>
                </div>

                <div>
                  <p className="text-xs text-slate-500">
                    Status
                  </p>

                  <p className="font-semibold text-green-700">
                    {booking.status}
                  </p>
                </div>

              </div>

            </div>
          )}

        </div>
      )}

      {/* Alternatives */}
      {recommendation?.alternatives?.length > 0 && (
        <div className="mt-8">

          <div>
            <h2 className="text-xl font-bold text-slate-900">
              Compare Other Centres
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              These centres were also evaluated by KisanFlow.
            </p>
          </div>

          <div className="mt-5 grid gap-5 lg:grid-cols-2">

            {recommendation.alternatives.map((centre) => (
              <div
                key={centre.id}
                className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
              >

                <div className="flex items-start justify-between gap-4">

                  <div>
                    <h3 className="text-xl font-semibold text-slate-900">
                      {centre.name}
                    </h3>

                    <p className="mt-1 text-sm text-slate-500">
                      Intelligence Score:{" "}
                      <span className="font-semibold text-slate-700">
                        {Number(centre.score).toFixed(2)}
                      </span>
                    </p>
                  </div>

                  <span
                    className={`rounded-full px-3 py-1 text-xs font-semibold ${getCongestionClass(
                      centre.congestion
                    )}`}
                  >
                    {centre.congestion}
                  </span>

                </div>

                <div className="mt-5 grid grid-cols-2 gap-3">

                  <div className="rounded-lg bg-slate-50 p-3">
                    <p className="text-xs text-slate-500">
                      Price
                    </p>

                    <p className="mt-1 font-semibold text-slate-900">
                      {formatCurrency(centre.price)}
                    </p>
                  </div>

                  <div className="rounded-lg bg-slate-50 p-3">
                    <p className="text-xs text-slate-500">
                      Waiting
                    </p>

                    <p className="mt-1 font-semibold text-slate-900">
                      {formatWaitTime(centre.eta_minutes)}
                    </p>
                  </div>

                  <div className="rounded-lg bg-slate-50 p-3">
                    <p className="text-xs text-slate-500">
                      Distance
                    </p>

                    <p className="mt-1 font-semibold text-slate-900">
                      {formatDistance(centre.distance_km)}
                    </p>
                  </div>

                  <div className="rounded-lg bg-slate-50 p-3">
                    <p className="text-xs text-slate-500">
                      Expected Return
                    </p>

                    <p className="mt-1 font-semibold text-slate-900">
                      {formatCurrency(
                        centre.expected_net_return
                      )}
                    </p>
                  </div>

                </div>

              </div>
            ))}

          </div>

        </div>
      )}

    </div>
  )
}

export default FarmerDashboard