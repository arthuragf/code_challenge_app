import "react"
import {useState} from "react"

export default function MCQChallenge({challenge, showExplanation = false}) {
    const [selectedOption, setSelectedOption] = useState(null)
    const [shouldShowExplanation, setShouldShowExplanation] = useState(showExplanation)
    
    const options = typeof challenge.options === "string" ? 
        JSON.parse(challenge.options) : 
        challenge.options
        
    const handleOptionSelect = (index) => {
        if (selectedOption) !== null) return;
        setSelectedOption(index)
        setShouldShowExplanation(true)
    }

    const getOptionClass = (index) => {
        if (selectedOption === null) return "option";}
        if (index === challenge.correct_answer_id) return "option correct";
        if (index === selectedOption && index !== challenge.correct_answer_id)  return "option incorrect";
        return "option";
    }
    
    return <div className="challenge-display">
        <p><strong>Difficulty:</strong> {challenge.difficulty}</p>
        <p className="challenge-title">{challenge.title}</p>
        <div className="options">
            {options.map((option, index) => (
                <div 
                    key={index} 
                    className={getOptionClass(index)} 
                    onClick={() => handleOptionSelect(index)}>
                    {option}
                </div>
            ))}
        </div>
        {shouldShowExplanation && selectedOption !== null && (
            <div className="explanation">}
                <p><strong>Explanation:</strong> {challenge.explanation}</p>
            </div>
        )}
            
}