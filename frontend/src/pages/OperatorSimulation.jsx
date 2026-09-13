import { useState } from "react"
import api from "../services/api"
import { DEMO_CENTRE_ID } from "../utils/constants"

function OperatorSimulation() {
  const [resourceType, setResourceType] =
    useState("Weighing Machine")

  const [resourceChange, setResourceChange] = useState(1)

  const [simulation, setSimulation] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const centreId = DEMO_CENTRE_ID

  const runSimulation = async () => {
    if (!resourceChange || Number(resourceChange) <= 0) {
      setError("Resource change must be greater than zero.")
      return
    }

    setError("")
    setSimulation(null)
    setLoading(true)

    try {
      const response = await api.post(
        "/api/operator/simulations",
        {
          centre_id: centreId,
          resource_type: resourceType,
          resource_change: Number(resourceChange),
        }
      )

      setSimulation(response.data)
    } catch (error) {
      console.error("Simulation failed:", error)

      setError(
        error.response?.data?.detail ||
        "Unable to run simulation."
      )
    } finally {
      setLoading(false)
    }
  }

  const calculatePercentageReduction = (
    before,
    after
  ) => {
    if (!before) {
      return 0
    }

    return Math.round(
      ((before - after) / before) * 100
    )
  }

  return (
    <div className="mx-auto max-w-7xl px-6 py-8">

      {/* Header */}
      <div>
        <p className="text-sm font-semibold tracking-wide text-orange-600">
          OPERATOR DECISION SUPPORT
        </p>

        <h1 className="mt-2 text-3xl font-bold text-slate-900">
          What-if Simulation
        </h1>

        <p className="mt-2 max-w-3xl text-slate-500">
          Simulate operational changes before taking action.
          KisanFlow estimates how additional resources could
          affect queue and waiting time.
        </p>
      </div>

      {/* Simulation Controls */}
      <div className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

        <h2 className="text-xl font-bold text-slate-900">
          Simulate Resource Change
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          Select a resource and see its predicted impact.
        </p>

        <div className="mt-6 grid gap-5 md:grid-cols-3">

          {/* Resource */}
          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">
              Resource
            </label>

            <select
              value={resourceType}
              onChange={(event) =>
                setResourceType(event.target.value)
              }
              className="w-full rounded-lg border border-slate-300 bg-white px-4 py-3 outline-none focus:border-green-500"
            >
              <option value="Weighing Machine">
                Weighing Machine
              </option>

              <option value="Processing Unit">
                Processing Unit
              </option>
            </select>
          </div>

          {/* Change */}
          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">
              Additional Units
            </label>

            <input
              type="number"
              min="1"
              value={resourceChange}
              onChange={(event) =>
                setResourceChange(event.target.value)
              }
              className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-green-500"
            />
          </div>

          {/* Button */}
          <div className="flex items-end">
            <button
              type="button"
              onClick={runSimulation}
              disabled={loading}
              className="w-full rounded-lg bg-orange-600 px-4 py-3 font-medium text-white hover:bg-orange-700 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading
                ? "Simulating..."
                : "Run Simulation"}
            </button>
          </div>

        </div>

        {error && (
          <div className="mt-5 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-600">
            {error}
          </div>
        )}

      </div>

      {/* Simulation Result */}
      {simulation && (
        <div className="mt-8">

          <div className="rounded-2xl border border-green-200 bg-green-50 p-6">

            <p className="text-sm font-semibold tracking-wide text-green-700">
              SIMULATION RESULT
            </p>

            <h2 className="mt-2 text-2xl font-bold text-slate-900">
              Add {simulation.resource_change}{" "}
              {simulation.resource_type}
              {simulation.resource_change > 1 ? "s" : ""}
            </h2>

            <p className="mt-2 text-slate-600">
              Predicted operational impact at Centre #
              {simulation.centre_id}
            </p>

            {/* Before / After */}
            <div className="mt-6 grid gap-5 md:grid-cols-2">

              {/* Before */}
              <div className="rounded-xl bg-white p-6 shadow-sm">

                <p className="text-sm font-semibold text-slate-500">
                  BEFORE
                </p>

                <div className="mt-5 grid grid-cols-2 gap-4">

                  <div>
                    <p className="text-xs text-slate-500">
                      Queue
                    </p>

                    <p className="mt-1 text-3xl font-bold text-slate-900">
                      {simulation.before_queue}
                    </p>

                    <p className="text-xs text-slate-400">
                      farmers
                    </p>
                  </div>

                  <div>
                    <p className="text-xs text-slate-500">
                      ETA
                    </p>

                    <p className="mt-1 text-3xl font-bold text-slate-900">
                      {simulation.before_wait}
                    </p>

                    <p className="text-xs text-slate-400">
                      minutes
                    </p>
                  </div>

                </div>

              </div>

              {/* After */}
              <div className="rounded-xl bg-green-50 p-6">

                <p className="text-sm font-semibold text-green-700">
                  AFTER
                </p>

                <div className="mt-5 grid grid-cols-2 gap-4">

                  <div>
                    <p className="text-xs text-slate-500">
                      Queue
                    </p>

                    <p className="mt-1 text-3xl font-bold text-slate-900">
                      {simulation.after_queue}
                    </p>

                    <p className="text-xs text-slate-400">
                      farmers
                    </p>
                  </div>

                  <div>
                    <p className="text-xs text-slate-500">
                      ETA
                    </p>

                    <p className="mt-1 text-3xl font-bold text-green-700">
                      {simulation.after_wait}
                    </p>

                    <p className="text-xs text-slate-400">
                      minutes
                    </p>
                  </div>

                </div>

              </div>

            </div>

            {/* Impact */}
            <div className="mt-5 grid gap-4 md:grid-cols-2">

              <div className="rounded-xl bg-white p-5 shadow-sm">

                <p className="text-sm text-slate-500">
                  Queue Reduction
                </p>

                <p className="mt-1 text-3xl font-bold text-green-700">
                  {simulation.before_queue -
                    simulation.after_queue}
                </p>

                <p className="mt-1 text-sm text-slate-500">
                  farmers
                  {" "}
                  (
                  {calculatePercentageReduction(
                    simulation.before_queue,
                    simulation.after_queue
                  )}
                  % reduction)
                </p>

              </div>

              <div className="rounded-xl bg-white p-5 shadow-sm">

                <p className="text-sm text-slate-500">
                  Waiting Time Reduction
                </p>

                <p className="mt-1 text-3xl font-bold text-green-700">
                  {(
                    simulation.before_wait -
                    simulation.after_wait
                  ).toFixed(2)}
                  {" "}
                  min
                </p>

                <p className="mt-1 text-sm text-slate-500">
                  predicted improvement
                </p>

              </div>

            </div>

          </div>

        </div>
      )}

      {/* Explanation */}
      <div className="mt-8 rounded-2xl border border-slate-200 bg-white p-6">

        <h2 className="text-xl font-bold text-slate-900">
          Why What-if Simulation?
        </h2>

        <p className="mt-3 max-w-4xl text-slate-600">
          Instead of blindly adding resources, operators can
          first evaluate the expected impact of a change.
          This turns KisanFlow from a monitoring system into
          a decision-support platform.
        </p>

        <div className="mt-5 rounded-xl bg-slate-50 p-5">

          <p className="font-semibold text-slate-900">
            Decision Loop
          </p>

          <p className="mt-2 text-sm text-slate-600">
            Current State → Prediction → Simulation →
            Operator Decision → Actual Outcome → Feedback
          </p>

        </div>

      </div>

    </div>
  )
}

export default OperatorSimulation