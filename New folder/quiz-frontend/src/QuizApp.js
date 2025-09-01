import React, { useEffect, useState, useRef } from 'react';

const QUESTIONS_API = 'http://localhost:3000/api/questions'; // you need to create this backend route to fetch questions
const SAVE_RESULT_API = 'http://localhost:3000/api/save-result';
const LOGIN_API = 'http://localhost:3000/auth/login';
const LOGOUT_API = 'http://localhost:3000/auth/logout';

function QuizApp() {
  const [user, setUser] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [index, setIndex] = useState(0);
  const [selected, setSelected] = useState(null);
  const [message, setMessage] = useState('');
  const [score, setScore] = useState(0);
  const [attempts, setAttempts] = useState(0);
  const [timeLeft, setTimeLeft] = useState(60);
  const timerRef = useRef(null);

  // Fetch questions from backend once logged in
  useEffect(() => {
    if (user) {
      fetch(QUESTIONS_API, { credentials: 'include' })
        .then(r => r.json())
        .then(setQuestions)
        .catch(console.error);
    }
  }, [user]);

  // Timer countdown
  useEffect(() => {
    if (!user || questions.length === 0) return;

    setTimeLeft(60);
    timerRef.current = setInterval(() => {
      setTimeLeft(t => {
        if (t === 1) {
          // Time's up, move to next question
          clearInterval(timerRef.current);
          setMessage('Time is up! Moving to next question.');
          nextQuestion();
          return 60;
        }
        return t - 1;
      });
    }, 1000);

    return () => clearInterval(timerRef.current);
  }, [index, user, questions]);

  function login(e) {
    e.preventDefault();
    const username = e.target.username.value;
    const password = e.target.password.value;
    fetch(LOGIN_API, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    })
      .then(res => {
        if (res.ok) {
          setUser(username);
          setMessage('');
        } else {
          setMessage('Login failed');
        }
      })
      .catch(() => setMessage('Login failed'));
  }

  function logout() {
    fetch(LOGOUT_API, { method: 'POST', credentials: 'include' }).then(() => {
      setUser(null);
      setQuestions([]);
      setIndex(0);
      setScore(0);
      setSelected(null);
      setMessage('');
    });
  }

  function handleAnswer(choiceNumber) {
    if (selected !== null) return; // already answered for this question

    const correctAnswer = questions[index].Correct_Answer; // "1", "2", "3" or "4"
    if (choiceNumber.toString() === correctAnswer.toString()) {
      setMessage('Correct answer!');
      setScore(s => s + 1);
      setSelected(choiceNumber);
      clearInterval(timerRef.current);
      setTimeout(() => nextQuestion(), 2000);
    } else {
      setAttempts(a => a + 1);
      if (attempts + 1 >= 2) {
        setMessage('Wrong answer! Moving to next question.');
        setSelected(choiceNumber);
        clearInterval(timerRef.current);
        setTimeout(() => nextQuestion(), 2000);
      } else {
        setMessage('Wrong answer! Try again.');
      }
    }
  }

  function nextQuestion() {
    setSelected(null);
    setAttempts(0);
    setMessage('');
    if (index + 1 < questions.length) {
      setIndex(i => i + 1);
    } else {
      // Quiz finished, save result
      fetch(SAVE_RESULT_API, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ score, total: questions.length }),
      }).then(() => setMessage(`Quiz completed! Your score: ${score} / ${questions.length}`));
    }
  }

  if (!user) {
    return (
      <div style={{ maxWidth: 400, margin: 'auto', padding: 20 }}>
        <h2>Login</h2>
        <form onSubmit={login}>
          <input name="username" placeholder="Username" required />
          <input name="password" type="password" placeholder="Password" required />
          <button type="submit">Login</button>
        </form>
        <p style={{ color: 'red' }}>{message}</p>
      </div>
    );
  }

  if (questions.length === 0) {
    return <p>Loading questions...</p>;
  }

  if (index >= questions.length) {
    return (
      <div style={{ maxWidth: 600, margin: 'auto', padding: 20 }}>
        <h2>Quiz finished!</h2>
        <p>{message}</p>
        <button onClick={logout}>Logout</button>
      </div>
    );
  }

  const q = questions[index];
  const choices = [
    { id: 1, text: q.Answer1 },
    { id: 2, text: q.Answer2 },
    { id: 3, text: q.Answer3 },
    { id: 4, text: q.Answer4 },
  ];

  return (
    <div style={{ maxWidth: 600, margin: 'auto', padding: 20, fontFamily: 'Arial, sans-serif' }}>
      <h2>Question {index + 1} / {questions.length}</h2>
      <div style={{ marginBottom: 10 }}>{q.Question}</div>
      <div>Time left: {timeLeft}s</div>

      <div style={{ marginTop: 20 }}>
        {choices.map(c => (
          <button
            key={c.id}
            onClick={() => handleAnswer(c.id)}
            disabled={selected !== null}
            style={{
              display: 'block',
              margin: '8px 0',
              backgroundColor:
                selected === c.id
                  ? c.id.toString() === q.Correct_Answer.toString()
                    ? 'green'
                    : 'red'
                  : '',
              color: selected === c.id ? 'white' : '',
              padding: 10,
              width: '100%',
              fontSize: '1em',
              cursor: selected === null ? 'pointer' : 'default',
            }}
          >
            {c.id}. {c.text}
          </button>
        ))}
      </div>

      <p style={{ fontWeight: 'bold', marginTop: 20 }}>{message}</p>

      <progress
        value={index + (selected !== null ? 1 : 0)}
        max={questions.length}
        style={{ width: '100%', height: '20px' }}
      />

      <div style={{ marginTop: 20 }}>
        <button onClick={logout}>Logout</button>
      </div>
    </div>
  );
}

export default QuizApp;
