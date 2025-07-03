import "react"
import {useState, useEffect} from "react"
import MCQChallenge from "./MCQChallenge.jsx"
import {UseApi} from "../utils/api.js"

export default function ChallengeGenerator() {
    const [challenge, setChallenge] = useState(null)
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState(null)
    const [difficulty, setDifficulty] = useState("easy")
    const [quota, setQuota] = useState(null)
    const {makeRequest} = UseApi()
    
    useEffect(() => {
        fetchQuota()
    }, [])
    
    const fetchQuota = async () => {
        try {
            const data = await makeRequest("quota")
            setQuota(data)
        } catch (err) {
            console.log(err)
            setError(err)
        }
    }
    const generateChallenge = async () => {
        if (isLoading || quota?.quota_remaining <= 0) return
        
        setIsLoading(true)
        setError(null)
        
        try {
            const data = await makeRequest("generate-challenge", {
                    method:  "POST",  
                    body: JSON.stringify({difficulty})
                }
            )
            setChallenge(data)
            fetchQuota() // Refresh quota after generating a challenge
        } catch (err) {
            setError(err.message || "An error occurred while generating the challenge.")
        } finally {
            setIsLoading(false)
        }
    }
    const getNextResetTime = () => {
        if ( !quota?.last_reset_date) return null
        const resetDate = new Date(quota.last_reset_date)
        resetDate.setHours(resetDate.getHours() + 24)
        return resetDate.toLocaleString()
    }
        
    return <div className="challenge-container">
        <h2>Coding Challenge Generator</h2>
        <div className="quota-display">
            <p>Challenges remaining today: {quota?.quota_remaining || 0}</p>
            {quota?.quota_remaining === 0 && (
                <p>Next reset: {getNextResetTime()}</p>
            )}
        </div>
        <div className="difficulty-selector">
            <label htmlFor="difficulty">Select Difficulty</label>
            <select 
                id="difficulty" 
                value={difficulty} 
                onChange={(e) => setDifficulty(e.target.value)} 
                disabled={isLoading}>
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
            </select>
        </div>
        <button onClick={generateChallenge} disabled={isLoading || quota?.quota_remaining <= 0} className="generate-button">
            {isLoading ? "Generating..." : "Generate Challenge"}
        </button>
        
        {error && <div className="error-message">
            <p>{error}</p>
        </div>}
        
        {challenge && <MCQChallenge challenge={challenge}/>}
    </div>
}