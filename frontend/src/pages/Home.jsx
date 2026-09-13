import { Link } from "react-router-dom"

function Home() {
  return (
    <div className="min-h-[calc(100vh-73px)] bg-slate-50 flex items-center justify-center px-6">
      <div className="w-full max-w-4xl text-center">

        {/* Brand */}
        <div>
          <h1 className="text-5xl font-bold text-green-700">
            KisanFlow
          </h1>

          <p className="mt-4 text-lg text-slate-600">
            AI-Powered Predictive Procurement Intelligence
          </p>

          <p className="mx-auto mt-3 max-w-2xl text-slate-500">
            Helping farmers make smarter procurement decisions and helping
            procurement centres manage queues, workload, and resources.
          </p>
        </div>

        {/* Portal Selection */}
        <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">

          <Link
            to="/farmer"
            className="w-full rounded-lg bg-green-600 px-8 py-3 font-medium text-white transition hover:bg-green-700 sm:w-auto"
          >
            Farmer Portal
          </Link>

          <Link
            to="/operator"
            className="w-full rounded-lg border border-slate-300 bg-white px-8 py-3 font-medium text-slate-700 transition hover:bg-slate-100 sm:w-auto"
          >
            Operator Portal
          </Link>

        </div>

        {/* Intelligence Highlights */}
        <div className="mt-14 grid gap-4 text-left sm:grid-cols-3">

          <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="font-semibold text-slate-800">
              Smart Recommendations
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Compare procurement price, waiting time, congestion, and
              travel distance to identify the best centre.
            </p>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="font-semibold text-slate-800">
              Predictive Intelligence
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Predict queue pressure, waiting time, congestion, and
              operational workload.
            </p>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="font-semibold text-slate-800">
              What-if Simulation
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Test resource changes before taking action and estimate
              their impact on queue and waiting time.
            </p>
          </div>

        </div>

      </div>
    </div>
  )
}

export default Home