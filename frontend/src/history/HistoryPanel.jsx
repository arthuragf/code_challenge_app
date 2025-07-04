import "react"
import {useState, useEffect} from "react"
import MCQChallenge from "../challenge/MCQChallenge.jsx"
import {UseApi} from "../utils/api.js"

export default function HistoryPanel() {
    const [history, setHistory] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState(null)
    const {makeRequest} = UseApi()
    
    useEffect(() => {
        fetchHistory()
    }, [])

    const fetchHistory = async () => {
        setIsLoading(true)
        setError(null)
        try {
            const data = await makeRequest("my-history")
            setHistory(data?.challenges)
        } catch (err) {
            setError("Failed to load history" + err.message || "An error occurred while fetching history.")
        } finally {
            setIsLoading(false)
        }
        
    }

    if (isLoading) {
        return <div className="loading">Loading history...</div>
    }

    if (error) {
        return <div className="error-message">
            <p>Error loading history:</p>
            <button onClick={fetchHistory}>Retry</button>
        </div>
    }
    return <div className="history-panel">
        <h2>History</h2>
        {history.length === 0 ? (
            <p>No challenges completed yet.</p>
        ) :
            <div className="history-list">
                {history.map((challenge, index) => {
                    return <MCQChallenge 
                                key={index} 
                                challenge={challenge} 
                                showExplanation={true} 
                            />
                })}
            </div>
        }
    </div>
}