# React Integration Guide

How to integrate AI coaching into your existing MathTutor React app.

## Overview

Your current Quiz.jsx has hardcoded coaching messages. We'll modify it to optionally call the backend API for AI-powered coaching while keeping static mode as fallback.

## Step 1: Create API Client

Create `src/utils/coachingAPI.js` in your MathTutor React app:

```javascript
// src/utils/coachingAPI.js
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const coachingAPI = {
  /**
   * Get coaching feedback from the API
   */
  async getCoaching({
    mode = 'static',  // 'static' or 'ai'
    harness = 'socratic',  // 'socratic', 'direct', 'step-by-step', 'discovery', 'adaptive'
    question,
    correctAnswer,
    studentAnswer,
    attempt,
    isCorrect,
    hintUsed,
    hint,
    explanation
  }) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/coach`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          mode,
          harness,
          context: {
            question,
            correct_answer: correctAnswer,
            student_answer: studentAnswer,
            attempt,
            is_correct: isCorrect,
            hint_used: hintUsed,
            hint,
            explanation
          }
        })
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Failed to get coaching:', error);
      // Return fallback static response
      return {
        message: isCorrect 
          ? "That's correct!" 
          : "Not quite. Try again!",
        hint: hint,
        show_hint: !isCorrect && attempt > 0,
        show_answer: attempt >= 3,
        encouragement: "Keep going!"
      };
    }
  },

  /**
   * Get list of available harnesses
   */
  async getHarnesses() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/harnesses`);
      if (!response.ok) throw new Error('Failed to fetch harnesses');
      return await response.json();
    } catch (error) {
      console.error('Failed to get harnesses:', error);
      return [];
    }
  },

  /**
   * Reset conversation history for a harness
   */
  async resetHarness(harness) {
    try {
      await fetch(`${API_BASE_URL}/api/reset/${harness}`, {
        method: 'POST'
      });
    } catch (error) {
      console.error('Failed to reset harness:', error);
    }
  }
};
```

## Step 2: Modify Quiz.jsx

### Option A: Minimal Change (Add AI Mode Toggle)

Add to the top of your Quiz component:

```javascript
import { coachingAPI } from '../utils/coachingAPI'

function Quiz({ topic, onComplete }) {
  // Existing state...
  const [questions, setQuestions] = useState([])
  // ...

  // NEW: Add coaching mode state
  const [coachingMode, setCoachingMode] = useState('static') // 'static' or 'ai'
  const [selectedHarness, setSelectedHarness] = useState('socratic')
  const [isLoadingCoaching, setIsLoadingCoaching] = useState(false)

  // ...existing code...

  // MODIFY: Update handleSubmit to use API
  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoadingCoaching(true)

    const numericAnswer = parseFloat(userAnswer)
    const isCorrect = Math.abs(numericAnswer - currentQuestion.answer) < 0.01
    const newAttemptCount = attemptCount + 1

    try {
      // Get coaching from API (or static fallback)
      const coaching = await coachingAPI.getCoaching({
        mode: coachingMode,
        harness: selectedHarness,
        question: currentQuestion.question,
        correctAnswer: currentQuestion.answer,
        studentAnswer: numericAnswer,
        attempt: newAttemptCount,
        isCorrect: isCorrect,
        hintUsed: hintUsed,
        hint: currentQuestion.hint,
        explanation: currentQuestion.explanation
      })

      setCoachMessage(coaching.message)

      if (isCorrect) {
        const answerRecord = {
          question: currentQuestion.question,
          userAnswer: numericAnswer,
          correctAnswer: currentQuestion.answer,
          isCorrect: true,
          explanation: currentQuestion.explanation,
          hintUsed,
          attempts: newAttemptCount,
          coachingMode,
          harness: selectedHarness
        }

        const newAnswers = [...answers, answerRecord]
        setAnswers(newAnswers)
        setFeedback('correct')

        setTimeout(() => {
          moveToNextQuestion(newAnswers)
        }, 3000)
      } else {
        setAttemptCount(newAttemptCount)
        setFeedback('incorrect')

        if (coaching.show_answer || newAttemptCount >= MAX_ATTEMPTS) {
          setShowingAnswer(true)
          const answerRecord = {
            question: currentQuestion.question,
            userAnswer: numericAnswer,
            correctAnswer: currentQuestion.answer,
            isCorrect: false,
            explanation: currentQuestion.explanation,
            hintUsed,
            attempts: newAttemptCount,
            coachingMode,
            harness: selectedHarness
          }
          const newAnswers = [...answers, answerRecord]
          setAnswers(newAnswers)

          setTimeout(() => {
            moveToNextQuestion(newAnswers)
          }, 5000)
        } else {
          if (coaching.show_hint) {
            setShowHint(true)
            setHintUsed(true)
          }

          setTimeout(() => {
            setFeedback(null)
            setUserAnswer('')
          }, 2000)
        }
      }
    } catch (error) {
      console.error('Error getting coaching:', error)
      // Fallback to your original static messages
      // ... (your original getCorrectMessage/getIncorrectMessage logic)
    } finally {
      setIsLoadingCoaching(false)
    }
  }

  // Rest of your component...
}
```

### Option B: Full Integration with UI Controls

Add settings panel to Quiz header:

