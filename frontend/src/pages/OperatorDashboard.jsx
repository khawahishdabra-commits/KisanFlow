import { useEffect, useState } from "react"
import api from "../services/api"
import { DEMO_CENTRE_ID } from "../utils/constants"

function OperatorDashboard() {
  const [dashboard, setDashboard] = useState(null)
  const [recommendation, setRecommendation] = useState(null)

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  const centreId = DEMO_CENTRE_ID

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const [dashboardResponse, recommendationResponse] =
          await Promise.all([
            api.get("/api/operator/dashboard", {
              params: {
                centre_id: centreId,
              },
            }),

            api.get(
              "/api/operator/resource-recommendation",
              {
                params: {
                  centre_id: centreId,
                },
              }
            ),
          ])

        setDashboard(dashboardResponse.data)
        setRecommendation(recommendationResponse.data)
      } catch (error) {
        console.error(
          "Failed to load operator dashboard:",
          error
        )

        setError(
          error.response?.data?.detail ||
          "Unable to load operator dashboard."
        )
      } finally {
        setLoading(false)
      }
    }

    loadDashboard()
  }, [])

  if (loading) {
    return (
      <div className="mx-auto max-w-7xl px-6 py-8">
        <div className="rounded-2xl border border-slate-200 bg-white p-8">
          <p className="text-slate-500">
            Loading operator dashboard...
          </p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="mx-auto max-w-7xl px-6 py-8">
        <div className="rounded-xl bg-red-50 px-5 py-4 text-red-600">
          {error}
        </div>
      </div>
    )
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

  return (
    <div className="mx-auto max-w-7xl px-6 py-8">

      {/* Header */}
      <div>
        <p className="text-sm font-semibold tracking-wide text-green-700">
          OPERATOR PORTAL
        </p>

        <h1 className="mt-2 text-3xl font-bold text-slate-900">
          {dashboard.centre.name}
        </h1>

        <p className="mt-2 text-slate-500">
          Monitor current operations and use KisanFlow
          intelligence to manage procurement capacity.
        </p>
      </div>

      {/* Current State */}
      <div className="mt-8">

        <h2 className="text-xl font-bold text-slate-900">
          Current Operations
        </h2>

        <div className="mt-5 grid gap-5 md:grid-cols-3">

          {/* Queue */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

            <p className="text-sm text-slate-500">
              Current Queue
            </p>

            <p className="mt-2 text-4xl font-bold text-slate-900">
              {dashboard.queue.current_queue}
            </p>

            <p className="mt-2 text-sm text-slate-500">
              farmers currently waiting
            </p>

          </div>

          {/* Wait */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

            <p className="text-sm text-slate-500">
              Current Estimated Wait
            </p>

            <p className="mt-2 text-4xl font-bold text-slate-900">
              {dashboard.queue.estimated_wait_minutes}
              <span className="ml-1 text-lg font-medium">
                min
              </span>
            </p>

            <p className="mt-2 text-sm text-slate-500">
              based on current queue
            </p>

          </div>

          {/* Congestion */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

            <p className="text-sm text-slate-500">
              Current Congestion
            </p>

            <div className="mt-4">
              <span
                className={`rounded-full px-4 py-2 text-sm font-semibold ${getCongestionClass(
                  dashboard.predictions.congestion
                )}`}
              >
                {dashboard.predictions.congestion}
              </span>
            </div>

            <p className="mt-4 text-sm text-slate-500">
              Centre operational status
            </p>

          </div>

        </div>

      </div>

      {/* Prediction Layer */}
      <div className="mt-8">

        <h2 className="text-xl font-bold text-slate-900">
          AI Predictions
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          KisanFlow predicts future operational pressure
          instead of only showing the current state.
        </p>

        <div className="mt-5 grid gap-5 md:grid-cols-2">

          {/* ETA Prediction */}
          <div className="rounded-2xl border border-green-200 bg-green-50 p-6">

            <p className="text-sm font-medium text-green-700">
              Predicted Processing ETA
            </p>

            <p className="mt-2 text-4xl font-bold text-slate-900">
              {dashboard.predictions.eta_minutes}
              <span className="ml-2 text-lg font-medium">
                min
              </span>
            </p>

            <p className="mt-2 text-sm text-slate-600">
              Estimated waiting time considering current
              queue and available processing capacity.
            </p>

          </div>

          {/* Workload */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6">

            <p className="text-sm font-medium text-slate-500">
              Predicted Workload
            </p>

            <p className="mt-2 text-4xl font-bold text-slate-900">
              {dashboard.predictions.predicted_workload}
            </p>

            <p className="mt-2 text-sm text-slate-500">
              expected procurement workload
            </p>

          </div>

        </div>

      </div>

      {/* Resources */}
      <div className="mt-8">

        <h2 className="text-xl font-bold text-slate-900">
          Resource Status
        </h2>

        <div className="mt-5 grid gap-5">

          {dashboard.resources.map((resource, index) => (
            <div
              key={index}
              className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
            >

              <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">

                <div>
                  <p className="text-lg font-semibold text-slate-900">
                    {resource.type}
                  </p>

                  <p className="mt-1 text-sm text-slate-500">
                    {resource.available} of {resource.total} units
                    currently available
                  </p>
                </div>

                <span className="w-fit rounded-full bg-green-100 px-3 py-1 text-sm font-semibold text-green-700">
                  {resource.status}
                </span>

              </div>

              <div className="mt-5 h-3 overflow-hidden rounded-full bg-slate-100">

                <div
                  className="h-full rounded-full bg-green-600"
                  style={{
                    width: `${
                      (resource.available /
                        resource.total) *
                      100
                    }%`,
                  }}
                />

              </div>

            </div>
          ))}

        </div>

      </div>

      {/* Resource Recommendation */}
      {recommendation && (
        <div className="mt-8 rounded-2xl border border-orange-200 bg-orange-50 p-6">

          <p className="text-sm font-semibold tracking-wide text-orange-700">
            RESOURCE RECOMMENDATION
          </p>

          <h2 className="mt-2 text-2xl font-bold text-slate-900">
            {recommendation.resource_type}
          </h2>

          <p className="mt-3 text-slate-600">
            {recommendation.reason}
          </p>

          <div className="mt-5 inline-flex rounded-lg bg-white px-5 py-3 shadow-sm">

            <div>
              <p className="text-xs text-slate-500">
                Recommended Change
              </p>

              <p className="mt-1 text-2xl font-bold text-orange-700">
                +{recommendation.recommended_change}
              </p>
            </div>

          </div>

        </div>
      )}

      {/* Decision Explanation */}
      <div className="mt-8 rounded-2xl border border-slate-200 bg-white p-6">

        <h2 className="text-xl font-bold text-slate-900">
          How KisanFlow Helps
        </h2>

        <p className="mt-3 max-w-4xl text-slate-600">
          KisanFlow combines current queue conditions,
          processing capacity and prediction logic to
          identify operational pressure and recommend
          actions before congestion becomes worse.
        </p>

        <div className="mt-5 grid gap-4 md:grid-cols-4">

          <div className="rounded-lg bg-slate-50 p-4">
            <p className="text-sm font-semibold text-slate-900">
              1. Observe
            </p>
            <p className="mt-1 text-xs text-slate-500">
              Current queue and resources
            </p>
          </div>

          <div className="rounded-lg bg-slate-50 p-4">
            <p className="text-sm font-semibold text-slate-900">
              2. Predict
            </p>
            <p className="mt-1 text-xs text-slate-500">
              Future ETA and workload
            </p>
          </div>

          <div className="rounded-lg bg-slate-50 p-4">
            <p className="text-sm font-semibold text-slate-900">
              3. Recommend
            </p>
            <p className="mt-1 text-xs text-slate-500">
              Resource action
            </p>
          </div>

          <div className="rounded-lg bg-slate-50 p-4">
            <p className="text-sm font-semibold text-slate-900">
              4. Act
            </p>
            <p className="mt-1 text-xs text-slate-500">
              Operator makes the decision
            </p>
          </div>

        </div>

      </div>

    </div>
  )
}

export default OperatorDashboard