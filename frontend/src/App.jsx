import { useState } from "react"

export default function App() {
  // all the state we need to track
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [checkPassword, setCheckPassword] = useState(false) // toggle for password check
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null) // stores whatever the backend sends back

  const handleScan = async () => {
    if (!email) return // dont do anything if email is empty
    setLoading(true)
    setResult(null)

    try {
      // build the url - add password param only if toggle is on and password is typed
      const res = await fetch(`http://localhost:8000/scan?email=${encodeURIComponent(email)}${checkPassword && password ? `&password=${encodeURIComponent(password)}` : ""}`)
      const data = await res.json()
      setResult(data)
    } catch (err) {
      // backend probably isnt running
      setResult({ error: "could not connect to backend" })
    }

    setLoading(false)
  }

  // colors for each risk level label
  const riskColors = {
    SAFE: "text-teal-400",
    LOW: "text-blue-300",
    MEDIUM: "text-yellow-400",
    HIGH: "text-orange-400",
    CRITICAL: "text-red-400",
  }

  // how wide the risk bar should be for each level
  const riskBarWidth = {
    SAFE: "w-[5%]",
    LOW: "w-[25%]",
    MEDIUM: "w-[50%]",
    HIGH: "w-[75%]",
    CRITICAL: "w-[100%]",
  }

  return (
    <div
      className="min-h-screen w-full px-4 py-10"
      style={{
        backgroundColor: "#042C53",
        // dot grid background - gives it that ocean depth feel
        backgroundImage: "radial-gradient(#185FA5 1px, transparent 1px)",
        backgroundSize: "22px 22px",
      }}
    >
      <div className="max-w-xl mx-auto">

        {/* header */}
        <div className="mb-8">
          <p className="text-[#B5D4F4] font-medium tracking-wider text-sm">breach-radar</p>
          <p className="text-[#378ADD] text-xs tracking-widest">personal exposure scanner</p>
        </div>

        {/* hero text */}
        <div className="text-center mb-8">
          <h1 className="text-[#E6F1FB] text-3xl font-medium mb-2">are you exposed?</h1>
          <p className="text-[#85B7EB] text-sm">scan your email against thousands of known data breaches</p>
        </div>

        {/* main input card */}
        <div className="bg-[#0C447C] border border-[#185FA5] rounded-xl p-5 mb-4">
          <div className="flex gap-3 mb-4">
            <input
              type="email"
              placeholder="your@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleScan()} // let them press enter too
              className="flex-1 bg-[#042C53] border border-[#185FA5] rounded-lg px-4 py-2.5 text-[#B5D4F4] placeholder-[#378ADD] text-sm outline-none"
            />
            <button
              onClick={handleScan}
              disabled={loading}
              className="bg-[#378ADD] text-[#042C53] font-medium text-sm px-5 py-2.5 rounded-lg hover:bg-[#85B7EB] transition-colors disabled:opacity-50"
            >
              {loading ? "scanning..." : "scan now"}
            </button>
          </div>

          {/* password toggle switch */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => setCheckPassword(!checkPassword)}
              className={`w-8 h-4 rounded-full transition-colors relative ${checkPassword ? "bg-[#378ADD]" : "bg-[#185FA5]"}`}
            >
              <span className={`absolute top-0.5 w-3 h-3 rounded-full bg-[#E6F1FB] transition-all ${checkPassword ? "left-4" : "left-0.5"}`} />
            </button>
            <span className="text-[#85B7EB] text-xs">also check password</span>
          </div>

          {/* password input - only shows when toggle is on */}
          {checkPassword && (
            <input
              type="password"
              placeholder="your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-3 w-full bg-[#042C53] border border-[#185FA5] rounded-lg px-4 py-2.5 text-[#B5D4F4] placeholder-[#378ADD] text-sm outline-none"
            />
          )}
        </div>

        {/* results section - only renders if we have a result */}
        {result && !result.error && (
          <>
            {/* stat cards */}
            <div className="grid grid-cols-2 gap-3 mb-4">
              <div className="bg-[#0C447C] border border-[#185FA5] rounded-xl p-4">
                <p className="text-[#378ADD] text-xs uppercase tracking-widest mb-1">breaches found</p>
                <p className={`text-2xl font-medium ${result.breach_count > 0 ? "text-red-400" : "text-teal-400"}`}>
                  {result.breach_count}
                </p>
              </div>
              <div className="bg-[#0C447C] border border-[#185FA5] rounded-xl p-4">
                <p className="text-[#378ADD] text-xs uppercase tracking-widest mb-1">password</p>
                <p className={`text-2xl font-medium ${result.password_pwned > 0 ? "text-red-400" : "text-teal-400"}`}>
                  {/* null means they didnt check password, 0 means clean, >0 means leaked */}
                  {result.password_pwned === null ? "—" : result.password_pwned > 0 ? "leaked" : "clean"}
                </p>
              </div>
            </div>

            {/* risk level bar */}
            <div className="bg-[#0C447C] border border-[#185FA5] rounded-xl p-4 mb-4">
              <div className="flex justify-between items-center mb-3">
                <p className="text-[#378ADD] text-xs uppercase tracking-widest">risk level</p>
                <span className={`text-xs font-medium px-3 py-1 rounded-full bg-[#042C53] border border-[#185FA5] ${riskColors[result.risk.label]}`}>
                  {result.risk.label}
                </span>
              </div>
              <div className="h-1.5 bg-[#042C53] rounded-full overflow-hidden">
                <div className={`h-full ${riskBarWidth[result.risk.label]} bg-[#85B7EB] rounded-full transition-all`} />
              </div>
              <p className="text-[#85B7EB] text-xs mt-3">{result.risk.advice}</p>
            </div>

            {/* breach list - only shows if there are breaches */}
            {result.breaches.length > 0 && (
              <div className="bg-[#0C447C] border border-[#185FA5] rounded-xl overflow-hidden">
                <p className="text-[#378ADD] text-xs uppercase tracking-widest px-4 py-3 border-b border-[#185FA5]">breach history</p>
                {result.breaches.map((breach, i) => (
                  <div key={i} className="flex items-center justify-between px-4 py-3 border-b border-[#042C53] last:border-0">
                    <div>
                      <p className="text-[#E6F1FB] text-sm font-medium">{breach.Name}</p>
                      <p className="text-[#378ADD] text-xs">{breach.BreachDate}</p>
                    </div>
                    {breach.DataClasses.length > 0 && (
                      <span className="text-xs px-2 py-1 rounded-full bg-[#042C53] border border-[#185FA5] text-[#85B7EB]">
                        {breach.DataClasses[0].toLowerCase()}
                      </span>
                    )}
                  </div>
                ))}
              </div>
            )}
          </>
        )}

        {/* error state */}
        {result?.error && (
          <div className="bg-[#0C447C] border border-red-900 rounded-xl p-4 text-red-400 text-sm">
            {result.error}
          </div>
        )}

        <p className="text-center text-[#185FA5] text-xs mt-8">powered by xposedornot — free & open source</p>
      </div>
    </div>
  )
}