```javascript
// Add this before the question-card div
<div className="coaching-settings">
  <div className="coaching-mode-toggle">
    <label>
      <input
        type="radio"
        name="mode"
        value="static"
        checked={coachingMode === 'static'}
        onChange={(e) => setCoachingMode(e.target.value)}
      />
      Static Coaching
    </label>
    <label>
      <input
        type="radio"
        name="mode"
        value="ai"
        checked={coachingMode === 'ai'}
        onChange={(e) => setCoachingMode(e.target.value)}
      />
      AI Coaching
    </label>
  </div>

  {coachingMode === 'ai' && (
    <div className="harness-selector">
      <label htmlFor="harness">Teaching Strategy:</label>
      <select
        id="harness"
        value={selectedHarness}
        onChange={(e) => setSelectedHarness(e.target.value)}
      >
        <option value="socratic">Socratic (Questioning)</option>
        <option value="direct">Direct (Clear Explanations)</option>
        <option value="step-by-step">Step-by-Step (Guided)</option>
        <option value="discovery">Discovery (Exploration)</option>
        <option value="adaptive">Adaptive (Personalized)</option>
      </select>
    </div>
  )}
</div>
```

## Step 3: Add Environment Variable

Create `.env.local` in your React app root:

```bash
VITE_API_URL=http://localhost:8000
```

For production:
```bash
VITE_API_URL=https://your-backend-api.herokuapp.com
```

## Step 4: Add CSS (Optional)

Add to `Quiz.css`:

```css
.coaching-settings {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.coaching-mode-toggle {
  display: flex;
  gap: 20px;
  margin-bottom: 10px;
}

.coaching-mode-toggle label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.harness-selector {
  display: flex;
  align-items: center;
  gap: 10px;
}

.harness-selector select {
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
}

.coach-message.loading {
  opacity: 0.6;
}
```

## Step 5: Test Integration

### 1. Start Backend
```bash
cd HarnessEval/backend
python server.py
```

### 2. Start React App
```bash
cd MathTutor-Original
npm run dev
```

### 3. Test Flow
1. Open app in browser
2. Select a quiz topic
3. Try answering a question wrong (trigger coaching)
4. Toggle between Static and AI mode
5. Try different harnesses

## Minimal Integration (No UI Changes)

If you don't want to modify the UI, you can hardcode AI mode:

```javascript
// At the top of Quiz.jsx
const USE_AI_COACHING = true;  // Set to false to use original static
const AI_HARNESS = 'socratic';  // Or 'direct', 'step-by-step', etc.

// Then in handleSubmit:
const coaching = await coachingAPI.getCoaching({
  mode: USE_AI_COACHING ? 'ai' : 'static',
  harness: AI_HARNESS,
  // ... rest of params
})
```

## Testing Different Harnesses

Create a test component to compare harnesses side-by-side:

```javascript
// src/components/HarnessComparison.jsx
import { useState } from 'react'
import { coachingAPI } from '../utils/coachingAPI'

function HarnessComparison() {
  const [responses, setResponses] = useState({})
  const harnesses = ['socratic', 'direct', 'step-by-step', 'discovery', 'adaptive']

  const testAllHarnesses = async () => {
    const testContext = {
      question: "What is 5 + 3?",
      correctAnswer: 8,
      studentAnswer: 7,
      attempt: 1,
      isCorrect: false,
      hint: "Try counting from 5"
    }

    const results = {}
    for (const harness of harnesses) {
      const response = await coachingAPI.getCoaching({
        mode: 'ai',
        harness,
        ...testContext
      })
      results[harness] = response.message
    }

    setResponses(results)
  }

  return (
    <div className="harness-comparison">
      <h2>Compare Teaching Strategies</h2>
      <button onClick={testAllHarnesses}>Test All Harnesses</button>

      <div className="responses-grid">
        {Object.entries(responses).map(([harness, message]) => (
          <div key={harness} className="harness-response">
            <h3>{harness}</h3>
            <p>{message}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default HarnessComparison
```

## Error Handling

Add robust error handling:

```javascript
const handleSubmit = async (e) => {
  e.preventDefault()
  setIsLoadingCoaching(true)

  try {
    const coaching = await coachingAPI.getCoaching({...})
    // Process coaching response
  } catch (error) {
    console.error('Coaching error:', error)

    // Show error to user
    setCoachMessage("Oops! The AI tutor is taking a break. Let's use our backup coaching.")

    // Fall back to static coaching
    const fallbackMessages = isCorrect ? getCorrectMessage(0) : getIncorrectMessage(attemptCount)
    setCoachMessage(fallbackMessages[0])
  } finally {
    setIsLoadingCoaching(false)
  }
}
```

## Production Checklist

- [ ] Environment variable for API URL
- [ ] Error handling and fallbacks
- [ ] Loading states during API calls
- [ ] CORS configured correctly
- [ ] Backend deployed and accessible
- [ ] API key secured (not in client code!)
- [ ] Rate limiting on backend
- [ ] Monitoring and logging
- [ ] User feedback collection
- [ ] A/B testing setup (optional)

## Gradual Rollout Strategy

### Phase 1: Internal Testing (Week 1)
- Enable AI for your own account only
- Test all harnesses thoroughly
- Fix bugs

### Phase 2: Beta Testing (Week 2-3)
- Enable for 10% of users
- Collect feedback
- Monitor costs and performance

### Phase 3: Controlled Rollout (Week 4)
- Increase to 50% of users
- Compare metrics: static vs AI
- Iterate on prompts

### Phase 4: Full Deployment (Week 5+)
- Enable for all users
- Make AI the default (keep static as fallback)
- Continuous improvement

## Monitoring

Track these metrics:
- API response time
- Error rate
- Cost per session
- Student satisfaction
- Learning outcomes
- Hint usage
- Completion rate

## Next Steps

1. **Quick Test**: Add coachingAPI.js, hardcode AI mode, test one question
2. **Full Integration**: Add UI controls, test all harnesses
3. **Deploy**: Deploy backend, update React app
4. **Evaluate**: Run A/B test, analyze results
5. **Optimize**: Improve prompts based on data

Ready to integrate? Start with the Quick Test approach!
